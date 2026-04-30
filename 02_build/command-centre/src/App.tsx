import NowPanel from './components/NowPanel';
import PromisesCard from './components/PromisesCard';
import StreamPanel from './components/StreamPanel';
import SearchHistory from './components/SearchHistory';
import AgentsPanel from './components/AgentsPanel';
import RnDPanel from './components/RnDPanel';
import SearchBar from './components/SearchBar';

export default function App() {
  return (
    <div className="app-shell">
      {/* ── Header ─────────────────────── */}
      <header className="app-header">
        <div className="app-header__brand">
          <div className="app-logo" />
          <div>
            <h1>Command Centre</h1>
            <p>Calm operational awareness</p>
          </div>
        </div>
        <SearchBar />
      </header>

      {/* ── Now panel (full-width, dominant) */}
      <NowPanel />

      {/* ── Lower panels grid ──────────── */}
      <div className="panels-grid">
        <PromisesCard />
        <StreamPanel />
        <SearchHistory />
        <div className="panels-stack">
          <AgentsPanel />
          <RnDPanel />
        </div>
      </div>
    </div>
  );
}
