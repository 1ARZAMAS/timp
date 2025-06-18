import React, { useState } from "react";

function App() {
  const [threatMin, setThreatMin] = useState("");
  const [threatMax, setThreatMax] = useState("");
  const [incidents, setIncidents] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    setError(null);
    try {
      const params = new URLSearchParams();
      if (threatMin) params.append("threat_min", threatMin);
      if (threatMax) params.append("threat_max", threatMax);

      const response = await fetch(`http://127.0.0.1:5000/incidents/search?${params.toString()}`);
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || "Ошибка запроса");
      }
      const data = await response.json();
      setIncidents(data);
    } catch (err) {
      setError(err.message);
      setIncidents([]);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "auto" }}>
      <h2>Поиск инцидентов по уровню угрозы</h2>
      <div>
        <label>
          Минимум угрозы:{" "}
          <input
            type="number"
            value={threatMin}
            onChange={(e) => setThreatMin(e.target.value)}
            placeholder="0"
          />
        </label>
      </div>
      <div>
        <label>
          Максимум угрозы:{" "}
          <input
            type="number"
            value={threatMax}
            onChange={(e) => setThreatMax(e.target.value)}
            placeholder="10"
          />
        </label>
      </div>
      <button onClick={handleSearch}>Найти</button>

      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}

      <ul>
        {incidents.map((inc) => (
          <li key={inc.id}>
            #{inc.id} - {inc.description} (Угроза: {inc.threat_level})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
