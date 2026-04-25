import { Session } from './types';

const BASE_URL = 'http://localhost:8001';

export async function fetchCurrentSession(): Promise<Session> {
  const res = await fetch(`${BASE_URL}/api/sessions/current`);
  if (!res.ok) throw new Error(`Failed to fetch session: ${res.status}`);
  return res.json();
}
