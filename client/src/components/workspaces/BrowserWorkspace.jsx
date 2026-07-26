import React from 'react';
import { Globe, Trash2, Cpu, Database, ShieldCheck } from 'lucide-react';

export const BrowserWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">BROWSER & CLEANER</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>AUTOMATION ENGINE: PLAYWRIGHT</span><br />
          <span>CACHE CONTROL: ACTIVE</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>BROWSER AGENT & CLEANER STATUS</span>
          <span>AUTOMATION GATEWAY</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Executing browser automation or cache cleaning routines...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Browser cleaner node active. Temporary cache and cookies inspected. 412 MB of cleanable temp files identified."}
          </p>
        )}
      </div>

      {/* Main Grid: Cleaner Status & Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Cache & Cookies Metrics */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">CACHE & STORAGE STATUS</h3>
          <div className="space-y-3">
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between items-center">
              <span className="text-xs text-[#9A9A9A] hud-font">TEMPORARY CACHE</span>
              <span className="text-sm font-bold text-white">412 MB</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between items-center">
              <span className="text-xs text-[#9A9A9A] hud-font">COOKIE SESSIONS</span>
              <span className="text-sm font-bold text-white">84 SESSIONS</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between items-center">
              <span className="text-xs text-[#9A9A9A] hud-font">DOWNLOAD LOGS</span>
              <span className="text-sm font-bold text-white">12 FILES</span>
            </div>
          </div>

          <button
            onClick={() => onSubmitQuery("Clean browser cache, cookies, and temporary files")}
            className="w-full py-3 bg-white text-black font-bold hud-font text-xs uppercase tracking-wider cursor-pointer hover:bg-slate-200 flex items-center justify-center space-x-2"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Purge Temporary Cache</span>
          </button>
        </div>

        {/* Open Automation Tabs & Bookmarks (2 cols) */}
        <div className="md:col-span-2 p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">AUTOMATED HEADLESS BROWSER TABS</h3>
          <div className="space-y-3">
            {[
              { url: 'https://console.groq.com/docs/models', title: 'Groq API Model Documentation', status: 'SYNCHRONIZED' },
              { url: 'https://python.langchain.com/docs/langgraph', title: 'LangGraph Multi-Agent Architecture', status: 'ACTIVE' },
              { url: 'https://tavily.com', title: 'Tavily Search API Dashboard', status: 'IDLE' },
            ].map((tab, i) => (
              <div key={i} className="p-4 border border-[#1E1E1E] bg-black flex justify-between items-center hover:border-white/40 transition-all">
                <div>
                  <h4 className="font-bold text-white text-sm">{tab.title}</h4>
                  <p className="hud-font text-[10px] text-[#9A9A9A] uppercase mt-1">{tab.url}</p>
                </div>
                <span className="hud-font text-[9px] border border-[#1E1E1E] px-2 py-1 text-white uppercase">{tab.status}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};

export default BrowserWorkspace;
