# Guion — Presentación de 15 minutos

**Min 0–2 · El problema.** FMCN decide dónde invertir en conservación y rinde cuentas a donantes; hoy no hay una vista única que cruce ANP con presión socioeconómica. Usuarios: dirección de programas, oficiales de proyecto, desarrollo institucional.

**Min 2–6 · Demo en vivo.** Flujo exacto a ensayar: (1) abrir el enlace; (2) clic en una Reserva de la Biosfera grande (p. ej. Calakmul) → popup con categoría, superficie, estados, marginación; (3) filtrar por categoría y por estado; (4) activar capa de marginación; (5) mover sliders del índice → recoloreo en vivo y Top 10 reordenándose; (6) clic en una fila del Top 10 → zoom al ANP. **Respaldo:** screenshots por si falla internet.

**Min 6–9 · Decisiones técnicas.** Stack abierto y estático (un HTML, $0, sin lock-in); fuentes oficiales (CONANP, CONAPO, INEGI); pipeline Python reproducible; el índice ponderado es el aporte de análisis — "no solo puntos en un mapa".

**Min 9–11 · Camino institucional y presupuesto.** Fase 1 estática ($0–50 USD/mes) → Fase 2 PostGIS + roles ($80–150 USD/mes). $300k MXN: grueso a capacitación, consultoría de endurecimiento, contingencia. Actualización semestral con el script existente.

**Min 11–13 · Ciberseguridad.** Qué no publicar (especies en riesgo, brigadas, donantes); público agregado vs. interno con Cloudflare Access y roles; riesgos y mitigaciones.

**Min 13–15 · Bitácora de IA.** Cerrar con la corrección 198→232 verificada en la Numeralia, la detección de la capa 2020 (182) en el servicio demo y los datos con codificación rota: la IA acelera, el criterio humano valida.

**Pregunta inevitable — "¿qué harías con más tiempo/presupuesto?":** PostGIS + tileserver, más capas (uso de suelo INEGI Serie VII, riqueza de especies CONABIO), actualización automatizada, autenticación con roles, módulo de reportes para donantes.
