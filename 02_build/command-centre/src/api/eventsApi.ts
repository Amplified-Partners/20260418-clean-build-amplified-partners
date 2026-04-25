import { VoiceEvent } from './types';

const BASE_URL = 'http://localhost:8001';

export async function fetchEvents(): Promise<VoiceEvent[]> {
  const res = await fetch(`${BASE_URL}/api/events`);
  if (!res.ok) throw new Error(`Failed to fetch events: ${res.status}`);
  return res.json();
}
