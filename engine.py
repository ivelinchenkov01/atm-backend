# engine.py
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

# ==============================
# 🔹 Load ATM data ONCE
# ==============================

atm_df = pd.read_excel("all_atm_FINAL.xlsx")

# --- Clean coordinates ---
atm_df["Latitude"] = pd.to_numeric(atm_df["Latitude"], errors="coerce")
atm_df["Longitude"] = pd.to_numeric(atm_df["Longitude"], errors="coerce")
atm_df.dropna(subset=["Latitude", "Longitude"], inplace=True)

# --- Bulgaria bounding box ---
atm_df = atm_df[
    atm_df["Latitude"].between(41.2, 44.2) &
    atm_df["Longitude"].between(22.35, 28.6)
].reset_index(drop=True)

# ==============================
# 🚀 KDTree (in RAM)
# ==============================

atm_coords_rad = np.radians(
    atm_df[["Latitude", "Longitude"]].values
)
atm_tree = cKDTree(atm_coords_rad)

# ==============================
# 🌍 PUBLIC FUNCTION
# ==============================

def find_nearest_atms(lat: float, lon: float, k: int = 5):
    """
    Returns k nearest ATMs to given lat/lon
    """
    dist_rad, idx = atm_tree.query(
        np.radians([[lat, lon]]), k=k
    )

    # 🔧 FIX: flatten results
    dist_rad = dist_rad.flatten()
    idx = idx.flatten()

    result = atm_df.iloc[idx].copy()
    result["distance_m"] = (dist_rad * 6371000).round().astype(int)

    return result[
        ["BANK", "CITY", "Latitude", "Longitude", "distance_m"]
    ]
