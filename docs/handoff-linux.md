# Handoff — Continuar en equipo Ubuntu (full Linux)

**Repo:** https://github.com/jbravo-747/fmcn-prototipo (privado, cuenta `jbravo-747`)
**Estado:** prototipo funcional terminado y validado; falta prueba visual en navegador, deploy y pulido final.

## Qué está hecho (no rehacer)

- `web/index.html` — **versión rediseñada** (pestañas Mapa/Metodología, panel "Herramientas SIG", export CSV, animaciones CSS). Incluye las 4 correcciones validadas: alias de estados `normEdo()`, separador " e " en `splitMunis()`, popup vía feature-state, ANP marinas con pilar socioeconómico = 0. `web/index-clasico.html` es el respaldo de la versión anterior.
- `web/data/` — snapshot validado: 182 ANP (capa CONANP 2020 del espejo REST) + 2,456 municipios (marginación 2010). El cruce resuelve 161/182 ANP.
- `data/raw/` (NO está en el repo, gitignored) — en el equipo Windows quedaron `anpmx` sept-2024 (232 ANP, validado vs Numeralia) e `IMM_2020` (2,469 municipios). Re-descargar si se necesita el pipeline: CONABIO geoportal (`anpmx`) y CONAPO (¡exige User-Agent de navegador: `curl -A "Mozilla/5.0" ...`!).
- `scripts/snapshot_servicios.py` — regenera web/data/ desde los servicios REST.
- `scripts/pipeline.py` — pipeline institucional geopandas; corre validaciones con anpmx+CONAPO; el join espacial exacto requiere el Marco Geoestadístico INEGI (incidencia documentada: portal JS, ~1.5 GB, quedó pendiente).
- `docs/` — documento-final.md y .docx (Partes 1,3,4,5, ≤4 págs), guion-presentacion.md, fuentes.md, despliegue.md.
- `BITACORA.md` — 20+ entradas; es entregable evaluado, seguir alimentándola.

## Setup en Ubuntu (10 min)

```bash
sudo apt update && sudo apt install -y git gh python3 python3-pip pandoc
gh auth login --web        # flujo de código de 8 caracteres, sin tokens
gh repo clone jbravo-747/fmcn-prototipo
cd fmcn-prototipo
```

Repo normal en ext4 — desaparecen el separate-git-dir y los problemas de OneDrive/DrvFs.

## Pendientes en orden

### 1. Prueba visual (15 min) — lo único no verificado aún
```bash
cd web && python3 -m http.server 8000
```
Abrir http://localhost:8000 y verificar: carga "182" en el contador de capas; clic en una ANP → popup con marginación y score; sliders → recoloreo + Top 10 se reordena; clic en fila del Top 10 → zoom; capa marginación on/off; pestaña Metodología; botón Exportar Datos descarga el CSV; probar también en ventana angosta (responsive). Anotar en BITACORA.md el resultado.

### 2. Adelgazar anp.geojson (9.7 MB → <5 MB)
En `scripts/snapshot_servicios.py` subir `maxAllowableOffset` de `0.005` a `0.01` y re-correr (`pip install requests`). Verificar que sigan siendo 182 y que los bordes se vean razonables en el mapa. Commit.

### 3. Deploy
**Plan A — Cloudflare Pages** (mantiene repo privado): dash.cloudflare.com → Workers & Pages → Create → Pages → conectar GitHub → repo `fmcn-prototipo` → framework None, build command vacío, **output directory: `web`** → Deploy. (El dashboard falló en el equipo Windows la noche del 11-jun; reintentar desde Ubuntu.)

**Plan B — GitHub Pages** (requiere repo público):
```bash
gh repo edit jbravo-747/fmcn-prototipo --visibility public --accept-visibility-change-consequences
git subtree push --prefix web origin gh-pages
gh api -X POST repos/jbravo-747/fmcn-prototipo/pages -f "source[branch]=gh-pages" -f "source[path]=/" 2>/dev/null || true
```
URL: https://jbravo-747.github.io/fmcn-prototipo/

Probar el enlace en laptop, celular e incógnito. Pedir a una tercera persona que lo abra.

### 4. Cerrar el documento
Poner la URL pública en la primera línea de `docs/documento-final.md`, regenerar el Word:
```bash
cd docs && pandoc documento-final.md -o documento-final.docx
```
Verificar ≤4 páginas. Tomar screenshots del prototipo para documento/presentación.

### 5. Presentación
Ensayar el guion (`docs/guion-presentacion.md`) con cronómetro al menos una vez; tener screenshots de respaldo por si falla internet en la demo.

### 6. Seguridad (no saltarse)
- **Revocar el token de GitHub expuesto** la noche del 11-jun: GitHub → Settings → Developer settings → Fine-grained tokens.
- En el equipo Windows quedó `gh` con "credentials saved in plain text" — opcional: `gh auth logout` allí si ya no se usará.
- Si se optó por repo público, revisar que no haya nada sensible (no lo hay a la fecha de este handoff, pero revisar commits futuros).

## Prompt listo para Claude Code en Ubuntu

> Proyecto FMCN clonado de github.com/jbravo-747/fmcn-prototipo. Lee docs/handoff-linux.md, BITACORA.md y plan-implementacion-fmcn.md para el contexto completo. Ejecuta los pendientes del handoff en orden: (1) prueba visual de web/index.html en servidor local con navegador headless verificando consola sin errores y el checklist del handoff; (2) re-simplificación de anp.geojson a <5 MB; (3) deploy según el plan que te indique; (4) URL pública en documento-final.md y regenerar el docx con pandoc; registra TODO en BITACORA.md (entregable evaluado). No rehagas nada que el handoff marque como hecho.
