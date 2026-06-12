# Plan de implementación — Evaluación técnica FMCN (Oficial de Innovación Tecnológica)

**Plazo:** 3 días | **Herramienta de ejecución:** Claude Cowork (desktop)
**Entregables:** (1) Prototipo funcional (enlace web), (2) Documento de máximo 4 páginas (Partes 1, 3, 4, 5), (3) Bitácora de IA, (4) Presentación de 15 min.

---

## Decisiones de arquitectura (ya tomadas, no reabrir)

| Decisión | Elección | Justificación ante el panel |
|---|---|---|
| Stack del prototipo | Web app estática: HTML + MapLibre GL JS + GeoJSON | Abre con un enlace sin instalaciones, costo $0, sin vendor lock-in, presupuesto libre para capacitación |
| Hosting | Cloudflare Pages (plan B: GitHub Pages) | Gratis, HTTPS, deploy en minutos |
| Procesamiento de datos | Python (geopandas) + mapshaper CLI | Reproducible, scripteable, auditable |
| Capa principal | ANP federales (CONANP, 232 ANP, sept. 2024) | Fuente primaria oficial |
| Capa de cruce | Índice de marginación CONAPO 2020 por municipio | Proxy de presión socioeconómica, dato oficial |
| Aporte de análisis | Índice de priorización 0–100 con pesos ajustables (sliders) | "No solo puntos en un mapa" — requisito explícito |

