import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

import geopandas as gpd
from rasterio.features import rasterize

# ----------------------------
# Konfiguracja strony
# ----------------------------
st.set_page_config(
    page_title="NDMI – styl QGIS",
    layout="centered"
)

st.title("Normalized Difference Moisture Index (NDMI)")

st.markdown("""
**NDMI** służy do określania zawartości wody w roślinności
oraz monitorowania suszy.  
Zakres wartości: **-1 do 1**
""")

# ----------------------------
# Wzór
# ----------------------------
st.subheader("Formuła:")
st.latex(r"NDMI = \frac{B8 - B11}{B8 + B11}")

# ----------------------------
# Dane wejściowe
# ----------------------------
st.subheader("Dane wejściowe")

use_example = st.button("Użyj danych przykładowych")

if use_example:
    b8_file = "data/B8.tiff"
    b11_file = "data/B11.tiff"
    area_file = "data/area.geojson"
    st.success("Użyto danych przykładowych z folderu data/")
else:
    b8_file = st.file_uploader("Upload B8 (NIR)", type="tif")
    b11_file = st.file_uploader("Upload B11 (SWIR)", type="tif")
    area_file = st.file_uploader("Upload area (GeoJSON)", type="geojson")

# ----------------------------
# Sprawdzenie
# ----------------------------
if b8_file is None or b11_file is None:
    st.info("Upload both B8 and B11 files or use example data.")
    st.stop()

# ----------------------------
# Wczytywanie rastrów
# ----------------------------
with rasterio.open(b8_file) as src:
    b8 = src.read(1).astype(np.float32)
    transform = src.transform
    raster_shape = src.shape

with rasterio.open(b11_file) as src:
    b11 = src.read(1).astype(np.float32)

# ----------------------------
# NDMI
# ----------------------------
ndmi = (b8 - b11) / (b8 + b11 + 1e-6)
ndmi = np.clip(ndmi, -0.8, 0.8)

# ----------------------------
# Skala QGIS
# ----------------------------
qgis_colors = [
    (-0.8, "#800000"),
    (-0.24, "#ff0000"),
    (-0.032, "#ffff00"),
    (0.032, "#00ffff"),
    (0.24, "#0000ff"),
    (0.8, "#000080")
]

values, colors = zip(*qgis_colors)

cmap = LinearSegmentedColormap.from_list(
    "ndmi_qgis",
    list(zip([(v + 0.8) / 1.6 for v in values], colors))
)

norm = Normalize(vmin=-0.8, vmax=0.8)

# ----------------------------
# Tytuł mapy
# ----------------------------
if area_file:
    st.subheader("NDMI map with selected area")
else:
    st.subheader("NDMI map (full area)")

fig, ax = plt.subplots(figsize=(4.5, 4.5))
img = ax.imshow(ndmi, cmap=cmap, norm=norm)

# ----------------------------
# Obszar zaznaczony (granatowy)
# ----------------------------
if area_file:
    gdf = gpd.read_file(area_file)

    mask_area = rasterize(
        [(geom, 1) for geom in gdf.geometry],
        out_shape=raster_shape,
        transform=transform,
        fill=0,
        dtype="uint8"
    )

    ax.imshow(
        np.ma.masked_where(mask_area == 0, mask_area),
        cmap=LinearSegmentedColormap.from_list("garnet", ["#7b112c", "#7b112c"]),
        alpha=1.0
    )

    rows, cols = np.where(mask_area == 1)
    if len(rows) > 0:
        pad = 30
        ax.set_xlim(cols.min() - pad, cols.max() + pad)
        ax.set_ylim(rows.max() + pad, rows.min() - pad)

# ----------------------------
# Legenda
# ----------------------------
cbar = plt.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("NDMI")

ax.axis("off")
st.pyplot(fig)



# ----------------------------
# Interpretacja
# ----------------------------
st.subheader("Interpretacja NDMI")

st.markdown("""
- **NDMI < -0.24** – gleba jałowa  
- **-0.24 do -0.032** – bardzo niska wilgotność  
- **-0.032 do 0.032** – stres wodny  
- **0.032 do 0.24** – umiarkowana wilgotność  
- **> 0.24** – wysoka wilgotność roślinności
""")

# ----------------------------
# Analiza NDMI w obrębie obszaru wektorowego
# ----------------------------
if area_file:
    ndmi_masked = np.where(mask_area == 1, ndmi, np.nan)

    mean_ndmi = np.nanmean(ndmi_masked)
    min_ndmi = np.nanmin(ndmi_masked)
    max_ndmi = np.nanmax(ndmi_masked)
    pixel_count = np.sum(mask_area == 1)

    st.subheader("Statystyki NDMI dla wybranego obszaru")

    st.markdown(f"""
    - **Średnia wartość NDMI:** `{mean_ndmi:.3f}`
    - **Minimalna wartość NDMI:** `{min_ndmi:.3f}`
    - **Maksymalna wartość NDMI:** `{max_ndmi:.3f}`
    - **Liczba pikseli w obszarze:** `{pixel_count}`
    """)