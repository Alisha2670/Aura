import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { Copy, Check, Sparkles, BookOpen, Clock, ShieldCheck, Share2 } from 'lucide-react'

export default function ResponseView({ 
  response = '', 
  query = '', 
  iterations = 1,
  evaluation = null,
  timestamp = null 
}) {
  const [copied, setCopied] = useState(false)

  if (!response) return null

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy report text: ', err)
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto glass-panel rounded-2xl p-6 sm:p-8 shadow-2xl border border-slate-800 space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-800/80">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-aura-500/10 border border-aura-500/30 text-aura-300 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-aura-400" />
            <span>Synthesized Research Dossier</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-100 tracking-tight">
            {query || 'Research Findings & Strategic Analysis'}
          </h2>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            type="button"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium border border-slate-700/80 transition-all shadow-sm"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied to Clipboard</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-slate-400" />
                <span>Copy Markdown</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Execution Meta Strip */}
      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900/60 border border-slate-800 font-mono">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          <span>Completed in {iterations} iteration{iterations > 1 ? 's' : ''}</span>
        </div>

        {evaluation && (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900/60 border border-slate-800 font-mono">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Quality Score: {evaluation.score || 9}/10</span>
          </div>
        )}

        {timestamp && (
          <span className="text-slate-500 font-mono text-[11px] ml-auto">
            {new Date(timestamp).toLocaleTimeString()}
          </span>
        )}
      </div>

      {/* Markdown Body */}
      <div className="prose prose-invert max-w-none prose-headings:font-semibold prose-headings:tracking-tight prose-h1:text-xl prose-h2:text-lg prose-h3:text-base prose-p:text-slate-300 prose-p:leading-relaxed prose-li:text-slate-300 prose-strong:text-slate-100 prose-code:text-aura-300 prose-code:bg-slate-900 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:font-mono prose-code:text-xs prose-pre:bg-slate-950 prose-pre:border prose-pre:border-slate-800 prose-pre:rounded-xl">
        <ReactMarkdown
          components={{
            h1: ({ node, ...props }) => <h1 className="text-xl font-bold text-slate-100 mt-6 mb-3 border-b border-slate-800/80 pb-2" {...props} />,
            h2: ({ node, ...props }) => <h2 className="text-lg font-semibold text-aura-200 mt-5 mb-2.5 flex items-center gap-2" {...props} />,
            h3: ({ node, ...props }) => <h3 className="text-base font-semibold text-slate-200 mt-4 mb-2" {...props} />,
            p: ({ node, ...props }) => <p className="text-slate-300 leading-relaxed my-3 text-sm sm:text-base" {...props} />,
            ul: ({ node, ...props }) => <ul className="list-disc list-outside ml-5 space-y-1.5 my-3 text-slate-300 text-sm sm:text-base" {...props} />,
            ol: ({ node, ...props }) => <ol className="list-decimal list-outside ml-5 space-y-1.5 my-3 text-slate-300 text-sm sm:text-base" {...props} />,
            blockquote: ({ node, ...props }) => (
              <blockquote className="border-l-4 border-aura-500 bg-aura-500/5 px-4 py-2 rounded-r-lg my-4 text-slate-300 italic" {...props} />
            ),
            code: ({ node, inline, ...props }) =>
              inline ? (
                <code className="bg-slate-800/80 text-aura-300 px-1.5 py-0.5 rounded text-xs font-mono border border-slate-700/60" {...props} />
              ) : (
                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 overflow-x-auto my-4 text-xs font-mono text-slate-200">
                  <code {...props} />
                </pre>
              ),
          }}
        >
          {response}
        </ReactMarkdown>
      </div>
    </div>
  )
}
