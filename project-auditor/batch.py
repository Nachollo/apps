#!/usr/bin/env python3
"""Audita el catálogo completo resolviendo carpetas por alias o source explícito."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict
from pathlib import Path

import auditor


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def resolve_project(base: Path, item: dict) -> Path | None:
    source = (item.get("source") or "").strip()
    if source:
        p = Path(source).expanduser()
        if not p.is_absolute():
            p = base / p
        if p.is_dir():
            return p.resolve()
    aliases = [item.get("name", ""), *(item.get("aliases") or [])]
    wanted = {norm(x) for x in aliases if x}
    children = [p for p in base.iterdir() if p.is_dir()]
    exact = [p for p in children if norm(p.name) in wanted]
    if exact:
        return exact[0].resolve()
    partial = [p for p in children if any(a and (a in norm(p.name) or norm(p.name) in a) for a in wanted)]
    return partial[0].resolve() if len(partial) == 1 else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Audita todos los proyectos del catálogo")
    ap.add_argument("--root", required=True, help="Carpeta que contiene los proyectos")
    ap.add_argument("--catalog", default="catalog.json")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--out", default="audit-results")
    args = ap.parse_args()

    base = Path(args.root).expanduser().resolve()
    if not base.is_dir():
        raise SystemExit(f"No existe --root: {base}")
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    reports = []
    missing = []
    for item in catalog.get("projects", []):
        p = resolve_project(base, item)
        if not p:
            missing.append(item.get("name", "sin nombre"))
            continue
        r = auditor.inspect(p, str(p), args.run, args.install, args.timeout)
        reports.append(r)
        auditor.save(r, out)

    reports.sort(key=lambda r: r.score, reverse=True)
    summary = {
        "root": str(base),
        "audited": [asdict(r) for r in reports],
        "missing": missing,
    }
    (out / "portfolio.audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Auditoría de cartera", "", f"Carpeta: `{base}`", "", "| Proyecto | Veredicto | Score | Confianza |", "|---|---|---:|---|"]
    for r in reports:
        lines.append(f"| {r.project} | {r.verdict} | {r.score}/100 | {r.confidence} |")
    lines += ["", "## No localizados"]
    lines += [f"- {x}" for x in missing] or ["- Ninguno"]
    (out / "portfolio.audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
