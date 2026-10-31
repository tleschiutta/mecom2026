# MECOM 2026 · Programa interactivo

Web del programa del XLII Congreso Argentino de Mecánica Computacional (MECOM 2026), Mendoza, 10 al 13 de noviembre de 2026.

**Link:** https://tleschiutta.github.io/mecom2026/

- Programa por día, con filtros por sesión y sala y búsqueda por título, autor o número de trabajo.
- Vista "Ahora": lo que está en curso y lo que sigue en cada sala.
- "Mi agenda": charlas marcadas con ☆, aviso de superposiciones y exportación al calendario (.ics).
- Se puede instalar en el celular y funciona sin conexión.

## Datos

Fuente: programa oficial publicado por AMCA (`MECOM_2026_Programa_Dias_y_Trabajos_A4.pdf`).

La app lee al abrir la planilla de Google **MECOM2026_Programa_BD** (hoja `programa`, publicada como CSV).
Para corregir algo alcanza con editar la planilla: los cambios aparecen en la app en pocos minutos.
Si la planilla no está disponible, la app usa la copia embebida en `index.html`.

## Estructura

- `index.html`, `manifest.json`, `sw.js`, `icon-*.png`: el sitio publicado.
- `fuente/`: plantilla de la app (`app.html`), datos (`data/*.csv`) y `build.py`, que regenera el sitio:
  `python3 fuente/build.py --site URL_CSV` (correr desde `fuente/`).
