# ✈️ Airline Crew Scheduling & Optimization

An optimization-based airline crew scheduling system that assigns pilots, copilots, and attendants to flights while considering operational constraints such as crew availability, airport location, overlapping flights, required rest time, and daily working-hour limits.

The project combines **Data Science, Mathematical Optimization, Backend API Development, and Full-Stack Web Development** into an end-to-end airline crew scheduling application.

---

## 📌 Project Overview

Airline crew scheduling is a complex optimization problem where available crew members must be assigned to flights while satisfying multiple operational constraints.

This project demonstrates how **Operations Research, Data Science, and Web Development** can be combined to create a practical crew scheduling system.

The system uses a **Python optimization engine with PuLP**, exposes the optimization functionality through a **FastAPI REST API**, and provides a **React dashboard** for monitoring and optimizing flight schedules.

The optimizer attempts to maximize the number of flights that receive a complete crew consisting of:

- 👨‍✈️ Pilot
- 👨‍✈️ Copilot
- 🧑‍✈️ Attendant

while minimizing the associated crew assignment cost.

---

## 🎯 Objectives

The main objectives of this project are:

- Assign available crew members to flights.
- Prevent crew members from being assigned to overlapping flights.
- Respect crew base-airport constraints.
- Maintain the required rest period between flights.
- Enforce maximum daily working hours.
- Maximize the number of completely assigned flights.
- Minimize crew assignment cost.
- Provide a web-based dashboard for schedule monitoring.
- Provide API endpoints for retrieving and optimizing schedules.

---

## 🚀 Features

### 🧠 Optimization

- Binary decision variables for crew-to-flight assignments.
- Complete crew requirement for an assigned flight.
- Pilot, copilot, and attendant role constraints.
- Crew location and flight chaining constraints.
- No-overlap constraints.
- Required rest-period constraints.
- Maximum daily working-hour constraints.
- Cost-aware optimization objective.
- CBC solver through PuLP.

### ⚙️ Backend

- Python-based optimization engine.
- FastAPI REST API.
- `/health` endpoint for backend health monitoring.
- `/schedule` endpoint for retrieving the current schedule.
- `/optimize` endpoint for generating an optimized schedule.
- JSON responses for frontend integration.
- Error handling for failed optimization and unavailable backend.

### 🖥️ Frontend

- React-based dashboard.
- Real-time backend status indicator.
- Flight statistics.
- Assigned and unassigned flight counters.
- Interactive optimization button.
- Refresh schedule functionality.
- Flight schedule table.
- Color-coded crew role badges.
- Assignment status indicators.
- Responsive dashboard design.
- User-friendly error and success messages.

---

## 🧠 Optimization Model

The scheduling problem is formulated as a **Binary Integer Programming** model using PuLP.

### Decision Variable

For every crew member and flight:

```text
x[crew_id, flight_id] = 1
