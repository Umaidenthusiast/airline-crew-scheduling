from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import csv
import subprocess
import sys
import json
import math


# ========================================================
# FastAPI Application
# ========================================================

app = FastAPI(
    title="Airline Crew Scheduling API",
    description="Backend API for airline crew scheduling and optimization",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================================
# Project Base Directory
# ========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ========================================================
# Helper Function
# ========================================================

def clean_nan_values(data):
    """
    Replace NaN values with None so that
    the data can be safely returned as JSON.
    """

    if isinstance(data, dict):
        return {
            key: clean_nan_values(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [clean_nan_values(item) for item in data]

    if isinstance(data, float) and math.isnan(data):
        return None

    return data


def load_schedule_with_flight_details():
    """Join saved assignments to their source flight data."""

    schedule_file = BASE_DIR / "output" / "optimized_schedule.json"
    flights_file = BASE_DIR / "data" / "flights.csv"

    if not schedule_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Optimized schedule not found. Run /optimize first."
        )

    if not flights_file.exists():
        raise HTTPException(
            status_code=500,
            detail="Flight data file is not available."
        )

    try:
        with open(schedule_file, "r", encoding="utf-8") as file:
            assignments = clean_nan_values(json.load(file))

        with open(flights_file, "r", encoding="utf-8", newline="") as file:
            flights_by_id = {
                flight["flight_id"]: flight
                for flight in csv.DictReader(file)
            }
    except json.JSONDecodeError as error:
        raise HTTPException(
            status_code=500,
            detail="Schedule file contains invalid JSON."
        ) from error
    except (OSError, csv.Error) as error:
        raise HTTPException(
            status_code=500,
            detail="Unable to read schedule data."
        ) from error

    schedule = []

    for assignment in assignments:
        flight_id = assignment.get("flight_id")
        flight = flights_by_id.get(flight_id)

        if flight is None:
            raise HTTPException(
                status_code=500,
                detail="Schedule data references an unknown flight."
            )

        try:
            duration_hours = float(flight["duration_hours"])
        except (KeyError, TypeError, ValueError) as error:
            raise HTTPException(
                status_code=500,
                detail="Flight data contains an invalid duration."
            ) from error

        schedule.append({
            "flight_id": flight_id,
            "departure": flight.get("departure"),
            "arrival": flight.get("arrival"),
            "start_time": flight.get("start_time"),
            "end_time": flight.get("end_time"),
            "duration_hours": duration_hours,
            "pilot": assignment.get("pilot"),
            "copilot": assignment.get("copilot"),
            "attendant": assignment.get("attendant"),
        })

    return schedule


def load_crew_count():
    """Read the existing crew CSV so the dashboard is not hard-coded."""

    try:
        with open(
            BASE_DIR / "data" / "crew.csv",
            "r",
            encoding="utf-8",
            newline=""
        ) as file:
            return sum(1 for _ in csv.DictReader(file))
    except (OSError, csv.Error):
        return None


# ========================================================
# Root Endpoint
# ========================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "Airline Crew Scheduling API is running"
    }


# ========================================================
# Health Check
# ========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ========================================================
# Get Optimized Schedule
# ========================================================

@app.get("/schedule")
def get_schedule():
    try:
        return {
            "status": "success",
            "schedule": load_schedule_with_flight_details(),
            "crew_count": load_crew_count()
        }


    except HTTPException:

        raise


    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to load the optimized schedule."
        )


# ========================================================
# Run Optimizer
# ========================================================

@app.post("/optimize")
def optimize_schedule():

    optimizer_path = (
        BASE_DIR /
        "src" /
        "optimizer.py"
    )

    schedule_file = (
        BASE_DIR /
        "output" /
        "optimized_schedule.json"
    )

    try:

        # Check optimizer exists

        if not optimizer_path.exists():

            raise HTTPException(
                status_code=500,
                detail="Optimizer file not found."
            )


        # Run optimizer

        result = subprocess.run(

            [
                sys.executable,
                str(optimizer_path)
            ],

            cwd=str(BASE_DIR),

            capture_output=True,

            text=True,

            encoding="utf-8",

            errors="replace"
        )


        # Check optimizer result

        if result.returncode != 0:

            print(f"Optimizer failed:\n{result.stderr}")

            raise HTTPException(

                status_code=500,

                detail="Optimization failed."
            )


        # Check output file

        if not schedule_file.exists():

            raise HTTPException(
                status_code=500,
                detail="Optimized schedule file was not created."
            )


        return {

            "status": "success",

            "message":
                "Schedule optimized successfully",

            "schedule":
                load_schedule_with_flight_details(),

            "crew_count":
                load_crew_count()

        }


    except HTTPException:

        raise


    except Exception:

        raise HTTPException(

            status_code=500,

            detail=
                "Unable to optimize the schedule."

        )
