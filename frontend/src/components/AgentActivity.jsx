import React, { useState } from 'react'
import { 
  GitCommit, 
  Search, 
  BarChart3, 
  CheckCircle2, 
  FileText, 
  Loader2, 
  ChevronDown, 
  ChevronUp, 
  Sparkles, 
  AlertCircle 
} from 'lucide-react'

const AGENT_STEPS = [
  { id: 'planner', name: 'Planner Agent', desc: 'Decomposes query into prioritized subtasks', icon: GitCommit },
  { id: 'researcher', name: 'Researcher Agent', desc: 'Executes live targeted web searches', icon: Search },
  { id: 'analyst', name: 'Analyst Agent', desc: 'Synthesizes multi-source evidence', icon: BarChart3 },
  { id: 'evaluator', name: 'Evaluator Agent', desc: 'Validates completeness & accuracy', icon: CheckCircle2 },
  { id: 'final', name: 'Synthesis Engine', desc: 'Generates final grounded report', icon: FileText },
]

export default function AgentActivity({ 
  currentStep = 'idle', 
  iterationCount = 0, 
  maxIterations = 2,
  plan = null,
  evaluation = null,
  isExecuting = false
}) {
  const [showPlanDetails, setShowPlanDetails] = useState(true)

  const getStepStatus = (stepId, index) => {
    if (!isExecuting && currentStep === 'idle') return 'idle'
    if (currentStep === 'final' || currentStep === 'completed') return 'completed'

    const stepOrder = ['planner', 'researcher', 'analyst', 'evaluator', 'final']
    const currentIndex = stepOrder.indexOf(currentStep)
    const thisIndex = stepOrder.indexOf(stepId)

    if (thisIndex < currentIndex) return 'completed'
    if (thisIndex === currentIndex) return 'active'
    return 'idle'
  }

  return (
    <div className="w-full max-w-4xl mx-auto glass-panel rounded-2xl p-5 shadow-xl border border-slate-800 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-aura-500/20 text-aura-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-100">Multi-Agent Workflow Pipeline</h3>
            <p className="text-xs text-slate-400">Autonomous iterative execution graph</p>
          </div>
        </div>

        {iterationCount > 0 && (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-300 text-xs font-mono">
            <span className="text-aura-400">Iteration:</span>
            <span>{iterationCount} / {maxIterations}</span>
          </div>
        )}
      </div>

      {/* Stepper Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        {AGENT_STEPS.map((step, idx) => {
          const Icon = step.icon
          const status = getStepStatus(step.id, idx)

          return (
            <div
              key={step.id}
              className={`relative rounded-xl p-3.5 transition-all duration-300 border flex flex-col justify-between ${
                status === 'active'
                  ? 'bg-aura-600/15 border-aura-500/60 shadow-lg shadow-aura-500/10 scale-[1.02]'
                  : status === 'completed'
                  ? 'bg-emerald-950/20 border-emerald-500/40 text-slate-300'
                  : 'bg-slate-900/40 border-slate-800/80 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div
                  className={`p-2 rounded-lg ${
                    status === 'active'
                      ? 'bg-aura-500 text-white shadow-md shadow-aura-500/30'
                      : status === 'completed'
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : 'bg-slate-800 text-slate-500'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                {status === 'active' && (
                  <Loader2 className="w-4 h-4 text-aura-400 animate-spin" />
                )}
                {status === 'completed' && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                )}
              </div>

              <div>
                <h4
                  className={`text-xs font-semibold ${
                    status === 'active'
                      ? 'text-aura-300'
                      : status === 'completed'
                      ? 'text-emerald-300'
                      : 'text-slate-400'
                  }`}
                >
                  {step.name}
                </h4>
                <p className="text-[11px] text-slate-500 mt-1 leading-tight line-clamp-2">
                  {step.desc}
                </p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Plan Breakdown Drawer */}
      {plan && plan.subtasks && plan.subtasks.length > 0 && (
        <div className="rounded-xl glass-card border border-slate-800/80 overflow-hidden">
          <button
            type="button"
            onClick={() => setShowPlanDetails(!showPlanDetails)}
            className="w-full flex items-center justify-between p-3 text-left hover:bg-slate-800/30 transition-colors"
          >
            <div className="flex items-center gap-2 text-xs font-medium text-slate-300">
              <span className="w-2 h-2 rounded-full bg-aura-400" />
              <span>Research Plan ({plan.subtasks.length} Subtasks Generated)</span>
            </div>
            {showPlanDetails ? (
              <ChevronUp className="w-4 h-4 text-slate-400" />
            ) : (
              <ChevronDown className="w-4 h-4 text-slate-400" />
            )}
          </button>

          {showPlanDetails && (
            <div className="p-3 pt-0 border-t border-slate-800/60 divide-y divide-slate-800/40">
              {plan.subtasks.map((st, i) => (
                <div key={i} className="py-2 flex items-start justify-between gap-3 text-xs">
                  <div className="flex-1">
                    <span className="text-slate-200 font-medium">{st.subtask || st.title}</span>
                    {st.target_aspect && (
                      <span className="ml-2 px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-aura-300 font-mono">
                        {st.target_aspect}
                      </span>
                    )}
                  </div>
                  {st.priority && (
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                      Priority: {st.priority}
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Evaluator Feedback Card */}
      {evaluation && (
        <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
          <div className="flex items-center gap-2">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                evaluation.verdict === 'GOOD' ? 'bg-emerald-400' : 'bg-amber-400 animate-pulse'
              }`}
            />
            <span className="font-medium text-slate-200">
              Evaluator Verdict: <span className="font-mono text-aura-300">{evaluation.verdict}</span>
            </span>
          </div>
          {evaluation.score !== undefined && (
            <span className="text-slate-400 font-mono">
              Quality Score: <span className="text-emerald-400 font-bold">{evaluation.score}/10</span>
            </span>
          )}
        </div>
      )}
    </div>
  )
}
