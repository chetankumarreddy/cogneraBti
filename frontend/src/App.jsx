import React, { useState, useEffect } from 'react';
import { Shield, Search, Database, Bot, Activity, Settings, Server, Cpu, Globe, CheckCircle2, Map, BarChart3, Briefcase, Plus, Calendar, Edit3, LineChart, Network, List, Wifi, WifiOff, RefreshCw, Terminal, AlertTriangle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState("NARRATIVE");
  const [searchTx, setSearchTx] = useState("0xeth_demo_02_velocity");
  const [persona, setPersona] = useState("Compliance Officer");
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [serverHealth, setServerHealth] = useState({ status: "CHECKING" });

  const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const fetchBackendData = () => {
    fetch(`${apiBase}/api/v1/health`)
      .then(r => r.json()).then(data => setServerHealth(data))
      .catch(e => setServerHealth({ status: "OFFLINE" }));
  };

  useEffect(() => {
    fetchBackendData();
    const interval = setInterval(fetchBackendData, 10000);
    return () => clearInterval(interval);
  }, []);

  const runAnalysis = async () => {
    setIsLoading(true);
    try {
      const r = await fetch(`${apiBase}/api/v1/analyze`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tx_id: searchTx, audience: persona })
      });
      if (r.ok) {
        setAnalysis(await r.json());
      } else { alert("Server Error 500."); }
    } catch(e) { alert("Backend Offline."); }
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0f172a] text-slate-100 font-sans select-none">
      <header className="bg-[#1e293b] text-white px-6 py-4 flex justify-between items-center shadow-md border-b border-slate-700 shrink-0">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3 border-r border-slate-600 pr-6">
            <Shield size={28} className="text-indigo-500"/>
            <div>
              <h1 className="text-xl font-bold tracking-tight">Cognira BTI</h1>
              <p className="text-[10px] text-indigo-300 font-mono uppercase tracking-wider">Enterprise Intelligence Engine</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3 font-mono text-[10px]">
          <div className={`px-3 py-1.5 rounded border flex items-center gap-2 ${serverHealth.status === 'ONLINE' ? 'bg-emerald-950/40 text-emerald-400 border-emerald-500/50' : 'bg-red-950/40 text-red-400 border-red-500/50 animate-pulse'}`}>
             {serverHealth.status === 'ONLINE' ? <Wifi size={12}/> : <WifiOff size={12}/>}
             <span>SERVER: {serverHealth.status}</span>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 max-w-7xl mx-auto w-full">
        <div className="space-y-6 animate-fadeIn">
          <div className="bg-[#1e293b] p-5 rounded-lg border border-slate-700 shadow-sm">
            <h2 className="text-sm font-bold uppercase text-indigo-400 mb-3 flex items-center gap-2 font-mono"><Search size={16}/> Signal Nexus (Forensic Decoupler)</h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1">
                <label className="text-[10px] font-mono text-slate-400 uppercase mb-1 block">Transaction Hash String (0x...)</label>
                <input type="text" className="w-full p-2.5 bg-[#0f172a] border border-slate-600 rounded font-mono text-sm outline-none focus:border-indigo-400" value={searchTx} onChange={e=>setSearchTx(e.target.value)} />
              </div>
              <button onClick={runAnalysis} disabled={isLoading} className="px-6 py-2.5 bg-indigo-600 text-white font-bold rounded text-sm hover:bg-indigo-500 uppercase">{isLoading ? "Processing..." : "Decouple Hash"}</button>
            </div>
          </div>

          {analysis && (
            <div className="grid grid-cols-3 gap-6 animate-fadeIn">
              <div className="col-span-1 space-y-6">
                  <div className={`p-5 rounded-lg border flex flex-col justify-center items-center text-center shadow-md ${analysis.risk.level === 'CRITICAL' ? 'bg-red-950/30 border-red-500/40 text-red-300' : 'bg-emerald-950/30 border-emerald-500/40 text-emerald-300'}`}>
                    <div className="text-[10px] font-bold uppercase font-mono mb-2 opacity-80">Risk Constellation</div>
                    <div className="text-4xl font-black">{analysis.risk.composite}%</div>
                    <div className="text-sm font-bold mt-2">{analysis.risk.level}</div>
                  </div>
              </div>
              <div className="col-span-2 space-y-6">
                  <div className="bg-[#1e293b] p-5 rounded-lg border border-slate-700 shadow-md">
                      <div className="flex justify-between items-center mb-3">
                         <h2 className="text-[10px] font-bold uppercase font-mono text-indigo-400"><Bot size={14} className="inline mr-1"/> Narrative Forge (with Deep RAG Context)</h2>
                      </div>
                      <div className="bg-[#0f172a] p-4 rounded border border-slate-600 text-[13px] text-slate-300 whitespace-pre-wrap font-sans min-h-[140px]">{analysis.narrative}</div>
                  </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
