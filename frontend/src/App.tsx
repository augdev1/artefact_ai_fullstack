import React, { useState, useEffect, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { ArtefactBrand } from './components/ArtefactBrand';
import { Message, ChatSession } from './types';
import { sendMessage, getHistory, clearHistory } from './api';

const QUICK_PROMPTS = [
  { label: 'Violões até R$ 1000', query: 'Quais opções de violões disponíveis custando até R$1000?', icon: '🎸' },
  { label: 'Preço Takamine GD20', query: 'Quanto custa o Takamine GD20 e opções de pagamento?', icon: '💰' },
  { label: 'Política de Devolução', query: 'Me arrependi da minha compra, posso devolver meu pedido?', icon: '📦' },
  { label: 'Horários e Endereço', query: 'Qual o endereço da loja e horário de funcionamento?', icon: '📍' },
];

export const App: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>(() => {
    try {
      const saved = localStorage.getItem('artefact_chat_sessions');
      return saved ? JSON.parse(saved) : [{ id: 'sess_default', title: 'Nova Conversa', date: new Date().toLocaleDateString('pt-BR') }];
    } catch {
      return [{ id: 'sess_default', title: 'Nova Conversa', date: new Date().toLocaleDateString('pt-BR') }];
    }
  });

  const [currentSessionId, setCurrentSessionId] = useState<string>(() => {
    return localStorage.getItem('artefact_current_session') || 'sess_default';
  });

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    localStorage.setItem('artefact_chat_sessions', JSON.stringify(sessions));
  }, [sessions]);

  useEffect(() => {
    localStorage.setItem('artefact_current_session', currentSessionId);
  }, [currentSessionId]);

  useEffect(() => {
    getHistory(currentSessionId).then(setMessages);
  }, [currentSessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleNewSession = () => {
    const id = 'sess_' + Date.now().toString(36);
    const newSession: ChatSession = { id, title: 'Nova Conversa', date: new Date().toLocaleDateString('pt-BR') };
    setSessions([newSession, ...sessions]);
    setCurrentSessionId(id);
    setMessages([]);
  };

  const handleDeleteSession = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    await clearHistory(id);
    const rest = sessions.filter((s) => s.id !== id);
    if (rest.length === 0) {
      handleNewSession();
    } else {
      setSessions(rest);
      if (currentSessionId === id) {
        setCurrentSessionId(rest[0].id);
      }
    }
  };

  const handleSend = async (override?: string) => {
    const text = (override || input).trim();
    if (!text || isLoading) return;
    setInput('');

    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    setIsLoading(true);

    if (messages.length === 0) {
      const title = text.slice(0, 26) + (text.length > 26 ? '...' : '');
      setSessions((prev) => prev.map((s) => (s.id === currentSessionId ? { ...s, title } : s)));
    }

    try {
      const res = await sendMessage(text, currentSessionId);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.response,
          tools_used: res.tools_used,
          guardrail_triggered: res.guardrail_triggered,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Tivemos uma instabilidade momentânea. Por favor, repita a pergunta!' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-[#0B0D13] text-slate-100 font-sans overflow-hidden">
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        isOpen={sidebarOpen}
        onSelectSession={setCurrentSessionId}
        onNewSession={handleNewSession}
        onDeleteSession={handleDeleteSession}
        onCloseMobile={() => setSidebarOpen(false)}
      />

      <main className="flex-1 flex flex-col h-full overflow-hidden bg-[#0B0D13]">
        <header className="h-16 border-b border-[#1A1F2C] bg-[#0E1017]/90 backdrop-blur flex items-center justify-between px-4 shrink-0">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-[#1A1F2C]"
          >
            ☰
          </button>
          <ArtefactBrand />
          <div className="text-xs text-slate-400 bg-[#161924] border border-[#23283B] rounded-full px-3 py-1">
            Campo Grande/MS
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          {messages.length === 0 && (
            <div className="max-w-2xl mx-auto my-auto pt-10 pb-6 flex flex-col items-center text-center">
              <div className="w-14 h-14 rounded-2xl bg-[#131620] border border-[#29324B] flex items-center justify-center text-2xl mb-4">
                🎸
              </div>
              <h1 className="text-2xl md:text-3xl font-bold font-display text-white mb-2">
                Como posso te ajudar hoje?
              </h1>
              <p className="text-sm text-slate-400 max-w-md mb-8">
                Assistente virtual da <strong className="text-slate-200">Empório da Música</strong>. Consulte instrumentos, preços e regras da loja.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg text-left">
                {QUICK_PROMPTS.map((p, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(p.query)}
                    className="p-3.5 rounded-xl bg-[#131620] hover:bg-[#1A1F2D] border border-[#1F2536] hover:border-[#E60067]/60 transition-all flex items-start space-x-3 text-sm text-slate-300"
                  >
                    <span className="text-lg">{p.icon}</span>
                    <div>
                      <div className="font-medium text-slate-200">{p.label}</div>
                      <div className="text-xs text-slate-500 line-clamp-1">{p.query}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="max-w-3xl mx-auto space-y-5">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex items-start space-x-3 ${m.role === 'user' ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-semibold ${
                    m.role === 'user'
                      ? 'bg-[#252C3E] text-white'
                      : 'bg-gradient-to-tr from-[#E60067] to-[#FF4589] text-white'
                  }`}
                >
                  {m.role === 'user' ? 'VOCÊ' : 'IA'}
                </div>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-[#1C2233] text-slate-100 border border-[#2B334B]'
                      : 'bg-[#13161F] text-slate-200 border border-[#1F2433]'
                  }`}
                >
                  {m.tools_used && m.tools_used.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-2 pb-2 border-b border-[#1F2536]">
                      <span className="text-[10px] text-slate-500 font-mono">Tools:</span>
                      {m.tools_used.map((t, ti) => (
                        <span key={ti} className="text-[10px] font-mono bg-[#1A1F2C] text-emerald-400 px-2 py-0.5 rounded">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                  {m.guardrail_triggered && (
                    <div className="text-[10px] font-mono text-[#FF4589] mb-1">
                      🛡️ Política de Escopo Ativada
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{m.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="text-xs text-slate-400 flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-[#E60067] animate-ping"></span>
                <span>Consultando catálogo e políticas...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <div className="p-4 md:p-6 bg-gradient-to-t from-[#0B0D13] to-transparent">
          <div className="max-w-3xl mx-auto">
            <div className="relative rounded-2xl bg-[#131620] border border-[#232A3D] focus-within:border-[#E60067]">
              <textarea
                rows={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Pergunte sobre instrumentos, preços, status de pedido ou regras da loja..."
                className="w-full bg-transparent text-sm text-slate-100 placeholder-slate-500 px-4 pt-3.5 pb-10 focus:outline-none resize-none"
              />
              <div className="absolute bottom-2.5 right-3">
                <button
                  onClick={() => handleSend()}
                  disabled={!input.trim() || isLoading}
                  className="bg-gradient-to-r from-[#E60067] to-[#FF2D75] text-white px-4 py-1.5 rounded-xl text-xs font-medium"
                >
                  Enviar →
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
export default App;
