# Inventario de código recuperado para Project Auditor

**Fecha de recuperación:** 21/09/2026

Este inventario distingue código fuente realmente localizado de documentación, builds compilados y artefactos visuales. Un dossier o una captura no se considera código fuente.

| Proyecto | Paquete / repo localizado | Evidencia | Estado de custodia |
|---|---|---|---|
| PromptForge | `promptforge-complete.zip` | 1.404 ficheros útiles sin node_modules; 292 ficheros fuente; Next.js, Prisma/SQLite, Capacitor, scripts Stripe | **FUENTE LOCALIZADA** |
| ReservIA | `ReservIA_Master_App_V4.1_Codigo_Revisado.zip` | 60 ficheros; 26 fuente; 4 suites; `npm test` reproducido 21/09/2026: **10/10** | **FUENTE LOCALIZADA Y TESTEADA** |
| SubvencIA | `subvenciones-review-v1.0.0_2026-09-17_22-18.zip` | 63 ficheros; 51 fuente; 24 test/smoke; Node/Electron/Tauri; BDNS, OCR, LLM, contabilidad, Excel, informe | **FUENTE LOCALIZADA** |
| MindMetrics | `mindmetrics-compliance-ready-v1_3(1).zip` + `mindmetrics-ultimate.zip` | React/Vite + documentación compliance. La versión ultimate pudo compilarse ejecutando Vite directamente en el entorno de revisión | **FUENTE LOCALIZADA** |
| TALSANET / TALSA | `Codigo_TALSA_y_Atelier_Revision.zip` | JS/HTML/CSS de TALSA y central, pero principalmente bajo `dist/`; 3 ficheros JS principales | **CÓDIGO EJECUTABLE LOCALIZADO; FUENTE ORIGINAL NO COMPLETA** |
| AXON | `AXON_web_dashboard_v0.1.zip` | HTML/CSS + un `app.js` mínimo | **FRONTEND ESTÁTICO LOCALIZADO; BACKEND NO LOCALIZADO** |
| Software Auditoría | GitHub `Nachollo/normativa-contable-espa-a`, PR #2 | 68 archivos cambiados; código Python real | **REPO LOCALIZADO** |
| Validador Cuentas Justificativas | GitHub `Nachollo/validador-cuentas-justificativas` | React/Electron/TypeScript, OCR y servicios | **REPO LOCALIZADO** |
| SENTINEL | PDFs `MOTOR COMPLETO` / `benchmark`; ruta histórica `C:\Users\Usuario\.minimax\workspace\sentinel-app` | Documentación describe motor y tests, pero no aparece el directorio/repo/ZIP | **CÓDIGO CORE NO LOCALIZADO** |
| PulseDJ | `PULSEDJ_IA_Dossier_Completo.docx` | Dossier declara 274 archivos fuente y 80.003 LOC, pero no se ha localizado el paquete original | **CÓDIGO NO LOCALIZADO** |
| Machine Tip | Proyecto histórico creado mediante Sites | No existe repo/ZIP accesible con los conectores actuales | **CÓDIGO NO EXPORTADO/NO LOCALIZADO** |
| ContaES | — | Sin ZIP/repo/source file identificado | **NO LOCALIZADO** |
| TraduFlow | — | Sin ZIP/repo/source file identificado | **NO LOCALIZADO** |
| Viajes | — | Sin ZIP/repo/source file identificado | **NO LOCALIZADO** |
| Copywriter | — | Sin ZIP/repo/source file identificado | **NO LOCALIZADO** |
| Qentyra | — | Arquitectura histórica descrita, pero sin repo/ZIP exacto identificado | **NO LOCALIZADO** |

## Referencias persistentes de Library

### PromptForge
- file_id: `file_0000000041f081f485ea7ab2a3d1dcdc`
- library_file_id: `libfile_c894aae446588191a1cabcbd3ada2717`
- path: `/promptforge-complete.zip`

### ReservIA V4.1
- file_id: `file_00000000d6ec81f8bd8b8014d0130155`
- library_file_id: `libfile_96c26c1f9f2881918b2a4859da7e34aa`
- path: `/ReservIA_Master_App_V4.1_Codigo_Revisado.zip`

### SubvencIA
- file_id: `file_000000008ebc81f4a5fb4908d07c2ff5`
- library_file_id: `libfile_46e050aad7988191a4470f30c842b793`
- path: `/subvenciones-review-v1.0.0_2026-09-17_22-18.zip`

### MindMetrics
- latest compliance package file_id: `file_00000000b37071f4af7d225bdbcb65ab`
- library_file_id: `libfile_470f278afd3c8191a087a4b168a1ec0a`
- path: `/mindmetrics-compliance-ready-v1_3(1).zip`
- build-capable ultimate package: `file_0000000041d472468f153ec9491c2a35`

### TALSANET / TALSA
- file_id: `file_000000006cbc81f5a01477a057b940d8`
- library_file_id: `libfile_8e840fe7b50c8191911fd2b573c38679`
- path: `/Codigo_TALSA_y_Atelier_Revision.zip`

### AXON
- file_id: `file_00000000871071f4b83c6f55a05ed36a`
- library_file_id: `libfile_d4f069d06cf081919d1a2f6ffa533595`
- path: `/AXON_web_dashboard_v0.1.zip`

## Archivos descartados como falsas pistas

- `OneDrive_1_6-7-2026.zip`: contiene 26 PDFs/justificantes de subvenciones, no software.
- `ecb8d712-67a8-43a5-a28f-9bc74bbb0bb2.zip`: contiene capturas PNG de MindMetrics, no fuente.
- `Flow_DJ_Brand_Assets_v2.x.zip`: branding; no acredita el código PulseDJ.
- `financial_news_scraper_package.zip`: scraper Python genérico; no se puede atribuir al core de SENTINEL sin evidencia adicional.

## Regla para BOSS BOT 7 / Project Auditor

No convertir en "código localizado" ningún dossier, PDF, screenshot o branding. Para cerrar un pendiente se exige uno de estos:
1. repo accesible;
2. ZIP/tar con fuente;
3. export oficial del builder que contenga código;
4. build ejecutable acompañado de suficiente código para trazabilidad.