**Cifra verificada (11-jun-2026):** CONANP administra **232 ANP federales** (98,000,719 ha). Fuentes: Numeralia SIMEC (https://simec.conanp.gob.mx/numeralia/Tablas_Numeralia.pdf) y gob.mx/conanp. El "dato preliminar" de 198 del caso es incorrecto — corregirlo explícitamente en Parte 1 y bitácora.

---

## DÍA 1 — Datos, verificación y Parte 1

### 1.1 Setup del proyecto (30 min)
- [ ] Crear carpeta `fmcn-prototipo/` con estructura:
  ```
  fmcn-prototipo/
  ├── data/raw/          # descargas originales (no tocar)
  ├── data/processed/    # GeoJSON finales
  ├── scripts/           # pipeline Python
  ├── web/               # la app (index.html, app.js, style.css)
  ├── docs/              # Partes 1, 3, 4, 5
  └── BITACORA.md        # bitácora de IA — actualizar en cada sesión
  ```
- [ ] `git init` + repo remoto (privado por ahora).
- [ ] Crear `BITACORA.md` con columnas: fecha/hora, herramienta+versión, prompt, resultado, validación (aceptado/corregido/descartado y cómo).

### 1.2 Descarga y verificación de fuentes (2–3 h)
- [ ] **ANP federales (shapefile):** geoportal CONABIO — http://www.conabio.gob.mx/informacion/gis/ → buscar `anpmx` ("Áreas Naturales Protegidas Federales de México, septiembre 2024"). Alternativa: http://sig.conanp.gob.mx/website/pagsig/info_shape.htm
  - Verificar: conteo de polígonos = 232. Documentar fecha de la capa y de descarga.
- [ ] **Índice de marginación por municipio (CONAPO 2020):** https://www.gob.mx/conapo → Datos Abiertos → "Índice de marginación por municipio 2020" (CSV/XLSX con clave geoestadística CVEGEO).
- [ ] **Marco Geoestadístico INEGI (polígonos municipales):** https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463770541 (Marco Geoestadístico, versión más reciente). Solo se necesita la capa municipal.
- [ ] **(Opcional, si hay tiempo el Día 2):** uso de suelo y vegetación INEGI Serie VII, o riqueza de especies de CONABIO.
- [ ] Registrar TODAS las fuentes en `docs/fuentes.md`: nombre, institución, URL exacta, fecha de publicación de la capa, fecha de consulta.
- [ ] **Si una fuente no descarga o cambió de URL:** documentarlo (el caso lo pide explícitamente) y usar la alternativa. No perder más de 45 min por fuente.

### 1.3 Pipeline de datos (3–4 h, con Cowork)
Prompt sugerido para Cowork:
> "Tengo en data/raw/ el shapefile de ANP federales de CONANP, el CSV de marginación de CONAPO 2020 y el marco geoestadístico municipal de INEGI. Escribe un script Python con geopandas que: (1) cargue el shapefile de ANP, valide que son 232 registros, reproyecte a EPSG:4326 y exporte GeoJSON; (2) haga join del índice de marginación con los polígonos municipales por CVEGEO, validando que no haya municipios sin match; (3) simplifique geometrías para que cada GeoJSON pese < 5 MB (usa mapshaper o shapely simplify, reporta el % de vértices eliminados); (4) calcule por ANP los campos: superficie_ha, categoria_manejo, estados, y el grado de marginación promedio de los municipios que intersecta. Imprime un reporte de validación al final."

- [ ] Validar manualmente contra la Numeralia: conteo por categoría de manejo (48 Reservas de la Biosfera, 28 Santuarios, etc.). Si no cuadra, investigar antes de seguir.
- [ ] **Anotar en bitácora cualquier error de la IA** (joins incorrectos, supuestos de CRS, etc.) — es material de oro para la Parte 5.

### 1.4 Redactar Parte 1 (1 h)
- [ ] Media página: problema (FMCN necesita priorizar inversión territorial y rendir cuentas a donantes con evidencia geográfica), usuarios (dirección de programas, oficiales de proyecto, área de desarrollo institucional/donantes), capas y fuentes con fechas.
- [ ] Incluir la corrección 198 → 232 con cita a la Numeralia SIMEC y fecha de consulta.

**Criterio de done Día 1:** GeoJSONs validados en `data/processed/`, fuentes documentadas, Parte 1 redactada, bitácora con al menos 3 entradas.

---

## DÍA 2 — Construcción del prototipo

### 2.1 Esqueleto de la app (mañana)
Prompt sugerido para Cowork:
> "Construye una web app estática (un solo index.html con JS y CSS embebidos o en archivos separados, sin frameworks ni build step) usando MapLibre GL JS desde CDN. Requisitos: (1) mapa base con tiles gratuitos (Carto Voyager o OSM); (2) carga los GeoJSON de data/processed/ (ANP y municipios); (3) al hacer clic en una ANP, popup con nombre, categoría de manejo, superficie, estados y grado de marginación promedio; (4) panel lateral con: toggle de capas, filtro por categoría de manejo (checkboxes) y filtro por estado (dropdown); (5) diseño limpio y profesional, responsive, en español. Sin localStorage."

- [ ] Probar localmente (`python -m http.server`). Verificar popups, filtros y rendimiento (si el mapa se arrastra lento, simplificar más las geometrías).

### 2.2 Índice de priorización (tarde — el diferenciador)
Prompt sugerido:
> "Agrega al panel un módulo 'Índice de priorización' con 3 sliders de pesos (0–100): (a) presión socioeconómica (grado de marginación promedio), (b) superficie del ANP (mayor superficie = mayor peso de conservación), (c) [tercer criterio según la capa opcional disponible, o densidad de municipios colindantes]. Normaliza cada criterio 0–1, calcula score ponderado 0–100 por ANP y recolorea los polígonos en una rampa de color en vivo al mover los sliders. Agrega una tabla 'Top 10 ANP prioritarias' que se actualice con los pesos, y una nota visible: 'Pesos ilustrativos y ajustables; la herramienta soporta la decisión, no la sustituye.'"

- [ ] Validar el cálculo a mano para 2–3 ANP (no confiar ciegamente en el JS generado — y anotarlo en la bitácora).

### 2.3 Deploy (1 h)
- [ ] Cloudflare Pages: conectar el repo, directorio `web/`, deploy. Plan B: GitHub Pages.
- [ ] Probar el enlace en: laptop, celular, y un navegador sin sesión (modo incógnito).
- [ ] Agregar en la app un footer con fuentes y fechas de los datos.

### 2.4 Captura de evidencia (30 min)
- [ ] Screenshots del prototipo para el documento y la presentación.
- [ ] Actualizar bitácora con los prompts del día y al menos un ejemplo de corrección.

**Criterio de done Día 2:** enlace público funcionando con mapa, 2 capas, popups, filtros e índice con sliders. **Esto es innegociable.**

---

## DÍA 3 — Documentos, bitácora y presentación

### 3.1 Parte 3 — Arquitectura e implementación (1.5 h, máx. 1 página)
Estructura:
1. **Qué usé y cómo se complementa:** CONANP (qué proteger) × CONAPO/INEGI (contexto social) × MapLibre (exploración) — pipeline reproducible en Python.
2. **De prototipo a sistema institucional:** hosting estático + tiles (~$0–50 USD/mes) → fase 2 con PostGIS + tileserver si crece (~$80–150 USD/mes en un VPS); actualización semestral de capas con el script existente (4 h de trabajo por ciclo); operación: 1 perfil técnico medio a tiempo parcial + soporte de consultoría puntual. Encaja holgado en los $300,000 MXN: grueso del presupuesto a capacitación (~$80–120k), consultoría de endurecimiento (~$100k) y contingencia.
3. **Adopción:** 2 talleres (técnico y no técnico), manual de una página, champions por área, sesión de retroalimentación al mes 3.
4. **Limitaciones honestas:** índice con pesos ilustrativos, sin autenticación en el prototipo, datos a fecha de corte (no tiempo real), simplificación de geometrías sacrifica precisión de bordes, una sola capa de cruce socioeconómico.

### 3.2 Parte 4 — Ciberseguridad (1 h, media página)
- **No publicar:** ubicaciones precisas de especies en riesgo (facilita caza furtiva/tala ilegal), datos de brigadas y comunidades, montos y condiciones por donante, infraestructura de vigilancia.
- **Control de acceso:** versión pública con datos agregados; versión interna detrás de autenticación — ejemplo concreto: Cloudflare Access (Zero Trust) con SSO por correo institucional y roles (dirección ve todo; oficiales ven su región; donantes ven dashboards agregados).
- **Riesgos y mitigación:** scraping de capas sensibles (no exponerlas en el frontend público), credenciales en el repo (secrets + repo privado), dependencia de URLs de fuentes oficiales que cambian (script de verificación + copia local versionada), pérdida de datos (backup del repo y de data/raw/).

### 3.3 Parte 5 — Bitácora (1.5 h, 1 página)
Consolidar `BITACORA.md` en narrativa:
1. **Herramientas y versiones:** Claude (Cowork desktop), Python 3.x + geopandas X.X, mapshaper X.X, MapLibre GL JS X.X, Cloudflare Pages. Rol de cada una.
2. **2–3 prompts más útiles** (copiar verbatim de la bitácora).
3. **Validaciones y correcciones — incluir obligatoriamente:**
   - El dato de 198 ANP del caso era incorrecto; verificado contra Numeralia SIMEC/CONANP: 232 ANP (fecha de consulta).
   - Al menos un error real de código o dato de la IA y cómo lo detectaste (validación manual del índice, conteos contra la Numeralia, etc.).
4. **Principio de trabajo:** toda cifra contra fuente primaria; todo código probado antes de integrarse; la IA acelera, el criterio humano valida.

### 3.4 Consolidación del documento (1.5 h)
- [ ] Unir Partes 1, 3, 4, 5 en un solo documento de **máximo 4 páginas** (Word o PDF), con el enlace del prototipo en la primera página y screenshots si cabe.
- [ ] Revisión ortotipográfica y de tono (público no técnico).

### 3.5 Presentación de 15 min (2 h + ensayo)
Guion sugerido:
- Min 0–2: el problema y a quién sirve.
- Min 2–6: **demo en vivo** del prototipo (clic, filtros, sliders del índice — ensayar el flujo exacto; tener screenshots de respaldo por si falla internet).
- Min 6–9: decisiones técnicas y trade-offs (por qué stack abierto, por qué estas capas).
- Min 9–11: camino a sistema institucional + presupuesto.
- Min 11–13: ciberseguridad.
- Min 13–15: bitácora de IA — cerrar con la corrección 198→232 como ejemplo de criterio.
- **Pregunta inevitable a preparar:** "¿qué harías con más tiempo/presupuesto?" → PostGIS + tileserver, más capas (Serie VII INEGI, CONABIO), actualización automatizada, autenticación con roles, módulo de reportes para donantes.

**Criterio de done Día 3:** documento de 4 páginas listo, enlace probado por tercera persona, guion ensayado al menos una vez con cronómetro.

---

## Contingencias
- **Fuente no descarga:** usar espejo (CONABIO ↔ CONANP), documentar el problema. No quemar más de 45 min.
- **Geometrías muy pesadas:** simplificar más agresivo con mapshaper (`-simplify 5% keep-shapes`); la fidelidad de bordes no es crítica para el caso de uso.
- **Cloudflare Pages falla:** GitHub Pages; último recurso: archivo HTML autocontenido que abra localmente (el caso lo permite).
- **Te quedas sin tiempo el Día 3:** recortar la capa opcional, nunca el índice de priorización ni la bitácora.
