import { useState } from "react";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    temperature: "",
    vibration: "",
    pressure: "",
    voltage: "",
    operating_hours: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const analyzeMachine = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          temperature: Number(form.temperature),
          vibration: Number(form.vibration),
          pressure: Number(form.pressure),
          voltage: Number(form.voltage),
          operating_hours: Number(form.operating_hours),
        }),
      });

      if (!response.ok) throw new Error("API request failed");

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Could not connect to FastAPI");
    } finally {
      setLoading(false);
    }
  };

  const risk = result
    ? Math.round(result.failure_probability * 100)
    : 0;

  return (
    <div className="dashboard">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="logo">
          <span>◈</span> PredictiveAI
        </div>

        <nav>
          <div className="nav-item active">⌂ Dashboard</div>
          <div className="nav-item">◉ Analyze</div>
          <div className="nav-item">⚙ Machines</div>
          <div className="nav-item">✦ AI Assistant</div>
          <div className="nav-item">◷ History</div>
          <div className="nav-item">⚙ Settings</div>
        </nav>

        <div className="system-card">
          <div className="online-dot"></div>
          <small>System Status</small>
          <strong>All Systems Online</strong>

          <small>AI Model</small>
          <strong>Gemini + ML</strong>

          <small>Last Update</small>
          <strong>Just now</strong>
        </div>
      </aside>

      {/* MAIN */}
      <main className="main">

        <header className="topbar">
          <div>
            <h1>
              Predictive Maintenance <span>AI</span>
            </h1>
            <p>Detect failures early. Keep your machines running.</p>
          </div>

          <div className="top-status">
            <span className="online-dot"></span>
            LIVE MONITORING
          </div>
        </header>

        {/* INPUT PANEL */}
        <section className="glass input-panel">
          <div className="section-title">
            <h2>Machine Diagnostics</h2>
            <span>ML + GenAI</span>
          </div>

          <div className="inputs">
            <input
              name="temperature"
              placeholder="Temperature °C"
              value={form.temperature}
              onChange={handleChange}
            />

            <input
              name="vibration"
              placeholder="Vibration"
              value={form.vibration}
              onChange={handleChange}
            />

            <input
              name="pressure"
              placeholder="Pressure"
              value={form.pressure}
              onChange={handleChange}
            />

            <input
              name="voltage"
              placeholder="Voltage V"
              value={form.voltage}
              onChange={handleChange}
            />

            <input
              name="operating_hours"
              placeholder="Operating Hours"
              value={form.operating_hours}
              onChange={handleChange}
            />

            <button onClick={analyzeMachine}>
              {loading ? "ANALYZING..." : "ANALYZE MACHINE →"}
            </button>
          </div>
        </section>

        {/* DASHBOARD CARDS */}
        <section className="grid">

          <div className="glass machine-card">
            <div className="card-header">
              <h2>Machine Overview</h2>
              <span>● LIVE</span>
            </div>

            <div className="machine-visual">
              <div className="machine-icon">⚙</div>

              <div className="sensor temp">
                🌡 {form.temperature || "--"}°C
                <small>Temperature</small>
              </div>

              <div className="sensor vibration">
                〰 {form.vibration || "--"}
                <small>Vibration</small>
              </div>

              <div className="sensor pressure">
                ◉ {form.pressure || "--"}
                <small>Pressure</small>
              </div>

              <div className="sensor voltage">
                ⚡ {form.voltage || "--"}V
                <small>Voltage</small>
              </div>
            </div>
          </div>

          {/* RISK */}
          <div className="glass risk-card">
            <h2>Failure Probability</h2>

            <div
              className="gauge"
              style={{
                background: `conic-gradient(#ff3b55 ${
                  risk * 3.6
                }deg, #18283c 0deg)`,
              }}
            >
              <div className="gauge-inner">
                <strong>{risk}%</strong>
                <span>{risk > 50 ? "HIGH RISK" : "LOW RISK"}</span>
              </div>
            </div>

            <div className="risk-warning">
              ⚠ {risk > 50 ? "High chance of failure" : "Machine condition stable"}
            </div>
          </div>

          {/* AI ANALYSIS */}
          <div className="glass analysis-card">
            <div className="card-header">
              <h2>✦ AI Root Cause Analysis</h2>
              <span className={risk > 50 ? "critical" : "safe"}>
                {risk > 50 ? "CRITICAL" : "NORMAL"}
              </span>
            </div>

            {result ? (
              <>
                <h3>AI Analysis</h3>
                <p>{result.analysis}</p>
              </>
            ) : (
              <div className="empty">
                Run machine analysis to generate
                AI-powered root cause analysis.
              </div>
            )}
          </div>
        </section>

        {/* SENSOR CARDS */}
        <section className="sensor-grid">
          <Sensor title="Temperature" value={form.temperature || "--"} unit="°C" icon="🌡" />
          <Sensor title="Vibration" value={form.vibration || "--"} unit="mm/s" icon="〰" />
          <Sensor title="Pressure" value={form.pressure || "--"} unit="psi" icon="◉" />
          <Sensor title="Voltage" value={form.voltage || "--"} unit="V" icon="⚡" />
        </section>

        {/* BOTTOM */}
        <section className="bottom-grid">

          <div className="glass trend-card">
            <div className="card-header">
              <h2>Sensor Trends</h2>
              <span>Last 24 Hours</span>
            </div>

            <div className="fake-chart">
              <div className="line one"></div>
              <div className="line two"></div>
              <div className="line three"></div>
            </div>
          </div>

          <div className="glass recommendations">
            <h2>✦ AI Recommendations</h2>

            {result ? (
              <p>{result.analysis}</p>
            ) : (
              <>
                <div>01 — Inspect cooling system</div>
                <div>02 — Check motor bearings</div>
                <div>03 — Verify power supply</div>
                <div>04 — Schedule maintenance</div>
              </>
            )}
          </div>

        </section>

      </main>
    </div>
  );
}

function Sensor({ title, value, unit, icon }) {
  return (
    <div className="glass sensor-card">
      <span>{icon}</span>
      <small>{title}</small>
      <strong>
        {value} <em>{unit}</em>
      </strong>
      <div className="mini-line"></div>
    </div>
  );
}

export default App;