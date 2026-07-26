import React from 'react';
import { GitBranch, GitCommit, GitPullRequest, AlertCircle, Bell } from 'lucide-react';

export const GitHubWorkspace = ({ aiResponse, isTyping, onSubmitQuery }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SPECIALIZED AGENT WORKSPACE</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">GITHUB</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>CONNECTED: GITHUB API</span><br />
          <span>STATUS: SYNCED</span>
        </div>
      </div>

      {/* Voice + Text Output Box */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
          <span>GITHUB AGENT SUMMARY</span>
          <span>BRANCH ENGINE</span>
        </div>
        {isTyping ? (
          <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
            Querying GitHub REST API & active repository commits...
          </p>
        ) : (
          <p className="text-xl md:text-2xl font-semibold leading-relaxed text-white">
            {aiResponse || "Repository 'SurveX-mark IV' active on branch 'main'. 14 recent commits verified cleanly."}
          </p>
        )}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'ACTIVE REPOSITORIES', val: '12', icon: GitBranch },
          { label: 'TOTAL COMMITS', val: '1,428', icon: GitCommit },
          { label: 'OPEN PULL REQUESTS', val: '3', icon: GitPullRequest },
          { label: 'PENDING ISSUES', val: '0', icon: AlertCircle },
        ].map((item, idx) => (
          <div key={idx} className="p-5 border border-[#1E1E1E] bg-[#0A0A0A] flex flex-col justify-between space-y-3">
            <div className="flex items-center justify-between text-[#9A9A9A] hud-font text-xs uppercase">
              <span>{item.label}</span>
              <item.icon className="w-4 h-4 text-white" />
            </div>
            <p className="text-3xl font-extrabold text-white">{item.val}</p>
          </div>
        ))}
      </div>

      {/* Main Grid: Repositories & Commits */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Active Repositories */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">REPOSITORIES</h3>
          <div className="space-y-3">
            {[
              { name: 'SurveX-mark IV', lang: 'Python / React', branch: 'main', updated: '2m ago' },
              { name: 'LangGraph-Supervisor-Core', lang: 'Python', branch: 'main', updated: '1h ago' },
              { name: 'Tavily-Neural-Search-Adapter', lang: 'JavaScript', branch: 'master', updated: '1d ago' },
            ].map((repo, i) => (
              <div key={i} className="p-4 border border-[#1E1E1E] bg-black flex justify-between items-center hover:border-white/40 transition-all">
                <div>
                  <h4 className="font-bold text-white uppercase text-sm">{repo.name}</h4>
                  <p className="hud-font text-[10px] text-[#9A9A9A] uppercase mt-1">{repo.lang} · Branch: {repo.branch}</p>
                </div>
                <span className="hud-font text-[9px] text-[#9A9A9A] uppercase">{repo.updated}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Commit History */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">RECENT COMMITS</h3>
          <div className="space-y-3">
            {[
              { msg: 'Migrate to llama-3.1-8b-instant and update supervisor', hash: 'a8f4c12', time: '10m ago' },
              { msg: 'Implement Tavily web search agent node in LangGraph', hash: 'c92d4ee', time: '2h ago' },
              { msg: 'Refactor calendar and email database CRUD procedures', hash: 'f102a99', time: '5h ago' },
            ].map((commit, i) => (
              <div key={i} className="p-3 border border-[#1E1E1E] bg-black flex justify-between items-start space-x-3">
                <div>
                  <p className="text-xs text-white font-medium">{commit.msg}</p>
                  <p className="hud-font text-[9px] text-[#9A9A9A] uppercase mt-1">HASH: {commit.hash}</p>
                </div>
                <span className="hud-font text-[9px] text-[#9A9A9A] uppercase whitespace-nowrap">{commit.time}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Suggested Actions */}
      <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-3">
        <h4 className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">SUGGESTED GITHUB COMMANDS</h4>
        <div className="flex flex-wrap gap-2">
          {["Check open pull requests", "List latest commits on main", "Show repository status", "Search GitHub for LangGraph"].map((q, i) => (
            <button
              key={i}
              onClick={() => onSubmitQuery(q)}
              className="px-3 py-1.5 border border-[#1E1E1E] hover:border-white text-xs hud-font uppercase text-[#9A9A9A] hover:text-white transition-all cursor-pointer"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

    </div>
  );
};

export default GitHubWorkspace;
