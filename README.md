# ✈️ Airline Crew Scheduling & Optimization

An optimization-based airline crew scheduling system that assigns pilots, copilots, and attendants to flights while considering operational constraints such as crew availability, airport location, overlapping flights, required rest time, and daily working-hour limits.

The project combines a **Python optimization backend using PuLP** with a **React dashboard** for viewing and optimizing the flight schedule.

---

## 📌 Project Overview

Airline crew scheduling is a complex optimization problem where available crew members must be assigned to flights while satisfying multiple operational constraints.

This project demonstrates how **Operations Research, Data Science, and Web Development** can be combined to create a practical crew scheduling system.

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

### Optimization

- Binary decision variables for crew-to-flight assignments.
- Complete crew requirement for an assigned flight.
- Pilot, copilot, and attendant role constraints.
- Crew location and flight chaining constraints.
- No-overlap constraints.
- Required rest-period constraints.
- Maximum daily working-hour constraints.
- Cost-aware optimization objective.
- CBC solver through PuLP.

### Backend

- Python-based optimization engine.
- FastAPI REST API.
- `/health` endpoint for backend health monitoring.
- `/schedule` endpoint for retrieving the current schedule.
- `/optimize` endpoint for generating an optimized schedule.
- JSON responses for frontend integration.
- Error handling for failed optimization and unavailable backend.

### Frontend

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

The scheduling problem is formulated as a **Binary Integer Programming** model.

### Decision Variable

For every crew member and flight:

```text
x[crew_id, flight_id] = 1

🧪 Validation & Testing

The project has been tested for:

Flight data loading.
Crew data loading.
Optimization model creation.
Optimization solver execution.
Flight coverage constraints.
Crew location constraints.
Flight overlap constraints.
Rest requirements.
Daily working-hour limits.
Schedule CSV generation.
Schedule JSON generation.
FastAPI health endpoint.
Schedule API.
Optimization API.
Frontend API integration.
Backend offline handling.
Optimization error handling.
Repeated button-click protection.
Frontend production build.

The frontend lint check completes with an existing React effect warning that does not prevent the application from running or building.

⚠️ Current Limitations

This project is currently a demonstration / academic optimization system and uses simulated data.

Current limitations include:

The dataset is relatively small.
Flight and crew data are stored in CSV files.
Real airline crew regulations are more complex.
Crew availability is modeled using simplified constraints.
The system does not currently integrate real airline operational data.
The optimization model does not represent every possible real-world scheduling rule.
Authentication and role-based access control are not implemented.
The application is designed primarily for local development and demonstration.

Future Scope

The project can be extended with:

Real airline scheduling data.
Larger datasets.
Multi-day crew scheduling.
Crew preferences.
Leave and unavailability management.
Aircraft compatibility constraints.
More detailed labor regulations.
Deadhead and positioning flights.
Crew accommodation planning.
Multi-objective optimization.
Database integration.
User authentication.
Deployment to a cloud platform.
Advanced analytics and visualization.
Historical schedule comparison.
Automatic re-optimization when flight conditions change.

🎓 Academic Relevance

This project demonstrates concepts from:

Data Science
Operations Research
Linear Programming
Integer Programming
Constraint Optimization
Python Programming
REST APIs
React Development
Data Processing
Software Engineering

It provides a practical example of how mathematical optimization can be integrated into a modern software application.

👨‍💻 Author

Umaid Gudmithe

Airline Crew Scheduling & Optimization Project

Built using Python, PuLP, FastAPI, React, Pandas, and Vite.