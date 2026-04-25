import { useEffect, useState } from 'react';
import { fetchPromises, PromiseItem, PromiseStatus } from '../promisesApi';

function groupByStatus(items: PromiseItem[]) {
  const counts: Record<PromiseStatus, number> = { KEPT: 0, MISSED: 0, PENDING: 0 };
  for (const p of items) counts[p.status] = (counts[p.status] ?? 0) + 1;
  return counts;
}

function last30Days(items: PromiseItem[]) {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 30);
  return items.filter((p) => new Date(p.due_at) >= cutoff);
}

function fmtDate(iso: string) {
  try {
    return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
  } catch {
    return iso;
  }
}

export default function PromisesCard() {
  const [promises, setPromises] = useState<PromiseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetchPromises()
      .then((data) => { if (!cancelled) setPromises(data); })
      .catch((err) => { if (!cancelled) setError(err.message ?? 'Unknown error'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  const counts = groupByStatus(promises);
  const recent = groupByStatus(last30Days(promises));

  if (loading) {
    return (
      <div className="glass-card" id="promises-card">
        <div className="card-label">Promises</div>
        <div className="card-status">Loading…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card" id="promises-card">
        <div className="card-label">Promises</div>
        <div className="card-status card-status--error">Could not load promises</div>
      </div>
    );
  }

  return (
    <div className="glass-card" id="promises-card">
      <div className="card-label">Promises</div>

      <div className="promises-stats">
        <div className="stat-row stat-row--kept">
          <span className="stat-number stat-number--kept">{counts.KEPT}</span>
          <span className="stat-label">Kept</span>
        </div>
        <div className="stat-row stat-row--missed">
          <span className="stat-number stat-number--missed">{counts.MISSED}</span>
          <span className="stat-label">Missed</span>
        </div>
        <div className="stat-row stat-row--pending">
          <span className="stat-number stat-number--pending">{counts.PENDING}</span>
          <span className="stat-label">Pending</span>
        </div>
      </div>

      <div className="promises-summary">
        Last 30 days: {recent.KEPT} kept, {recent.MISSED} missed, {recent.PENDING} pending
      </div>

      <button
        className="details-toggle"
        id="promises-details-toggle"
        onClick={() => setShowDetails((v) => !v)}
      >
        {showDetails ? '▴ Hide details' : '▾ Details'}
      </button>

      {showDetails && (
        <div className="promises-detail">
          {promises.length === 0 ? (
            <p className="card-status">No promises found.</p>
          ) : (
            <ul className="promise-list">
              {promises.map((p) => (
                <li key={p.id} className="promise-item">
                  <span className="promise-item__desc" title={p.description}>{p.description}</span>
                  <span className={`promise-item__badge promise-item__badge--${p.status.toLowerCase()}`}>
                    {p.status}
                  </span>
                  <span className="promise-item__due">{fmtDate(p.due_at)}</span>
                </li>
              ))}
            </ul>
          )}
          <p className="promises-source">Based on: /api/promises</p>
        </div>
      )}
    </div>
  );
}
