import sys
import pandas as pd
import pulp
import json

sys.path.append("src")

from load_data import flights_df, crew_df


# ============================================================
# 1. CREATE OPTIMIZATION MODEL
# ============================================================

model = pulp.LpProblem(
    "Airline_Crew_Scheduling",
    pulp.LpMaximize
)


# ============================================================
# 2. CREATE DECISION VARIABLES
# ============================================================

# x[crew_id, flight_id] = 1
# if crew member is assigned to the flight
# otherwise 0

x = {}

for _, crew in crew_df.iterrows():

    for _, flight in flights_df.iterrows():

        crew_id = crew["crew_id"]
        flight_id = flight["flight_id"]

        x[crew_id, flight_id] = pulp.LpVariable(
            f"x_{crew_id}_{flight_id}",
            cat="Binary"
        )


# ============================================================
# 3. CREATE FLIGHT ASSIGNMENT VARIABLES
# ============================================================

# flight_assigned[flight_id] = 1
# if the flight has:
# Pilot + Copilot + Attendant

flight_assigned = {}

for _, flight in flights_df.iterrows():

    flight_id = flight["flight_id"]

    flight_assigned[flight_id] = pulp.LpVariable(
        f"flight_assigned_{flight_id}",
        cat="Binary"
    )


# ============================================================
# 4. FLIGHT COVERAGE CONSTRAINTS
# ============================================================

for _, flight in flights_df.iterrows():

    flight_id = flight["flight_id"]

    # -------------------------
    # Pilot
    # -------------------------

    pilot_vars = []

    for _, crew in crew_df.iterrows():

        if crew["role"] == "Pilot":

            pilot_vars.append(
                x[crew["crew_id"], flight_id]
            )

    model += (
        pulp.lpSum(pilot_vars)
        == flight_assigned[flight_id]
    )


    # -------------------------
    # Copilot
    # -------------------------

    copilot_vars = []

    for _, crew in crew_df.iterrows():

        if crew["role"] == "Copilot":

            copilot_vars.append(
                x[crew["crew_id"], flight_id]
            )

    model += (
        pulp.lpSum(copilot_vars)
        == flight_assigned[flight_id]
    )


    # -------------------------
    # Attendant
    # -------------------------

    attendant_vars = []

    for _, crew in crew_df.iterrows():

        if crew["role"] == "Attendant":

            attendant_vars.append(
                x[crew["crew_id"], flight_id]
            )

    model += (
        pulp.lpSum(attendant_vars)
        == flight_assigned[flight_id]
    )


print("Flight coverage constraints added successfully.")


# ============================================================
# 5. CREW LOCATION AND CHAINING CONSTRAINTS
# ============================================================

REQUIRED_REST_HOURS = 2


# ============================================================
# 5.1 CREATE START VARIABLES
# ============================================================

# start[crew_id, flight_id] = 1 if this is the first
# flight assigned to the crew member.

crew_starts = {}

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for _, flight in flights_df.iterrows():

        flight_id = flight["flight_id"]

        # A crew member can only start a schedule from
        # their base airport.

        if crew["base_airport"] == flight["departure"]:

            crew_starts[
                crew_id,
                flight_id
            ] = pulp.LpVariable(
                f"start_{crew_id}_{flight_id}",
                cat="Binary"
            )


# ============================================================
# 5.2 CREATE VALID FLIGHT TRANSITIONS
# ============================================================

crew_transitions = {}

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for _, previous_flight in flights_df.iterrows():

        previous_id = previous_flight["flight_id"]

        for _, next_flight in flights_df.iterrows():

            next_id = next_flight["flight_id"]

            # A flight cannot follow itself.
            if previous_id == next_id:
                continue

            # The previous flight must arrive at the same
            # airport where the next flight departs.
            same_airport = (
                previous_flight["arrival"]
                == next_flight["departure"]
            )

            # Calculate rest time.
            rest_hours = (
                next_flight["start_time"]
                - previous_flight["end_time"]
            ).total_seconds() / 3600

            enough_rest = (
                rest_hours >= REQUIRED_REST_HOURS
            )

            # Create a transition only when the movement
            # and rest requirements are satisfied.

            if same_airport and enough_rest:

                crew_transitions[
                    crew_id,
                    previous_id,
                    next_id
                ] = pulp.LpVariable(
                    f"transition_{crew_id}_{previous_id}_{next_id}",
                    cat="Binary"
                )


# ============================================================
# 5.3 EACH CREW MEMBER CAN HAVE ONLY ONE START
# ============================================================

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    start_variables = [
        variable
        for (start_crew_id, _), variable
        in crew_starts.items()
        if start_crew_id == crew_id
    ]

    model += (
        pulp.lpSum(start_variables)
        <= 1
    )


