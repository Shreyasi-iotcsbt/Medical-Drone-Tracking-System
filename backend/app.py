from datetime import datetime, timezone
from math import radians, sin, cos, asin, sqrt
from threading import Lock
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Medical Drone Tracking Simulator")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local demo only. Restrict this before deployment.
    allow_methods=["*"],
    allow_headers=["*"],
)

# DEMO COORDINATES ONLY — not a real or approved flight plan.
# Replace these with verified route coordinates only after checking permissions.
ROUTE = [
    {"name": "A", "label": "Dum Dum Municipal Specialized Hospital", "lat": 22.6390316, "lon": 88.4150925},
    {"name": "B", "label": "Chinar Park checkpoint", "lat": 22.6230, "lon": 88.4510},
    {"name": "C", "label": "Sector V checkpoint", "lat": 22.57545, "lon": 88.43226},
    {"name": "D", "label": "Peerless Hospital (Garia area) — demo destination", "lat": 22.4726, "lon": 88.3957},
]

CHECKPOINT_RADIUS_M = 35
DEVIATION_LIMIT_M = 100
STEP_SECONDS = 0.8
lock = Lock()

state = {
    "running": False,
    "mode": "outbound",
    "lat": ROUTE[0]["lat"],
    "lon": ROUTE[0]["lon"],
    "altitude_m": 30.0,
    "speed_m_s": 12.0,
    "last_update": None,
    "visited": ["A"],
    "package_picked_up": True,
    "package_handover_confirmed": False,
    "mission_complete": False,
    "alert": "Ready. Start the simulation.",
    "deviation_enabled": False,
    "step_index": 0,
    "leg_index": 0,
    "progress": 0.0,
    "history": [],
}

