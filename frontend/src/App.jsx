import { useEffect, useRef, useState } from "react"
import "./App.css"
import FlightTable from "./components/FlightTable"

const API_URL = "https://airline-crew-scheduling.onrender.com"

function getErrorMessage(detail, fallback) {

  if (typeof detail === "string" && detail.trim()) {
    return detail
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => item?.msg || item?.message)
      .filter(Boolean)

    if (messages.length > 0) {
      return messages.join(". ")
    }
  }

  if (detail && typeof detail === "object") {
    const message = detail.message || detail.msg || detail.error

    return typeof message === "string" && message.trim()
      ? message
      : fallback
  }

  return fallback
}

async function getResponseData(response) {

  try {
    const data = await response.json()

    return data && typeof data === "object" ? data : {}
  } catch {
    return {}
  }
}

function App() {

  const [schedule, setSchedule] = useState([])
  const [loading, setLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")
  const [crewCount, setCrewCount] = useState(null)
  const [backendStatus, setBackendStatus] = useState("checking")
  const optimizationInProgress = useRef(false)
  const refreshInProgress = useRef(false)
  const scheduleRequestId = useRef(0)


  // =====================================================
  // Fetch Schedule
  // =====================================================

  const fetchSchedule = async () => {

    const requestId = ++scheduleRequestId.current

    try {

      setError("")

      const response = await fetch(
        `${API_URL}/schedule`
      )

      const data = await getResponseData(response)

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data.detail, "Unable to load the schedule.")
        )
      }

      if (!Array.isArray(data.schedule)) {
        throw new Error("The backend returned invalid schedule data.")
      }

      if (requestId !== scheduleRequestId.current) {
        return
      }

      setSchedule(data.schedule)
      setCrewCount(data.crew_count ?? null)
      setBackendStatus("online")

    } catch (err) {

      console.error("Schedule error:", err)

      if (requestId !== scheduleRequestId.current) {
        return
      }

      const isNetworkError = err instanceof TypeError

      if (isNetworkError) {
        setBackendStatus("offline")
      }

      setError(isNetworkError
        ? "Cannot reach the backend. Ensure it is running, then try again."
        : err.message || "Unable to load schedule."
      )

    }
  }


  // =====================================================
  // Check Backend Health
  // =====================================================

  const checkHealth = async () => {

    try {

      const response = await fetch(`${API_URL}/health`)

      if (!response.ok) {
        throw new Error("Health check failed")
      }

      const data = await response.json()

      if (data.status !== "healthy") {
        throw new Error("Backend is unhealthy")
      }

      setBackendStatus("online")

    } catch (err) {

      console.error("Health check error:", err)
      setBackendStatus("offline")

    }
  }


  // =====================================================
  // Optimize Schedule
  // =====================================================

  const optimizeSchedule = async () => {

    if (optimizationInProgress.current || refreshInProgress.current || loading) {
      return
    }

    try {

      optimizationInProgress.current = true
      ++scheduleRequestId.current
      setLoading(true)
      setError("")
      setMessage("")

      const response = await fetch(
        `${API_URL}/optimize`,
        {
          method: "POST"
        }
      )

      const data = await getResponseData(response)

      if (!response.ok) {
        throw new Error(
          getErrorMessage(data.detail, "Optimization failed.")
        )
      }

      // Apply the optimized assignments returned by the API immediately.
      if (!Array.isArray(data.schedule)) {
        throw new Error("The backend returned invalid schedule data.")
      }

      setSchedule(data.schedule)
      setCrewCount(data.crew_count ?? null)
      setBackendStatus("online")

      setMessage(
        data.message ||
        "Schedule optimized successfully!"
      )

      window.setTimeout(() => setMessage(""), 4000)

    } catch (err) {

      console.error(
        "Optimization error:",
        err
      )

      const isNetworkError = err instanceof TypeError

      if (isNetworkError) {
        setBackendStatus("offline")
      }

      setError(isNetworkError
        ? "Cannot reach the backend. Ensure it is running, then try again."
        : err.message || "Unable to optimize schedule."
      )

    } finally {

      optimizationInProgress.current = false
      setLoading(false)

    }
  }


  // =====================================================
  // Load Schedule When Page Opens
  // =====================================================

  useEffect(() => {

    checkHealth()
    fetchSchedule()

  }, [])

  const refreshData = async () => {

    if (refreshInProgress.current || optimizationInProgress.current) {
      return
    }

    try {
      refreshInProgress.current = true
      setRefreshing(true)
      await checkHealth()
      await fetchSchedule()
    } finally {
      refreshInProgress.current = false
      setRefreshing(false)
    }
  }

  // =====================================================
  // Calculate Statistics
  // =====================================================

  const assignedFlights = schedule.filter(
    (flight) =>
      flight.pilot &&
      flight.copilot &&
      flight.attendant
  ).length


  const unassignedFlights = schedule.filter(
    (flight) =>
      !(
        flight.pilot &&
        flight.copilot &&
        flight.attendant
      )
  ).length


  const scheduleDate = schedule
    .map((flight) => flight.start_time)
    .filter(Boolean)
    .sort()[0]

  const displayedDate = scheduleDate
    ? new Date(scheduleDate.replace(" ", "T")).toLocaleDateString(
      undefined,
      { year: "numeric", month: "long", day: "numeric" }
    )
    : "No schedule date"


  return (

    <div className="app">


      {/* =================================================
          Header
      ================================================= */}

      <header className="header">

  <div className="brand">

    <div className="brand-icon">
      ✈
    </div>

    <div>
      <h1>
        AEROOPS
      </h1>

      <p>
        Airline Crew Scheduling & Optimization
      </p>
    </div>

  </div>

  <div className={`status status-${backendStatus}`}>

    <span className="status-dot"></span>

    {backendStatus === "online"
      ? "System Online"
      : backendStatus === "checking"
        ? "Checking System..."
        : "System Offline"
    }

  </div>

</header>

      {/* =================================================
          Dashboard
      ================================================= */}

      <main className="dashboard">


        {/* =================================================
            Summary Cards
        ================================================= */}

        <section className="summary-grid">


          <div className="card">

            <h3>
              Total Flights
            </h3>

            <p className="number">
              {schedule.length}
            </p>

          </div>


          <div className="card">

            <h3>
              Total Crew
            </h3>

            <p className="number">
              {crewCount ?? "-"}
            </p>

          </div>


          <div className="card">

            <h3>
              Assigned Flights
            </h3>

            <p className="number">
              {assignedFlights}
            </p>

          </div>


          <div className="card">

            <h3>
              Unassigned Flights
            </h3>

            <p className="number">
              {unassignedFlights}
            </p>

          </div>

        </section>


        {/* =================================================
            Error Message
        ================================================= */}

        {error && (

          <div className="error-message">

            <strong>Error:</strong> {error}

          </div>

        )}


        {/* =================================================
            Success Message
        ================================================= */}

        {message && (

          <div className="success-message">

            {message}

          </div>

        )}


        {/* =================================================
            Actions
        ================================================= */}

        <section className="actions">


          <button
            className="primary-button"
            onClick={optimizeSchedule}
            disabled={loading || refreshing}
          >

            {loading
              ? "Optimizing..."
              : "Optimize Schedule"
            }

          </button>


          <button
            className="secondary-button"
            onClick={refreshData}
            disabled={loading || refreshing}
          >

            {refreshing ? "Refreshing..." : "Refresh Data"}

          </button>


        </section>


        {/* =================================================
            Flight Schedule
        ================================================= */}

        <section className="panel">


          <div className="panel-header">

            <h2>
              Flight Schedule
            </h2>

            <span>
              {displayedDate}
            </span>

          </div>


          {schedule.length > 0 ? (

            <FlightTable
              schedule={schedule}
            />

          ) : (

            <div className="empty-state">

              <p>
                No schedule data available.
              </p>

              <span>
                Run the optimizer to generate a schedule.
              </span>

            </div>

          )}


        </section>


      </main>


    </div>

  )

}

export default App