# ============================================================
# 5.4 EVERY ASSIGNED FLIGHT MUST HAVE A START OR PREDECESSOR
# ============================================================

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for _, flight in flights_df.iterrows():

        flight_id = flight["flight_id"]

        start_variable = crew_starts.get(
            (crew_id, flight_id),
            0
        )

        incoming_transitions = [
            transition
            for (
                transition_crew_id,
                previous_id,
                next_id
            ), transition
            in crew_transitions.items()

            if (
                transition_crew_id == crew_id
                and next_id == flight_id
            )
        ]

        # Every assigned flight must have exactly one
        # way of being reached:
        #
        # 1. It is the crew member's first flight, OR
        # 2. It follows a previous flight.

        model += (
            start_variable
            + pulp.lpSum(incoming_transitions)
            == x[crew_id, flight_id]
        )


# ============================================================
# 5.5 A FLIGHT CAN HAVE AT MOST ONE NEXT FLIGHT
# ============================================================

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for _, flight in flights_df.iterrows():

        flight_id = flight["flight_id"]

        outgoing_transitions = [
            transition
            for (
                transition_crew_id,
                previous_id,
                next_id
            ), transition
            in crew_transitions.items()

            if (
                transition_crew_id == crew_id
                and previous_id == flight_id
            )
        ]

        # One flight cannot lead to multiple simultaneous
        # next flights for the same crew member.

        model += (
            pulp.lpSum(outgoing_transitions)
            <= x[crew_id, flight_id]
        )


# ============================================================
# 5.6 TRANSITIONS REQUIRE BOTH FLIGHTS TO BE ASSIGNED
# ============================================================

for (
    crew_id,
    previous_id,
    next_id
), transition in crew_transitions.items():

    model += (
        transition
        <= x[crew_id, previous_id]
    )

    model += (
        transition
        <= x[crew_id, next_id]
    )


print(
    "Crew location and chaining constraints "
    "added successfully."
)

# ============================================================
# 6. NO-OVERLAP CONSTRAINT
# ============================================================

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for i, flight_a in flights_df.iterrows():

        for j, flight_b in flights_df.iterrows():

            if i >= j:
                continue

            # Check whether the two flights overlap

            if (
                flight_a["start_time"] < flight_b["end_time"]
                and
                flight_a["end_time"] > flight_b["start_time"]
            ):

                model += (
                    x[crew_id, flight_a["flight_id"]]
                    +
                    x[crew_id, flight_b["flight_id"]]
                    <= 1
                )


print("No-overlap constraints added successfully.")


# ============================================================
# 7. REST REQUIREMENT CONSTRAINT
# ============================================================

REQUIRED_REST_HOURS = 2


for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    for i, flight_a in flights_df.iterrows():

        for j, flight_b in flights_df.iterrows():

            if i >= j:
                continue

            # Time between Flight A ending and Flight B starting

            gap_ab = (
                flight_b["start_time"]
                - flight_a["end_time"]
            ).total_seconds() / 3600


            # Time between Flight B ending and Flight A starting

            gap_ba = (
                flight_a["start_time"]
                - flight_b["end_time"]
            ).total_seconds() / 3600


            # If A comes before B

            if 0 <= gap_ab < REQUIRED_REST_HOURS:

                model += (
                    x[crew_id, flight_a["flight_id"]]
                    +
                    x[crew_id, flight_b["flight_id"]]
                    <= 1
                )


            # If B comes before A

            elif 0 <= gap_ba < REQUIRED_REST_HOURS:

                model += (
                    x[crew_id, flight_a["flight_id"]]
                    +
                    x[crew_id, flight_b["flight_id"]]
                    <= 1
                )


print("Rest requirement constraints added successfully.")


# ============================================================
# 8. DAILY WORKING HOURS CONSTRAINT
# ============================================================

for _, crew in crew_df.iterrows():

    crew_id = crew["crew_id"]

    # Get all dates in the flight dataset

    dates = flights_df[
        "start_time"
    ].dt.date.unique()


    for date in dates:

        daily_flights = flights_df[
            flights_df["start_time"].dt.date == date
        ]


        model += (
            pulp.lpSum(
                x[crew_id, flight["flight_id"]]
                * flight["duration_hours"]

                for _, flight in daily_flights.iterrows()
            )
            <= crew["max_hours_day"]
        )


print("Daily working hours constraints added successfully.")


# ============================================================
# 9. OBJECTIVE FUNCTION
# ============================================================

# Goal:
#
# 1. Maximize fully assigned flights
# 2. Minimize crew cost
#
# A large weight makes flight coverage
# more important than cost savings.

FLIGHT_WEIGHT = 10000


# Total number of fully assigned flights

total_assigned_flights = pulp.lpSum(
    flight_assigned[flight_id]
    for flight_id in flight_assigned
)


# Total crew assignment cost

