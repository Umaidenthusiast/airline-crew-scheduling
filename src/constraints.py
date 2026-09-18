from datetime import datetime
import pandas as pd


def at_base(crew, flight):
    """
    Check whether the crew member is based at
    the flight's departure airport.
    """

    return crew["base_airport"] == flight["departure"]


def is_available(crew, flight, assigned_flights):
    """
    Check whether a crew member is available for a flight.

    Returns False if the new flight overlaps with
    any flight already assigned to the crew member.
    """

    for assigned_flight in assigned_flights:

        # Check if the flights overlap
        if (
            flight["start_time"] < assigned_flight["end_time"]
            and
            flight["end_time"] > assigned_flight["start_time"]
        ):
            return False

    return True


def within_hours_limit(crew, flight, assigned_flights):
    """
    Check whether assigning the new flight would keep
    the crew member within their maximum daily working hours.
    """

    current_hours = 0

    # Calculate hours already assigned
    for assigned_flight in assigned_flights:

        duration = (
            assigned_flight["end_time"]
            - assigned_flight["start_time"]
        ).total_seconds() / 3600

        current_hours += duration

    # Calculate duration of the new flight
    new_duration = (
        flight["end_time"]
        - flight["start_time"]
    ).total_seconds() / 3600

    # Check maximum daily hours
    return current_hours + new_duration <= crew["max_hours_day"]


def has_required_rest(
    crew,
    flight,
    assigned_flights,
    minimum_rest_hours=2
):
    """
    Check whether the crew member gets the required
    amount of rest between flights.
    """

    minimum_rest = pd.Timedelta(hours=minimum_rest_hours)

    for assigned_flight in assigned_flights:

        # New flight happens after an assigned flight
        if flight["start_time"] >= assigned_flight["end_time"]:

            rest_time = (
                flight["start_time"]
                - assigned_flight["end_time"]
            )

            if rest_time < minimum_rest:
                return False

        # New flight happens before an assigned flight
        elif assigned_flight["start_time"] >= flight["end_time"]:

            rest_time = (
                assigned_flight["start_time"]
                - flight["end_time"]
            )

            if rest_time < minimum_rest:
                return False

    return True