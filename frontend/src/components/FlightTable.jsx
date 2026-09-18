function FlightTable({ schedule }) {

  const formatTime = (value) => {

    if (!value) {
      return "-"
    }

    const date = new Date(value.replace(" ", "T"))

    return Number.isNaN(date.getTime())
      ? "-"
      : date.toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit"
        })
  }


  // Determine assignment status
  const getStatus = (flight) => {

    const assignedCrew = [
      flight.pilot,
      flight.copilot,
      flight.attendant
    ].filter(Boolean).length

    if (assignedCrew === 3) {
      return {
        text: "Assigned",
        className: "status-assigned"
      }
    }

    if (assignedCrew > 0) {
      return {
        text: "Partially Assigned",
        className: "status-partial"
      }
    }

    return {
      text: "Unassigned",
      className: "status-unassigned"
    }
  }


  return (

    <div className="flight-table-container">

      <table className="flight-table">

        <thead>

          <tr>
            <th>Flight</th>
            <th>Route</th>
            <th>Departure</th>
            <th>Arrival</th>
            <th>Duration</th>
            <th>Pilot</th>
            <th>Copilot</th>
            <th>Attendant</th>
            <th>Status</th>
          </tr>

        </thead>


        <tbody>

          {schedule.map((flight) => {

            const status = getStatus(flight)

            return (

              <tr key={flight.flight_id}>

                {/* Flight ID */}
                <td>
                  <span className="flight-id">
                    {flight.flight_id}
                  </span>
                </td>


                {/* Route */}
                <td>

                  <div className="route">

                    <span className="airport">
                      {flight.departure || "-"}
                    </span>

                    <span className="route-arrow">
                      →
                    </span>

                    <span className="airport">
                      {flight.arrival || "-"}
                    </span>

                  </div>

                </td>


                {/* Departure */}
                <td>

                  <span className="time">
                    {formatTime(flight.start_time)}
                  </span>

                </td>


                {/* Arrival */}
                <td>

                  <span className="time">
                    {formatTime(flight.end_time)}
                  </span>

                </td>


                {/* Duration */}
                <td>

                  {flight.duration_hours != null
                    ? (
                      <span className="duration">
                        {flight.duration_hours}h
                      </span>
                    )
                    : "-"
                  }

                </td>


                {/* Pilot */}
                <td>

                  {flight.pilot ? (
                    <span className="crew-badge pilot">
                      {flight.pilot}
                    </span>
                  ) : (
                    <span className="crew-empty">
                      —
                    </span>
                  )}

                </td>


                {/* Copilot */}
                <td>

                  {flight.copilot ? (
                    <span className="crew-badge copilot">
                      {flight.copilot}
                    </span>
                  ) : (
                    <span className="crew-empty">
                      —
                    </span>
                  )}

                </td>


                {/* Attendant */}
                <td>

                  {flight.attendant ? (
                    <span className="crew-badge attendant">
                      {flight.attendant}
                    </span>
                  ) : (
                    <span className="crew-empty">
                      —
                    </span>
                  )}

                </td>


                {/* Status */}
                <td>

                  <span
                    className={`assignment-status ${status.className}`}
                  >
                    <span className="status-indicator"></span>
                    {status.text}
                  </span>

                </td>

              </tr>

            )

          })}

        </tbody>

      </table>

    </div>

  )
}

export default FlightTable