#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys, tempfile, time
from dataclasses import dataclass, asdict, field
from pathlib import Path

EXCLUDE={'.git','node_modules','.next','dist','build','coverage','.venv','venv','__pycache__','.pytest_cache'}
SOURCE={'.py','.js','.jsx','.ts','.tsx','.mjs','.cjs','.go','.rs','.java','.kt','.php','.rb'}
TEXT=SOURCE|{'.json','.md','.html','.css','.scss','.sql','.yml','.yaml','.toml','.ini','.txt'}
MOCK=('mock','mocked','demo','placeholder','fake','stub','dummy','todo','fixme','coming soon','not implemented','modo demostración','modo demo','simulad','hardcoded')
FEATURES={
 'backend':(r'\bexpress\b',r'\bfastapi\b',r'\bdjango\b',r'\bflask\b',r'app\.(get|post|put|delete)\('),
 'database':(r'postgres',r'mysql',r'sqlite',r'mongodb',r'prisma',r'supabase',r'firebase',r'sqlalchemy',r'drizzle'),
 'auth':(r'nextauth',r'auth0',r'clerk',r'jwt',r'oauth',r'bcrypt',r'passport'),
 'payments':(r'stripe',r'paddle',r'paypal',r'payment_intent',r'checkout\.sessions'),
 'ai':(r'openai',r'anthropic',r'gemini',r'ollama',r'llama',r'langchain',r'transformers'),
 'integrations':(r'webhook',r'fetch\(',r'axios\.',r'requests\.',r'httpx\.',r'twilio',r'whatsapp',r'calendar')}
CLAIMS=(r'\d+\s*/\s*\d+\s+(tests?|pruebas?)\s+(passing|passed|ok|superad)',r'\d+[+]?\s+(endpoints?|rutas?)\b',r'\d+(?:[.,]\d+)?\s*(ms|μs|us)\b',r'\b100%\s+funcional\b',r'production[- ]ready')

@dataclass
class Cmd:
 name:str; command:str; attempted:bool; passed:bool|None; returncode:int|None=None; seconds:float|None=None; output_tail:str=''; reason:str=''
@dataclass
class Report:
 project:str; source:str; verdict:str; score:int; confidence:str; files_total:int; source_files:int; source_lines:int; test_files:int; mock_hits:int; mock_files:int
 readme_claims:list[str]=field(default_factory=list); features:dict=field(default_factory=dict); commands:list[Cmd]=field(default_factory=list); strengths:list[str]=field(default_factory=list); blockers:list[str]=field(default_factory=list)

def files(root):
 for p in root.rglob('*'):
  if p.is_file() and not any(x in EXCLUDE for x in p.parts) and (p.suffix.lower() in TEXT or p.name in {'Dockerfile','Makefile'}): yield p

def txt(p,limit=1_000_000):
 try: return '' if p.stat().st_size>limit else p.read_text(encoding='utf-8',errors='ignore')
 except OSError: return ''

def is_test(rel):
 r=rel.replace('\\','/')
 return bool(re.search(r'(^|/)(tests?|__tests__)(/|$)|\.(test|spec)\.(js|jsx|ts|tsx)$|(^|/)test_.+\.py$|_test\.py$',r,re.I))

def scripts(root):
 try: return (json.loads(txt(root/'package.json')).get('scripts') or {}) if (root/'package.json').exists() else {}
 except Exception: return {}

def planned(root):
 out=[]; s=scripts(root); npm='npm.cmd' if os.name=='nt' else 'npm'
 if (root/'package.json').exists() and shutil.which(npm):
  if 'test' in s and 'no test specified' not in str(s['test']).lower(): out.append(('tests',[npm,'test']))
  if 'build' in s: out.append(('build',[npm,'run','build']))
  if 'lint' in s: out.append(('lint',[npm,'run','lint']))
 py=any((root/x).exists() for x in ('pyproject.toml','pytest.ini','setup.cfg','requirements.txt'))
 if py:
  if shutil.which('pytest'): out.append(('tests',['pytest','-q']))
  out.append(('python_compile',[sys.executable,'-m','compileall','-q','.']))
 return out

