# 🚁 Medical Drone Tracking System

### Smart Route Monitoring • GPS Simulation • Checkpoint Tracking • Delivery Status

A simulation-based medical drone tracking system designed to demonstrate how essential medical supplies can be monitored during transportation using route visualization, simulated GPS coordinates, checkpoint tracking, and delivery status updates.

The project models a drone travelling between designated locations, following a planned route, monitoring its progress, and returning to its starting point after completing the delivery.

---

## 🎯 Project Objective

The primary objective is to develop a simple and interactive tracking platform that demonstrates how drone-based medical delivery can be monitored digitally.

The system aims to make the delivery process easier to visualize by tracking the drone's simulated position, monitoring route progress, and identifying deviations from the planned path.

## 🗺️ Demonstration Route

**Route:** A → B → C → D → A

| Point | Location                        | Purpose              |
| ----- | ------------------------------- | -------------------- |
| A     | Dum Dum Hospital                | Starting point       |
| B     | Chinar Park                     | First checkpoint     |
| C     | Sector V                        | Second checkpoint    |
| D     | Placeholder hospital near Garia | Delivery destination |
| A     | Dum Dum Hospital                | Return to base       |

*The route is intended for demonstration purposes. Locations and route coordinates can be adjusted as the project develops.*

## ✨ Key Features

* **📍 Simulated GPS Tracking** — Displays the drone's simulated position during the journey.
* **🗺️ Route Visualization** — Represents the planned delivery route and its checkpoints.
* **🚦 Checkpoint Monitoring** — Tracks progress through the designated locations.
* **⚠️ Route Deviation Detection** — Demonstrates how movement away from a planned route can trigger an alert.
* **📦 Delivery Status Monitoring** — Represents delivery progress and package handover.
* **↩️ Return-to-Base Simulation** — Models the drone's journey back to its starting point.
* **🖥️ Interactive Dashboard** — Provides a visual interface for monitoring the simulated mission.
* **🧩 Modular Architecture** — Separates backend logic from frontend presentation.

## ⚙️ Technology Stack

| Component               | Technology            |
| ----------------------- | --------------------- |
| Backend                 | Python, FastAPI       |
| Frontend                | HTML, CSS, JavaScript |
| API Documentation       | FastAPI / Swagger UI  |
| Development Environment | Visual Studio Code    |
| Version Control         | Git and GitHub        |

## 🏗️ Project Structure

```text
MEDICAL_DRONE_TRACKER/
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   └── 3D.html
│
├── .vscode/
│   ├── launch.json
│   └── settings.json
│
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or later
* pip
* A modern web browser
* Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Shreyasi-iotcsbt/Medical-Drone-Tracking-System.git
cd Medical-Drone-Tracking-System
```

### 2. Install Backend Dependencies

Open a terminal in the project directory and run:

```bash
python -m pip install fastapi uvicorn
```

### 3. Start the Backend

```bash
cd backend
python -m uvicorn app:app --reload
```

The backend should be available at:

* **API:** http://127.0.0.1:8000
* **Interactive API documentation:** http://127.0.0.1:8000/docs

### 4. Start the Frontend

Open a **second terminal** in the project root and run:

```bash
python -m http.server 5500
```

Open the dashboard in your browser:

* **Main dashboard:** http://127.0.0.1:5500/frontend/index.html
* **3D view:** http://127.0.0.1:5500/frontend/3D.html

Keep both terminals running while testing the application.

> **Note:** If the dashboard cannot communicate with the backend, check the API URL in the frontend code and configure FastAPI CORS if required.

## 🔄 How the System Works

1. **Mission Initialization:** The drone begins at the designated starting location.
2. **Route Planning:** The system defines the ordered checkpoints for the journey.
3. **Position Simulation:** The drone's position is updated using simulated location data.
4. **Progress Monitoring:** The dashboard represents movement between checkpoints.
5. **Deviation Monitoring:** The system can identify simulated movement outside the planned route.
6. **Delivery Confirmation:** The destination is marked as reached and package handover is represented.
7. **Return Journey:** The drone follows the return route to the starting point.

## 🔐 Safety and Scope

This project currently demonstrates a **software-based simulation**, not the operation of a physical drone.

* GPS positions and mission events may be simulated.
* No real medical supplies are transported by this prototype.
* Route deviation alerts demonstrate a monitoring concept and should not be treated as a validated safety system.
* Real drone integration, live GPS telemetry, secure communications, and hardware testing would require additional development.

## 🔮 Future Enhancements

* Integration with live GPS or authorized drone telemetry.
* Interactive route planning using map services.
* Real-time tracking and mission event logs.
* More robust geofencing and route deviation detection.
* Delivery verification and timestamped handover records.
* Authentication, role-based access, and secure API communication.
* Integration with drone communication protocols where supported by the hardware.

## 🎓 Project Use Cases

* Academic demonstration of drone delivery monitoring.
* Prototype for medical supply transportation workflows.
* Learning project for API integration and dashboard development.
* Exploration of route tracking, geofencing, and delivery-status systems.

## 👩‍💻 Author

**Shreyasi Ghosh, Sharanya Mukherjee**

GitHub: [@Shreyasi-iotcsbt](https://github.com/Shreyasi-iotcsbt)

## 📄 License

This project is intended for educational and demonstration purposes. A formal open-source license can be added when the distribution terms are decided.

---

*Building a smarter way to visualize and monitor medical delivery missions.* 🚁
