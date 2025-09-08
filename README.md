# 🚆 Metlink KPL Train Tracker

A simple real-time train tracker for the **KPL line in Wellington**, built with FastAPI + Leaflet, deployable on Vercel.

## Features
- Backend (FastAPI) serves train positions and route data from Metlink Open Data API.
- Frontend (Leaflet) displays live train positions and the KPL line polyline.
- Auto-refreshes train positions every 15 seconds.

## Setup
1. Clone the repo
2. Run backend locally:
   ```bash
   pip install -r requirements.txt
   uvicorn api.metlink:app --reload
   ```
3. Open `frontend/index.html` in browser.

## Deploy to Vercel
- Push repo to GitHub
- Import into Vercel
- Add environment variable:
  - `METLINK_API_KEY` = your Metlink API key
- Deploy 🚀