def run_cmd(name,cmd,root,timeout):
 t=time.time()
 try:
  p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,env={**os.environ,'CI':'1'})
  return Cmd(name,' '.join(cmd),True,p.returncode==0,p.returncode,round(time.time()-t,2),(p.stdout or '')[-4000:])
 except subprocess.TimeoutExpired as e: return Cmd(name,' '.join(cmd),True,False,None,round(time.time()-t,2),str(e.stdout or '')[-4000:],f'timeout>{timeout}s')
 except OSError as e: return Cmd(name,' '.join(cmd),False,None,reason=str(e))

def inspect(root:Path,source:str,run=False,install=False,timeout=180):
 fs=list(files(root)); sf=lines=tests=mh=mf=0; hit={k:[] for k in FEATURES}
 for p in fs:
  rel=p.relative_to(root).as_posix(); t=txt(p); low=t.lower()
  if p.suffix.lower() in SOURCE: sf+=1; lines+=t.count('\n')+(1 if t else 0)
  if is_test(rel): tests+=1
  n=sum(low.count(x) for x in MOCK)
  if n: mh+=n; mf+=1
  for k,pats in FEATURES.items():
   if any(re.search(q,t,re.I) for q in pats): hit[k].append(rel)
 readme=next((root/n for n in ('README.md','readme.md','README') if (root/n).exists()),None)
 cl=[]
 if readme:
  for line in txt(readme).splitlines():
   if any(re.search(q,line,re.I) for q in CLAIMS): cl.append(re.sub(r'\s+',' ',line.strip())[:300])
 cmds=[]
 if install and (root/'package.json').exists():
  npm='npm.cmd' if os.name=='nt' else 'npm'; cmd=[npm,'ci' if (root/'package-lock.json').exists() else 'install','--ignore-scripts']
  cmds.append(run_cmd('install',cmd,root,timeout) if shutil.which(npm) else Cmd('install',npm,False,None,reason='npm no disponible'))
 for name,cmd in planned(root): cmds.append(run_cmd(name,cmd,root,timeout) if run else Cmd(name,' '.join(cmd),False,None,reason='usa --run'))
 feat={k:{'present':bool(v),'files':v[:10],'count_files':len(v)} for k,v in hit.items()}
 score=0; strong=[]; block=[]
 if sf>=10: score+=15; strong.append(f'base de código: {sf} ficheros fuente')
 elif sf>=3: score+=8
 else: block.append('muy pocos ficheros fuente')
 if lines>=1500: score+=10
 elif lines>=300: score+=5
 else: block.append('volumen de lógica bajo')
 if tests>=5: score+=15; strong.append(f'{tests} ficheros de test')
 elif tests: score+=7
 else: block.append('sin tests localizados')
 if any(c.name=='tests' and c.passed is True for c in cmds): score+=20; strong.append('tests ejecutados y superados')
 if any(c.name=='tests' and c.passed is False for c in cmds): score-=15; block.append('tests fallan')
 if any(c.name=='build' and c.passed is True for c in cmds): score+=15; strong.append('build superado')
 if any(c.name=='build' and c.passed is False for c in cmds): score-=12; block.append('build falla')
 if feat['backend']['present']: score+=8
 if feat['database']['present']: score+=7
 if feat['auth']['present']: score+=5
 if mh==0: score+=5
 elif mh/max(lines,1)*1000>8: score-=15; block.append(f'alta densidad demo/mock: {mh} menciones en {mf} ficheros')
 elif mh>3: score-=7; block.append(f'señales demo/mock: {mh} menciones')
 if cl and not any(c.name=='tests' and c.passed is True for c in cmds): score-=min(10,len(cl)*2); block.append('claims cuantificados sin reproducción de tests')
 ui=sum(1 for p in fs if p.suffix.lower() in {'.html','.css','.scss','.jsx','.tsx'})
 if ui>=3 and not feat['backend']['present'] and not feat['database']['present']: score-=12; block.append('UI sin evidencia suficiente de backend/persistencia')
 score=max(0,min(100,score)); executed=any(c.name in {'tests','build'} and c.attempted for c in cmds); conf='alta' if executed else ('media' if sf>=5 else 'baja')
 verdict='FUNCIONAL PROBADO' if score>=75 and executed and not any(c.attempted and c.passed is False for c in cmds) else 'FUNCIONAL PARCIAL / FALTA ACREDITAR' if score>=55 else 'PROTOTIPO / DEMO' if score>=30 else 'PAJA / CLAIMS NO ACREDITADAS'
 return Report(root.name,source,verdict,score,conf,len(fs),sf,lines,tests,mh,mf,cl[:30],feat,cmds,strong,block)

