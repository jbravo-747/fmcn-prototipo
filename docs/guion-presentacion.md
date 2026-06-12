# Guion — Presentación de 15 minutos

**Min 0–2 · El problema.** FMCN decide dónde invertir en conservación y rinde cuentas a donantes; hoy no hay una vista única que cruce ANP con presión socioeconómica. Usuarios: dirección de programas, oficiales de proyecto, desarrollo institucional.

**Min 2–6 · Demo en vivo.** Flujo exacto a ensayar: (1) abrir el enlace; (2) clic en una Reserva de la Biosfera grande (p. ej. Calakmul) → popup con categoría, superficie, estados, marginación; (3) filtrar por categoría y por estado; (4) activar capa de marginación; (5) mover sliders del índice → recoloreo en vivo y Top 10 reordenándose; (6) clic en una fila del Top 10 → zoom al ANP. **Respaldo:** screenshots por si falla internet.

**Min 6–9 · Decisiones técnicas.** Stack abierto y estático (un HTML, $0, sin lock-in); fuentes oficiales (CONANP, CONAPO, INEGI); pipeline Python reproducible; el índice ponderado es el aporte de análisis — "no solo puntos en un mapa".

**Min 9–11 · Camino institucional y presupuesto.** Fase 1 estática ($0–50 USD/mes) → Fase 2 PostGIS + roles ($80–150 USD/mes). $300k MXN: grueso a capacitación, consultoría de endurecimiento, contingencia. Actualización semestral con el script existente.

**Min 11–13 · Ciberseguridad.** Qué no publicar (especies en riesgo, brigadas, donantes); público agregado vs. interno con Cloudflare Access y roles; riesgos y mitigaciones.

**Min 13–15 · Bitácora de IA.** Cerrar con la corrección 198→232 verificada en la Numeralia, la detección de la capa 2020 (182) en el servicio demo y los datos con codificación rota: la IA acelera, el criterio humano valida.

**Pregunta inevitable — "¿qué harías con más tiempo/presupuesto?":** PostGIS + tileserver, más capas (uso de suelo INEGI Serie VII, riqueza de especies CONABIO), actualización automatizada, autenticación con roles, módulo de reportes para donantes.

---

## Preguntas frecuentes — respuestas preparadas

**Datos y metodología**

1. **"¿Por qué el mapa dice 182 ANP si tú mismo afirmas que son 232?"** — Porque son dos cosas distintas y lo digo en pantalla: el demo consume un servicio REST público cuya capa es la versión 2020 (182 ANP); la cifra vigente verificada contra la Numeralia SIMEC es 232, y el pipeline con el shapefile sept-2024 de CONABIO ya valida ese conteo y sus categorías. Preferí mostrar la limitación a maquillarla — el contador dice la verdad de lo que se está viendo.

2. **"¿Qué tan confiable es el cruce ANP–municipio?"** — En el demo es por nombre (interpretando el campo MUNICIPIOS), una aproximación: resuelve 161 de 182; las ~21 sin cruce son marinas o con ubicación en texto libre, y la app lo reporta en pantalla. La versión institucional lo sustituye por un join espacial exacto con geopandas. El cruce se validó con una reimplementación independiente en Python: 182/182 coincidencias con la app.

3. **"¿Quién definió los pesos 50/30/20 del índice?"** — Nadie: son ilustrativos, y por eso son sliders. La herramienta soporta la decisión, no la sustituye; la calibración real se haría en taller con los expertos de programas. Es deliberado que mover los pesos reordene el Top 10 en vivo: muestra la sensibilidad de la decisión.

4. **"¿Por qué marginación como proxy de presión sobre las ANP?"** — Es la capa socioeconómica oficial (CONAPO), municipal, pública y actualizada; correlaciona con presiones documentadas (cambio de uso de suelo, extracción). Es *una* dimensión, no la única — el diseño admite añadir más criterios al índice.

5. **"¿Qué pasa con las ANP marinas en el índice?"** — No tienen municipios, así que su pilar socioeconómico cuenta como 0 conservando el peso (decisión documentada en la bitácora: renormalizar las inflaba al Top 1 solo por superficie). Si bajas el peso de marginación con el slider, suben solas — coherente.

**Técnica**

6. **"¿Por qué no usaste ArcGIS/QGIS Online?"** — Costo de licencias, lock-in y barrera para compartir. Esto es un HTML estático con MapLibre (open source): se abre con un enlace, cuesta ~$0/mes y cualquier perfil técnico medio lo mantiene. QGIS sí se usa en el flujo institucional para inspección, pero el entregable es web.

7. **"¿Qué pasa si se cae el servicio REST del que dependen las capas?"** — Nada: la app sirve copias locales versionadas (`web/data/`) generadas por un script de snapshot; el servicio en vivo es el respaldo, no la dependencia. Esa decisión vino de una contingencia real durante el desarrollo.

8. **"¿Esto escala?"** — Fase 2 documentada: PostGIS + tileserver (~$80–150 USD/mes) cuando crezcan capas y usuarios. El pipeline ya está escrito para esa transición; las capas se actualizan semestralmente reutilizándolo (~4 h por ciclo).

**Uso de IA**

9. **"¿Cuánto de esto lo hizo la IA y cómo sabes que está bien?"** — La IA generó la mayoría del código y borradores; cada salida pasó por validación documentada en la bitácora (24 entradas): toda cifra contra fuente primaria (ahí cayó el 198→232 del propio caso), todo código probado antes de integrarse (un harness de 12 verificaciones en navegador corre contra producción), y el índice se verificó con una reimplementación independiente más un cálculo a mano (Montes Azules = 63). La bitácora registra también los errores de la IA y cómo se detectaron — son evidencia de criterio, no vergüenzas.

10. **"Dame un ejemplo de error de la IA que hayas atrapado."** — El mejor: la paginación del servicio dependía de un flag (`exceededTransferLimit`) que el servidor omite en GeoJSON — la app habría cargado 50 de 182 ANP en silencio. Se detectó probando la consulta exacta antes de integrar. Otro: CONAPO usa nombres largos de estado ("Coahuila de Zaragoza") que rompían el cruce de 5 estados completos; lo reveló una validación independiente en Python, no el ojo.

**Seguridad y operación**

11. **"¿Es seguro tener esto público?"** — Lo público no contiene nada sensible: capas oficiales ya públicas y un índice derivado. La línea roja documentada: nunca exponer ubicaciones de especies en riesgo, datos de brigadas/comunidades ni montos por donante; eso iría en la versión interna con autenticación y roles (Fase 2). El repo es privado; el hosting (Vercel) despliega automático desde Git.

12. **"¿Qué le falta para ser producto?"** — Calibración de pesos con expertos, join espacial exacto con la capa INEGI (incidencia documentada: portal con tokens, ~1.5 GB), autenticación con roles, más dimensiones en el índice y pruebas con usuarios reales. Todo está priorizado en el documento final dentro del presupuesto planteado.
