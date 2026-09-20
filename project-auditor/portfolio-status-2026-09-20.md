# Estado de cartera — 20/09/2026

Este documento recoge únicamente conclusiones respaldadas por código, artefactos o repositorios accesibles. No se otorga el estado "FUNCIONAL PROBADO" si no se han reproducido tests/build o una prueba end-to-end.

## Resumen

| Proyecto | Evidencia revisada | Estado provisional | Motivo principal |
|---|---|---|---|
| ReservIA | Dashboard + Widget HTML standalone | PROTOTIPO / DEMO | UI funcional local, sin backend/API/persistencia acreditada; el propio código declara modo demostración |
| Go Prompts AI / Prompts | HTML guardado + web pública viva | FUNCIONAL PARCIAL / SERVICIO DESPLEGADO, BACKEND NO AUDITADO | Web accesible, catálogo, pricing, login y señales de Supabase/Stripe; falta código/backend y prueba de checkout/auth |
| Software Auditoría | PR #2 `Nachollo/normativa-contable-espa-a` | FUNCIONAL PARCIAL / FALTA ACREDITAR | 68 archivos y lógica sustantiva, pero tests ad hoc, integración OpenAI incompatible y V1 local no usa Ollama/Llama |
| Validador cuentas justificativas / base SubvencIA | `Nachollo/validador-cuentas-justificativas` main | PROTOTIPO AVANZADO | Mucho código real, OCR/contabilidad/normativa/exportación; CI decorativo, sin test script y fallbacks simulados |
| SENTINEL | PDFs técnicos MOTOR COMPLETO + benchmark | CLAIMS NO ACREDITADOS CON CÓDIGO | Documentación muy detallada y reproducible en teoría, pero no se ha localizado el repo/código fuente para ejecutar los 145/148 tests |

---

## ReservIA

### Evidencia localizada
- `ReservIA_Dashboard_Standalone.html`
- `ReservIA_Widget_Standalone.html`

### Hallazgos
- Dashboard: 0 llamadas `fetch`, 0 Axios, 0 WebSocket, 0 Supabase/Firebase, 0 Stripe.
- Widget: 0 llamadas `fetch`, 0 Axios, 0 WebSocket, 0 Supabase/Firebase, 0 Stripe.
- El dashboard contiene textos y acciones de "cuenta piloto".
- El chat responde con un mensaje fijo e indica expresamente que funciona en "modo demostración local".
- El widget indica que hay que conectar el backend de ReservIA para responder con IA y ejecutar reservas.

### Conclusión provisional
La interfaz existe y es demostrable, pero estos artefactos no acreditan:
- reservas persistentes;
- disponibilidad real;
- integración con calendarios;
- IA operativa;
- backend multiempresa;
- pagos;
- comunicaciones externas.

**Estado: PROTOTIPO / DEMO.**

---

## Go Prompts AI / proyecto Prompts

### Evidencia localizada
- HTML guardado de una aplicación Next.
- Web pública `gopromptsai.com` accesible el 20/09/2026.

### Hallazgos
- La web pública expone catálogo, login, suscripción y agentes.
- La página de pricing muestra una suscripción Pro y declara pago seguro con Stripe.
- El HTML guardado contiene referencias a Supabase y Stripe.
- Existe navegación pública de colecciones y precios.

### Limitación
Un HTML guardado y una web pública no permiten verificar:
- código backend;
- reglas de autorización;
- webhooks;
- checkout real hasta confirmación;
- persistencia de compras;
- seguridad;
- generación real de agentes.

**Estado: FUNCIONAL PARCIAL / SERVICIO DESPLEGADO, BACKEND NO AUDITADO.**

---

## Software Auditoría — `Nachollo/normativa-contable-espa-a` PR #2

### Evidencia
PR #2:
- 68 archivos cambiados;
- 13.282 líneas añadidas;
- 21 módulos bajo `src/`;
- 4 archivos `test_*.py`;
- generación de papeles de trabajo;
- materialidad, muestreo, matriz de riesgos, circularización, OCR y procesamiento documental.

