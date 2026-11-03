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
    <aside
      className={`
        fixed inset-y-0 left-0 z-40 w-72 bg-[#0E1017] border-r border-[#1B202E] flex flex-col transition-all duration-300 ease-in-out
        md:relative md:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full md:w-0 md:opacity-0 md:border-none'}
      `}
    >
      <div className="p-4 border-b border-[#1B202E] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-xl">🎸</span>
          <span className="font-semibold text-sm text-slate-200">Empório da Música</span>
        </div>
        <button
          onClick={onCloseMobile}
          className="md:hidden text-slate-400 hover:text-white p-1 rounded-md"
        >
          ✕
        </button>
      </div>

      <div className="p-3">
        <button
          onClick={onNewSession}
          className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-[#1E2333] to-[#181C2A] hover:from-[#262D42] hover:to-[#1E2436] text-slate-200 hover:text-white border border-[#2B334B] hover:border-[#E60067] rounded-xl py-2.5 px-4 text-sm font-medium transition-all shadow-sm"
        >
          <span className="text-base font-bold text-[#E60067]">+</span>
          <span>Nova Conversa</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
        <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider px-2 py-1">
          Histórico de Conversas
        </div>
        {sessions.map((s) => {
          const isActive = s.id === currentSessionId;
          return (
            <div
              key={s.id}
              onClick={() => onSelectSession(s.id)}
              className={`
                group flex items-center justify-between px-3 py-2.5 rounded-lg text-sm cursor-pointer transition-all
                ${
                  isActive
                    ? 'bg-[#181C2A] text-white border-l-2 border-[#E60067] font-medium'
                    : 'text-slate-400 hover:bg-[#12151F] hover:text-slate-200'
                }
              `}
            >
              <div className="flex items-center space-x-2.5 truncate">
                <span className="text-xs text-slate-500">💬</span>
                <span className="truncate">{s.title || 'Conversa'}</span>
              </div>
              <button
                onClick={(e) => onDeleteSession(e, s.id)}
                className="opacity-0 group-hover:opacity-100 hover:text-red-400 p-1 text-xs text-slate-500 transition-opacity"
                title="Excluir conversa"
              >
                🗑
              </button>
            </div>
          );
        })}
      </div>

      <div className="p-3 border-t border-[#1B202E] bg-[#0A0C12] text-xs text-slate-400">
        <div className="flex items-center justify-between mb-1">
          <span className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-[11px] font-medium text-slate-300">LangChain ReAct</span>
          </span>
          <span className="text-[10px] text-slate-500 uppercase font-mono">v1.0</span>
        </div>
      </div>
    </aside>
  );
};
