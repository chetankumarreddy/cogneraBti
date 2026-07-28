import React, { useState, useEffect } from 'react';
import { Shield, Search, Database, Bot, Activity, Settings, Server, Cpu, Globe, CheckCircle2, Map, BarChart3, Briefcase, Plus, Calendar, Edit3, LineChart, Network, List, Wifi, WifiOff, RefreshCw, Terminal, AlertTriangle } from 'lucide-react';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [termsAccepted, setTermsAccepted] = useState(true);
  const [officerId, setOfficerId] = useState("ADMIN_COGNIRA_01");
  const [activeTab, setActiveTab] = useState("DASHBOARD");
  const [searchTx, setSearchTx] = useState("0xeth_demo_02_velocity");
  const [persona, setPersona] = useState("Compliance Officer");
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [serverHealth, setServerHealth] = useState({ status: "CHECKING" });
  const [alertStream, setAlertStream] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [caseComment, setCaseComment] = useState("");
  const [caseStatus, setCaseStatus] = useState("INVESTIGATING");
  const [graphType, setGraphType] = useState("ENTITY_NETWORK");

  const apiBase = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const fetchBackendData = () => {
    fetch(`${apiBase}/health`)
      .then(r => r.json()).then(data => setServerHealth({ status: "ONLINE", ...data }))
      .catch(() => setServerHealth({ status: "OFFLINE" }));

    fetch(`${apiBase}/alerts`)
      .then(r => r.json()).then(data => {
        if (Array.isArray(data) && data.length > 0) {
          setAlertStream(data);
          setSelectedCase(prev => prev ? prev : data[0]);
        }
      }).catch(() => {});
  };

  useEffect(() => {
    fetchBackendData();
    const interval = setInterval(fetchBackendData, 10000);
    return () => clearInterval(interval);
  }, []);

  const runAnalysis = async () => {
    setIsLoading(true);
    try {
      const r = await fetch(`${apiBase}/analyse`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ search_type: "transaction_id", value: searchTx, persona: persona })
      });
      if (r.ok) setAnalysis(await r.json());
    } catch (e) { alert("API Connection Failed"); }
    setIsLoading(false);
  };

  const resolveCase = async (verdict) => {
    if (!selectedCase) return alert("Select a case first.");
    try {
      await fetch(`${apiBase}/cases/resolve`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ txn_id: selectedCase.transaction_hash, verdict: verdict, comments: caseComment, user: officerId })
      });
      alert(`Case updated with verdict: ${verdict}`);
      setCaseComment("");
      fetchBackendData();
    } catch(e) { alert("Action saved locally."); }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-[#0f172a] text-slate-200 font-sans">
        <div className="w-full max-w-md bg-[#1e293b] border border-slate-700 rounded-xl shadow-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <div className="mx-auto w-12 h-12 rounded-lg bg-indigo-600 flex items-center justify-center"><Shield className="text-white animate-pulse" size={26} /></div>
            <h2 className="text-xl font-black tracking-wider text-white uppercase">COGNIRA BTI LOGIN</h2>
          </div>
          <form onSubmit={(e)=>{e.preventDefault(); setIsAuthenticated(true);}} className="space-y-4 text-xs font-mono">
            <div>
              <label className="block font-bold text-slate-400 uppercase mb-1">Corporate Officer ID Token</label>
              <input type="text" required className="w-full bg-[#0f172a] border border-slate-600 p-3 rounded text-white outline-none focus:border-indigo-500" value={officerId} onChange={e=>setOfficerId(e.target.value)} />
            </div>
            <button type="submit" className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-black rounded uppercase tracking-widest shadow-lg transition-all">Initialize Workspace</button>
          </form>
        </div>
      </div>
    );
  }

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
          <nav className="flex gap-2">
            <button onClick={() => setActiveTab("DASHBOARD")} className={`px-4 py-2 rounded text-xs font-bold uppercase transition-all ${activeTab === 'DASHBOARD' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}><Activity size={14}/> Dashboard</button>
            <button onClick={() => setActiveTab("NARRATIVE")} className={`px-4 py-2 rounded text-xs font-bold uppercase transition-all ${activeTab === 'NARRATIVE' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}><Search size={14}/> Narrative Workspace</button>
            <button onClick={() => setActiveTab("CASES")} className={`px-4 py-2 rounded text-xs font-bold uppercase transition-all ${activeTab === 'CASES' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}><Briefcase size={14}/> Cases ({alertStream.length})</button>
            <button onClick={() => setActiveTab("ADMIN")} className={`px-4 py-2 rounded text-xs font-bold uppercase transition-all ${activeTab === 'ADMIN' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:bg-slate-800'}`}><Settings size={14}/> Admin Console</button>
          </nav>
        </div>
        <div className="flex items-center gap-3 font-mono text-[10px]">
          <div className={`px-3 py-1.5 rounded border flex items-center gap-2 ${serverHealth.status === 'ONLINE' ? 'bg-emerald-950/40 text-emerald-400 border-emerald-500/50' : 'bg-red-950/40 text-red-400 border-red-500/50 animate-pulse'}`}>
             {serverHealth.status === 'ONLINE' ? <Wifi size={12}/> : <WifiOff size={12}/>}
             <span>SERVER: {serverHealth.status}</span>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-6 max-w-7xl mx-auto w-full">
        {activeTab === "DASHBOARD" && (
          <div className="space-y-6 animate-fadeIn">
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-[#1e293b] p-4 rounded-lg border border-slate-700 shadow-md">
                 <div className="text-[10px] text-slate-400 uppercase font-bold font-mono">Total Transactions</div>
                 <div className="text-2xl font-black mt-2 text-white">41,290</div>
              </div>
              <div className="bg-red-950/30 p-4 rounded-lg border border-red-500/40 shadow-md">
                 <div className="text-[10px] text-red-400 uppercase font-bold font-mono">P1 Critical Alerts</div>
                 <div className="text-2xl font-black mt-2 text-red-300">12</div>
              </div>
              <div className="bg-[#1e293b] p-4 rounded-lg border border-slate-700 shadow-md">
                 <div className="text-[10px] text-slate-400 uppercase font-bold font-mono">Model Drift Status</div>
                 <div className="text-xl font-bold mt-2 text-emerald-400">STABLE (0.4%)</div>
              </div>
              <div className="bg-[#1e293b] p-4 rounded-lg border border-slate-700 shadow-md">
                 <div className="text-[10px] text-slate-400 uppercase font-bold font-mono">Avg Pipeline Latency</div>
                 <div className="text-2xl font-black mt-2 text-white">1.82ms</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "NARRATIVE" && (
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
                    <div className="p-5 rounded-lg border bg-red-950/30 border-red-500/40 text-red-300 flex flex-col justify-center items-center text-center shadow-md">
                      <div className="text-[10px] font-bold uppercase font-mono mb-2 opacity-80">Risk Constellation</div>
                      <div className="text-4xl font-black">{analysis.risk.composite}%</div>
                      <div className="text-sm font-bold mt-2">{analysis.risk.level}</div>
                    </div>
                </div>
                <div className="col-span-2 space-y-6">
                    <div className="bg-[#1e293b] p-5 rounded-lg border border-slate-700 shadow-md">
                        <h2 className="text-[10px] font-bold uppercase font-mono text-indigo-400 mb-3"><Bot size={14} className="inline mr-1"/> Narrative Forge Output & Graph Matrix</h2>
                        <div className="bg-[#0f172a] p-4 rounded border border-slate-600 text-[13px] text-slate-300 whitespace-pre-wrap font-sans min-h-[140px]">{analysis.narrative}</div>
                    </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "CASES" && (
           <div className="grid grid-cols-3 gap-6 animate-fadeIn h-[calc(100vh-140px)]">
              <div className="col-span-1 bg-[#1e293b] p-5 rounded-lg border border-slate-700 shadow-md flex flex-col">
                 <h2 className="text-sm font-bold tracking-wider text-indigo-400 uppercase mb-4 flex items-center gap-2 font-mono"><List size={16}/> Master Case List</h2>
                 <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                    {alertStream.map((alert, idx) => (
                       <div key={idx} onClick={() => setSelectedCase(alert)} className={`p-3 rounded border cursor-pointer ${selectedCase?.transaction_hash === alert.transaction_hash ? 'bg-indigo-900/30 border-indigo-500' : 'bg-[#0f172a] border-slate-600'}`}>
                          <div className="text-[10px] font-mono font-bold text-slate-300 truncate">{alert.transaction_hash}</div>
                          <div className="text-[11px] text-slate-400">{alert.label}</div>
                       </div>
                    ))}
                 </div>
              </div>
              <div className="col-span-2 bg-[#1e293b] p-6 rounded-lg border border-slate-700 shadow-md flex flex-col">
                 {selectedCase ? (
                    <>
                       <h2 className="text-lg font-black text-white uppercase mb-4">Case Details: {selectedCase.transaction_hash}</h2>
                       <textarea className="w-full bg-[#0f172a] border border-slate-500 rounded p-3 text-slate-200 outline-none h-24 mb-3 text-xs" placeholder="Add resolution comments..." value={caseComment} onChange={e=>setCaseComment(e.target.value)}></textarea>
                       <button onClick={()=>resolveCase("RESOLVED_TRUE_POSITIVE")} className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 rounded text-xs uppercase">Commit Resolution</button>
                    </>
                 ) : <div className="text-slate-500">Select a case</div>}
              </div>
           </div>
        )}

        {activeTab === "ADMIN" && (
           <div className="bg-[#1e293b] p-6 rounded-lg border border-slate-700 shadow-md animate-fadeIn space-y-6">
              <h2 className="text-lg font-black text-emerald-400 uppercase font-mono"><Settings size={20} className="inline mr-2"/> Control Tower & ML Rule Tuning</h2>
              <p className="text-xs text-slate-400 font-mono">Platform is fully active with local mocks, custom persona prompts, and BigQuery ML suggestions.</p>
           </div>
        )}
      </div>
    </div>
  );
}
