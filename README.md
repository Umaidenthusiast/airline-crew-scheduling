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

x[crew_id, flight_id] = 1
if the crew member is assigned to the flight.

Otherwise:


x[crew_id, flight_id] = 0

### 📐 Constraints

The optimizer applies several scheduling constraints.

1. Flight Coverage

Every completely assigned flight must have:

One Pilot
One Copilot
One Attendant

A flight is considered fully assigned only when all three roles are available.

2. Crew Location

Crew members can begin their schedule from their assigned base airport.

The model also supports flight chaining when the arrival airport of one flight matches the departure airport of another flight.

3. No Overlapping Flights

A crew member cannot be assigned to two flights that occur at overlapping times.

4. Required Rest

A minimum rest period is maintained between compatible flight assignments.

The current demonstration model uses:

Required Rest = 2 hours
5. Daily Working Hours

Each crew member has a maximum number of working hours per day.

The optimizer ensures that the total assigned flight duration does not exceed this limit.

### 💰 Optimization Objective

The model uses a weighted objective function.

The primary objective is to:

Maximize the number of completely assigned flights.

The secondary objective is to:

Minimize the total crew assignment cost.

Conceptually:

Objective =
    Flight Weight × Fully Assigned Flights
    - Total Crew Cost

A large flight-weight value ensures that complete flight coverage has priority over small differences in crew cost.

### 📊 Example Dataset

The project currently uses simulated CSV data.

Flights

The demonstration dataset contains 10 flights operating between airports such as:

BOM
DEL
BLR
HYD
MAA

Each flight contains information such as:

Flight ID
Departure airport
Arrival airport
Start time
End time
Flight duration
Crew

The demonstration dataset contains 8 crew members across:

Pilots
Copilots
Attendants

Crew records include:

Crew ID
Name
Role
Base airport
Maximum daily working hours
Hourly cost
 ### 🖥️ Dashboard

The React dashboard provides a visual interface for monitoring the scheduling system.

It displays:

Total Flights
Total Crew
Assigned Flights
Unassigned Flights
Backend System Status
Flight Schedule
Pilot assignments
Copilot assignments
Attendant assignments
Assignment status

The dashboard also provides:

Optimize Schedule
Refresh Data

actions.

🛠️ Technology Stack
Technology	Purpose
Python	Optimization and data processing
Pandas	Dataset processing
PuLP	Mathematical optimization
CBC	Optimization solver
FastAPI	Backend REST API
React	Frontend dashboard
Vite	Frontend development/build tool
JavaScript	Frontend logic
CSS	Dashboard styling
JSON	API and schedule data
CSV	Dataset storage
### 📁 Project Structure
airline-crew-scheduling/
│
├── backend/
│   └── main.py
│
├── data/
│   ├── flights.csv
│   └── crew.csv
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FlightTable.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── output/
│   ├── optimized_schedule.csv
│   └── optimized_schedule.json
│
├── src/
│   ├── load_data.py
│   ├── generate_data.py
│   ├── constraints.py
│   ├── scheduler.py
│   └── optimizer.py
│
├── .gitignore
├── README.md
└── requirements.txt
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Umaidenthusiast/airline-crew-scheduling.git
cd airline-crew-scheduling
2. Create a Python Virtual Environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install Python Dependencies
pip install -r requirements.txt
### ▶️ Running the Project

The project consists of a Python/PuLP optimization engine, FastAPI backend, and React frontend.

Start the Backend

From the project root:

uvicorn backend.main:app --reload

The backend will be available at:

http://127.0.0.1:8000

Health endpoint:

http://127.0.0.1:8000/health
Start the Frontend

Open another terminal:

cd frontend

Install frontend dependencies:

npm install

Start the development server:

npm run dev

Open the Vite development URL shown in the terminal.

### 🧪 Validation & Testing

The project has been tested for:

Flight data loading
Crew data loading
Optimization model creation
Optimization solver execution
Flight coverage constraints
Crew location constraints
Flight overlap constraints
Rest requirements
Daily working-hour limits
Schedule CSV generation
Schedule JSON generation
FastAPI health endpoint
Schedule API
Optimization API
Frontend API integration
Backend offline handling
Optimization error handling
Repeated button-click protection
Stale request protection
Frontend production build

The frontend lint check completes with an existing React effect warning that does not prevent the application from running or building.

### 📈 Example Optimization Result

For the current simulated dataset, the optimizer successfully generates a schedule while respecting the implemented constraints.

Example output:

Optimization Status:
Optimal

Fully Assigned Flights:
2

Total Crew Cost:
460.0

The exact assignment can vary depending on the optimization solution.

The generated schedule is saved as:

output/optimized_schedule.csv

and:

output/optimized_schedule.json
### ⚠️ Current Limitations

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
### 🔮 Future Scope

The project can be extended with:

Real airline scheduling data
Larger datasets
Multi-day crew scheduling
Crew preferences
Leave and unavailability management
Aircraft compatibility constraints
More detailed labor regulations
Deadhead and positioning flights
Crew accommodation planning
Multi-objective optimization
Database integration
User authentication
Cloud deployment
Advanced analytics and visualization
Historical schedule comparison
Automatic re-optimization when flight conditions change
### 🎓 Academic Relevance

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

### 👨‍💻 Author

Umaid Gudmithe

Airline Crew Scheduling & Optimization Project

Built using:

Python · Pandas · PuLP · FastAPI · React · JavaScript · CSS · Vite

### ⭐ Project Highlights

This project combines three major areas:

Data Science
      +
Mathematical Optimization
      +
Full-Stack Web Development

The result is a complete end-to-end airline crew scheduling application with an optimization engine and interactive web dashboard.

