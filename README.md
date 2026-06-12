# Prototipo FMCN — Priorización territorial de ANP federales

Visor web de Áreas Naturales Protegidas federales (CONANP) cruzadas con el índice de marginación municipal (CONAPO 2020), con un índice de priorización 0–100 de pesos ajustables.

## Estructura

```
fmcn-prototipo/
├── data/raw/          # descargas originales (no tocar)
├── data/processed/    # GeoJSON finales que consume la app
├── scripts/           # pipeline Python reproducible
├── web/               # app estática (index.html)
├── docs/              # Partes 1, 3, 4, 5 y fuentes.md
└── BITACORA.md        # bitácora de IA
```

## Ejecutar localmente

```
cd web
python -m http.server 8000
# abrir http://localhost:8000
```

## Deploy

Cloudflare Pages (directorio `web/`) o GitHub Pages. Sin build step.

## Fuentes

Ver `docs/fuentes.md`. Datos: CONANP (sept. 2024), CONAPO (2020), INEGI.
