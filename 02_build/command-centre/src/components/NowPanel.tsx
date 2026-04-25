import { useEffect, useState } from 'react';
import { fetchTasks } from '../api/tasksApi';
import { fetchCurrentSession } from '../api/sessionsApi';
import { Task, Session } from '../api/types';

/** Format time as HH:MM */
function formatTime(d: Date) {
  return d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}

/** Format date as "Wed 12 Mar 2026" */
function formatDate(d: Date) {
  return d.toLocaleDateString('en-GB', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

/** Priority indicator dot */
function PriorityDot({ priority }: { priority: Task['priority'] }) {
  const cls =
    priority === 'HIGH'
      ? 'priority-dot priority-dot--high'
      : priority === 'MEDIUM'
        ? 'priority-dot priority-dot--medium'
        : 'priority-dot priority-dot--low';
  return <span className={cls} />;
}

/** Status badge */
function StatusBadge({ status }: { status: Task['status'] }) {
  const label =
    status === 'IN_PROGRESS'
      ? 'In progress'
      : status === 'TODO'
        ? 'To do'
        : status === 'NEEDS_DETAILS'
          ? 'Needs info'
          : status.toLowerCase();
  return <span className={`task-badge task-badge--${status.toLowerCase()}`}>{label}</span>;
}

export default function NowPanel() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [session, setSession] = useState<Session | null>(null);
  const [now, setNow] = useState(new Date());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchTasks(), fetchCurrentSession()])
      .then(([t, s]) => {
        if (!cancelled) {
          setTasks(t);
          setSession(s);
        }
      })
      .catch(() => {
        if (!cancelled) setError(true);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  // Top 3 active tasks, sorted: IN_PROGRESS first, then by priority
  const priorityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
  const activeTasks = tasks
    .filter((t) => t.status === 'TODO' || t.status === 'IN_PROGRESS' || t.status === 'NEEDS_DETAILS')
    .sort((a, b) => {
      if (a.status === 'IN_PROGRESS' && b.status !== 'IN_PROGRESS') return -1;
      if (b.status === 'IN_PROGRESS' && a.status !== 'IN_PROGRESS') return 1;
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    })
    .slice(0, 3);

  return (
    <div className="glass-card now-panel" id="now-panel">
      <div className="now-panel__header">
        <div className="now-panel__focus">
          <span className="card-label">Now</span>
          {session && (
            <h2 className="now-panel__focus-title">
              <span className="focus-indicator" />
              {session.focus_title}
            </h2>
          )}
          {!session && !loading && (
            <h2 className="now-panel__focus-title now-panel__focus-title--empty">
              No active focus
            </h2>
          )}
        </div>
        <div className="now-panel__clock">
          <div className="clock-time">{formatTime(now)}</div>
          <div className="clock-date">{formatDate(now)}</div>
        </div>
      </div>

      <div className="now-panel__tasks">
        {loading && <div className="card-status">Loading tasks…</div>}
        {error && <div className="card-status card-status--error">Could not load tasks</div>}
        {!loading && !error && activeTasks.length === 0 && (
          <div className="card-status">All clear — nothing pending</div>
        )}
        {activeTasks.map((task, i) => (
          <div key={task.id} className="task-row">
            <span className="task-row__index">{i + 1}</span>
            <PriorityDot priority={task.priority} />
            <span className="task-row__title">{task.title}</span>
            <StatusBadge status={task.status} />
          </div>
        ))}
      </div>
    </div>
  );
}
