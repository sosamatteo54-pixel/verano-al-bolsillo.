# Verano al Bolsillo (nombre provisional)

Sitio estático (HTML, CSS y JavaScript sin dependencias) sobre viajes económicos por Argentina. No usa servidor, base de datos, claves ni servicios de pago. No incluye analítica ni publicidad, y no está aprobado por ningún programa de monetización.

## Arquitectura
Un script de Python (solo librería estándar, se usa en tu computadora) genera el HTML final a partir de `data/` y `content/`. Lo publicado es HTML real e indexable; el texto de los artículos no depende de JavaScript. JavaScript se usa solo para el menú móvil, la búsqueda y la calculadora, y hay alternativa sin JS (listado completo y fórmula escrita).
Cambios respecto de la estructura sugerida: se agregan `build.py`, `content/`, `tools/check.py`, `articulos/index.html` (listado y búsqueda), `data/site.json` y `data/search-index.json` (generado). Los borradores son entradas `pendiente` de `data/articles.json` y se construyen solo con `--preview`.

```text
build.py  README.md  LANZAMIENTO.md  LICENSE  robots.txt  sitemap.xml  404.html  index.html
data/        site.json  articles.json  search-index.json(generado)
content/     <slug>.html (texto de cada artículo)
drafts/      README.md  article-template.md  fichas-de-investigacion.md
assets/      css/styles.css  js/main.js  js/search.js  img/
tools/       check.py
destinos/ escapadas/ playas-y-naturaleza/ presupuestos/ articulos/ paginas/   (generados)
```

## Probar en local
```bash
python3 build.py --preview     # incluye borradores con aviso y noindex
python3 tools/check.py         # enlaces, H1, títulos, JSON y XML
python3 -m http.server 8000    # abrí http://localhost:8000
```
Probá a mano: búsqueda ("presupuesto", una palabra inexistente, Limpiar), calculadora, teclado (Tab, foco visible), 320 px de ancho, JavaScript desactivado y la consola sin errores.

## Configurar antes de publicar (`data/site.json`)
- `base_url`: URL final sin barra final (ej. la de tu hosting o dominio). Sin esto no hay canonical ni URLs en el sitemap.
- `email_contacto` y `titular_legal`: reales. Si quedan vacíos, las páginas lo dicen con honestidad.

## Agregar un artículo
1. Copiá `drafts/article-template.md` y completá la investigación con fuentes que abras y compruebes.
2. Escribí `content/<slug>.html` (solo `<p>`, `<h2>`, listas; enlaces internos relativos como `../otro-slug/`).
3. Agregá la entrada en `data/articles.json` con `revision_humana: "pendiente"`.
4. Revisalo con `python3 build.py --preview`.
5. Al aprobarlo: `revision_humana: "aprobado"`, `verificado` y `fecha_publicacion` (AAAA-MM-DD).
6. `python3 build.py` (producción), `python3 tools/check.py`, y subí los cambios.

## Publicar gratis
Confirmá en cada servicio que su plan gratuito vigente cubre tu uso.
- **GitHub Pages**: repositorio público → Settings → Pages → Deploy from a branch → `main` y carpeta `/ (root)`. La URL será del tipo `https://USUARIO.github.io/REPOSITORIO/`; cargala en `base_url`.
- **Cloudflare Pages**: conectá el repositorio, sin comando de build (la salida ya está generada) y directorio de salida `/`.
Mantené el repositorio sin datos privados: no subas claves, correos personales ni documentos.

## Google Search Console
1. Publicá con `base_url` correcto y entrá en Search Console con tu cuenta.
2. Agregá la propiedad y verificala con el método que ofrezca (para URL-prefix, normalmente un archivo HTML o una metaetiqueta que debés subir).
3. En "Sitemaps", enviá `sitemap.xml`. La indexación no es inmediata ni está garantizada.

## AdSense
No hay anuncios ni código de AdSense. Cuando consideres que el sitio cumple los requisitos, revisá las políticas vigentes de Google, actualizá la política de privacidad y resolvé el consentimiento que corresponda antes de activar nada. No hay promesa de aprobación ni de ingresos.
