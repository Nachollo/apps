# Auditoría de proyecto — Go Prompts AI / PromptForge

**Fecha:** 20/09/2026  
**Evidencia revisada:** exportación HTML de `gopromptsai.com` desde una ruta de dashboard autenticado.

## Estado provisional

**FUNCIONAL PARCIAL / PRODUCTO WEB REAL EVIDENCIADO — backend y pagos no reproducidos de forma independiente.**

## Evidencia positiva

- El artefacto es una página Next.js procedente de `https://www.gopromptsai.com/es/dashboard/collection/...`, no una maqueta standalone.
- Contiene chunks de Next.js, Vercel Analytics y Speed Insights.
- El HTML contiene datos server-rendered de catálogo con IDs, códigos de producto, categorías, precios y conteos de prompts.
- Existen rutas de dashboard y biblioteca.
- El artefacto contiene estado de usuario y flujo de cuenta.
- Existe lógica/UX para compra como invitado y creación posterior de contraseña para proteger las compras.
- Aparecen campos de suscripción y una promoción de suscripción.
- Se localizan URLs de almacenamiento `*.supabase.co/storage/v1/object/public/...`, evidencia de uso de infraestructura Supabase al menos para assets/datos asociados.
- El producto permite copiar prompts y abrirlos en ChatGPT, Claude, Gemini y DeepSeek.
- El HTML revisado muestra un catálogo grande servido a la aplicación, no un listado puramente hardcoded de unas pocas tarjetas.

## Límites de la evidencia

### 1. No se dispone del repositorio fuente

El HTML de producción permite acreditar bastante comportamiento desplegado, pero no permite revisar arquitectura de servidor, secretos, RLS de Supabase, seguridad, tests ni calidad del código fuente.

### 2. Pagos no probados de extremo a extremo

El artefacto contiene campos relacionados con productos/suscripciones y mensajes sobre compras, pero no he ejecutado un checkout ni una transacción. No puedo confirmar que Stripe cobre correctamente desde esta evidencia.

### 3. No se ha auditado control de acceso

La página exportada procede de un dashboard con contenido de usuario, pero no puedo confirmar desde el HTML guardado que todas las colecciones privadas estén correctamente protegidas en servidor.

## Conclusión

Go Prompts AI es, de los proyectos revisados hasta ahora, uno de los que presenta **más evidencia de producto realmente desplegado**. No debe clasificarse como demo. La siguiente auditoría debe centrarse en repositorio fuente, Supabase/RLS, autenticación, checkout, webhooks, entrega post-pago y tests.
