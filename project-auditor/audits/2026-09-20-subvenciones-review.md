# Auditoría de proyecto — Subvenciones Review v1.0

**Fecha:** 20/09/2026  
**Artefacto revisado:** `subvenciones-review-v1.0.0_2026-09-17_22-18.zip`  
**Tamaño ZIP:** 295.187 bytes  
**Contenido extraído:** 63 ficheros

## Estado provisional

**FUNCIONAL PARCIAL / PRODUCTO REAL — núcleo aprovechable, pero todavía no apto para uso profesional sin correcciones.**

A diferencia del validador antiguo, este ZIP contiene un backend real, persistencia SQLite, API Fastify, aplicación Electron, configuración Tauri, generadores de Excel/Word/ZIP, OCR, cliente LLM OpenAI-compatible/Ollama, lógica de facturas, personal, morosidad y una suite automática de tests. No es una maqueta.

## Pruebas reproducidas

Se ejecutó:

```
npm test
```

Resultado inicial, sin `node_modules`:

- **44 tests descubiertos**
- **42 pasan**
- **2 no llegan a ejecutar por dependencias ausentes en el entorno:** `exceljs` y `adm-zip`

Se intentó `npm ci --ignore-scripts`, pero la instalación agotó el tiempo disponible del entorno y dejó esos paquetes incompletos. La segunda ejecución mantuvo 42/44 y los mismos dos errores de resolución. Por tanto, **no se consideran dos fallos de lógica del proyecto**, pero tampoco puede afirmarse 44/44 hasta reproducir la instalación completa.

## Evidencia positiva

- `package.json` define test real mediante `node --test`.
- Backend Fastify con rutas de expedientes, convocatorias, documentos, BDNS, exportación y descargas.
- Persistencia local mediante `node:sqlite`.
- OCR real diseñado con `pdf-parse`, `pdfjs-dist`, `canvas` y `tesseract.js`.
- Cliente LLM real sin SDK obligatorio:
  - OpenAI-compatible: POST a `/v1/chat/completions`.
  - Ollama local: POST a `/api/chat`.
  - modo heurístico local como fallback.
- Generación real de Excel mediante `exceljs`.
- Generación de documentos Word mediante `docx`.
- Compresión ZIP y estructura de expedientes.
- Tests reales sobre análisis de convocatorias, mínimis, clasificación, facturas, morosidad y personal.
- El fallback BDNS devuelve estado `no_disponible` y exige revisión manual; no inventa ayudas.

## Bloqueos técnicos críticos

### 1. El servidor importa dependencias OCR que no están declaradas

`services/ocr.js` importa directamente:

```js
import { createCanvas } from 'canvas';
```

y dinámicamente:

```js
import('pdfjs-dist/legacy/build/pdf.mjs')
```

Ni `canvas` ni `pdfjs-dist` aparecen en `dependencies`, `devDependencies` ni en `package-lock.json`.

`server.js` importa `services/ocr.js` al arrancar, por lo que una instalación limpia no puede cargar el servidor mientras falte `canvas`.

Prueba reproducida:

```
ERR_MODULE_NOT_FOUND: Cannot find package 'canvas' imported from .../services/ocr.js
```

**Corrección:** declarar versiones compatibles de `canvas` y `pdfjs-dist`, regenerar lockfile y añadir un test de arranque limpio.

### 2. El empaquetado Windows referencia recursos que no existen en el ZIP

`package.json` exige:

- `build/icon.ico`
- `LICENSE.txt`
- carpeta `tesseract-lang`

Ninguno está incluido en el ZIP revisado.

El bundle Tauri también referencia cinco iconos PNG/ICO/ICNS no presentes; en `src-tauri/icons` solo existe `icon.svg`.

**Impacto:** el instalador no está acreditado aunque el README afirme que se genera con `npm run build:win`.

### 3. No existe CI en el artefacto

La suite es ejecutable localmente, pero el ZIP no contiene workflow CI. No hay una evidencia automática de instalación limpia + tests + build del instalador.

## Bloqueos profesionales / normativos críticos

### 4. Elegibilidad del IVA codificada de forma incorrecta

`services/facturas_validacion.js` decide:

- si el beneficiario parece asociación/fundación/ONG → IVA elegible;
- si no → IVA no elegible.

La Ley 38/2003, art. 31.8, no usa la forma jurídica como criterio: los impuestos indirectos no son subvencionables **cuando sean susceptibles de recuperación o compensación**.

Fuente oficial: https://www.boe.es/buscar/act.php?id=BOE-A-2003-20977#a31

**Impacto:** puede excluir IVA de una empresa que no pueda recuperarlo o incluir IVA de una entidad sin ánimo de lucro que sí tenga derecho a deducción/compensación.

**Corrección:** campo explícito por expediente/beneficiario sobre recuperabilidad del IVA, soportado documentalmente, nunca inferido por el nombre.

### 5. Cuenta justificativa simplificada mal parametrizada

`config/umbrales.js` y `services/dossier.js` codifican:

- 60.000 € “con proyecto”
- 30.000 € “sin proyecto”

El art. 75.1 RLGS establece, con carácter general, que para subvenciones **de importe inferior a 60.000 €** puede utilizarse cuenta justificativa simplificada **si así lo prevén las bases reguladoras**. No establece esa bifurcación genérica 60.000/30.000.

Fuente oficial: https://www.boe.es/buscar/act.php?id=BOE-A-2006-13371#a75

**Corrección:** no inferir modalidad por importe únicamente; leer expresamente bases/convocatoria.

### 6. Error de cálculo en morosidad cuando la entrega es posterior a la factura

`services/morosidad.js` pretende usar la fecha de entrega/servicio si es posterior a la factura, pero solo la sustituye si:

```js
diasEntregaPago > diasFacturaPago
```

