import sys
import pandas as pd

sys.path.append("src")

from load_data import flights_df, crew_df

from constraints import (
    at_base,
    is_available,
    within_hours_limit,
    has_required_rest
)


# ============================================================
# CREATE EMPTY SCHEDULE
# ============================================================

# Store assigned flights for every crew member
crew_schedule = {}

for _, crew in crew_df.iterrows():
    crew_schedule[crew["crew_id"]] = []


# ============================================================
# CHECK ALL CONSTRAINTS
# ============================================================

def can_assign(crew, flight, assigned_flights):
    """
    Check whether a crew member satisfies all scheduling
    constraints for a particular flight.
    """

    # Check base airport
    if not at_base(crew, flight):
        return False

    # Check overlapping flights
    if not is_available(crew, flight, assigned_flights):
        return False

    # Check maximum working hours
    if not within_hours_limit(
        crew,
        flight,
        assigned_flights
    ):
        return False

    # Check required rest period
    if not has_required_rest(
        crew,
        flight,
        assigned_flights
    ):
        return False

    return True


# ============================================================
# CALCULATE CREW WORKLOAD
# ============================================================

def calculate_workload(crew_id):
    """
    Calculate the total working hours currently assigned
    to a crew member.
    """

    total_hours = 0

    for flight in crew_schedule[crew_id]:

        total_hours += flight["duration_hours"]

    return total_hours


# ============================================================
# STORE FINAL FLIGHT ASSIGNMENTS
# ============================================================

flight_assignments = []


# ============================================================
# PROCESS EACH FLIGHT
# ============================================================

for _, flight in flights_df.iterrows():

    assigned_crew = {}

    # --------------------------------------------------------
    # Assign crew for each required role
    # --------------------------------------------------------

    for role in ["Pilot", "Copilot", "Attendant"]:

        # Store all valid crew members
        valid_crew = []

        # Check every crew member
        for _, crew in crew_df.iterrows():

            # Skip crew members with the wrong role
            if crew["role"] != role:
                continue

            crew_id = crew["crew_id"]

            # Get existing flights of this crew member
            assigned_flights = crew_schedule[crew_id]

            # Check all constraints
            if can_assign(
                crew,
                flight,
                assigned_flights
            ):

                # Calculate current workload
                workload = calculate_workload(crew_id)

                valid_crew.append(
                    (crew_id, workload)
                )

        # ----------------------------------------------------
        # Choose the crew member with the lowest workload
        # ----------------------------------------------------

        if valid_crew:

            # Sort by workload
            valid_crew.sort(
                key=lambda x: x[1]
            )

            # Select crew member with lowest workload
            selected_crew_id = valid_crew[0][0]

            # Assign the flight
            crew_schedule[selected_crew_id].append(
                flight
            )

            assigned_crew[role] = selected_crew_id

        else:

            # No valid crew available
            assigned_crew[role] = None


    # --------------------------------------------------------
    # Store assignment for this flight
    # --------------------------------------------------------

    flight_assignments.append({

        "flight_id": flight["flight_id"],

        "pilot": assigned_crew["Pilot"],

        "copilot": assigned_crew["Copilot"],

        "attendant": assigned_crew["Attendant"]

    })


# ============================================================
# DISPLAY FINAL ASSIGNMENTS
# ============================================================

print("\nFlight Assignments:")

for assignment in flight_assignments:

    print(assignment)


# ============================================================
# CONVERT TO DATAFRAME
# ============================================================

schedule_df = pd.DataFrame(
    flight_assignments
)


print("\nSchedule DataFrame:")

print(schedule_df)


# ============================================================
# DISPLAY CREW WORKLOAD
# ============================================================

print("\nCrew Workload:")

for crew_id in crew_schedule:

    workload = calculate_workload(
        crew_id
    )

    number_of_flights = len(
        crew_schedule[crew_id]
    )

    print(
        crew_id,
        "→ Flights:",
        number_of_flights,
        "| Hours:",
        workload
    )


# ============================================================
# SAVE SCHEDULE
# ============================================================

schedule_df.to_csv(
    "output/schedule.csv",
    index=False
)

print(
    "\nSchedule saved successfully "
    "to output/schedule.csv"
)