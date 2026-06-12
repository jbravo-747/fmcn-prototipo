# -*- coding: utf-8 -*-
"""
Snapshot de los servicios REST usados por el prototipo.
Genera copias locales en web/data/ para que la app no dependa del servicio en vivo
(plan B ante CORS o caída del servidor). Solo requiere `requests`.

Uso:  python scripts/snapshot_servicios.py
"""
import json
import pathlib
import requests

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "web" / "data"
OUT.mkdir(parents=True, exist_ok=True)

SRV_ANP = "https://rmgir.proyectomesoamerica.org/server/rest/services/Aplicativos/SEDATU_TABASCO/MapServer/47/query"
SRV_MARG = "https://rmgir.proyectomesoamerica.org/server/rest/services/ANR/Indicadores/MapServer/5/query"


def paginado(url, params, formato, tam_pagina):
    """Descarga todas las páginas de un layer ArcGIS REST."""
    feats, offset = [], 0
    while True:
        p = dict(params, resultOffset=offset, f=formato)
        r = requests.get(url, params=p, timeout=120)
        r.raise_for_status()
        j = r.json()
        page = j.get("features", [])
        feats.extend(page)
        flag = j.get("exceededTransferLimit") or (j.get("properties") or {}).get("exceededTransferLimit")
        # Continuar si el flag lo indica o si la página vino llena (el flag puede faltar en f=geojson)
        if not page or (not flag and len(page) < tam_pagina):
            break
        offset += len(page)
    return feats


def main():
    print("Descargando ANP (GeoJSON simplificado)...")
    anp = paginado(SRV_ANP, {
        "where": "1=1",
        "outFields": "ID_ANP,NOMBRE,CAT_MANEJO,ESTADOS,MUNICIPIOS,REGION,SUPERFICIE,S_TERRES,S_MARINA,PRIM_DEC",
        "returnGeometry": "true", "outSR": "4326",
        "geometryPrecision": "4", "maxAllowableOffset": "0.005",
        "resultRecordCount": "50",
    }, "geojson", 50)
    fc = {"type": "FeatureCollection", "features": anp}
    (OUT / "anp.geojson").write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(anp)} ANP -> web/data/anp.geojson (esperado: 182 en la capa 2020)")
    assert len(anp) == 182, f"Conteo inesperado de ANP: {len(anp)}"

    print("Descargando marginación municipal (solo atributos)...")
    munis = paginado(SRV_MARG, {
        "where": "1=1",
        "outFields": "CVE_MUN,NOM_ENT,NOM_MUN,IM_2010,GM_2010,POB_TOT",
        "returnGeometry": "false", "resultRecordCount": "1000",
    }, "json", 1000)
    attrs = [m["attributes"] for m in munis]
    (OUT / "marginacion_municipal.json").write_text(json.dumps(attrs, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(attrs)} municipios -> web/data/marginacion_municipal.json (esperado: ~2456 en 2010)")

    print("Listo. La app usará estas copias locales automáticamente.")


if __name__ == "__main__":
    main()
