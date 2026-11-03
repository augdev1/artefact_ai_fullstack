export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  tools_used?: string[];
  guardrail_triggered?: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  date: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  tools_used: string[];
  guardrail_triggered: boolean;
  guardrail_reason?: string;
}