total_crew_cost = pulp.lpSum(

    x[crew_id, flight_id]

    *

    crew_df.loc[
        crew_df["crew_id"] == crew_id,
        "hourly_cost"
    ].iloc[0]

    *

    flights_df.loc[
        flights_df["flight_id"] == flight_id,
        "duration_hours"
    ].iloc[0]

    for crew_id, flight_id in x
)


# Combined objective

model += (
    FLIGHT_WEIGHT * total_assigned_flights
    - total_crew_cost
)


print("Optimization model created successfully.")


# ============================================================
# 10. MODEL INFORMATION
# ============================================================

print("\nNumber of decision variables:")

print(
    len(x) + len(flight_assigned)
)


print("\nObjective:")

print(
    "Maximize fully assigned flights "
    "and minimize crew cost"
)


# ============================================================
# 11. SOLVE MODEL
# ============================================================

model.solve(
    pulp.PULP_CBC_CMD(msg=False)
)


# ============================================================
# 12. DISPLAY OPTIMIZATION STATUS
# ============================================================

print("\nOptimization Status:")

print(
    pulp.LpStatus[model.status]
)


if model.status != pulp.LpStatusOptimal:

    print("Optimization failed; no schedule was written.")
    sys.exit(1)


# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

if model.status == pulp.LpStatusOptimal:

    # --------------------------------------------------------
    # Number of fully assigned flights
    # --------------------------------------------------------

    assigned_count = int(
        sum(
            pulp.value(
                flight_assigned[flight_id]
            )
            for flight_id in flight_assigned
        )
    )


    print("\nFully Assigned Flights:")

    print(
        assigned_count
    )


    # --------------------------------------------------------
    # Total crew cost
    # --------------------------------------------------------

    print("\nTotal Crew Cost:")

    print(
        round(
            pulp.value(total_crew_cost),
            2
        )
    )


    # --------------------------------------------------------
    # Objective value
    # --------------------------------------------------------

    print("\nObjective Value:")

    print(
        round(
            pulp.value(model.objective),
            2
        )
    )


    # ========================================================
    # 14. DISPLAY OPTIMIZED ASSIGNMENTS
    # ========================================================

    print("\nOptimized Flight Assignments:")


    optimized_assignments = []


    for _, flight in flights_df.iterrows():

        flight_id = flight["flight_id"]

        assigned_pilot = None
        assigned_copilot = None
        assigned_attendant = None


        # ----------------------------------------------------
        # Find assigned crew
        # ----------------------------------------------------

        for _, crew in crew_df.iterrows():

            crew_id = crew["crew_id"]

            value = pulp.value(
                x[crew_id, flight_id]
            )


            if value == 1:

                if crew["role"] == "Pilot":

                    assigned_pilot = crew_id

                elif crew["role"] == "Copilot":

                    assigned_copilot = crew_id

                elif crew["role"] == "Attendant":

                    assigned_attendant = crew_id


        # ----------------------------------------------------
        # Print assignment
        # ----------------------------------------------------

        if (
            assigned_pilot
            and assigned_copilot
            and assigned_attendant
        ):

            print(
                f"{flight_id} -> "
                f"Pilot: {assigned_pilot}, "
                f"Copilot: {assigned_copilot}, "
                f"Attendant: {assigned_attendant}"
            )

        else:

            print(
                f"{flight_id} -> UNASSIGNED"
            )


        # ----------------------------------------------------
        # Store assignment
        # ----------------------------------------------------

        optimized_assignments.append({

            "flight_id": flight_id,

            "pilot": assigned_pilot,

            "copilot": assigned_copilot,

            "attendant": assigned_attendant

        })


    # ========================================================
    # 15. CREATE OPTIMIZED SCHEDULE DATAFRAME
    # ========================================================

    optimized_schedule_df = pd.DataFrame(
        optimized_assignments
    )


    print("\nOptimized Schedule DataFrame:")

    print(
        optimized_schedule_df
    )


   # --------------------------------------------------
# Create optimized schedule DataFrame
# --------------------------------------------------

schedule_df = pd.DataFrame(
    optimized_assignments
)

print("\nOptimized Schedule DataFrame:")
print(schedule_df)


# --------------------------------------------------
# Save optimized schedule as CSV
# --------------------------------------------------

schedule_df.to_csv(
    "output/optimized_schedule.csv",
    index=False
)

print(
    "\nOptimized schedule saved successfully to "
    "output/optimized_schedule.csv"
)


# --------------------------------------------------
# Save optimized schedule as JSON
# --------------------------------------------------

optimized_schedule_json = [
    {
        key: None if pd.isna(value) else value
        for key, value in record.items()
    }
    for record in schedule_df.to_dict(orient="records")
]


with open(
    "output/optimized_schedule.json",
    "w"
) as file:

    json.dump(
        optimized_schedule_json,
        file,
        indent=4,
        allow_nan=False
    )


print(
    "Optimized schedule saved successfully to "
    "output/optimized_schedule.json"
)