### Hallazgos favorables
- Hay código Python real y módulos especializados.
- OCR con Tesseract/OpenCV.
- Procesamiento masivo.
- Persistencia/SQLite/SQLAlchemy.
- Clasificación local con transformers/embeddings.
- OpenAI opcional en configuración.
- Generadores de papeles y entregables.

### Bloqueos
1. **Los 4 `test_*.py` son scripts ad hoc:** no usan `pytest`, `unittest` ni contienen `assert`.
2. **OpenAI incompatible:** `requirements.txt` fija `openai==1.3.0`, pero el código usa `openai.ChatCompletion.create`, API legacy incompatible con OpenAI Python >=1.
3. **La V1 definida no está implementada como se pidió:** no se localiza Ollama ni Llama 3.1 8B; la IA local actual usa BART/Transformers/SentenceTransformer.
4. Los claims del PR no se han reproducido mediante CI/build/test verificable.

### Conclusión provisional
No es "paja": existe una base considerable de código y arquitectura. Tampoco puede considerarse V1 lista para uso profesional hasta corregir integración IA, convertir pruebas en tests reproducibles y ejecutar un caso real de auditoría.

**Estado: FUNCIONAL PARCIAL / FALTA ACREDITAR.**

---

## Validador de cuentas justificativas — base reutilizable para SubvencIA

Repositorio: `Nachollo/validador-cuentas-justificativas`.

### Evidencia favorable
- React + TypeScript + Electron.
- OCR con `tesseract.js`.
- Servicios de contabilidad, normativa, regulación, Excel y persistencia local.
- Procesador documental y UI de carga múltiple.
- Generación de reportes.

### Bloqueos
1. `.github/workflows/blank.yml` es el workflow de ejemplo: únicamente ejecuta `echo Hello, world!`; no construye ni prueba la app.
2. `package.json` no define un script `test`.
3. `OCRService.ts` contiene varios comentarios y caminos explícitos de simulación.
4. Si OCR falla, `simulateOCRFromFileName()` fabrica facturas/nóminas con importes y fechas aleatorios.
5. Parte de `TestingService` verifica mocks y lógica simulada, no documentos reales.

### Riesgo profesional
En una aplicación destinada a cuentas justificativas, un fallback que **inventa datos** no puede quedar activo en producción. Ante fallo de OCR debe devolver estado de error/revisión manual, nunca generar contenido plausible.

**Estado: PROTOTIPO AVANZADO / BASE TÉCNICA REUTILIZABLE.**

---

## SENTINEL

### Evidencia documental
Los documentos técnicos encontrados describen:
- A.M.E. v3;
- Node.js/Fastify/SQLite/Transformers;
- benchmarking;
- 145/145 o 148/148 tests según documento/versión;
- comandos concretos para ejecutar la suite.

### Limitación crítica
No se ha localizado entre los repositorios GitHub accesibles el repositorio `sentinel-app` ni los archivos `tests/ame-*.js` descritos en los PDFs.

Por tanto no se pueden reproducir:
- tests;
- latencias;
- benchmark;
- tamaño del motor;
- comportamiento end-to-end.

**Estado: CLAIMS TÉCNICOS DOCUMENTADOS, PERO NO ACREDITADOS CON EL CÓDIGO DISPONIBLE.**

---

## Próximas acciones automáticas del Project Auditor

1. localizar repos/carpeta de SENTINEL y ejecutar su suite;
2. ejecutar build real de `validador-cuentas-justificativas`;
3. eliminar fallbacks de datos inventados del validador;
4. convertir su CI en build + lint + tests reales;
5. corregir OpenAI y sustituir/añadir Ollama Llama 3.1 8B en Software Auditoría;
6. transformar los scripts `test_*.py` en pruebas reproducibles;
7. localizar código real de ReservIA y contrastarlo con los HTML standalone;
8. auditar checkout/auth/backend de Go Prompts solo cuando se disponga de código o un entorno de prueba autorizado.
