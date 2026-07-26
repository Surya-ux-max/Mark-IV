import React from 'react';
import { Cpu, HardDrive, ShieldCheck, Activity } from 'lucide-react';

export const SystemWorkspace = ({ systemMetrics, agentTrace = [] }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">SYSTEM DASHBOARD</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>HOST OPERATING SYSTEM: WINDOWS</span><br />
          <span>SUPERVISOR GRAPH: ONLINE</span>
        </div>
      </div>

      {/* Hardware / Performance Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'GRAPH LATENCY', val: systemMetrics?.latency || '0.12s', icon: Activity },
          { label: 'CPU LOAD', val: systemMetrics?.cpu || '14%', icon: Cpu },
          { label: 'MEMORY LOAD', val: '99.87%', icon: HardDrive },
          { label: 'SECURITY SHIELD', val: 'ACTIVE', icon: ShieldCheck },
        ].map((item, idx) => (
          <div key={idx} className="p-5 border border-[#1E1E1E] bg-[#0A0A0A] space-y-2">
            <div className="flex justify-between items-center text-[#9A9A9A] text-[10px] hud-font uppercase">
              <span>{item.label}</span>
              <item.icon className="w-3.5 h-3.5 text-white" />
            </div>
            <p className="text-2xl font-extrabold text-white">{item.val}</p>
          </div>
        ))}
      </div>

      {/* LangGraph Trace & DB Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Agent Routing Trace */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">LANGGRAPH AGENT EXECUTION TRACE</h3>
          <div className="p-4 border border-[#1E1E1E] bg-black space-y-3">
            <div className="flex items-center space-x-2 text-xs hud-font text-white">
              <span className="w-2 h-2 rounded-full bg-white animate-ping" />
              <span>START → SUPERVISOR ROUTER</span>
            </div>
            {agentTrace.length === 0 ? (
              <p className="hud-font text-xs text-[#9A9A9A] uppercase">Awaiting graph execution trace...</p>
            ) : (
              agentTrace.map((node, i) => (
                <div key={i} className="flex items-center space-x-2 text-xs hud-font text-[#9A9A9A] pl-4 border-l border-white/20">
                  <span>↓</span>
                  <span className="text-white font-bold uppercase">{node}</span>
                </div>
              ))
            )}
            <div className="flex items-center space-x-2 text-xs hud-font text-slate-400">
              <span>↓</span>
              <span>COMPILE FINAL CONVERSATIONAL RESPONSE</span>
            </div>
          </div>
        </div>

        {/* Database & Infrastructure Status */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">INFRASTRUCTURE STATUS</h3>
          <div className="space-y-3 hud-font text-xs">
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">PRIMARY DATABASE</span>
              <span className="text-white font-bold">PostgreSQL (markIV) / SQLite3</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">ORCHESTRATION ENGINE</span>
              <span className="text-white font-bold">LangGraph Multi-Agent</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">LLM PROVIDER</span>
              <span className="text-white font-bold">Groq (llama-3.1-8b-instant)</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">FRONTEND DEV SERVER</span>
              <span className="text-white font-bold">Vite 5 + React 18</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};

export default SystemWorkspace;
