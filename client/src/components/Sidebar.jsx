import React from 'react';
import { 
  Home, GitBranch, CloudSun, Globe, Calendar, Mail, 
  Brain, Cpu, Terminal, Settings, History 
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'home', label: 'HOME', icon: Home },
  { id: 'github', label: 'GITHUB', icon: GitBranch },
  { id: 'weather', label: 'WEATHER', icon: CloudSun },
  { id: 'search', label: 'SEARCH', icon: Globe },
  { id: 'calendar', label: 'CALENDAR', icon: Calendar },
  { id: 'email', label: 'EMAIL', icon: Mail },
  { id: 'coding', label: 'CODING', icon: Terminal },
  { id: 'browser', label: 'BROWSER', icon: Cpu },
  { id: 'memory', label: 'MEMORY', icon: Brain },
  { id: 'system', label: 'SYSTEM', icon: Cpu },
  { id: 'settings', label: 'SETTINGS', icon: Settings },
];

export const Sidebar = ({ activeTab, onSelectTab, onToggleMemory, memoryCount = 0 }) => {
  return (
    <aside className="w-[200px] flex-shrink-0 h-screen bg-[#0A0A0A] border-r border-[#1E1E1E] flex flex-col justify-between select-none z-30 font-sans">
      
      {/* Top Branding Header */}
      <div>
        <div className="p-5 border-b border-[#1E1E1E]">
          <div className="flex items-center space-x-2">
            <div className="w-2.5 h-2.5 bg-white rounded-full animate-pulse" />
            <span className="hud-font font-bold text-xs uppercase tracking-[0.2em] text-white">
              SURVEX OS
            </span>
          </div>
          <p className="hud-font text-[8px] text-[#9A9A9A] uppercase tracking-widest mt-1">
            COGNITIVE PLATFORM
          </p>
        </div>

        {/* Navigation Items List */}
        <nav className="p-3 space-y-1">
          {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
            const isActive = activeTab === id;
            return (
              <button
                key={id}
                onClick={() => onSelectTab(id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-none text-[11px] hud-font font-bold tracking-widest uppercase transition-all duration-150 cursor-pointer ${
                  isActive
                    ? 'border-l-2 border-white bg-white/10 text-white shadow-inner'
                    : 'border-l-2 border-transparent text-[#9A9A9A] hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-[#9A9A9A]'}`} />
                <span>{label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Memory Drawer Trigger */}
      <div className="p-3 border-t border-[#1E1E1E] space-y-2">
        <button
          onClick={onToggleMemory}
          className="w-full flex items-center justify-between px-3 py-2.5 border border-[#1E1E1E] bg-black hover:border-white text-white text-[10px] hud-font uppercase font-bold tracking-wider transition-all cursor-pointer group"
        >
          <div className="flex items-center space-x-2">
            <History className="w-3.5 h-3.5 text-[#9A9A9A] group-hover:text-white transition-colors" />
            <span>SESSION MEMORY</span>
          </div>
          {memoryCount > 0 && (
            <span className="bg-white/20 px-1.5 py-0.5 text-[8px] rounded text-white">
              {memoryCount}
            </span>
          )}
        </button>
      </div>

    </aside>
  );
};

export default Sidebar;
