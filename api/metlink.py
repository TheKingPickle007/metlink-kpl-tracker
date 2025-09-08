from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import polyline
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("METLINK_API_KEY", "zV7BfC6K6i66viZiQhgoe4PNhFQD4geJ4lLZ9jNT")
BASE_URL = "https://api.opendata.metlink.org.nz/v1/gtfs"

async def fetch_json(endpoint: str):
    headers = {"x-api-key": API_KEY}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/{endpoint}", headers=headers)
        r.raise_for_status()
        return r.json()

@app.get("/vehicles/kpl")
async def get_kpl_vehicles():
    headers = {"x-api-key": API_KEY}
    url = "https://api.opendata.metlink.org.nz/v1/gtfs-rt/vehiclepositions"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

    vehicles = []
    for entity in data.get("entity", []):
        vp = entity.get("vehicle", {})
        trip = vp.get("trip", {})
        if trip.get("route_id") == "KPL":
            position = vp.get("position", {})
            vehicles.append({
                "id": vp.get("vehicle", {}).get("id"),
                "lat": position.get("latitude"),
                "lng": position.get("longitude"),
                "bearing": position.get("bearing"),
                "status": vp.get("current_status"),
            })
    return {"vehicles": vehicles}

@app.get("/route/kpl")
async def get_kpl_route():
    shapes = await fetch_json("shapes")
    routes = await fetch_json("routes")

    kpl_shapes = set()
    for r in routes.get("routes", []):
        if r.get("route_id") == "KPL":
            kpl_shapes.add(r.get("shape_id"))

    kpl_coords = []
    for s in shapes.get("shapes", []):
        if s.get("shape_id") in kpl_shapes:
            pts = polyline.decode(s.get("shape_polyline"))
            kpl_coords.extend(pts)

    return {"route": kpl_coords}
