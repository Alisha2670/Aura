import React from 'react'
import { History, Plus, Trash2, Clock, X, Sparkles } from 'lucide-react'

export default function Sidebar({
  isOpen,
  onToggle,
  history = [],
  selectedId = null,
  onSelectHistory,
  onDeleteHistory,
  onNewResearch
}) {
  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isOpen && (
        <div
          onClick={onToggle}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* Sidebar Panel */}
      <aside
        className={`fixed top-0 left-0 h-full w-72 bg-[#0E1322] border-r border-slate-800 z-50 transform transition-transform duration-300 ease-in-out flex flex-col justify-between ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 flex flex-col h-full overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
            <div className="flex items-center gap-2 text-slate-200 font-semibold text-sm">
              <History className="w-4 h-4 text-aura-400" />
              <span>Research History</span>
            </div>
            <div className="flex items-center gap-1.5">
              <button
                onClick={onNewResearch}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-aura-600 hover:bg-aura-500 text-white text-xs font-medium transition-colors shadow-sm"
                title="Start New Research"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>New</span>
              </button>
              <button
                onClick={onToggle}
                className="p-1 rounded-lg text-slate-400 hover:text-white lg:hidden"
                title="Close Sidebar"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* History List */}
          <div className="flex-1 overflow-y-auto py-3 space-y-1.5 pr-1">
            {history.length === 0 ? (
              <div className="py-12 text-center text-xs text-slate-500 flex flex-col items-center gap-2">
                <Clock className="w-6 h-6 text-slate-600" />
                <span>No past research sessions yet</span>
              </div>
            ) : (
              history.map((item) => {
                const isSelected = selectedId === item.id
                return (
                  <div
                    key={item.id}
                    className={`group flex items-center justify-between p-2.5 rounded-xl text-xs cursor-pointer transition-all border ${
                      isSelected
                        ? 'bg-aura-500/15 border-aura-500/50 text-slate-100'
                        : 'bg-slate-900/30 border-transparent hover:border-slate-800 hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <div
                      onClick={() => onSelectHistory(item.id)}
                      className="flex-1 truncate pr-2"
                    >
                      <p className="truncate font-medium">{item.query}</p>
                      <p className="text-[10px] text-slate-500 mt-0.5 font-mono">
                        {item.created_at ? new Date(item.created_at).toLocaleDateString(undefined, {
                          month: 'short',
                          day: 'numeric',
                        }) : ''}
                      </p>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        onDeleteHistory(item.id)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-rose-500/20 text-slate-500 hover:text-rose-400 transition-opacity"
                      title="Delete research run"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )
              })
            )}
          </div>

          {/* Sidebar Footer */}
          <div className="pt-3 border-t border-slate-800/80 text-[11px] text-slate-500 flex items-center justify-between">
            <span>{history.length} Session{history.length === 1 ? '' : 's'}</span>
            <span className="font-mono text-[10px] text-emerald-400">SQLite Active</span>
          </div>
        </div>
      </aside>
    </>
  )
}
