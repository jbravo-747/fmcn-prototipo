# -*- coding: utf-8 -*-
"""
Pipeline institucional de datos — FMCN prototipo.

Procesa las fuentes primarias descargadas en data/raw/:
  1. Shapefile de ANP federales CONANP (sept. 2024, capa `anpmx` del geoportal CONABIO).
     Valida que sean 232 registros (Numeralia SIMEC, consulta 2026-06-11).
  2. Índice de marginación por municipio CONAPO 2020 (CSV/XLSX, clave CVEGEO).
  3. Marco Geoestadístico municipal INEGI (polígonos).

Genera en data/processed/ los GeoJSON que consume la web app, con join espacial
EXACTO (sustituye el cruce aproximado por nombre que usa el modo demo).

Requisitos: pip install geopandas pandas shapely pyogrio
Uso:        python scripts/pipeline.py
"""
import json
import pathlib
import sys

import geopandas as gpd
import pandas as pd

BASE = pathlib.Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

# Ajustar a los nombres reales de los archivos descargados:
SHP_ANP = RAW / "anpmx.shp"                          # CONANP sept. 2024
CSV_MARG = RAW / "IMM_2020.csv"                      # CONAPO 2020
SHP_MUN = RAW / "mg_municipios.shp"                  # INEGI Marco Geoestadístico

ANP_ESPERADAS = 232          # Numeralia SIMEC/CONANP, consulta 2026-06-11
TOL_SIMPLIFICACION = 0.005   # grados (~500 m); subir si los GeoJSON pesan > 5 MB
MAX_MB = 5

GRADO_NUM = {"Muy bajo": 1, "Bajo": 2, "Medio": 3, "Alto": 4, "Muy alto": 5}
NUM_GRADO = {v: k for k, v in GRADO_NUM.items()}


def reporte(msg):
    print(f"[pipeline] {msg}")


def simplificar_y_exportar(gdf, destino):
    """Simplifica geometrías y exporta GeoJSON; reporta reducción de vértices."""
    def n_vertices(geom):
        return len(geom.wkt)  # proxy barato del tamaño
    antes = gdf.geometry.apply(n_vertices).sum()
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(TOL_SIMPLIFICACION, preserve_topology=True)
    despues = gdf.geometry.apply(n_vertices).sum()
    gdf.to_file(destino, driver="GeoJSON")
    mb = destino.stat().st_size / 1e6
    reporte(f"{destino.name}: {mb:.1f} MB, reducción ~{100 * (1 - despues / antes):.0f}%")
    if mb > MAX_MB:
        reporte(f"ADVERTENCIA: {destino.name} pesa más de {MAX_MB} MB; "
                f"aumentar TOL_SIMPLIFICACION o usar mapshaper: "
                f"mapshaper {destino} -simplify 5% keep-shapes -o {destino}")
    return gdf


def main():
    # ---------- 1. ANP ----------
    if not SHP_ANP.exists():
        sys.exit(f"Falta {SHP_ANP}. Descargar de http://www.conabio.gob.mx/informacion/gis/ (capa anpmx).")
    anp = gpd.read_file(SHP_ANP)
    reporte(f"ANP cargadas: {len(anp)}")
    if len(anp) != ANP_ESPERADAS:
        reporte(f"ADVERTENCIA: se esperaban {ANP_ESPERADAS} ANP (Numeralia SIMEC). "
                "Verificar versión de la capa antes de continuar.")
    anp = anp.to_crs(4326)

    # Conteo por categoría de manejo para validar contra la Numeralia
    if "CAT_MANEJO" in anp.columns:
        reporte("Conteo por categoría:\n" + anp["CAT_MANEJO"].value_counts().to_string())

    # ---------- 2. Marginación CONAPO 2020 ----------
    if not CSV_MARG.exists():
        sys.exit(f"Falta {CSV_MARG}. Descargar de gob.mx/conapo (Índice de marginación por municipio 2020).")
    marg = pd.read_csv(CSV_MARG, dtype={"CVE_MUN": str, "CVEGEO": str})
    col_cve = "CVE_MUN" if "CVE_MUN" in marg.columns else "CVEGEO"
    col_gm = next(c for c in marg.columns if c.upper().startswith("GM"))
    col_im = next(c for c in marg.columns if c.upper().startswith("IM"))
    marg[col_cve] = marg[col_cve].str.zfill(5)
    reporte(f"Municipios CONAPO: {len(marg)} (esperado: 2469 en 2020)")

    # ---------- 3. Municipios INEGI + join ----------
    if not SHP_MUN.exists():
        sys.exit(f"Falta {SHP_MUN}. Descargar Marco Geoestadístico de INEGI (capa municipal).")
    mun = gpd.read_file(SHP_MUN).to_crs(4326)
    cve_mun_col = "CVEGEO" if "CVEGEO" in mun.columns else "CVE_MUN"
    mun[cve_mun_col] = mun[cve_mun_col].astype(str).str.zfill(5)
    mun = mun.merge(marg[[col_cve, col_im, col_gm]], left_on=cve_mun_col, right_on=col_cve, how="left")
    sin_match = mun[col_im].isna().sum()
    reporte(f"Municipios sin match de marginación: {sin_match} (investigar si > 5)")

    # ---------- 4. Cruce espacial ANP × municipios ----------
    anp = anp.reset_index(drop=True)
    anp["anp_idx"] = anp.index
    inter = gpd.sjoin(anp[["anp_idx", "geometry"]], mun[[cve_mun_col, col_im, col_gm, "geometry"]],
                      how="left", predicate="intersects")
    agg = inter.groupby("anp_idx").agg(
        im_promedio=(col_im, "mean"),
        n_municipios=(cve_mun_col, "nunique"),
    )
    anp = anp.merge(agg, left_on="anp_idx", right_index=True, how="left")
    anp["gm_promedio"] = anp["im_promedio"].apply(
        lambda v: None if pd.isna(v) else
        "Muy alto" if v >= 1 else "Alto" if v >= 0.25 else "Medio" if v >= -0.5 else
        "Bajo" if v >= -1.25 else "Muy bajo")
    reporte(f"ANP con cruce socioeconómico: {anp['im_promedio'].notna().sum()} de {len(anp)} "
            "(las marinas pueden no intersectar municipios)")

    # ---------- 5. Exportar ----------
    simplificar_y_exportar(anp.drop(columns=["anp_idx"]), PROC / "anp.geojson")
    simplificar_y_exportar(mun, PROC / "municipios_marginacion.geojson")

    # Copia para la web app (usa estos en lugar del servicio en vivo)
    webdata = BASE / "web" / "data"
    webdata.mkdir(exist_ok=True)
    (webdata / "anp.geojson").write_bytes((PROC / "anp.geojson").read_bytes())
    attrs = mun[[cve_mun_col, col_im, col_gm]].rename(
        columns={cve_mun_col: "CVE_MUN", col_im: "IM_2010", col_gm: "GM_2010"})
    # Nota: la app espera NOM_ENT/NOM_MUN para el cruce por nombre; con el pipeline
    # el cruce exacto ya viene en anp.geojson (im_promedio), así que no son necesarios.
    (webdata / "marginacion_municipal.json").write_text(
        attrs.to_json(orient="records", force_ascii=False), encoding="utf-8")

    reporte("Pipeline completado. Validar manualmente 2-3 ANP contra la Numeralia antes de publicar.")


if __name__ == "__main__":
    main()