def distance_m(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371000 * 2 * asin(min(1, sqrt(a)))

def current_path():
    # Outbound A->B->C->D, then return D->C->B->A.
    return ROUTE if state["mode"] == "outbound" else list(reversed(ROUTE))

def snapshot():
    return {
        **state,
        "route": ROUTE,
        "route_distance_m": round(sum(
            distance_m(ROUTE[i]["lat"], ROUTE[i]["lon"], ROUTE[i+1]["lat"], ROUTE[i+1]["lon"])
            for i in range(len(ROUTE)-1)
        )),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/")
def root():
    return {"message": "Medical Drone Tracking Simulator API", "dashboard": "Open index.html using the local web server.", "docs": "/docs"}

@app.get("/api/route")
def get_route():
    return {"route": ROUTE, "return_route": list(reversed(ROUTE))}

@app.get("/api/status")
def get_status():
    with lock:
        return snapshot()

@app.post("/api/simulation/start")
def start_simulation():
    with lock:
        if state["mission_complete"]:
            return {"ok": False, "message": "Mission is complete. Reset to run again."}
        state["running"] = True
        state["alert"] = "Simulation running — simulated GPS only."
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        return {"ok": True, "message": state["alert"]}

@app.post("/api/simulation/pause")
def pause_simulation():
    with lock:
        state["running"] = False
        state["alert"] = "Simulation paused."
        return {"ok": True, "message": state["alert"]}

@app.post("/api/simulation/reset")
def reset_simulation():
    with lock:
        state.update({
            "running": False, "mode": "outbound",
            "lat": ROUTE[0]["lat"], "lon": ROUTE[0]["lon"],
            "altitude_m": 30.0, "speed_m_s": 12.0,
            "last_update": None, "visited": ["A"],
            "package_picked_up": True, "package_handover_confirmed": False,
            "mission_complete": False, "alert": "Ready. Start the simulation.",
            "deviation_enabled": False, "step_index": 0, "leg_index": 0,
            "progress": 0.0, "history": [],
        })
        return {"ok": True, "message": "Simulation reset."}

@app.post("/api/simulation/deviation")
def toggle_deviation():
    with lock:
        state["deviation_enabled"] = not state["deviation_enabled"]
        state["alert"] = (
            "TEST MODE: simulated route deviation enabled."
            if state["deviation_enabled"] else
            "Deviation test disabled."
        )
        return {"ok": True, "deviation_enabled": state["deviation_enabled"]}

@app.post("/api/package/confirm-handover")
def confirm_handover():
    with lock:
        if "D" not in state["visited"] or state["mode"] != "return":
            return {"ok": False, "message": "Reach destination D on the outbound journey before confirming handover."}
        state["package_handover_confirmed"] = True
        state["alert"] = "Package handover manually confirmed in simulation."
        return {"ok": True, "message": state["alert"]}

@app.post("/api/simulation/tick")
def simulation_tick():
    with lock:
        if not state["running"] or state["mission_complete"]:
            return snapshot()

        path = current_path()
        if state["leg_index"] >= len(path) - 1:
            if state["mode"] == "outbound":
                state["mode"] = "return"
                state["leg_index"] = 0
                state["progress"] = 0.0
                state["alert"] = "Outbound route complete. Return journey started."
                path = current_path()
            else:
                state["running"] = False
                state["mission_complete"] = True
                state["speed_m_s"] = 0.0
                state["alert"] = "Mission complete: returned to launch station A."
                return snapshot()

        start = path[state["leg_index"]]
        end = path[state["leg_index"] + 1]
        state["progress"] += 0.035  # about 29 ticks per leg
        t = min(1.0, state["progress"])

        lat = start["lat"] + (end["lat"] - start["lat"]) * t
        lon = start["lon"] + (end["lon"] - start["lon"]) * t

        # Intentional simulated offset for testing alerts; never controls a real drone.
        if state["deviation_enabled"] and 0.30 <= t <= 0.75:
            lon += 0.0030

        state["lat"], state["lon"] = lat, lon
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        state["speed_m_s"] = 12.0

        nearest = min(
            distance_m(lat, lon, p["lat"], p["lon"]) for p in ROUTE
        )
        # Estimate distance to planned route segment for the current leg.
        route_distance = distance_m(lat, lon, start["lat"], start["lon"])
        segment_length = distance_m(start["lat"], start["lon"], end["lat"], end["lon"])
        # In deviation-test mode, use the injected offset as a clear demo alert.
        deviated = state["deviation_enabled"] and 0.30 <= t <= 0.75
        if deviated:
            state["alert"] = "ROUTE DEVIATION ALERT — simulated position is off route."
        else:
            state["alert"] = "Tracking normally — simulated GPS."

        if t >= 1.0:
            reached = end["name"]
            if reached not in state["visited"]:
                state["visited"].append(reached)
            state["leg_index"] += 1
            state["progress"] = 0.0
            if state["mode"] == "outbound" and reached == "D":
                state["mode"] = "return"
                state["leg_index"] = 0
                state["alert"] = "Reached destination D. Return journey started."
            elif state["mode"] == "return" and reached == "A":
                state["running"] = False
                state["mission_complete"] = True
                state["speed_m_s"] = 0.0
                state["alert"] = "Mission complete: returned to launch station A."

        state["history"].append({
            "time": state["last_update"], "lat": state["lat"], "lon": state["lon"],
            "mode": state["mode"], "alert": state["alert"]
        })
        state["history"] = state["history"][-500:]
        return snapshot()

@app.get("/api/history")
def get_history():
    with lock:
        return {"history": state["history"]}

class Telemetry(BaseModel):
    lat: float
    lon: float
    altitude_m: float | None = None
    speed_m_s: float | None = None

@app.post("/api/telemetry")
def receive_simulated_telemetry(data: Telemetry):
    # For later integration testing only. No flight commands are accepted.
    if not -90 <= data.lat <= 90 or not -180 <= data.lon <= 180:
        return {"ok": False, "message": "Invalid coordinates."}
    with lock:
        state["lat"], state["lon"] = data.lat, data.lon
        state["altitude_m"], state["speed_m_s"] = data.altitude_m, data.speed_m_s
        state["last_update"] = datetime.now(timezone.utc).isoformat()
        state["alert"] = "External telemetry received (read-only endpoint)."
        return {"ok": True, "message": state["alert"]}
    