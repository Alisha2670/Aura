import React, { useState } from 'react'
import { ExternalLink, Globe, ChevronDown, ChevronUp, Link2, Layers } from 'lucide-react'

export default function SourceList({ sources = [] }) {
  const [expandedIndex, setExpandedIndex] = useState(null)

  if (!sources || sources.length === 0) return null

  const getDomain = (url) => {
    try {
      const parsed = new URL(url)
      return parsed.hostname.replace('www.', '')
    } catch {
      return 'web'
    }
  }

  const toggleExpand = (idx) => {
    setExpandedIndex(expandedIndex === idx ? null : idx)
  }

  return (
    <div className="w-full max-w-4xl mx-auto glass-panel rounded-2xl p-6 shadow-xl border border-slate-800 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-100">Grounded Sources & Citations</h3>
            <p className="text-xs text-slate-400">Direct external web intelligence verified by Tavily</p>
          </div>
        </div>

        <div className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-300 text-xs font-mono">
          <span className="text-emerald-400 font-semibold">{sources.length}</span> Verified Source{sources.length > 1 ? 's' : ''}
        </div>
      </div>

      {/* Sources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
        {sources.map((source, idx) => {
          const domain = getDomain(source.url)
          const isExpanded = expandedIndex === idx

          return (
            <div
              key={idx}
              className="group rounded-xl glass-card border border-slate-800/80 hover:border-aura-500/40 p-4 transition-all duration-200 flex flex-col justify-between space-y-3"
            >
              {/* Card Top */}
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-md bg-aura-500/20 text-aura-300 text-[11px] font-bold font-mono">
                    [{idx + 1}]
                  </span>
                  <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800 text-[11px] text-slate-300 font-medium">
                    <Globe className="w-3 h-3 text-slate-400" />
                    <span>{domain}</span>
                  </div>
                </div>

                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-1.5 rounded-lg bg-slate-800/60 hover:bg-aura-500 text-slate-400 hover:text-white transition-colors"
                  title="Open source link in new tab"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>

              {/* Snippet Preview */}
              <div className="text-xs text-slate-300 leading-relaxed">
                <p className={isExpanded ? '' : 'line-clamp-3'}>
                  {source.snippet || 'No preview snippet available.'}
                </p>
              </div>

              {/* URL & Expand Footer */}
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px]">
                <span className="text-slate-500 truncate max-w-[200px]" title={source.url}>
                  {source.url}
                </span>

                {source.snippet && source.snippet.length > 150 && (
                  <button
                    type="button"
                    onClick={() => toggleExpand(idx)}
                    className="text-aura-400 hover:text-aura-300 font-medium inline-flex items-center gap-0.5 ml-auto"
                  >
                    <span>{isExpanded ? 'Less' : 'More'}</span>
                    {isExpanded ? (
                      <ChevronUp className="w-3 h-3" />
                    ) : (
                      <ChevronDown className="w-3 h-3" />
                    )}
                  </button>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
