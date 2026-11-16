import { useEffect, useState } from "react";
import "chart.js/auto";
import { Line, Bar } from "react-chartjs-2";

const label = (m) => new Date(m + "-01").toLocaleDateString("fr-FR", { month: "short", year: "2-digit" });
const tone = (v) => (v >= 90 ? "good" : v >= 70 ? "mid" : "low");

export default function App() {
  const [region, setRegion] = useState("");
  const [month, setMonth] = useState("");
  const [d, setD] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    setErr("");
    fetch("/api/dashboard?" + new URLSearchParams({ region, month }))
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then(setD)
      .catch(() => setErr("Impossible de joindre l'API. Vérifiez que le backend tourne sur le port 8000."));
  }, [region, month]);

  if (err) return <p className="error">{err}</p>;
  if (!d) return <p className="loading">Chargement des indicateurs…</p>;
  const s = d.summary;

  return (
    <main>
      <p className="notice">Démonstration : toutes les données sont fictives.</p>
      <header>
        <h1>Performance des formations sanitaires</h1>
        <div className="filters">
          <select value={region} onChange={(e) => setRegion(e.target.value)} aria-label="Région">
            <option value="">Toutes les régions</option>
            {d.filters.regions.map((r) => <option key={r}>{r}</option>)}
          </select>
          <select value={d.month} onChange={(e) => setMonth(e.target.value)} aria-label="Mois">
            {[...d.filters.months].reverse().map((m) => <option key={m} value={m}>{label(m)}</option>)}
          </select>
        </div>
      </header>

      <section className="kpis">
        <div className={"score " + tone(s.composite)}>
          <span className="big">{s.composite}%</span>
          <span>Score composite</span>
          <small>60 % quantité + 40 % qualité</small>
        </div>
        <div><strong>{s.quantity}%</strong><span>Score quantité</span></div>
        <div><strong>{s.quality}%</strong><span>Score qualité</span></div>
        <div><strong>{s.facilities}</strong><span>Formations sanitaires</span></div>
      </section>

      <section className="card">
        <h2>Évolution sur 12 mois</h2>
        <Line
          data={{
            labels: d.trend.map((t) => label(t.month)),
            datasets: [
              { label: "Composite", data: d.trend.map((t) => t.composite), borderColor: "#1f6f54", borderWidth: 3, tension: 0.3 },
              { label: "Quantité", data: d.trend.map((t) => t.quantity), borderColor: "#c98a1b", tension: 0.3 },
              { label: "Qualité", data: d.trend.map((t) => t.quality), borderColor: "#4a6fa5", tension: 0.3 },
            ],
          }}
          options={{ scales: { y: { min: 40, max: 110 } }, plugins: { legend: { position: "bottom" } } }}
        />
      </section>

      <section className="card">
        <h2>Classement des formations sanitaires</h2>
        <Bar
          data={{
            labels: d.facilities.map((f) => f.name),
            datasets: [{
              label: "Score composite (%)",
              data: d.facilities.map((f) => f.composite),
              backgroundColor: d.facilities.map((f) => ({ good: "#1f6f54", mid: "#c98a1b", low: "#b5443a" }[tone(f.composite)])),
            }],
          }}
          options={{ indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { min: 0, max: 120 } } }}
        />
      </section>

      <section className="card">
        <h2>Taux de réalisation par indicateur</h2>
        <div className="scroll">
          <table>
            <thead><tr><th>Indicateur</th><th>Type</th><th>Réalisé</th><th>Cible</th><th>Taux</th></tr></thead>
            <tbody>
              {d.indicators.map((i) => (
                <tr key={i.label}>
                  <td>{i.label}</td>
                  <td>{i.kind === "quantity" ? "Quantité" : "Qualité"}</td>
                  <td>{i.value}</td><td>{i.target}</td>
                  <td className="rate"><div className={"bar " + tone(i.rate)} style={{ width: Math.min(i.rate, 100) + "%" }} />{i.rate}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
