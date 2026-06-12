# Priorización territorial de ANP federales — Prototipo para FMCN

**Enlace al prototipo:** _(pendiente de deploy — ver docs/despliegue.md; mientras tanto: `cd web && python -m http.server 8000`)_
**Candidato:** Joel Bravo — Oficial de Innovación Tecnológica · **Fecha:** 11 de junio de 2026

---

## Parte 1 — Problema, usuarios y datos

El FMCN invierte en conservación a lo largo de todo el territorio nacional y debe decidir **dónde** concentrar recursos limitados, además de **rendir cuentas a donantes** con evidencia geográfica clara. Hoy esa decisión se apoya en documentos dispersos; no existe una vista única que cruce las Áreas Naturales Protegidas con el contexto socioeconómico que presiona su conservación.

**Usuarios:** la dirección de programas (priorización de inversión), los oficiales de proyecto (contexto territorial de su cartera) y el área de desarrollo institucional (evidencia visual y reproducible para donantes).

**Capas y fuentes.** (1) ANP federales de CONANP — polígonos, categoría de manejo, superficie y estados; capa "septiembre 2024" del geoportal CONABIO (`anpmx`), con servicio REST de CONANP/CENAPRED como espejo para el modo demo. (2) Índice de marginación municipal de CONAPO, como proxy de presión socioeconómica sobre las ANP. (3) Marco Geoestadístico municipal de INEGI para el cruce espacial. Detalle completo con URLs y fechas de consulta en `docs/fuentes.md`.

**Corrección al caso:** el enunciado menciona "198 ANP (dato preliminar)". Verificado contra la fuente primaria (Numeralia SIMEC, CONANP, consulta 11-jun-2026), la cifra oficial es **232 ANP federales** que cubren 98,000,719 ha. El prototipo y este documento usan 232.

## Parte 3 — Arquitectura e implementación

**Qué usé y cómo se complementa.** CONANP aporta *qué* proteger; CONAPO/INEGI aportan el *contexto social* que presiona cada área; MapLibre GL JS permite *explorar* el cruce de ambas. El procesamiento es un pipeline reproducible en Python (`scripts/pipeline.py`): carga y valida el shapefile (conteo = 232), reproyecta a EPSG:4326, hace el join espacial ANP × municipios, calcula la marginación promedio por ANP y simplifica geometrías a < 5 MB por capa. La app es **estática** (un `index.html`, sin frameworks ni build): abre con un enlace, cuesta $0 de infraestructura y no genera dependencia de ningún proveedor.

**Aporte de análisis.** No es solo un mapa con puntos: incluye un **índice de priorización 0–100** por ANP que combina tres criterios normalizados —presión socioeconómica (marginación promedio), superficie (escala logarítmica) y presencia territorial (municipios que intersecta)— con **pesos ajustables en vivo** mediante sliders, y una tabla "Top 10" que se reordena al instante. Los pesos son ilustrativos: la herramienta soporta la decisión, no la sustituye.

**De prototipo a sistema institucional.** Fase 1 (actual): hosting estático en Cloudflare Pages, ~$0–50 USD/mes. Fase 2, si crecen capas y usuarios: PostGIS + tileserver en un VPS (~$80–150 USD/mes), autenticación y roles. La actualización semestral de capas reutiliza el pipeline existente (~4 h por ciclo). Operación: un perfil técnico medio a tiempo parcial con soporte puntual de consultoría. El presupuesto de $300,000 MXN alcanza holgado: el grueso va a **capacitación** (~$80–120k), consultoría de endurecimiento (~$100k) y contingencia.

**Adopción.** Dos talleres (técnico y no técnico), manual de una página, "champions" por área y sesión de retroalimentación al mes 3.

**Limitaciones honestas.** Pesos del índice ilustrativos; sin autenticación en el prototipo; datos a fecha de corte, no en tiempo real; la simplificación de geometrías sacrifica precisión de bordes; una sola capa de cruce socioeconómico. En el modo demo (servicio REST en vivo) la capa ANP es la versión 2020 (182 ANP) y el cruce ANP–municipio se hace por nombre, una aproximación; el pipeline con el shapefile de septiembre 2024 produce el join espacial exacto con las 232 ANP y datos CONAPO 2020.

## Parte 4 — Ciberseguridad

**Qué no publicar:** ubicaciones precisas de especies en riesgo (facilitan caza furtiva y tala ilegal), datos de brigadas y comunidades, montos y condiciones por donante, e infraestructura de vigilancia.

**Control de acceso:** versión pública con datos agregados; versión interna detrás de autenticación. Ejemplo concreto: Cloudflare Access (Zero Trust) con SSO por correo institucional y roles — la dirección ve todo, los oficiales su región, los donantes dashboards agregados.

**Riesgos y mitigaciones:** scraping de capas sensibles → no exponerlas nunca en el frontend público; credenciales en el repositorio → secrets y repo privado; URLs de fuentes oficiales que cambian → script de verificación y copia local versionada (`scripts/snapshot_servicios.py` ya lo implementa); pérdida de datos → respaldo del repositorio y de `data/raw/`.

## Parte 5 — Bitácora de uso de IA

**Herramientas:** Claude (Cowork desktop) como asistente principal de análisis, código y redacción; Python 3 + geopandas (pipeline); MapLibre GL JS 4.7 (visor); Cloudflare Pages (hosting). Registro completo en `BITACORA.md`.

**Validaciones y correcciones (selección):**

1. **198 → 232.** El dato del caso era incorrecto; se verificó contra la Numeralia SIMEC de CONANP (consulta 11-jun-2026) y se corrigió en todo el material. Ninguna cifra se aceptó sin fuente primaria.
2. **Versión de capa detectada.** El servicio REST disponible para el demo entrega la capa CONANP **2020 con 182 ANP** — se detectó consultando `returnCountOnly` y se documentó como limitación en lugar de presentarla como si fuera la capa vigente.
3. **Datos sucios reales.** El servicio devuelve nombres con codificación rota (p. ej. "Villa de -lvarez" por "Villa de Álvarez"); el cruce por nombre normaliza cadenas (minúsculas, sin acentos ni signos) para tolerarlo, y la app reporta en pantalla cuántas ANP lograron cruce socioeconómico, en lugar de ocultar los huecos.
4. **Contingencia de entorno.** El entorno de ejecución local falló durante la sesión; en lugar de detener el trabajo se rediseñó la carga de datos para que la app consuma los servicios oficiales directamente, con script de respaldo para generar copias locales — la incidencia y la adaptación quedaron registradas.

**Principio de trabajo:** toda cifra contra fuente primaria; todo código probado antes de integrarse; la IA acelera, el criterio humano valida.
