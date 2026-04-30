import { useState, useEffect } from 'react';

const BASE_URL = 'http://localhost:8001';

interface SavedSearch {
  id: number;
  query: string;
  categories: string;
  total: number;
  searched_at: string;
}

interface WatchedSearch {
  id: number;
  query: string;
  categories: string;
  schedule: string;
  last_run: string;
  next_run: string;
  has_changes: boolean;
}

export default function SearchHistory() {
  const [tab, setTab] = useState<'recent' | 'watched'>('recent');
  const [recent, setRecent] = useState<SavedSearch[]>([]);
  const [watched, setWatched] = useState<WatchedSearch[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    // Refresh every 30 seconds to catch watcher updates
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  async function loadData() {
    try {
      const [recentRes, watchedRes] = await Promise.all([
        fetch(`${BASE_URL}/api/searches?limit=20`),
        fetch(`${BASE_URL}/api/searches/watched`),
      ]);
      const recentData = await recentRes.json();
      const watchedData = await watchedRes.json();
      setRecent(recentData.searches || []);
      setWatched(watchedData.watched || []);
    } catch {
      // Backend might not be ready
    } finally {
      setLoading(false);
    }
  }

  async function toggleWatch(query: string, isCurrentlyWatched: boolean) {
    if (isCurrentlyWatched) {
      await fetch(`${BASE_URL}/api/searches/watch?query=${encodeURIComponent(query)}`, { method: 'DELETE' });
    } else {
      await fetch(`${BASE_URL}/api/searches/watch?query=${encodeURIComponent(query)}&schedule=daily`, { method: 'POST' });
    }
    loadData();
  }

  async function markSeen(query: string) {
    await fetch(`${BASE_URL}/api/searches/seen?query=${encodeURIComponent(query)}`, { method: 'POST' });
    loadData();
  }

  function timeAgo(dateStr: string): string {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
  }

  const watchedQueries = new Set(watched.map(w => w.query));
  const changedQueries = new Set(watched.filter(w => w.has_changes).map(w => w.query));

  return (
    <div className="glass-card search-history">
      <div className="search-history__header">
        <span className="card-label" style={{ marginBottom: 0 }}>
          SEARCH INTEL
          {changedQueries.size > 0 && (
            <span className="search-history__badge">{changedQueries.size} new</span>
          )}
        </span>
        <div className="search-history__tabs">
          <button
            className={`search-history__tab ${tab === 'recent' ? 'search-history__tab--active' : ''}`}
            onClick={() => setTab('recent')}
          >
            Recent
          </button>
          <button
            className={`search-history__tab ${tab === 'watched' ? 'search-history__tab--active' : ''}`}
            onClick={() => setTab('watched')}
          >
            Watched {watched.length > 0 && <span className="search-history__count">{watched.length}</span>}
          </button>
        </div>
      </div>

      {loading ? (
        <div className="search-history__empty">Loading…</div>
      ) : tab === 'recent' ? (
        <div className="search-history__list">
          {recent.length === 0 ? (
            <div className="search-history__empty">
              No searches yet — hit ⌘K
            </div>
          ) : (
            recent.map((s) => (
              <div key={s.id} className="search-history__item">
                <div className="search-history__item-main">
                  <span className="search-history__query">{s.query}</span>
                  <span className="search-history__meta">
                    {s.total} results · {timeAgo(s.searched_at)}
                  </span>
                </div>
                <button
                  className={`search-history__watch-btn ${watchedQueries.has(s.query) ? 'search-history__watch-btn--active' : ''}`}
                  onClick={() => toggleWatch(s.query, watchedQueries.has(s.query))}
                  title={watchedQueries.has(s.query) ? 'Stop watching' : 'Watch this search'}
                >
                  {watchedQueries.has(s.query) ? '👁️' : '○'}
                </button>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="search-history__list">
          {watched.length === 0 ? (
            <div className="search-history__empty">
              No watched searches — click 👁️ on a recent search
            </div>
          ) : (
            watched.map((w) => (
              <div
                key={w.id}
                className={`search-history__item ${w.has_changes ? 'search-history__item--changed' : ''}`}
              >
                <div className="search-history__item-main">
                  <span className="search-history__query">
                    {w.has_changes && <span className="search-history__dot" />}
                    {w.query}
                  </span>
                  <span className="search-history__meta">
                    {w.schedule} · last: {timeAgo(w.last_run)}
                  </span>
                </div>
                <div className="search-history__actions">
                  {w.has_changes && (
                    <button className="search-history__seen-btn" onClick={() => markSeen(w.query)}>
                      ✓
                    </button>
                  )}
                  <button
                    className="search-history__watch-btn search-history__watch-btn--active"
                    onClick={() => toggleWatch(w.query, true)}
                    title="Stop watching"
                  >
                    👁️
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
