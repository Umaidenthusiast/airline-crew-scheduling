import pandas as pd
import sys

sys.path.append("src")

from load_data import flights_df, crew_df

# Load the original greedy schedule
greedy_schedule_df = pd.read_csv("output/schedule.csv")

# Load the optimized schedule
schedule_df = pd.read_csv("output/optimized_schedule.csv")

# Load the optimized schedule
schedule_df = pd.read_csv("output/optimized_schedule.csv")

print("Optimized Schedule:")
print(schedule_df)


# --------------------------------------------------
# Count flight assignment status
# --------------------------------------------------

role_columns = ["pilot", "copilot", "attendant"]

fully_assigned = 0
partially_assigned = 0
unassigned = 0


for _, flight in schedule_df.iterrows():

    assigned_roles = 0

    for role in role_columns:
        if pd.notna(flight[role]):
            assigned_roles += 1

    if assigned_roles == 3:
        fully_assigned += 1

    elif assigned_roles > 0:
        partially_assigned += 1

    else:
        unassigned += 1


print("\nAssignment Summary:")
print("Fully Assigned Flights:", fully_assigned)
print("Partially Assigned Flights:", partially_assigned)
print("Completely Unassigned Flights:", unassigned)


# --------------------------------------------------
# Crew workload and cost
# --------------------------------------------------

crew_workload = {}

# Initialize every crew member
for _, crew in crew_df.iterrows():

    crew_workload[crew["crew_id"]] = {
        "flights": 0,
        "hours": 0.0,
        "hourly_cost": crew["hourly_cost"],
        "total_cost": 0.0
    }


# Calculate workload from optimized schedule
for _, flight in schedule_df.iterrows():

    flight_id = flight["flight_id"]

    # Find the flight details
    flight_data = flights_df[
        flights_df["flight_id"] == flight_id
    ].iloc[0]

    duration = flight_data["duration_hours"]

    # Check each role
    for role in role_columns:

        crew_id = flight[role]

        if pd.notna(crew_id):

            crew_id = str(crew_id)

            crew_workload[crew_id]["flights"] += 1

            crew_workload[crew_id]["hours"] += duration


# Calculate total cost
total_crew_cost = 0.0

for crew_id, data in crew_workload.items():

    data["total_cost"] = (
        data["hours"] * data["hourly_cost"]
    )

    total_crew_cost += data["total_cost"]


# --------------------------------------------------
# Display crew workload
# --------------------------------------------------

print("\nCrew Workload:")

for crew_id, data in crew_workload.items():

    print(
        f"{crew_id} → "
        f"Flights: {data['flights']} | "
        f"Hours: {data['hours']} | "
        f"Cost: {data['total_cost']}"
    )


# --------------------------------------------------
# Display total cost
# --------------------------------------------------

print("\nTotal Crew Cost:")
print(total_crew_cost)

# --------------------------------------------------
# Compare Greedy and Optimized Schedules
# --------------------------------------------------

def count_fully_assigned(schedule):
    count = 0

    for _, flight in schedule.iterrows():

        if (
            pd.notna(flight["pilot"])
            and pd.notna(flight["copilot"])
            and pd.notna(flight["attendant"])
        ):
            count += 1

    return count


greedy_fully_assigned = count_fully_assigned(
    greedy_schedule_df
)

optimized_fully_assigned = count_fully_assigned(
    schedule_df
)

improvement = (
    optimized_fully_assigned
    - greedy_fully_assigned
)


print("\nSchedule Comparison:")
print(
    "Greedy Fully Assigned Flights:",
    greedy_fully_assigned
)

print(
    "Optimized Fully Assigned Flights:",
    optimized_fully_assigned
)

print(
    "Improvement:",
    improvement
)