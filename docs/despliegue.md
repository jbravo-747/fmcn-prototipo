# Despliegue

## Prueba local

```
cd web
python -m http.server 8000
```

Abrir http://localhost:8000. La app intenta usar `web/data/` (copias locales) y, si no existen, descarga las capas del servicio REST en vivo.

**Recomendado antes de publicar:** generar las copias locales para no depender del servidor externo:

```
pip install requests
python scripts/snapshot_servicios.py
```

## Repositorio git (esta sesión)

El repo se inicializó con `git init --separate-git-dir=~/fmcn-prototipo.git` porque la carpeta vive en un mount de OneDrive (DrvFs) que no permite `chmod`. La metadata git queda en `~/fmcn-prototipo.git` (ext4) y `web/.git` es un archivo que apunta ahí. **Empujar a GitHub desde WSL** (`git remote add origin … && git push -u origin main`); desde Git para Windows esa ruta de gitdir no resuelve. `data/raw/` (descargas pesadas) está en `.gitignore`; `web/data/` sí se versiona porque la app lo consume.

## Cloudflare Pages (plan A)

1. Subir el repo a GitHub (privado está bien).
2. Cloudflare Dashboard → Workers & Pages → Create → Pages → conectar el repo.
3. Build settings: framework **None**, build command vacío, **output directory: `web`**.
4. Deploy → URL `https://<proyecto>.pages.dev`.

## GitHub Pages (plan B)

Settings → Pages → Deploy from branch → carpeta `/web` (o mover el contenido de `web/` a la raíz de una rama `gh-pages`).

## Checklist post-deploy

- Probar el enlace en laptop, celular y ventana de incógnito.
- Verificar popups, filtros, sliders y la capa de marginación.
- Si el servicio REST falla por CORS en producción, ejecutar el snapshot y redeployar (las copias locales en `web/data/` tienen prioridad).
- Pedir a una tercera persona que abra el enlace antes de la presentación.
