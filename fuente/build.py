"""Genera la app.
  python3 build.py                -> build/index.html (archivo único, datos embebidos)
  python3 build.py --site URL_CSV -> site/ listo para GitHub Pages (PWA + lectura de la planilla)
"""
import csv, json, sys, datetime, pathlib, shutil
root = pathlib.Path(__file__).parent
SRC = root/"src" if (root/"src").exists() else root   # en el repo, la plantilla está junto a build.py
items = list(csv.DictReader(open(root/"data/programa.csv", encoding="utf-8")))
ses = {r["codigo"]: r["nombre"] for r in csv.DictReader(open(root/"data/sesiones.csv", encoding="utf-8"))}
cols = ["id","tipo","sesion","dia","inicio","fin","sala","titulo","autores","notas"]
items = [{k: (r.get(k) or "").strip() for k in cols} for r in items]
version = datetime.date.today().isoformat()
data = {"version": version, "sesiones": ses, "items": items}
html = (SRC/"app.html").read_text(encoding="utf-8")
html = html.replace("/*__DATA__*/", "window.PROGRAMA = " + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";")
if "--site" in sys.argv:
    url = sys.argv[sys.argv.index("--site")+1] if len(sys.argv) > sys.argv.index("--site")+1 else ""
    html = html.replace('const CSV_URL = "";', f'const CSV_URL = {json.dumps(url)};')
    out = root/"site" if (root/"src").exists() else root.parent; out.mkdir(exist_ok=True)
    (out/"index.html").write_text(html, encoding="utf-8")
    for f in ["manifest.json","icon-192.png","icon-512.png"]: shutil.copy(SRC/f, out/f)
    (out/"sw.js").write_text((SRC/"sw.js").read_text(encoding="utf-8").replace("__VERSION__", version+"-"+datetime.datetime.now().strftime("%H%M%S")), encoding="utf-8")
    print(f"site/ listo ({len(items)} filas) · CSV_URL = {url or '(sin planilla)'}")
else:
    (root/"build").mkdir(exist_ok=True)
    (root/"build/index.html").write_text(html, encoding="utf-8")
    print(f"{len(items)} filas -> build/index.html")
