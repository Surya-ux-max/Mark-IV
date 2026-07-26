import React from 'react';
import { Brain, Database, Cpu, HardDrive } from 'lucide-react';

export const MemoryWorkspace = ({ aiResponse, isTyping, conversations = [] }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">MEMORY</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>VECTOR DB: CHROMADB / SQLITE</span><br />
          <span>RECALL BANDWIDTH: 100% NOMINAL</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>MEMORY AGENT CONTEXT RECALL</span>
          <span>SEMANTIC EMBEDDINGS</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Querying vector embeddings & memory database...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Operator profile identified as Surya. Long-term preferences and session memory loaded cleanly."}
          </p>
        )}
      </div>

      {/* Memory Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Long-Term Memory (1 col) */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">LONG-TERM OPERATOR PROFILE</h3>
          <div className="space-y-3">
            {[
              { key: 'OPERATOR NAME', val: 'Surya' },
              { key: 'PRIMARY SYSTEM EMAIL', val: 'suryapr.exe14@gmail.com' },
              { key: 'POSTGRES DB NAME', val: 'markIV' },
              { key: 'PREFERRED MODEL', val: 'llama-3.1-8b-instant' },
            ].map((fact, i) => (
              <div key={i} className="p-3 border border-[#1E1E1E] bg-black">
                <p className="hud-font text-[9px] text-[#9A9A9A] uppercase">{fact.key}</p>
                <p className="text-sm font-bold text-white mt-0.5">{fact.val}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Session Conversation Timeline (2 cols) */}
        <div className="md:col-span-2 p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">SESSION CONVERSATION LOGS</h3>
          <div className="space-y-3 max-h-[340px] overflow-y-auto pr-2 scrollbar-thin">
            {conversations.length === 0 ? (
              <p className="hud-font text-xs text-[#9A9A9A] uppercase">No session messages recorded yet.</p>
            ) : (
              conversations.map((msg, i) => (
                <div key={i} className="p-3 border border-[#1E1E1E] bg-black space-y-1">
                  <div className="flex justify-between items-center text-[9px] hud-font">
                    <span className={`px-1.5 py-0.5 font-bold uppercase ${msg.sender === 'operator' ? 'bg-white/10 text-white' : 'bg-white text-black'}`}>
                      {msg.sender === 'operator' ? 'SURYA' : 'SURVEX'}
                    </span>
                    <span className="text-[#9A9A9A]">
                      {new Date(msg.timestamp || Date.now()).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-xs text-white leading-relaxed">{msg.message}</p>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

    </div>
  );
};

export default MemoryWorkspace;
