# 🌱 Verticulture

**Turn your empty space into a working farm.**

Verticulture is a full-stack web application that helps first-time growers convert unused space — backyards, terraces, balconies, or indoor rooms — into productive vertical micro-farms. It recommends crops based on a user's available space and soil type, generates personalized growing and maintenance schedules, and surfaces market prices and nearby suppliers to support both home growing and small-scale selling.

## Features

- **Account system** — sign up, log in, and stay logged in across sessions (bcrypt-hashed passwords)
- **Space mapping** — enter your area, space type (backyard/terrace/balcony/room), and sunlight hours
- **Soil profiling** — manual soil type selection or photo-based detection
- **Crop recommendations** — a scoring algorithm ranks crops by fit for your space, soil, and sunlight, tagging each as best for home use or selling
- **Growing guides** — for any recommended crop: estimated tray/planting-spot capacity for your space, watering and fertilizing schedules, and a step-by-step growing procedure
- **Monitoring & maintenance** — a task dashboard (watering, fertilizing, pruning, pest checks) with due dates, a "mark done" flow that reschedules automatically, and a care-health score visualized as a progress ring
- **Market & suppliers** — search live crop prices by region, and find nearby fertilizer/seed/equipment suppliers using your browser's location

## Tech stack

**Backend:** FastAPI, SQLAlchemy, SQLite, Pydantic, Passlib (bcrypt)
**Frontend:** Vanilla HTML, CSS, and JavaScript (no framework/build step)

## Project structure


## Setup

### Backend

```bash
pip install -r requirements.txt
python -m app.seed        # seeds crops, market prices, and suppliers
uvicorn app.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

### Frontend

From the project root, in a separate terminal:

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500/index.html` in your browser.

> Note: use a plain static server (like the one above) rather than an auto-reloading dev server — this app keeps state in the browser across a multi-step flow, and live-reload extensions will interrupt it.

## How it works

1. **Sign up** and log in
2. **Map your space** — enter its size, type, and sunlight
3. **Set your soil type** — manually or by photo
4. **Get crop recommendations** ranked by fit for your space
5. **Open a growing guide** for any crop — see tray capacity, watering/fertilizing schedule, and step-by-step instructions
6. **Start growing** — this creates a real maintenance schedule
7. **Track care tasks** on the monitoring dashboard, and watch your care-health score update as you keep up with them
8. **Check the market** — current prices and nearby suppliers when you're ready to sell

## License

This project was built as a personal/portfolio project.
