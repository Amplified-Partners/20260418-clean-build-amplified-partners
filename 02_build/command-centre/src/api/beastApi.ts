const BASE_URL = 'http://localhost:8001';

export interface BeastStats {
  total_transcripts: number;
  today_transcripts: number;
  total_duration_hours: number;
  total_action_items: number;
  total_content_pieces: number;
  pending_analysis: number;
  error?: string;
}

export interface BeastTranscript {
  id: string;
  filename?: string;
  status?: string;
  duration_seconds?: number;
  created_at?: string;
  transcript_text?: string;
  summary?: string;
  action_items?: string[];
  [key: string]: unknown; // flexible for unknown fields
}

export interface BeastBriefing {
  id: string;
  title?: string;
  content?: string;
  created_at?: string;
  [key: string]: unknown;
}

export interface Container {
  name: string;
  status: string;
  image: string;
  health: 'healthy' | 'unhealthy' | 'running';
  location: 'mac' | 'beast';
}

export interface InfraStatus {
  mac: Container[];
  beast: Container[];
  mac_count: number;
  beast_count: number;
  total: number;
  timestamp: string;
}

export async function fetchBeastStats(): Promise<BeastStats> {
  const res = await fetch(`${BASE_URL}/api/beast/stats`);
  if (!res.ok) throw new Error(`Beast stats: ${res.status}`);
  return res.json();
}

export async function fetchBeastTranscripts(): Promise<BeastTranscript[]> {
  const res = await fetch(`${BASE_URL}/api/beast/transcripts`);
  if (!res.ok) throw new Error(`Beast transcripts: ${res.status}`);
  return res.json();
}

export async function fetchBeastBriefings(): Promise<BeastBriefing[]> {
  const res = await fetch(`${BASE_URL}/api/beast/briefings`);
  if (!res.ok) throw new Error(`Beast briefings: ${res.status}`);
  return res.json();
}

export async function fetchInfraContainers(): Promise<InfraStatus> {
  const res = await fetch(`${BASE_URL}/api/infra/containers`);
  if (!res.ok) throw new Error(`Infra containers: ${res.status}`);
  return res.json();
}
