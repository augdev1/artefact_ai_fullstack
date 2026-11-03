import React from 'react';
import { ChatSession } from '../types';

interface SidebarProps {
  sessions: ChatSession[];
  currentSessionId: string;
  isOpen: boolean;
  onSelectSession: (id: string) => void;
  onNewSession: () => void;
  onDeleteSession: (e: React.MouseEvent, id: string) => void;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  currentSessionId,
  isOpen,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  onCloseMobile,
}) => {
  return (
    <>
      {isOpen && (
        <div 
          onClick={onCloseMobile}
          className="fixed inset-0 bg-black/60 backdrop-blur-xs z-30 md:hidden transition-opacity"
        />
      )}
      <aside
        className={`
          fixed md:static inset-y-0 left-0 z-40 h-full bg-[#0E1017] border-r border-[#1B202E] flex flex-col transition-all duration-300 ease-in-out shrink-0 overflow-hidden
          ${isOpen 
            ? 'w-72 opacity-100 translate-x-0 pointer-events-auto' 
            : 'w-0 opacity-0 -translate-x-full md:translate-x-0 border-r-0 pointer-events-none'}
        `}
      >
        <div className="w-72 h-full flex flex-col shrink-0">
          <div className="p-4 border-b border-[#1B202E] flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-xl">🎸</span>
              <span className="font-semibold text-sm text-slate-200">Empório da Música</span>
            </div>
            <button
              onClick={onCloseMobile}
              className="text-slate-400 hover:text-white p-1 rounded-md cursor-pointer hover:bg-[#1A1F2C]"
              title="Fechar sidebar"
            >
              ✕
            </button>
          </div>

          <div className="p-3">
            <button
              onClick={onNewSession}
              className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-[#1E2333] to-[#181C2A] hover:from-[#262D42] hover:to-[#1E2436] text-slate-200 hover:text-white border border-[#2B334B] hover:border-[#E60067] rounded-xl py-2.5 px-4 text-sm font-medium transition-all shadow-sm cursor-pointer"
            >
              <span className="text-base font-bold text-[#E60067]">+</span>
              <span>Nova Conversa</span>
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1.5">
            <div className="flex items-center justify-between text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-2 py-1">
              <span>Histórico de Conversas</span>
              <span className="text-[10px] text-slate-600 font-mono">{sessions.length}</span>
            </div>
            {sessions.map((s) => {
              const isActive = s.id === currentSessionId;
              return (
                <div
                  key={s.id}
                  onClick={() => onSelectSession(s.id)}
                  className={`
                    group flex items-center justify-between px-3 py-2.5 rounded-xl text-sm cursor-pointer transition-all
                    ${
                      isActive
                        ? 'bg-[#181C2A] text-white border-l-2 border-[#E60067] shadow-sm font-medium'
                        : 'text-slate-400 hover:bg-[#12151F] hover:text-slate-200'
                    }
                  `}
                >
                  <div className="flex items-center space-x-2.5 truncate flex-1 mr-2">
                    <span className="text-xs text-slate-500">💬</span>
                    <span className="truncate">{s.title || 'Conversa'}</span>
                  </div>
                  <button
                    onClick={(e) => onDeleteSession(e, s.id)}
                    className="p-1.5 rounded-md text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition-colors cursor-pointer"
                    title="Apagar esta conversa"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              );
            })}
          </div>

          <div className="p-3 border-t border-[#1B202E] bg-[#0A0C12] space-y-2">
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span className="flex items-center space-x-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-[11px] font-medium text-slate-300">LangChain Ativo</span>
              </span>
              <span className="text-[10px] text-slate-500 uppercase font-mono">v1.0</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

