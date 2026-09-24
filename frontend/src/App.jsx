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
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const analyzeMachine = async () => {
    setLoading(true);

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

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Could not connect to FastAPI.");
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <h1>Predictive Maintenance AI</h1>
      <p>Machine Failure Prediction & Root Cause Analysis</p>

      <div className="form">
        <input
          name="temperature"
          placeholder="Temperature (°C)"
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
          placeholder="Voltage (V)"
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
          {loading ? "Analyzing..." : "Analyze Machine"}
        </button>
      </div>

      {result && (
        <div className="result">
          <h2>Analysis Result</h2>

          <h3>Status: {result.status}</h3>

          <p>
            Failure Probability:{" "}
            {(result.failure_probability * 100).toFixed(2)}%
          </p>

          <h3>AI Analysis</h3>
          <p>{result.analysis}</p>

          <h3>Knowledge Sources</h3>

          {result.sources?.map((source, index) => (
            <p key={index}>• {source}</p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;