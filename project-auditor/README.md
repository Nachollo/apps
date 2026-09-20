# Project Auditor V1

Bot local para auditar proyectos por **evidencias técnicas**, no por apariencia ni por lo que afirme el README.

## Qué comprueba

- cantidad real de código y tests;
- si existen backend, base de datos, autenticación, pagos, IA e integraciones;
- señales de `demo`, `mock`, `stub`, `placeholder`, `TODO`, datos falsos o funcionalidad simulada;
- claims cuantificados del README (por ejemplo `145/145 tests passing`) y si se han reproducido;
- tests, build y lint cuando el proyecto expone comandos estándar y se usa `--run`;
- penaliza proyectos que parecen producto por UI pero no acreditan backend/persistencia;
- genera un informe Markdown y JSON con fortalezas, bloqueos, evidencias y comandos ejecutados.

## Veredictos

1. `FUNCIONAL PROBADO`: evidencia fuerte y test/build ejecutado sin fallos.
2. `FUNCIONAL PARCIAL / FALTA ACREDITAR`: hay producto real, pero faltan comprobaciones o integraciones.
3. `PROTOTIPO / DEMO`: existe implementación, pero no acredita todavía un producto operativo completo.
4. `PAJA / CLAIMS NO ACREDITADAS`: la apariencia o las promesas superan claramente la evidencia técnica encontrada.

El score no sustituye una auditoría de seguridad, legal, de mercado ni una prueba manual end-to-end.

## Uso en Windows 11

Solo análisis estático:

```powershell
python auditor.py --path "C:\ruta\al\proyecto"
```

Ejecutar tests/build detectados:

```powershell
python auditor.py --path "C:\ruta\al\proyecto" --run
```

Si es un proyecto Node y faltan dependencias:

```powershell
python auditor.py --path "C:\ruta\al\proyecto" --install --run
```

`--install` usa `npm ci/install --ignore-scripts` para reducir el riesgo de scripts de instalación. Los scripts `test`, `build` o `lint` sí pueden ejecutar código del proyecto; úsalo solo en código de confianza o una VM/contenedor.

Repositorio Git:

```powershell
python auditor.py --repo "https://github.com/usuario/proyecto.git" --run
```

## Auditar toda la cartera

Si todos los proyectos cuelgan de una carpeta, el bot intenta resolverlos por nombre/alias y genera un resumen global:

```powershell
python batch.py --root "C:\\ruta\\proyectos" --run
```

Los que no pueda localizar de forma inequívoca quedan como `No localizados`; no inventa rutas.

## Catálogo

`catalog.json` incluye el inventario inicial: ContaES, SENTINEL, PulseDJ, TraduFlow, PromptForge, Viajes, ReservIA, Machine Tip, Copywriter, AXON, MindMetrics, SubvencIA, TALSANET, Qentyra y Software Auditoría.

El campo `source` se deja vacío hasta conocer la carpeta o repo exacto. Así el bot no inventa dónde está cada proyecto.

## Prueba del propio auditor

```powershell
python -m unittest discover -s tests -v
```

Incluye un fixture deliberadamente de “paja” para comprobar que una demo con claims como `145/145 tests passing` no sea aprobada sin evidencias reproducibles.

## Siguiente capa

La V2 debería conservar histórico por proyecto, comparar auditorías entre fechas y añadir pruebas end-to-end específicas por producto (por ejemplo reservas reales, pagos, audio, OCR o consultas externas), además del análisis genérico actual.


## Repositorios remotos en el catálogo

Un proyecto puede auditarse directamente desde GitHub sin tener una copia local:

```json
{
  "name": "Software Auditoría",
  "repository": "https://github.com/Nachollo/normativa-contable-espa-a.git",
  "ref": "copilot/fix-75705fbf-ec86-411e-8e16-2c0962564099"
}
```

`batch.py` prioriza `repository`/`repo`; si no existe, intenta localizar la carpeta local por `source` o aliases. Esto permite una cartera híbrida de repos GitHub y proyectos locales.

Ejemplo:

```powershell
python batch.py --root "C:\ruta\proyectos" --catalog catalog.json --run
```

Los repos remotos se clonan temporalmente y se eliminan tras la auditoría.
