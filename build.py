#!/usr/bin/env python3
"""Genera el sitio estático. Uso:
  python3 build.py            -> solo artículos con revision_humana = "aprobado" (producción)
  python3 build.py --preview  -> suma los "pendiente" con aviso visible y noindex (solo para revisar)
Nunca incluye artículos "rechazado". Solo usa la librería estándar."""
import json, sys, shutil, html
from pathlib import Path
R = Path(__file__).parent
PREVIEW = "--preview" in sys.argv
S = json.loads((R/"data/site.json").read_text("utf-8"))
ALL = json.loads((R/"data/articles.json").read_text("utf-8"))
E = html.escape
BASE = S["base_url"].rstrip("/")
MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
def fecha(s):
    if not s: return "pendiente"
    y, m, d = s.split("-"); return f"{int(d)} de {MESES[int(m)-1]} de {y}"
ARTS = [a for a in ALL if a["revision_humana"] == "aprobado" or (PREVIEW and a["revision_humana"] == "pendiente")]
for a in ARTS:
    if a["revision_humana"] == "aprobado" and not (a.get("verificado") and a.get("fecha_publicacion")):
        sys.exit(f"ERROR: '{a['slug']}' está aprobado pero falta 'verificado' o 'fecha_publicacion'.")
BY = {a["slug"]: a for a in ARTS}
SECS = {
 "destinos": ("Destinos", "Destinos baratos y actividades gratuitas", ["Destinos baratos", "Actividades gratuitas"],
   "<p>Un destino económico no es solo el que tiene alojamiento barato: importa el costo de llegar, de moverse y de comer, y qué actividades no requieren pagar entrada. Cuando haya datos verificados, cada ficha de destino indicará su fuente y su fecha de comprobación.</p><p>Hasta entonces, mostramos únicamente lo que ya está revisado. Los destinos concretos se incorporan de a uno, con fuentes oficiales; no publicamos listas genéricas.</p>"),
 "escapadas": ("Escapadas", "Escapadas de fin de semana y cómo llegar", ["Escapadas de fin de semana", "Cómo llegar"],
   "<p>El costo y la factibilidad de una escapada dependen de tu ciudad de salida: no es lo mismo salir de Rosario, Mendoza, Tucumán o Buenos Aires. Por eso las guías por región se publican solo cuando hay datos de transporte vigentes y comprobados.</p><p>Mientras tanto, este es el material de método que sí está disponible.</p>"),
 "playas-y-naturaleza": ("Playas y naturaleza", "Playas y costa, ríos, lagos y sierras", ["Playas y costa", "Ríos, lagos y sierras"],
   "<p>Antes de elegir playa, río, lago o sierra, consultá a la autoridad local el estado de accesos, habilitación de balnearios o campings, clima y alertas. No recomendamos ingresar a sectores cerrados o no habilitados.</p>"),
 "presupuestos": ("Presupuestos", "Presupuestos, ahorro y consejos para viajar", ["Presupuestos y ahorro", "Consejos para viajar"],
   "<p>Armá tu presupuesto con tus propios datos. La calculadora de abajo suma lo que cargues; el sitio no completa precios por vos. Para cada gasto, usá una cotización o tarifa actual de la fuente oficial o del prestador.</p>"),
}
NAV = [("destinos/", "Destinos"), ("escapadas/", "Escapadas"), ("playas-y-naturaleza/", "Playas y naturaleza"), ("presupuestos/", "Presupuestos"), ("articulos/", "Artículos")]
PAGES = [("sobre-nosotros", "Sobre el proyecto"), ("contacto", "Contacto"), ("privacidad", "Política de privacidad"), ("metodologia-precios", "Metodología de precios"), ("politica-editorial", "Política editorial")]

