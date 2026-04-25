import { useEffect, useState } from 'react';

interface GraphEntity {
  name: string;
  summary: string;
}

export default function RnDPanel() {
  const [entities, setEntities] = useState<GraphEntity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    // Try FalkorDB MCP on port 8001 (avoiding conflict with our backend on 8000)
    // Falls back to static data if unavailable
    let cancelled = false;
    fetch('http://localhost:3002/api/graph/entities?limit=5')
      .then((r) => r.json())
      .then((data) => { if (!cancelled && Array.isArray(data)) setEntities(data); })
      .catch(() => { if (!cancelled) setError(true); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  // Static R&D items when FalkorDB isn't available via UI
  const staticItems = [
    { icon: '🧫', title: 'Pudding Discovery', desc: 'Cross-industry insight extraction' },
    { icon: '🔬', title: 'Slime Mould Routing', desc: 'Client scheduling optimisation' },
    { icon: '📊', title: 'Death Spiral Detector', desc: 'Altman Z-Score early warning' },
    { icon: '🧠', title: 'Knowledge Vault', desc: '5,000+ docs in ~/vault/' },
  ];

  return (
    <div className="glass-card rnd-panel" id="rnd-panel">
      <div className="card-label">R&D</div>
      <div className="rnd-content">
        {entities.length > 0 ? (
          entities.map((e, i) => (
            <div key={i} className="rnd-item">
              <span className="rnd-item__icon">🔗</span>
              <div className="rnd-item__body">
                <span className="rnd-item__title">{e.name}</span>
                <span className="rnd-item__desc">{e.summary}</span>
              </div>
            </div>
          ))
        ) : (
          staticItems.map((item, i) => (
            <div key={i} className="rnd-item">
              <span className="rnd-item__icon">{item.icon}</span>
              <div className="rnd-item__body">
                <span className="rnd-item__title">{item.title}</span>
                <span className="rnd-item__desc">{item.desc}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
