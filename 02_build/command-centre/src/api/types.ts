/**
 * Shared TypeScript types for the Amplified Command Centre API.
 * Matches the Pydantic models in backend/main.py
 */

// ── Promises ──────────────────────────────────────────
export type PromiseStatus = 'PENDING' | 'KEPT' | 'MISSED';

export interface PromiseItem {
  id: string;
  description: string;
  origin_event_id?: string | null;
  due_at: string;
  status: PromiseStatus;
  resolved_at?: string | null;
}

// ── Tasks ─────────────────────────────────────────────
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE' | 'BLOCKED' | 'NEEDS_DETAILS';
export type TaskType = 'COMM' | 'WRITING' | 'R_AND_D' | 'ADMIN';
export type Priority = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Task {
  id: string;
  title: string;
  description: string;
  origin_event_id?: string | null;
  session_id?: string | null;
  type: TaskType;
  status: TaskStatus;
  priority: Priority;
  due_at?: string | null;
  created_at: string;
  updated_at: string;
  promise_id?: string | null;
}

// ── Sessions ──────────────────────────────────────────
export type SessionStatus = 'ACTIVE' | 'PAUSED' | 'DONE';

export interface Session {
  id: string;
  focus_title: string;
  started_at: string;
  ended_at?: string | null;
  status: SessionStatus;
  tasks_created: string[];
  events: string[];
}

// ── Voice Events ──────────────────────────────────────
export type EventType = 'FOCUS_UPDATE' | 'TASK_INTENT' | 'IDEA' | 'RANT' | 'QUESTION' | 'META_STATE';

export interface VoiceEvent {
  id: string;
  timestamp: string;
  source: string;
  type: EventType;
  text: string;
  tags: string[];
  confidence: number;
  session_id?: string | null;
}