Si la entrega es posterior a la factura, `diasEntregaPago` será normalmente menor, por lo que esa condición no se cumple. El cálculo sigue desde factura.

La Ley 3/2004, art. 4, sitúa el plazo general en 30 días desde la recepción de mercancías o prestación del servicio cuando no exista otro plazo válido; además contempla el procedimiento de aceptación/verificación.

Fuente oficial: https://www.boe.es/buscar/act.php?id=BOE-A-2004-21830#a4

**Impacto:** falsos incumplimientos y días de pago incorrectos.

### 7. Las 3 ofertas se aplican con un único umbral de 15.000 € y sobre total de factura

`UMBRALES.tres_ofertas = 15000` y `services/excel.js` marca cualquier factura cuyo `importe_total` supere ese valor.

La LGS art. 31.3 remite a las cuantías del contrato menor. La LCSP art. 118 distingue:

- obras: valor estimado inferior a 40.000 €;
- suministros/servicios: valor estimado inferior a 15.000 €.

Fuentes oficiales:
- https://www.boe.es/buscar/act.php?id=BOE-A-2003-20977#a31
- https://www.boe.es/buscar/act.php?id=BOE-A-2017-12902#a118

**Impacto:** una obra de 20.000 € se marcaría erróneamente como obligada a 3 ofertas. Además debe distinguirse el concepto de valor/importe aplicable y no usar mecánicamente el total con IVA.

### 8. Publicidad codificada con umbrales genéricos sin base universal

El Excel impone de forma fija:

- placa > 30.000 €
- díptico/web > 50.000 €
- acto público > 100.000 €

Estas obligaciones dependen de las bases, resolución y, en su caso, del fondo/programa financiador. No existe una regla general de la LGS que permita aplicar esos tres umbrales a toda subvención.

**Corrección:** extraer la obligación concreta de la normativa del expediente; si no está acreditada, estado “pendiente de determinar”, nunca obligación automática.

### 9. Validación IRPF compara totales incompatibles

En `services/personal_validacion.js`, para cada contrato/persona:

- suma el IRPF de las nóminas de esa persona;
- selecciona modelos 111/190 solo por ejercicio;
- compara el **importe total del modelo** con el IRPF de esa persona.

Un 111/190 agregado de toda la plantilla no puede conciliarse individualmente contra una sola persona sin desglose.

**Impacto:** genera falsos errores de IRPF cuando existen varios trabajadores.

### 10. RLC/RNT presenta el mismo problema de agregación

Para cada persona compara el total de Seguridad Social de sus nóminas con `importe_total` del RLC/RNT del ejercicio.

RLC y RNT son documentos colectivos; la conciliación requiere periodo, CCC y desglose adecuado. El total del RLC no puede compararse directamente con la cuota empresarial de un empleado.

### 11. Horas de convenio: 1.800 horas como supuesto puede convertirse en falso incumplimiento

Si no hay `horas_anuales_convenio`, el sistema toma 1.800 h/año como referencia y puede generar incidencias de horas.

**Corrección:** 1.800 puede servir como estimación informativa, pero no debe producir un incumplimiento profesional hasta conocer convenio, contrato, jornada y reglas específicas de la convocatoria.

### 12. La integración BDNS apunta a una ruta distinta de la API oficial documentada

El código usa por defecto:

`https://www.infosubvenciones.es/bdnstrans/buscar`

La documentación Swagger oficial de SNPSAP publica, entre otros:

- `GET /concesiones/busqueda`
- `GET /minimis/busqueda`

Fuente oficial: https://www.infosubvenciones.es/bdnstrans/doc/swagger

**Impacto:** la consulta automática no está acreditada y puede caer sistemáticamente al modo manual.

### 13. El cálculo de mínimis no filtra realmente “cualquier período de tres años”

`procesarRespuestaBDNS()` suma todas las ayudas devueltas marcadas como mínimis y guarda el resultado como `total_minimis_3anios`, pero no filtra por fecha.

Además, el Reglamento (UE) 2023/2831 aplica el límite de 300.000 € a una **única empresa** durante cualquier período de tres años, concepto que puede incluir empresas vinculadas; consultar solo un CIF no resuelve por sí mismo esa condición.

Fuente oficial: https://eur-lex.europa.eu/eli/reg/2023/2831/oj

## Valoración técnica

Este proyecto es **bastante mejor base que el validador antiguo**. Tiene arquitectura coherente, persistencia, backend, APIs, generación documental y tests reales. El problema principal ya no es “hacer una app”; es **hacer fiables las reglas profesionales y conseguir un build limpio reproducible**.

## Orden de corrección recomendado

1. Corregir dependencias `canvas` + `pdfjs-dist` y conseguir arranque limpio.
2. Completar recursos de Electron/Tauri y generar un instalador reproducible.
3. Corregir IVA según recuperabilidad.
4. Corregir morosidad desde fecha de recepción/prestación/aceptación.
5. Separar umbrales de 3 ofertas por obras vs servicios/suministros.
6. Eliminar reglas universales inventadas de publicidad.
7. Corregir art. 75 RLGS y hacer que mande la convocatoria/bases.
8. Rehacer conciliación 111/190 y RLC/RNT por periodos y magnitudes comparables.
9. Implementar API oficial BDNS/minimis y ventana móvil de 3 años + empresa única.
10. Ejecutar instalación limpia → unit tests → smokes → build Windows en CI.

## Conclusión

**No es paja.** Hay una aplicación real y una parte significativa de la lógica funciona. Pero hoy no debe utilizarse para emitir conclusiones profesionales automáticas sin revisión: varios errores de dominio podrían producir falsos “OK” o falsos incumplimientos. Tras corregir los puntos anteriores, es un candidato claro a convertirse en la base de SubvencIA.
