# Fuentes de datos

| Capa | Institución | URL exacta | Fecha de publicación | Fecha de consulta | Estado | Notas |
|---|---|---|---|---|---|---|
| ANP federales (polígonos) | CONANP / CONABIO (geoportal) | http://www.conabio.gob.mx/informacion/gis/maps/geo/anpmx.zip (capa `anpmx`, "ANP Federales de México, septiembre 2024") | sept. 2024 | 2026-06-11 | **Descargada y validada** | `anpmx.zip`, 5.96 MB, **232 polígonos**. Conteo por categoría verificado contra la Numeralia (ver abajo). Alternativa: http://sig.conanp.gob.mx/website/pagsig/info_shape.htm |
| Numeralia ANP (validación de conteo) | CONANP / SIMEC | https://simec.conanp.gob.mx/numeralia/Tablas_Numeralia.pdf | — | 2026-06-11 | Consultada | 232 ANP federales, 98,000,719 ha. Corrige el "dato preliminar" de 198 del caso. Categorías confirmadas con `anpmx`: 79 PN, 57 APFF, 48 RB, 28 Santuario, 15 APRN, 5 MN |
| Índice de marginación por municipio 2020 | CONAPO | https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xlsx | mayo 2021 | 2026-06-11 | **Descargada y validada** | `IMM_2020.xlsx`, 1.06 MB, **2469 municipios** con CVE_MUN, IM_2020, GM_2020. El host exige `User-Agent` de navegador. Convertida a `IMM_2020.csv` para el pipeline |
| Marco Geoestadístico (municipios) | INEGI | https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463807469 (MG Censo 2020) | dic. 2020 | 2026-06-11 | **No descargada (ver Incidencias)** | Descarga vía portal JS con tokens; archivo nacional integrado ~1.5 GB. Solo se necesita la capa municipal (AGEM) para el cruce espacial del pipeline |

## Servicios REST usados por el modo demo (verificados 2026-06-11)

| Servicio | URL | Contenido | Nota |
|---|---|---|---|
| ANP federales (CONANP, 2020) | https://rmgir.proyectomesoamerica.org/server/rest/services/Aplicativos/SEDATU_TABASCO/MapServer/47 | 182 polígonos con ID_ANP, NOMBRE, CAT_MANEJO, ESTADOS, MUNICIPIOS, SUPERFICIE, fechas de decreto. GeoJSON con paginación | Espejo en el Atlas Nacional de Riesgos (CENAPRED); capa **2020 (182 ANP)**, anterior a la vigente (232). Documentado como limitación del demo |
| Marginación municipal (CONAPO) | https://rmgir.proyectomesoamerica.org/server/rest/services/ANR/Indicadores/MapServer/5 | 2,456 municipios con CVE_MUN, NOM_ENT, NOM_MUN, IM_2010, GM_2010, POB_TOT | Versión **2010** en el servicio; el pipeline usa el CSV CONAPO **2020** |

## Incidencias de descarga

- **2026-06-11:** entorno local de ejecución (sandbox Linux de Cowork) no disponible durante la sesión → imposible correr geopandas/descargar shapefiles en el momento. Adaptación: la app consume los servicios REST oficiales directamente y `scripts/snapshot_servicios.py` genera copias locales; `scripts/pipeline.py` queda listo para procesar las fuentes primarias (shapefile sept. 2024, 232 ANP) cuando se descarguen.
- **2026-06-11:** la página de metadatos de CONABIO (geoportal.conabio.gob.mx/metadatos/doc/html/anpmx.html) respondió vacía vía fetch automatizado; la descarga del shapefile debe hacerse manualmente desde http://www.conabio.gob.mx/informacion/gis/.
- **2026-06-11:** el servicio REST devuelve nombres con codificación rota en mayúsculas acentuadas (p. ej. "Villa de -lvarez"); el cruce por nombre normaliza cadenas para tolerarlo.
- **2026-06-11 (descarga de primarias):** las dos primeras fuentes primarias **sí descargaron y se validaron**: `anpmx.zip` de CONABIO (232 ANP, categorías vs Numeralia) e `IMM_2020.xlsx` de CONAPO (2469 municipios). Dos fricciones resueltas: el host de CONAPO devuelve **HTTP 000 si falta `User-Agent`** de navegador (se usa `-A "Mozilla/5.0"`), y el entorno no traía `pip` (PEP 668; bootstrap con `get-pip.py --break-system-packages` para instalar geopandas).
- **2026-06-11 (INEGI no descargable en presupuesto):** el **Marco Geoestadístico municipal de INEGI** no se pudo descargar dentro del límite de 45 min/fuente: la descarga es vía portal JS con tokens de sesión (sin URL estática) y el conjunto nacional integrado pesa ~1.5 GB (inviable en el almacenamiento sincronizado de esta sesión). Impacto acotado: `pipeline.py` valida igual el conteo (232) y las categorías de las ANP y el conteo de CONAPO (2469); solo queda pendiente el **cruce espacial exacto** ANP × municipio, que en el modo demo se aproxima por nombre. Acción siguiente: descargar la capa municipal (AGEM) desde el portal de INEGI y volver a correr `pipeline.py` (ya probado hasta ese paso).