def page(depth, path, title, desc, body, noindex=False, head="", current=None):
    root = "../" * depth
    canon = f'<link rel="canonical" href="{BASE}/{path}">' if BASE else ""
    og = f'<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:locale" content="es_AR">' + (f'<meta property="og:url" content="{BASE}/{path}">' if BASE else "")
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    nav = "".join(f'<li><a href="{root}{h}"' + (' aria-current="page"' if h == current else "") + f'>{n}</a></li>' for h, n in NAV)
    fl = "".join(f'<li><a href="{root}paginas/{s}.html">{n}</a></li>' for s, n in PAGES)
    return f'''<!doctype html>
<html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{robots}{canon}{og}
<link rel="stylesheet" href="{root}assets/css/styles.css">{head}</head>
<body><a class="skip" href="#contenido">Saltar al contenido</a>
<header class="site"><div class="wrap"><a class="brand" href="{root}index.html">{E(S["nombre"])}</a>
<button class="nav-btn" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
<nav id="menu" aria-label="Principal"><ul>{nav}</ul></nav></div></header>
<main id="contenido" tabindex="-1"><div class="wrap">{body}</div></main>
<footer class="site"><div class="wrap"><div class="cols">
<div><strong>{E(S["nombre"])}</strong><p>{E(S["lema"])}. Sitio editorial independiente sobre viajes por Argentina.</p></div>
<div><strong>Información</strong><ul>{fl}</ul></div>
<div><strong>Secciones</strong><ul>{"".join(f'<li><a href="{root}{h}">{n}</a></li>' for h, n in NAV)}</ul></div></div>
<small>Los datos de viaje cambian: verificá precios, horarios y accesos con la fuente oficial antes de salir.</small></div></footer>
<script src="{root}assets/js/main.js" defer></script>{'<script src="' + root + 'assets/js/search.js" defer></script>' if "resultados" in body else ""}
</body></html>'''

def card(a, root):
    b = ' <span class="badge">Borrador pendiente de revisión</span>' if a["revision_humana"] != "aprobado" else ""
    return f'<li class="card"><p class="tag">{E(a["categoria"])} · {E(a["region"])}</p><h3><a href="{root}articulos/{a["slug"]}/">{E(a["titulo"])}</a></h3><p>{E(a["descripcion"])}</p>{b}</li>'

def grid(items, root): return '<ul class="grid" id="resultados">' + "".join(card(a, root) for a in items) + "</ul>"
def write(rel, text):
    p = R/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, "utf-8")
def searchform(root, action):
    return f'''<form class="search" id="buscador" role="search" action="{action}" method="get" data-root="{root}"><label for="q">Buscar artículos</label>
<input id="q" name="q" type="search" autocomplete="off" placeholder="Ej.: presupuesto, transporte, clima"><button class="btn" type="submit">Buscar</button><button class="btn sec" type="button" id="limpiar">Limpiar búsqueda</button></form>
<p id="estado-busqueda" role="status" aria-live="polite"></p>'''

# Limpieza: elimina páginas de artículos que ya no corresponden (p. ej. borradores de un build anterior)
if (R/"articulos").exists():
    for d in (R/"articulos").iterdir():
        if d.is_dir() and d.name not in BY: shutil.rmtree(d)

# Artículos
for a in ARTS:
    ok = a["revision_humana"] == "aprobado"
    body = (R/"content"/f'{a["slug"]}.html').read_text("utf-8")
    aviso = "" if ok else '<p class="aviso" role="note"><strong>Borrador pendiente de revisión humana.</strong> Este texto no está verificado ni aprobado: no lo difundas ni lo tomes como información confirmada. No se incluye en el sitemap y está marcado como noindex.</p>'
    rel = "".join(f'<li><a href="../{s}/">{E(BY[s]["titulo"])}</a></li>' for s in a["relacionados"] if s in BY)
    ld = ""
    if ok and BASE:
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": a["titulo"], "description": a["descripcion"], "datePublished": a["fecha_publicacion"], "dateModified": a["verificado"], "inLanguage": "es-AR", "mainEntityOfPage": f'{BASE}/articulos/{a["slug"]}/'},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Artículos", "item": f"{BASE}/articulos/"},
                {"@type": "ListItem", "position": 3, "name": a["titulo"]}]}]}, ensure_ascii=False) + "</script>"
    h = f'''<p class="crumbs"><a href="../../index.html">Inicio</a> › <a href="../">Artículos</a> › {E(a["titulo"])}</p>
<article><h1>{E(a["titulo"])}</h1>{aviso}
<p class="meta">{E(a["categoria"])} · Región: {E(a["region"])} · Tipo de viaje: {E(a["tipo_viaje"])}<br>Redactado: {fecha(a["redactado"])} · Publicado: {fecha(a.get("fecha_publicacion"))} · Última verificación: {fecha(a.get("verificado"))}<br>{E(a["autoria"])}</p>
{body}
<section class="verificar"><h2>Qué verificar antes de salir</h2><ul>{"".join(f"<li>{E(v)}</li>" for v in a["verificar"])}</ul></section>
<h2>Fuentes para comprobar</h2><ul>{"".join(f'<li><a href="{E(f["url"])}" rel="noopener" target="_blank">{E(f["texto"])}</a></li>' for f in a["fuentes"])}</ul>
{"<h2>Seguir leyendo</h2><ul>" + rel + "</ul>" if rel else ""}</article>'''
    write(f'articulos/{a["slug"]}/index.html', page(2, f'articulos/{a["slug"]}/', f'{a["titulo"]} | {S["nombre"]}', a["descripcion"], h, noindex=not ok, head=ld, current="articulos/"))

