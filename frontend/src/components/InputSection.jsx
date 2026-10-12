import React, { useState } from 'react'
import { Sparkles, Search, CornerDownLeft, Loader2, Lightbulb } from 'lucide-react'

const PRESET_QUERIES = [
  'Compare PostgreSQL vs MongoDB for high-throughput time-series analytics',
  'Analyze pricing and latency tradeoffs between Claude 3.5 Sonnet and GPT-4o',
  'Evaluate Next.js App Router vs Remix for enterprise scale applications',
  'What are the state-of-the-art multi-agent framework patterns in 2025?'
]

export default function InputSection({ onSubmit, isLoading }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e?.preventDefault()
    const trimmed = query.trim()
    if (!trimmed || isLoading) return
    onSubmit(trimmed)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleSelectPreset = (preset) => {
    if (isLoading) return
    setQuery(preset)
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      {/* Input Box Card */}
      <form
        onSubmit={handleSubmit}
        className="glass-panel rounded-2xl p-3 shadow-xl border border-slate-800/80 focus-within:border-aura-500/60 focus-within:ring-2 focus-within:ring-aura-500/20 transition-all duration-200"
      >
        <div className="flex items-start gap-3 p-2">
          <div className="p-2 rounded-xl bg-aura-500/10 text-aura-400 mt-1">
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin text-aura-400" />
            ) : (
              <Sparkles className="w-5 h-5" />
            )}
          </div>

          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            placeholder="Ask AURA to research, compare architectures, analyze pricing, or synthesize complex topics..."
            rows={2}
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 resize-none outline-none text-sm md:text-base leading-relaxed disabled:opacity-50"
          />
        </div>

        {/* Footer controls */}
        <div className="flex items-center justify-between pt-2 px-2 border-t border-slate-800/60 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline text-slate-500">Press</span>
            <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 font-mono border border-slate-700">
              Enter ↵
            </kbd>
            <span className="hidden sm:inline text-slate-500">to submit</span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-[11px] text-slate-500 font-mono">
              {query.length} chars
            </span>
            <button
              type="submit"
              disabled={!query.trim() || isLoading}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-aura-600 hover:bg-aura-500 disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed text-white font-medium text-xs md:text-sm shadow-lg shadow-aura-600/20 transition-all duration-150"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Researching...</span>
                </>
              ) : (
                <>
                  <Search className="w-4 h-4" />
                  <span>Deep Research</span>
                  <CornerDownLeft className="w-3 h-3 text-aura-200" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Preset Query Chips */}
      <div className="space-y-2">
        <div className="flex items-center gap-1.5 text-xs font-medium text-slate-400">
          <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
          <span>Suggested Research Prompts</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {PRESET_QUERIES.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectPreset(preset)}
              disabled={isLoading}
              className="text-left text-xs px-3 py-1.5 rounded-lg glass-card border border-slate-800 hover:border-aura-500/40 hover:bg-aura-500/10 text-slate-300 hover:text-white transition-all duration-150 disabled:opacity-40 disabled:pointer-events-none"
            >
              {preset}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
