import pandas as pd
import matplotlib.pyplot as plt

import sys

sys.path.append("src")

from load_data import flights_df


# --------------------------------------------------
# Load optimized schedule
# --------------------------------------------------

schedule_df = pd.read_csv(
    "output/optimized_schedule.csv"
)


# --------------------------------------------------
# Prepare flight information
# --------------------------------------------------

# Convert time columns to datetime
flights_df["start_time"] = pd.to_datetime(
    flights_df["start_time"]
)

flights_df["end_time"] = pd.to_datetime(
    flights_df["end_time"]
)


# Merge schedule with flight information
schedule = schedule_df.merge(
    flights_df[
        [
            "flight_id",
            "start_time",
            "end_time"
        ]
    ],
    on="flight_id"
)


# --------------------------------------------------
# Create crew assignment records
# --------------------------------------------------

records = []

roles = [
    "pilot",
    "copilot",
    "attendant"
]

for _, flight in schedule.iterrows():

    for role in roles:

        crew_id = flight[role]

        if pd.notna(crew_id):

            records.append({
                "crew_id": crew_id,
                "flight_id": flight["flight_id"],
                "start_time": flight["start_time"],
                "end_time": flight["end_time"],
                "role": role
            })


assignment_df = pd.DataFrame(records)


# Check whether there are assignments
if assignment_df.empty:

    print("No crew assignments available to visualize.")

    sys.exit()


# --------------------------------------------------
# Create crew list
# --------------------------------------------------

crew_members = sorted(
    assignment_df["crew_id"].unique()
)


# --------------------------------------------------
# Create Gantt chart
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(12, 6)
)


for index, crew_id in enumerate(crew_members):

    crew_flights = assignment_df[
        assignment_df["crew_id"] == crew_id
    ]

    for _, flight in crew_flights.iterrows():

        start = flight["start_time"]
        end = flight["end_time"]

        duration = (
            end - start
        ).total_seconds() / 3600

        start_hour = (
            start.hour
            + start.minute / 60
        )

        ax.barh(
            index,
            duration,
            left=start_hour,
            height=0.5
        )

        ax.text(
            start_hour + duration / 2,
            index,
            flight["flight_id"],
            ha="center",
            va="center"
        )


# --------------------------------------------------
# Format chart
# --------------------------------------------------

ax.set_yticks(
    range(len(crew_members))
)

ax.set_yticklabels(
    crew_members
)

ax.set_xlabel(
    "Time of Day"
)

ax.set_ylabel(
    "Crew Member"
)

ax.set_title(
    "Optimized Airline Crew Schedule"
)

ax.set_xlim(
    5,
    20
)

ax.set_xticks(
    range(5, 21)
)

ax.grid(
    axis="x",
    alpha=0.3
)


plt.tight_layout()


# --------------------------------------------------
# Save chart
# --------------------------------------------------

# Save visualization as PNG
plt.savefig(
    "output/optimized_schedule.png",
    dpi=300,
    bbox_inches="tight"
)

# Save visualization as PDF
plt.savefig(
    "output/optimized_schedule.pdf",
    bbox_inches="tight"
)

print(
    "\nOptimized schedule visualization saved successfully:"
)

print(
    "PNG → output/optimized_schedule.png"
)

print(
    "PDF → output/optimized_schedule.pdf"
)

print(
    "\nOptimized schedule visualization "
    "saved successfully to "
    "output/optimized_schedule.png"
)


# Display chart
plt.show()