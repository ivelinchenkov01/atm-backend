# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine import find_nearest_atms

app = FastAPI(title="ATM Finder API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/nearest")
def nearest(lat: float, lon: float, k: int = 5):
    df = find_nearest_atms(lat, lon, k)
    return df.to_dict(orient="records")