# Índice de búsqueda: solo lo que se construyó
write("data/search-index.json", json.dumps([{"titulo": a["titulo"], "descripcion": a["descripcion"], "categoria": a["categoria"], "region": a["region"], "tipo_viaje": a["tipo_viaje"], "tags": a["tags"], "url": f'articulos/{a["slug"]}/', "borrador": a["revision_humana"] != "aprobado"} for a in ARTS], ensure_ascii=False, indent=1))

# Listado de artículos
lst = f'<h1>Artículos</h1><p class="lead">Guías para planificar viajes por Argentina. Buscá por tema o recorré el listado completo.</p>{searchform("../", "./")}' + (grid(ARTS, "../") if ARTS else '<ul id="resultados" class="grid"></ul><p>Todavía no hay artículos aprobados para publicar.</p>') + '<noscript><p>La búsqueda necesita JavaScript; el listado de arriba muestra todos los artículos.</p></noscript>'
write("articulos/index.html", page(1, "articulos/", f'Artículos | {S["nombre"]}', "Listado de guías para planificar viajes económicos por Argentina, con búsqueda por tema.", lst, current="articulos/"))

# Secciones
CALC = '''<h2>Calculadora con tus propios datos</h2><p>Cargá valores que hayas confirmado con cada prestador. Si dejás un campo vacío, se toma como cero.</p>
<form id="calc"><fieldset><legend>Datos de tu viaje</legend>
<div class="fila"><label for="personas">Cantidad de personas</label><input id="personas" name="personas" inputmode="numeric" required></div>
<div class="fila"><label for="noches">Cantidad de noches</label><input id="noches" name="noches" inputmode="numeric"></div>
<div class="fila"><label for="transporte">Transporte total del grupo (ida y vuelta)</label><input id="transporte" name="transporte" inputmode="decimal"></div>
<div class="fila"><label for="alojamiento">Alojamiento por noche (todo el grupo)</label><input id="alojamiento" name="alojamiento" inputmode="decimal"></div>
<div class="fila"><label for="comida">Comidas por persona y por día</label><input id="comida" name="comida" inputmode="decimal"></div>
<div class="fila"><label for="actividades">Entradas y actividades por persona (total)</label><input id="actividades" name="actividades" inputmode="decimal"></div>
<div class="fila"><label for="otros">Otros gastos del viaje (total)</label><input id="otros" name="otros" inputmode="decimal"></div>
<div class="fila"><label for="imprevistos">Margen para imprevistos (%)</label><input id="imprevistos" name="imprevistos" inputmode="decimal"></div>
<button class="btn" type="submit">Calcular</button></fieldset></form>
<output id="calc-out" class="total" for="calc" role="status">Completá el formulario y presioná Calcular.</output>
<noscript><p>Sin JavaScript, usá esta fórmula: transporte + alojamiento × noches + comida × personas × (noches + 1) + actividades × personas + otros, más el margen de imprevistos.</p></noscript>'''
for slug, (nom, tit, cats, intro) in SECS.items():
    parts = ""
    for c in cats:
        xs = [a for a in ARTS if a["categoria"] == c]
        parts += f"<h2>{c}</h2>" + (grid(xs, "../") if xs else '<p>Sin artículos aprobados en esta categoría por ahora. Se agregan cuando tienen datos verificados y fuentes oficiales.</p>')
    body = f'<h1>{tit}</h1><div class="lead">{intro}</div>{parts}' + (CALC if slug == "presupuestos" else "")
    write(f"{slug}/index.html", page(1, f"{slug}/", f"{tit} | {S['nombre']}", intro.split("</p>")[0][3:].replace("<", "")[:155], body, current=f"{slug}/"))

