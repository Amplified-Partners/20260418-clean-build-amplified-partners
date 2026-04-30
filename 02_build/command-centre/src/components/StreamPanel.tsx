import { useEffect, useState } from 'react';
import { fetchBeastTranscripts, fetchBeastStats, BeastTranscript, BeastStats } from '../api/beastApi';

function timeAgo(isoStr: string) {
  const diff = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

export default function StreamPanel() {
  const [transcripts, setTranscripts] = useState<BeastTranscript[]>([]);
  const [stats, setStats] = useState<BeastStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchBeastTranscripts(), fetchBeastStats()])
      .then(([t, s]) => {
        if (!cancelled) {
          setTranscripts(t);
          setStats(s);
        }
      })
      .catch(() => { if (!cancelled) setError(true); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  return (
    <div className="glass-card" id="stream-panel">
      <div className="card-label-row">
        <span className="card-label">Voice Stream</span>
        <span className="card-label card-label--source">Beast Pipeline</span>
      </div>

      {/* Stats bar */}
      {stats && !('error' in stats && stats.error) && (
        <div className="stream-stats">
          <div className="stream-stat">
            <span className="stream-stat__number">{stats.total_transcripts}</span>
            <span className="stream-stat__label">Transcripts</span>
          </div>
          <div className="stream-stat">
            <span className="stream-stat__number">{stats.total_duration_hours.toFixed(1)}h</span>
            <span className="stream-stat__label">Recorded</span>
          </div>
          <div className="stream-stat">
            <span className="stream-stat__number">{stats.total_action_items}</span>
            <span className="stream-stat__label">Actions</span>
          </div>
          <div className="stream-stat">
            <span className="stream-stat__number">{stats.pending_analysis}</span>
            <span className="stream-stat__label">Pending</span>
          </div>
        </div>
      )}

      {loading && <div className="card-status">Connecting to Beast…</div>}
      {error && <div className="card-status card-status--error">Could not reach Beast pipeline</div>}

      {!loading && !error && transcripts.length === 0 && (
        <div className="stream-empty">
          <div className="stream-empty__icon">🎙️</div>
          <div className="stream-empty__text">Pipeline ready — no transcripts yet</div>
          <div className="stream-empty__hint">
            Record via Plaud Pin, AirPods, or upload audio to
            <span className="stream-empty__url"> voice.beast.amplifiedpartners.ai</span>
          </div>
        </div>
      )}

      {!loading && !error && transcripts.length > 0 && (
        <ul className="stream-list">
          {transcripts.map((t) => (
            <li key={t.id} className="stream-item">
              <span className="stream-icon stream-icon--task_intent">🎙️</span>
              <div className="stream-item__body">
                <span className="stream-item__text">
                  {t.summary || t.transcript_text?.slice(0, 120) || t.filename || 'Transcript'}
                </span>
                <div className="stream-item__meta">
                  {t.status && (
                    <span className={`stream-type stream-type--${t.status === 'completed' ? 'task_intent' : 'meta_state'}`}>
                      {t.status}
                    </span>
                  )}
                  {t.duration_seconds && (
                    <span className="stream-tag">{formatDuration(t.duration_seconds)}</span>
                  )}
                  {t.action_items && t.action_items.length > 0 && (
                    <span className="stream-tag">{t.action_items.length} actions</span>
                  )}
                </div>
              </div>
              {t.created_at && (
                <span className="stream-item__time">{timeAgo(t.created_at)}</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
