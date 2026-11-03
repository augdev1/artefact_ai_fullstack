import { ChatResponse, Message } from './types';

const API_BASE = '/api';

export async function sendMessage(message: string, sessionId: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) {
    throw new Error(`Failed to send message: ${res.statusText}`);
  }
  return res.json();
}

export async function getHistory(sessionId: string): Promise<Message[]> {
  const res = await fetch(`${API_BASE}/chat/history/${sessionId}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.messages || [];
}

export async function clearHistory(sessionId: string): Promise<boolean> {
  const res = await fetch(`${API_BASE}/chat/history/${sessionId}`, { method: 'DELETE' });
  return res.ok;
}