# Portada
feat = grid(ARTS[:3], "") if ARTS else "<p>Todavía no hay artículos aprobados para destacar.</p>"
regs = ["Patagonia", "Cuyo", "Noroeste", "Noreste y Litoral", "Centro y Sierras", "Costa de Buenos Aires"]
home = f'''<section class="hero"><h1>{E(S["lema"])}</h1><p class="lead">Guías para planificar escapadas y vacaciones por Argentina con información comprobable: qué gastos calcular, cómo comparar el transporte y qué verificar antes de salir.</p>{searchform("", "articulos/")}</section>
<h2>Categorías</h2><ul class="grid">{"".join(f'<li class="card"><h3><a href="{h}/">{E(t)}</a></h3><p>{E(" · ".join(c))}</p></li>' for h, (n, t, c, _) in SECS.items())}</ul>
<h2>Artículos destacados</h2>{feat}
<h2>Escapadas por región</h2><p>Estamos investigando regiones de a una. Cada guía se publicará solo con datos verificados y fuentes oficiales; no mostramos destinos ni precios sin respaldo.</p>
<ul class="grid">{"".join(f'<li class="card estado"><h3>{r}</h3><p><span class="badge">En investigación</span></p></li>' for r in regs)}</ul>
<h2>Guía rápida para calcular tu presupuesto</h2><ol><li>Listá transporte, alojamiento, comidas, actividades e imprevistos.</li><li>Separá costos por persona, por grupo, por noche y por viaje.</li><li>Confirmá cada monto con una fuente actual y anotá la fecha.</li><li>Sumá con la <a href="presupuestos/">calculadora de presupuestos</a>.</li></ol>
<h2>Viajar con responsabilidad</h2><ul><li>Consultá clima, rutas y alertas con fuentes oficiales antes de salir.</li><li>Usá solo accesos, campings y balnearios habilitados.</li><li>Llevá tu basura y respetá las normas de áreas protegidas.</li><li>Confirmá por escrito lo que incluye cada reserva.</li></ul>'''
write("index.html", page(0, "", f'{S["nombre"]} | {S["lema"]}', "Guías para planificar viajes y escapadas por Argentina: presupuesto, transporte y qué verificar antes de salir.", home))