def markdown(r):
 L=[f'# Auditoría — {r.project}','',f'Veredicto: {r.verdict}',f'Score: {r.score}/100',f'Confianza: {r.confidence}',f'Fuente: {r.source}','',f'Ficheros: {r.files_total}; fuente: {r.source_files}; líneas: {r.source_lines}; tests: {r.test_files}; demo/mock: {r.mock_hits}.','','## Capacidades']
 L += [f'- {k}: {"sí" if v["present"] else "no"} ({v["count_files"]} ficheros)' for k,v in r.features.items()]
 L += ['','## Comandos'] + ([f'- {c.name}: {"OK" if c.passed else "FALLO" if c.attempted else "NO EJECUTADO"} — {c.command} {c.reason}' for c in r.commands] or ['- Ninguno detectado'])
 L += ['','## Claims'] + ([f'- {x}' for x in r.readme_claims] or ['- Ninguno detectado'])
 L += ['','## Fortalezas'] + ([f'- {x}' for x in r.strengths] or ['- Sin fortalezas acreditadas suficientes'])
 L += ['','## Bloqueos'] + ([f'- {x}' for x in r.blockers] or ['- Sin bloqueos críticos por estas reglas'])
 return '\n'.join(L)+'\n'

def save(r,out):
 out.mkdir(parents=True,exist_ok=True); slug=re.sub(r'[^A-Za-z0-9._-]+','_',r.project); j=out/f'{slug}.audit.json'; m=out/f'{slug}.audit.md'; j.write_text(json.dumps(asdict(r),ensure_ascii=False,indent=2),encoding='utf-8'); m.write_text(markdown(r),encoding='utf-8'); return j,m

def clone(url):
 td=tempfile.TemporaryDirectory(prefix='project-auditor-'); dst=Path(td.name)/'repo'; p=subprocess.run(['git','clone','--depth','1',url,str(dst)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
 if p.returncode: td.cleanup(); raise RuntimeError(p.stdout[-3000:])
 return dst,td

def main():
 ap=argparse.ArgumentParser(); g=ap.add_mutually_exclusive_group(required=True); g.add_argument('--path'); g.add_argument('--repo'); ap.add_argument('--run',action='store_true'); ap.add_argument('--install',action='store_true'); ap.add_argument('--timeout',type=int,default=180); ap.add_argument('--out',default='audit-results'); a=ap.parse_args(); td=None
 try:
  root,td=clone(a.repo) if a.repo else (Path(a.path).expanduser().resolve(),None)
  if not root.is_dir(): raise RuntimeError(f'No existe: {root}')
  r=inspect(root,a.repo or str(root),a.run,a.install,a.timeout); j,m=save(r,Path(a.out)); print(markdown(r)); print('JSON:',j); print('Markdown:',m); return 0 if r.score>=30 else 2
 finally:
  if td: td.cleanup()
if __name__=='__main__': raise SystemExit(main())
