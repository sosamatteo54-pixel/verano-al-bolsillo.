# Lista de lanzamiento y verificación

Estados: OK = comprobado en esta construcción · PENDIENTE = lo hace el propietario · NO VERIFICADO = no se pudo comprobar aquí.

| Ítem | Estado |
|---|---|
| Enlaces y recursos internos (tools/check.py) | OK en modo preview |
| JSON válido (articles.json, site.json, search-index.json) | OK |
| sitemap.xml bien formado | OK (vacío hasta definir base_url) |
| Un H1, título único, lang es-AR y meta description por página | OK |
| Sin "TODO", anuncios ni scripts de terceros en el HTML | OK |
| Búsqueda y calculadora en un navegador real | NO VERIFICADO |
| Diseño a 320 px y escritorio | NO VERIFICADO |
| Navegación por teclado, foco y contraste | NO VERIFICADO |
| Consola del navegador sin errores | NO VERIFICADO |
| Funcionamiento sin JavaScript | NO VERIFICADO |
| Definir `base_url` en data/site.json y reconstruir | PENDIENTE |
| Definir `email_contacto` y `titular_legal` | PENDIENTE |
| Abrir y comprobar todas las fuentes de cada artículo | PENDIENTE |
| Cambiar `revision_humana` a `aprobado` con `verificado` y `fecha_publicacion` | PENDIENTE |
| Ejecutar `python3 build.py` (sin --preview) antes de publicar | PENDIENTE |
| Elegir licencia (LICENSE) | PENDIENTE |
| Revisar y adaptar la política de privacidad | PENDIENTE |
| Search Console: propiedad y envío de sitemap | PENDIENTE |
| Imágenes: el sitio no usa imágenes; si agregás, registrar autor, origen, URL y licencia | PENDIENTE |

## Datos que el propietario debe verificar
- Que cada URL de fuente abra y contenga lo que el artículo afirma (varias apuntan a la página principal del organismo y hay que ubicar la sección concreta).
- Estado actual de servicios, tarifas, rutas y trenes antes de citarlos.
- Cualquier precio, horario o requisito que se agregue: con fuente y fecha.

## Antes de pedir AdSense (sin promesas de aprobación)
Tené contenido propio y útil suficiente, páginas editoriales completas, contacto real y política de privacidad adaptada. Revisá los requisitos y políticas vigentes de Google, resolvé el consentimiento aplicable a tu audiencia y actualizá la política antes de activar nada. No agregues anuncios hasta que corresponda.
