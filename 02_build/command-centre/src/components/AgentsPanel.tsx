import { useEffect, useState } from 'react';
import { fetchInfraContainers, Container, InfraStatus } from '../api/beastApi';

function parseUptime(status: string): string {
  // "Up 12 minutes (healthy)" → "12m"
  const match = status.match(/Up\s+(.*?)(?:\s*\(|$)/i);
  if (!match) return status;
  const raw = match[1].trim();
  return raw
    .replace(/\s*minutes?/, 'm')
    .replace(/\s*hours?/, 'h')
    .replace(/\s*days?/, 'd')
    .replace(/\s*seconds?/, 's')
    .replace(/\s*weeks?/, 'w');
}

/** Friendly display name for containers */
function friendlyName(name: string): string {
  return name
    .replace('amplified-', '')
    .replace(/-1$/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/** Map container to role description */
function containerRole(name: string): string {
  const roles: Record<string, string> = {
    'amplified-falkordb': 'Knowledge Graph',
    'amplified-falkordb-mcp': 'Graph MCP Server',
    'amplified-openclaw': 'Agent Framework',
    'amplified-picoclaw': 'Lightweight Agents',
    'amplified-unified-personal-1': 'Personal Services',
    'amplified-unified-business-1': 'Business Services',
    // Beast
    'traefik': 'Reverse Proxy + TLS',
    'litellm': 'Model Router',
    'ollama': 'Local LLM Inference',
    'portainer': 'Container Mgmt',
    'searxng': 'Private Search',
    'pii-tokeniser': 'PII Protection',
    'openclaw-agents': 'Agent Runtime',
    'postgres': 'Database',
    'postgresql': 'Database',
    'redis': 'Cache + PII Tokens',
    'langfuse': 'LLM Observability',
    'n8n': 'Workflow Automation',
    'code-server': 'Remote IDE',
    'voice-pipeline': 'Voice Transcription',
  };
  // Try exact match first, then partial
  if (roles[name]) return roles[name];
  for (const [key, role] of Object.entries(roles)) {
    if (name.includes(key)) return role;
  }
  return '';
}

export default function AgentsPanel() {
  const [infra, setInfra] = useState<InfraStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [showBeast, setShowBeast] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetchInfraContainers()
      .then((data) => { if (!cancelled) setInfra(data); })
      .catch(() => { if (!cancelled) setError(true); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  if (loading) {
    return (
      <div className="glass-card" id="agents-panel">
        <div className="card-label">Infrastructure</div>
        <div className="card-status">Checking containers…</div>
      </div>
    );
  }

  if (error || !infra) {
    return (
      <div className="glass-card" id="agents-panel">
        <div className="card-label">Infrastructure</div>
        <div className="card-status card-status--error">Could not read container status</div>
      </div>
    );
  }

  const macContainers = infra.mac;
  const beastContainers = infra.beast;

  return (
    <div className="glass-card" id="agents-panel">
      <div className="card-label-row">
        <span className="card-label">Infrastructure</span>
        <span className="infra-count">{infra.total} containers</span>
      </div>

      {/* Mac section */}
      <div className="infra-section">
        <div className="infra-section__header">
          <span className="infra-section__title">🖥️ Mac Mini</span>
          <span className="infra-section__count">{infra.mac_count}</span>
        </div>
        <ul className="agents-list">
          {macContainers.map((c) => (
            <ContainerRow key={c.name} container={c} />
          ))}
        </ul>
      </div>

      {/* Beast section */}
      <div className="infra-section">
        <div className="infra-section__header">
          <span className="infra-section__title">🦾 Beast</span>
          <span className="infra-section__count">{infra.beast_count}</span>
          {beastContainers.length > 4 && (
            <button className="details-toggle" onClick={() => setShowBeast(!showBeast)}>
              {showBeast ? '▴ Less' : `▾ All ${infra.beast_count}`}
            </button>
          )}
        </div>
        <ul className="agents-list">
          {(showBeast ? beastContainers : beastContainers.slice(0, 4)).map((c) => (
            <ContainerRow key={c.name} container={c} />
          ))}
        </ul>
      </div>
    </div>
  );
}

function ContainerRow({ container: c }: { container: Container }) {
  const healthClass = c.health === 'healthy' ? 'active' : c.health === 'unhealthy' ? 'error' : 'idle';
  const healthLabel = c.health === 'healthy' ? 'Healthy' : c.health === 'unhealthy' ? 'Error' : 'Up';

  return (
    <li className="agent-item">
      <div className="agent-item__info">
        <span className="agent-item__name">{friendlyName(c.name)}</span>
        <span className="agent-item__role">{containerRole(c.name) || c.image.split('/').pop()?.split(':')[0]}</span>
      </div>
      <div className="agent-item__right">
        <span className="agent-item__uptime">{parseUptime(c.status)}</span>
        <span className={`agent-status agent-status--${healthClass}`}>
          <span className="agent-status__dot" />
          {healthLabel}
        </span>
      </div>
    </li>
  );
}
