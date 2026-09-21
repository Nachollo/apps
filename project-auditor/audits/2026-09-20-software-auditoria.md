# Auditoría de proyecto — Software Auditoría

**Fecha:** 20/09/2026  
**Repositorio:** https://github.com/Nachollo/normativa-contable-espa-a  
**Rama revisada:** `copilot/fix-75705fbf-ec86-411e-8e16-2c0962564099`  
**PR:** #2  
**Head revisado:** `6496dcbeb268521a98d6aa4a164404805a63a29e`

## Estado provisional

**FUNCIONAL PARCIAL / FALTA ACREDITAR — no apto todavía para confiar en entregables profesionales finales.**

No es una maqueta vacía: el PR contiene un núcleo contable con SQLAlchemy, carga documental, OCR, clasificación, materialidad, muestreo, matrices de riesgo, papeles Excel y varios scripts de prueba. Sin embargo, existen discrepancias materiales entre lo que el PR afirma que hace y lo que el código implementa.

## Evidencia positiva

- PR con 68 archivos modificados y 13.282 líneas añadidas.
- Existen 4 ficheros de prueba: `test_complete_system.py`, `test_area_summaries.py`, `test_circularization.py` y `test_questionnaires_and_ratios.py`.
- `src/accounting_core.py` implementa persistencia contable mediante SQLAlchemy.
- `src/document_classifier.py` extrae texto de PDF, Word, Excel e imágenes; usa `pytesseract` para OCR.
- `src/ai_processor.py` contiene modelos locales reales (SentenceTransformer y zero-shot BART) y ruta OpenAI opcional.
- `main_audit.py` integra carga contable, clasificación, papeles de trabajo y módulos de cierre.

## Bloqueos críticos

### 1. No hay ejecución CI que acredite el PR

Para el head revisado no constan workflow runs ni estados de CI asociados. Los scripts de prueba existen, pero son principalmente scripts ejecutables ad hoc; la ausencia de CI impide afirmar que el sistema esté reproduciblemente verde.

### 2. Ruta OpenAI incompatible con la dependencia fijada

`requirements.txt` fija `openai==1.3.0`, mientras `src/ai_processor.py` llama a:

`openai.ChatCompletion.create(...)`

La interfaz `openai.ChatCompletion.create()` fue retirada en `openai>=1.0.0`; la migración oficial usa `client.chat.completions.create()`.

Referencia oficial: https://github.com/openai/openai-python/discussions/742

**Impacto:** la opción OpenAI fallará si se activa con las dependencias declaradas.

### 3. El balance final solo procesa 20 cuentas

En `src/final_audit_module.py`, `generate_final_balance()` itera:

`for account in accounts[:20]:  # Sample data`

**Impacto:** el “balance final” puede omitir cuentas reales. Esto invalida su uso como balance final de auditoría.

### 4. Papeles de trabajo con columnas placeholder

En `src/comprehensive_audit_papers.py`, varias columnas de las áreas se rellenan explícitamente con cero:

`# Fill remaining columns with placeholders`

Además, el papel de partes vinculadas incorpora filas de ejemplo fijas para socios, administradores y empresas del grupo.

**Impacto:** algunos papeles parecen completos visualmente, pero contienen campos que no proceden de evidencia contable/documental.

### 5. El paquete final no genera las CCAA completas que afirma el flujo

`generate_annual_accounts_review()` genera un **checklist de revisión** con marcas `✓`, no los estados financieros completos.

En el fichero revisado no se localizan generadores de ECPN, EFE o IGPN; sin embargo, `generate_audit_report()` redacta que se han auditado balance, PyG, ECPN, EFE y memoria.

**Impacto:** riesgo de generar un informe que haga referencia a estados que el propio sistema no ha producido ni validado.

### 6. Artículo 229 LSC incorrectamente interpretado

`generate_art229_confirmation()` crea una confirmación sobre acceso a información, limitaciones al alcance, independencia y procedimientos de auditoría.

El artículo 229 de la LSC regula el **deber de evitar situaciones de conflicto de interés de los administradores** y la comunicación de esos conflictos.

Fuente oficial: https://www.boe.es/buscar/act.php?id=BOE-A-2010-10544#a229

**Impacto:** contenido jurídico incorrecto para un entregable profesional.

### 7. RLC y RNT están mal definidos en `config.json`

El proyecto define:

- `rlc`: “registro mercantil”
- `rnt`: “registro propiedad”

En el ámbito laboral/TGSS:

- **RLC** = Recibo de Liquidación de Cotizaciones.
- **RNT** = Relación Nominal de Trabajadores.

Fuente oficial TGSS: https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/CotizacionRecaudacionTrabajadores/9896/38386/38394

**Impacto:** clasificación documental errónea en un área crítica para auditoría/subvenciones.

### 8. La “auto-recuperación con IA” no es IA

`src/emergency_control.py` describe expresamente el analizador como:

`heuristic analysis (simulated AI behavior)`

Es un motor de reglas/patrones de excepciones y reintentos. Puede ser útil, pero no debe venderse ni etiquetarse como recuperación mediante IA.

### 9. La IA local no coincide con la arquitectura objetivo

La configuración activa modelos locales, pero el código usa SentenceTransformer y `facebook/bart-large-mnli`. No existe integración con Ollama/Llama 3.1 8B en este PR.

## Prioridad de corrección

1. Bloquear cualquier informe final mientras existan `accounts[:20]`, placeholders y estados financieros no generados.
2. Corregir inmediatamente Art. 229, RLC y RNT.
3. Migrar la integración OpenAI a la API v1 actual o retirar esa opción hasta corregirla.
4. Crear CI real que instale dependencias y ejecute todos los tests en una base de datos temporal limpia.
5. Convertir tests ad hoc en pruebas automáticas con assertions y fixtures reproducibles.
6. Separar claramente `demo/sample` de código de producción.
7. Implementar generación y conciliación real de Balance, PyG, EIGR/IGPN, ECPN, EFE y Memoria antes de afirmar que el paquete de CCAA está completo.
8. Añadir proveedor local Ollama/Llama 3.1 8B si se mantiene la arquitectura definida para Windows 11 / 16 GB.

## Conclusión

El proyecto **sí contiene trabajo técnico aprovechable**, especialmente núcleo contable, extracción documental y generadores de papeles. Sin embargo, el estado actual mezcla funcionalidad real con muestras, placeholders y afirmaciones superiores a la evidencia implementada. Debe tratarse como **V1 técnica en desarrollo**, no como sistema de auditoría terminado.
