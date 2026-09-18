import pandas as pd


# -----------------------------
# FLIGHT DATA
# -----------------------------

flights = [
    {
        "flight_id": "FL001",
        "departure": "BOM",
        "arrival": "DEL",
        "start_time": "2026-09-01 06:00",
        "end_time": "2026-09-01 08:00"
    },
    {
        "flight_id": "FL002",
        "departure": "BOM",
        "arrival": "BLR",
        "start_time": "2026-09-01 07:00",
        "end_time": "2026-09-01 09:00"
    },
    {
        "flight_id": "FL003",
        "departure": "DEL",
        "arrival": "HYD",
        "start_time": "2026-09-01 10:00",
        "end_time": "2026-09-01 12:00"
    },
    {
        "flight_id": "FL004",
        "departure": "BOM",
        "arrival": "MAA",
        "start_time": "2026-09-01 09:30",
        "end_time": "2026-09-01 11:30"
    },
    {
        "flight_id": "FL005",
        "departure": "BLR",
        "arrival": "DEL",
        "start_time": "2026-09-01 11:00",
        "end_time": "2026-09-01 13:00"
    },
    {
    "flight_id": "FL006",
    "departure": "HYD",
    "arrival": "BOM",
    "start_time": "2026-09-01 13:00",
    "end_time": "2026-09-01 15:00"
    },
    {
    "flight_id": "FL007",
    "departure": "MAA",
    "arrival": "BLR",
    "start_time": "2026-09-01 13:30",
    "end_time": "2026-09-01 15:30"
    },
    {
    "flight_id": "FL008",
    "departure": "DEL",
    "arrival": "BOM",
    "start_time": "2026-09-01 14:00",
    "end_time": "2026-09-01 16:00"
    },
    {
    "flight_id": "FL009",
    "departure": "BLR",
    "arrival": "HYD",
    "start_time": "2026-09-01 16:00",
    "end_time": "2026-09-01 18:00"
    },
    {
    "flight_id": "FL010",
    "departure": "BOM",
    "arrival": "DEL",
    "start_time": "2026-09-01 17:00",
    "end_time": "2026-09-01 19:00"
    }
]


# Convert list of dictionaries into DataFrame
flights_df = pd.DataFrame(flights)


# Convert time columns into datetime
flights_df["start_time"] = pd.to_datetime(
    flights_df["start_time"]
)

flights_df["end_time"] = pd.to_datetime(
    flights_df["end_time"]
)


# Calculate flight duration automatically
flights_df["duration_hours"] = (
    flights_df["end_time"] - flights_df["start_time"]
).dt.total_seconds() / 3600


# Display the dataset
print(flights_df)


# Display data types
print("\nData types:")
print(flights_df.dtypes)

flights_df.to_csv("data/flights.csv", index=False)

# -----------------------------
# CREW DATA
# -----------------------------

crew = [
    {
        "crew_id": "C001",
        "name": "Rahul",
        "role": "Pilot",
        "base_airport": "BOM",
        "max_hours_day": 8,
        "hourly_cost": 50
    },
    {
        "crew_id": "C002",
        "name": "Amit",
        "role": "Pilot",
        "base_airport": "DEL",
        "max_hours_day": 8,
        "hourly_cost": 50
    },
    {
        "crew_id": "C003",
        "name": "Priya",
        "role": "Copilot",
        "base_airport": "BOM",
        "max_hours_day": 8,
        "hourly_cost": 40
    },
    {
        "crew_id": "C004",
        "name": "Neha",
        "role": "Copilot",
        "base_airport": "BLR",
        "max_hours_day": 8,
        "hourly_cost": 40
    },
    {
        "crew_id": "C005",
        "name": "Arjun",
        "role": "Attendant",
        "base_airport": "BOM",
        "max_hours_day": 10,
        "hourly_cost": 25
    },
    {
        "crew_id": "C006",
        "name": "Sneha",
        "role": "Attendant",
        "base_airport": "DEL",
        "max_hours_day": 10,
        "hourly_cost": 25
    },
    {
        "crew_id": "C007",
        "name": "Vikram",
        "role": "Attendant",
        "base_airport": "BLR",
        "max_hours_day": 10,
        "hourly_cost": 25
    },
    {
        "crew_id": "C008",
        "name": "Karan",
        "role": "Attendant",
        "base_airport": "HYD",
        "max_hours_day": 10,
        "hourly_cost": 25
    }
]

# Convert crew list into DataFrame
crew_df = pd.DataFrame(crew)

# Display crew dataset
print("\nCrew Dataset:")
print(crew_df)

# Display crew data types
print("\nCrew Data Types:")
print(crew_df.dtypes)

# Save crew dataset to CSV
crew_df.to_csv("data/crew.csv", index=False)