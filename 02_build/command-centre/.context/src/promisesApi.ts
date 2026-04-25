// src/promisesApi.ts
export type PromiseStatus = 'PENDING' | 'KEPT' | 'MISSED';

export interface PromiseItem {
    id: string;
    description: string;
    origin_event_id?: string | null;
    due_at: string;       // ISO datetime
    status: PromiseStatus;
    resolved_at?: string | null;
}

const BASE_URL = 'http://localhost:8000';

export async function fetchPromises(): Promise<PromiseItem[]> {
    const res = await fetch(`${BASE_URL}/api/promises`);
    if (!res.ok) {
        throw new Error(`Failed to fetch promises: ${res.status}`);
    }
    return res.json();
}