# Páginas editoriales
mail = f'<a href="mailto:{E(S["email_contacto"])}">{E(S["email_contacto"])}</a>' if S["email_contacto"] else None
titular = E(S["titular_legal"]) if S["titular_legal"] else None
EDIT = {
 "sobre-nosotros": ("Sobre el proyecto", f"<p>{E(S['nombre'])} es un sitio editorial que busca ayudar a viajeros de toda Argentina a planificar escapadas y vacaciones con información comprobable. {('Titular del sitio: ' + titular + '.') if titular else 'La identidad del titular del sitio todavía no fue informada.'}</p><p>Los textos pueden redactarse con asistencia de herramientas de IA, pero ninguno se publica sin revisión humana de hechos, fuentes y enlaces. No afirmamos haber visitado un destino salvo que así se indique expresamente en el artículo.</p>"),
 "contacto": ("Contacto", f"<p>Para correcciones, consultas o sugerencias: {mail}.</p>" if mail else "<p>Este sitio todavía no tiene un canal de contacto público habilitado.</p>"),
 "privacidad": ("Política de privacidad", f"<p>En su estado actual, este sitio no incluye formularios de envío de datos, herramientas de analítica ni publicidad. La calculadora de presupuestos opera en tu navegador y no envía lo que cargás. El servicio de hosting puede registrar datos técnicos de acceso (como dirección IP y navegador) según sus propias políticas.</p><p>Si en el futuro se agregan analítica, publicidad u otros servicios, esta política se actualizará antes de activarlos. Los servicios publicitarios de terceros pueden usar cookies o tecnologías similares conforme a sus políticas y a la normativa aplicable, y puede requerirse tu consentimiento.</p><p>{('Consultas sobre privacidad: ' + mail + '.') if mail else 'Aún no hay un canal de contacto informado para consultas de privacidad.'}</p><p>Este texto es una plantilla informativa y no garantiza el cumplimiento legal; el titular debe revisarlo y adaptarlo.</p>"),
 "metodologia-precios": ("Metodología de precios", "<p>Por ahora este sitio no publica precios estimados. Una cifra solo se incluirá cuando provenga de una fuente oficial o de un prestador identificado, con la fecha de consulta y el alcance indicado (por persona, por grupo, por noche o por viaje).</p><p>Si un dato no puede verificarse, el artículo lo dice y remite a la fuente a consultar. Las estimaciones propias solo se publicarán con la metodología y las fuentes que las respalden.</p>"),
 "politica-editorial": ("Política editorial", "<p>Cada artículo debe tener una intención de búsqueda concreta, fuentes verificables, fecha de última verificación y una sección de qué comprobar antes de salir.</p><ul><li>No se inventan precios, horarios, citas, reseñas ni fuentes.</li><li>Los borradores pasan por revisión humana antes de publicarse.</li><li>Las imágenes se usan solo con permiso y atribución registrada.</li><li>Las correcciones se registran y actualizan la fecha de verificación.</li><li>No se publica contenido masivo que solo cambie el nombre de la localidad.</li></ul>"),
}
for s, (t, b) in EDIT.items():
    write(f"paginas/{s}.html", page(1, f"paginas/{s}.html", f'{t} | {S["nombre"]}', f"{t} de {S['nombre']}.", f"<h1>{t}</h1>{b}"))

# 404 (enlaces absolutos respecto de la raíz configurada)
r404 = (BASE + "/") if BASE else "/"
p404 = page(0, "404.html", f'Página no encontrada | {S["nombre"]}', "La página que buscás no existe o cambió de dirección.", f'<h1>No encontramos esa página</h1><p class="lead">Puede haber cambiado de dirección o no existir.</p><p><a class="btn" href="{r404}">Ir al inicio</a> <a class="btn sec" href="{r404}articulos/">Ver artículos</a></p>', noindex=True)
p404 = p404.replace('href="assets/', f'href="{r404}assets/').replace('src="assets/', f'src="{r404}assets/').replace('href="index.html"', f'href="{r404}"')
for h, _ in NAV: p404 = p404.replace(f'href="{h}"', f'href="{r404}{h}"')
p404 = p404.replace('href="paginas/', f'href="{r404}paginas/')
write("404.html", p404)

# robots y sitemap (solo URLs canónicas indexables)
urls = ["", *[f"{s}/" for s in SECS], "articulos/", *[f"paginas/{s}.html" for s, _ in PAGES], *[f'articulos/{a["slug"]}/' for a in ARTS if a["revision_humana"] == "aprobado"]]
write("robots.txt", "User-agent: *\nAllow: /\n" + (f"Sitemap: {BASE}/sitemap.xml\n" if BASE else ""))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ("".join(f"<url><loc>{BASE}/{u}</loc></url>\n" for u in urls) if BASE else "<!-- Definí base_url en data/site.json y volvé a ejecutar build.py para generar las URLs. -->\n") + "</urlset>\n"
write("sitemap.xml", sm)
print(f"Modo: {'PREVIEW' if PREVIEW else 'PRODUCCIÓN'} | artículos construidos: {len(ARTS)} | aprobados: {sum(a['revision_humana']=='aprobado' for a in ARTS)}")
if not BASE: print("AVISO: base_url vacío en data/site.json -> sin canonical ni URLs en sitemap.xml.")
