import React, { useState, useEffect } from 'react'
import { Sparkles, Brain, Cpu, ShieldCheck, AlertCircle, RefreshCw, Menu, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import InputSection from './components/InputSection'
import AgentActivity from './components/AgentActivity'
import ResponseView from './components/ResponseView'
import SourceList from './components/SourceList'
import Sidebar from './components/Sidebar'
import { 
  checkBackendHealth, 
  runResearchQuery, 
  fetchResearchHistory, 
  fetchResearchById, 
  deleteResearchById 
} from './api/client'

export default function App() {
  const [backendStatus, setBackendStatus] = useState({ online: false, checking: true })
  const [isExecuting, setIsExecuting] = useState(false)
  const [currentStep, setCurrentStep] = useState('idle')
  const [researchData, setResearchData] = useState(null)
  const [error, setError] = useState(null)
  const [submittedQuery, setSubmittedQuery] = useState('')
  
  // History state
  const [history, setHistory] = useState([])
  const [selectedHistoryId, setSelectedHistoryId] = useState(null)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  // Load backend health and history on mount
  useEffect(() => {
    async function loadInitialData() {
      const health = await checkBackendHealth()
      setBackendStatus({ online: health.online, checking: false })
      
      const historyList = await fetchResearchHistory()
      setHistory(historyList)
    }
    loadInitialData()
  }, [])

  // Dynamic agent step simulation while executing
  useEffect(() => {
    let timer1, timer2, timer3
    if (isExecuting) {
      setCurrentStep('planner')
      timer1 = setTimeout(() => setCurrentStep('researcher'), 2500)
      timer2 = setTimeout(() => setCurrentStep('analyst'), 6000)
      timer3 = setTimeout(() => setCurrentStep('evaluator'), 9500)
    }
    return () => {
      clearTimeout(timer1)
      clearTimeout(timer2)
      clearTimeout(timer3)
    }
  }, [isExecuting])

  const handleResearchSubmit = async (query) => {
    setIsExecuting(true)
    setError(null)
    setSubmittedQuery(query)
    setResearchData(null)
    setSelectedHistoryId(null)

    try {
      const data = await runResearchQuery(query)
      setResearchData(data)
      setSelectedHistoryId(data.id)
      setCurrentStep('final')

      // Refresh history list
      const updatedHistory = await fetchResearchHistory()
      setHistory(updatedHistory)
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during research execution.')
      setCurrentStep('idle')
    } finally {
      setIsExecuting(false)
    }
  }

  const handleSelectHistory = async (id) => {
    try {
      setError(null)
      setSelectedHistoryId(id)
      const dossier = await fetchResearchById(id)
      setResearchData(dossier)
      setSubmittedQuery(dossier.query)
      setCurrentStep('final')
      setIsSidebarOpen(false) // Close mobile drawer
    } catch (err) {
      setError('Could not retrieve historical research dossier.')
    }
  }

  const handleDeleteHistory = async (id) => {
    try {
      await deleteResearchById(id)
      setHistory((prev) => prev.filter((item) => item.id !== id))
      if (selectedHistoryId === id) {
        handleNewResearch()
      }
    } catch (err) {
      console.error('Failed to delete history item:', err)
    }
  }

  const handleNewResearch = () => {
    setResearchData(null)
    setSelectedHistoryId(null)
    setSubmittedQuery('')
    setCurrentStep('idle')
    setError(null)
  }

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex relative overflow-x-hidden selection:bg-aura-500 selection:text-white">
      {/* Sidebar Component */}
      <Sidebar
        isOpen={isSidebarOpen}
        onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
        history={history}
        selectedId={selectedHistoryId}
        onSelectHistory={handleSelectHistory}
        onDeleteHistory={handleDeleteHistory}
        onNewResearch={handleNewResearch}
      />

      {/* Main Content Viewport */}
      <div className="flex-1 lg:pl-72 flex flex-col items-center justify-start p-4 sm:p-8 relative">
        {/* Background ambient lighting */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-aura-600/15 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute top-1/3 right-10 w-96 h-96 bg-purple-600/10 rounded-full blur-[100px] pointer-events-none" />

        {/* Top Navigation Bar */}
        <header className="w-full max-w-5xl flex items-center justify-between py-4 mb-8 border-b border-slate-800/80 relative z-10">
          <div className="flex items-center gap-3">
            {/* Mobile Sidebar Toggle Button */}
            <button
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white lg:hidden"
              title="Toggle History Sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>

            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-aura-500 to-aura-700 flex items-center justify-center shadow-lg shadow-aura-500/25 border border-aura-400/30">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-aura-300 bg-clip-text text-transparent">
                  AURA
                </span>
                <span className="text-[10px] uppercase font-mono tracking-wider px-1.5 py-0.5 rounded bg-aura-500/20 text-aura-300 border border-aura-500/30">
                  v1.0 Multi-Agent
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Autonomous Research & Decision Engine</p>
            </div>
          </div>

          {/* Backend Connectivity Status Pill */}
          <div className="flex items-center gap-2 text-xs font-mono px-3 py-1.5 rounded-full glass-card border border-slate-800">
            <span
              className={`w-2 h-2 rounded-full ${
                backendStatus.online
                  ? 'bg-emerald-400 shadow-sm shadow-emerald-400 animate-pulse'
                  : 'bg-rose-400'
              }`}
            />
            <span className="text-slate-300">
              {backendStatus.checking
                ? 'Checking Engine...'
                : backendStatus.online
                ? 'FastAPI Engine Connected'
                : 'Backend Offline'}
            </span>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="w-full max-w-5xl space-y-8 relative z-10 pb-16">
          {/* Research Input Box */}
          <InputSection onSubmit={handleResearchSubmit} isLoading={isExecuting} />

          {/* Error Alert Display */}
          {error && (
            <div className="max-w-4xl mx-auto p-4 rounded-xl bg-rose-950/40 border border-rose-800/80 text-rose-300 flex items-start gap-3 text-sm">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-semibold text-rose-200">Execution Error</p>
                <p className="text-xs text-rose-300/90 mt-0.5 leading-relaxed">{error}</p>
              </div>
              <button
                onClick={() => handleResearchSubmit(submittedQuery)}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-rose-200 text-xs font-medium transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Retry
              </button>
            </div>
          )}

          {/* Multi-Agent Activity Stepper */}
          {(isExecuting || researchData) && (
            <AgentActivity
              currentStep={currentStep}
              iterationCount={researchData?.iteration_count || (isExecuting ? 1 : 0)}
              maxIterations={2}
              plan={researchData?.plan}
              evaluation={researchData?.evaluation}
              isExecuting={isExecuting}
            />
          )}

          {/* Synthesized Report Dossier */}
          {researchData && (researchData.response || researchData.final_answer) && (
            <ResponseView
              response={researchData.response || researchData.final_answer}
              query={researchData.query || submittedQuery}
              iterations={researchData.iteration_count || 1}
              evaluation={researchData.evaluation}
              timestamp={researchData.created_at ? new Date(researchData.created_at).getTime() : Date.now()}
            />
          )}

          {/* Grounded Sources & Citations */}
          {researchData && researchData.sources && researchData.sources.length > 0 && (
            <SourceList sources={researchData.sources} />
          )}
        </main>

        {/* Footer */}
        <footer className="w-full max-w-5xl pt-8 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
          <div className="flex items-center gap-2">
            <span>AURA Autonomous Research Engine</span>
            <span>•</span>
            <span>FastAPI + LangGraph + Groq + Tavily + SQLite</span>
          </div>
          <div className="font-mono text-[11px] text-slate-600">
            Built for High-Precision Generative & Agentic AI
          </div>
        </footer>
      </div>
    </div>
  )
}
