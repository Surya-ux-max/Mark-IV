import React, { useState } from 'react';
import { Terminal, Code, FileText, Play, CheckCircle } from 'lucide-react';

export const CodingWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  const [codePrompt, setCodePrompt] = useState('');
  const [activeTab, setActiveTab] = useState('editor');

  const defaultSnippet = `// SurveX LangGraph Supervisor Core Node
def supervisor_node(state: AgentState):
    messages = state["messages"]
    next_agent = run_supervisor(messages)
    return {"next": next_agent}

# Execution compiled cleanly (0 warnings)
print("SurveX Agent Graph Nominal")`;

  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">CODING</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>RUNTIME: PYTHON 3.11</span><br />
          <span>COMPILER STATUS: STABLE</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>CODING AGENT ANALYSIS</span>
          <span>DEV TERMINAL</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Analyzing abstract syntax tree & compiling script...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Project architecture analyzed. 1,805 modules active. The codebase is refactored, decoupled, and compiled with zero errors."}
          </p>
        )}
      </div>

      {/* Main Coding Layout: Code Editor & Terminal */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* File Directory (1 col) */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">WORKSPACE FILES</h3>
          <div className="space-y-2 text-xs hud-font">
            {[
              'server/main.py',
              'server/agents/supervisor.py',
              'server/agents/weather_agent.py',
              'server/graph/builder.py',
              'client/src/App.jsx',
              'client/src/components/Dashboard.jsx'
            ].map((f, i) => (
              <div key={i} className="p-2 border border-[#1E1E1E] bg-black text-[#9A9A9A] hover:border-white hover:text-white transition-all cursor-pointer truncate">
                {f}
              </div>
            ))}
          </div>
        </div>

        {/* Code Editor & Console Output (2 cols) */}
        <div className="md:col-span-2 p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4 flex flex-col justify-between">
          <div className="flex justify-between items-center border-b border-[#1E1E1E] pb-3">
            <div className="flex space-x-2">
              <button
                onClick={() => setActiveTab('editor')}
                className={`px-3 py-1 text-xs hud-font uppercase tracking-wider ${activeTab === 'editor' ? 'border-b-2 border-white text-white font-bold' : 'text-[#9A9A9A]'}`}
              >
                Code Output
              </button>
              <button
                onClick={() => setActiveTab('terminal')}
                className={`px-3 py-1 text-xs hud-font uppercase tracking-wider ${activeTab === 'terminal' ? 'border-b-2 border-white text-white font-bold' : 'text-[#9A9A9A]'}`}
              >
                Terminal Output
              </button>
            </div>
            <span className="hud-font text-[9px] text-[#9A9A9A]">UTF-8 · PYTHON</span>
          </div>

          {activeTab === 'editor' ? (
            <pre className="p-4 border border-[#1E1E1E] bg-black text-xs font-mono text-[#9A9A9A] overflow-x-auto leading-relaxed min-h-[220px]">
              <code className="text-white">{defaultSnippet}</code>
            </pre>
          ) : (
            <div className="p-4 border border-[#1E1E1E] bg-black text-xs font-mono text-[#9A9A9A] min-h-[220px] space-y-1">
              <p className="text-white">$ uvicorn main:app --reload</p>
              <p>INFO: Application startup complete.</p>
              <p>INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)</p>
              <p className="text-white">$ npm run dev</p>
              <p>VITE v5.4.19 ready in 312 ms</p>
            </div>
          )}

          {/* Quick Prompt Input */}
          <form onSubmit={(e) => {
            e.preventDefault();
            if (codePrompt.trim()) {
              onSubmitQuery(`Write python code for: ${codePrompt}`);
              setCodePrompt('');
            }
          }} className="flex space-x-2 pt-2">
            <input
              type="text"
              value={codePrompt}
              onChange={e => setCodePrompt(e.target.value)}
              placeholder="Ask Coding Agent to generate code or debug..."
              className="flex-1 bg-black border border-[#1E1E1E] px-3 py-2 text-xs text-white placeholder-[#9A9A9A] focus:outline-none focus:border-white hud-font"
            />
            <button type="submit" className="px-4 py-2 bg-white text-black font-bold hud-font text-xs uppercase tracking-wider cursor-pointer">
              Generate
            </button>
          </form>

        </div>

      </div>

    </div>
  );
};

export default CodingWorkspace;
