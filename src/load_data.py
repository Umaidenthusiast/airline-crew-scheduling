import pandas as pd


# Load flight data
flights_df = pd.read_csv("data/flights.csv")

# Load crew data
crew_df = pd.read_csv("data/crew.csv")


# Convert flight times to datetime
flights_df["start_time"] = pd.to_datetime(flights_df["start_time"])
flights_df["end_time"] = pd.to_datetime(flights_df["end_time"])


# Display loaded data
print("Flights:")
print(flights_df)

print("\nCrew:")
print(crew_df)