# Auditoría de proyecto — Validador Cuentas Justificativas

**Fecha:** 20/09/2026  
**Repositorio:** https://github.com/Nachollo/validador-cuentas-justificativas  
**Rama:** `main`  
**Commit revisado:** `461aac417f2d4c0c2bbfe0bec9daab7685fbb6dc`

## Estado provisional

**PROTOTIPO / DEMO con componentes reales.**

El proyecto contiene una aplicación React/Electron sustancial y algunas piezas reales —especialmente OCR y persistencia de escritorio—, pero numerosas funciones de negocio siguen simuladas.

## Evidencia positiva

- Aplicación React + TypeScript + Electron.
- `src/services/OCRService.ts` inicializa Tesseract y ejecuta `worker.recognize(file)`.
- `public/electron.js` y `public/preload.js` implementan IPC y lectura/escritura real mediante `fs-extra`.
- `LocalStorageService.ts` contiene rutas para persistencia real en Electron.
- Existen servicios separados para OCR, contabilidad, normativa, Excel, exportación y autoguardado.

## Bloqueos

### 1. CI decorativo

`.github/workflows/blank.yml` únicamente ejecuta mensajes `echo`; no instala dependencias, no compila y no ejecuta tests.

Por tanto, la existencia del workflow no acredita que el proyecto compile.

### 2. No hay script de tests en `package.json`

El proyecto define `dev`, `build`, `lint` y tareas Electron, pero no `test`.

### 3. Rutas OCR simuladas junto al OCR real

`DocumentUploader.tsx` incluye procesamiento “Simular OCR” y genera confianza aleatoria.

`OCRService.ts` sí tiene OCR real, pero ante ciertos fallos cae a `simulateOCRFromFileName()`, que genera datos de ejemplo y valores aleatorios.

**Impacto:** la interfaz puede mostrar resultados aparentemente analizados aunque procedan de simulación.

### 4. Excel y reportes parcialmente simulados

`ExcelService.ts` contiene comentarios explícitos de “Simular generación de Excel”.

`ReportGenerator.tsx` usa alertas de “Simular descarga”.

### 5. Normativa parcialmente simulada/hardcoded

`RegulationService.ts` incorpora reglas aplicadas de ejemplo con estados `passed: true`.

`NormativeService.ts` contiene extracción simulada de PDF/Word y, en web, almacenamiento mediante `localStorage`.

### 6. Dependencias de IA declaradas sin evidencia de uso

`package.json` declara `@tensorflow/tfjs`, `@tensorflow/tfjs-node`, `natural` y `compromise`.

La búsqueda en código no localizó imports/uso de TensorFlow; `natural` y `compromise` aparecen en configuración/dependencias, pero no se acreditó una canalización de IA real equivalente a lo prometido en README.

### 7. Tests internos no equivalen a una suite automatizada

`TestingService.ts` crea documentos mock y contiene referencias a `jest.fn()`, pero Jest no figura como dependencia ni existe script `test`.

## Conclusión

El proyecto no es “paja” total: **OCR Tesseract, Electron, IPC y persistencia contienen implementación real**. Sin embargo, demasiadas funciones de negocio están simuladas para considerarlo un producto terminado.

La recomendación técnica es **no mantenerlo como producto independiente**: rescatar OCR/persistencia/IPC útiles y migrarlos al proyecto de Software Auditoría/SubvencIA que se vaya a convertir en la base única.
