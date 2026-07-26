import React, { useState } from 'react';
import { Globe, Search as SearchIcon, ExternalLink, ShieldCheck } from 'lucide-react';

export const SearchWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSubmitQuery(`Search online for ${searchQuery}`);
      setSearchQuery('');
    }
  };

  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">NEURAL SEARCH</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>PROVIDER: TAVILY SEARCH API</span><br />
          <span>REAL-TIME WEB FEED</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>TAVILY AGENT SYNTHESIS</span>
          <span>LIVE WEB INDEX</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Gathering neural search results from Tavily API...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Neural search node active. Ready to fetch real-time articles, documentation, and live web intelligence."}
          </p>
        )}
      </div>

      {/* Search Input Bar */}
      <form onSubmit={handleSearch} className="relative w-full">
        <input
          type="text"
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          placeholder="Search the web with Tavily AI engine..."
          className="w-full bg-[#0A0A0A] border border-[#1E1E1E] hover:border-white/30 focus:border-white px-5 py-4 text-sm text-white placeholder-[#9A9A9A] focus:outline-none transition-all hud-font"
        />
        <button
          type="submit"
          className="absolute right-3 top-1/2 -translate-y-1/2 px-5 py-2 bg-white text-black font-bold hud-font text-xs uppercase tracking-wider cursor-pointer hover:bg-slate-200"
        >
          Search
        </button>
      </form>

      {/* Sample Live Web Intelligence Sources */}
      <div className="space-y-4">
        <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">REAL-TIME WEB SOURCES</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { title: 'LangGraph Documentation & Architecture Guide', domain: 'langchain.com', snippet: 'Build language agents as graphs with stateful multi-actor workflows.' },
            { title: 'Tavily Search API for AI Agents', domain: 'tavily.com', snippet: 'Optimized search engine designed specifically for LLMs and autonomous AI agents.' },
            { title: 'Groq Llama 3.1 Instant Speed Benchmarks', domain: 'groq.com', snippet: 'Sub-second latency token streaming with Llama 3.1 8B Instant models.' },
            { title: 'FastAPI Python Framework Docs', domain: 'fastapi.tiangolo.com', snippet: 'High performance asynchronous Web API framework in Python 3.10+.' },
          ].map((item, i) => (
            <div key={i} className="p-5 border border-[#1E1E1E] bg-[#0A0A0A] space-y-2 hover:border-white/40 transition-all">
              <div className="flex justify-between items-center text-[10px] hud-font text-[#9A9A9A] uppercase">
                <span>{item.domain}</span>
                <ExternalLink className="w-3 h-3 text-white" />
              </div>
              <h4 className="font-bold text-white text-sm uppercase">{item.title}</h4>
              <p className="hud-font text-xs text-[#9A9A9A] leading-relaxed">{item.snippet}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default SearchWorkspace;
