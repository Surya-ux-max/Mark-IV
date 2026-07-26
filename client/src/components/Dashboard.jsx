import React from 'react';
import { Activity, Mic, Cpu } from 'lucide-react';

/**
 * Clean Conversational Command Center Dashboard.
 * Renders the central reactor and the dynamic voice Q&A subtitle panels.
 */
export const Dashboard = ({ 
  operatorQuery, 
  aiResponse, 
  isTyping,
  micStatus
}) => {
  return (
    <div className="w-full h-full min-h-screen flex flex-col items-center justify-between p-6 max-w-4xl mx-auto z-20 relative select-text">
      
      {/* 1. TOP HEADER */}
      <div className="w-full flex items-center justify-between hud-border p-4 rounded-lg bg-black/60 z-20">
        <div className="flex items-center space-x-2.5">
          <Activity className="w-4 h-4 text-white animate-pulse" />
          <span className="hud-font text-xs font-bold uppercase tracking-widest text-white">SURVEX CORE INJECTOR</span>
        </div>
        <div className="hud-font text-[10px] text-slate-400 uppercase tracking-widest flex items-center space-x-3">
          <span>LOAD: STABLE</span>
          <span className="text-white/20">|</span>
          <span className="text-white">99.87% SYNC</span>
        </div>
      </div>

      {/* 2. CENTER REACTOR INDICATOR (WebGL Canvas mounts in parent behind this) */}
      <div className="flex-1 w-full relative flex items-center justify-center my-6 min-h-[300px]">
        <div className="absolute w-[240px] h-[240px] md:w-[320px] md:h-[320px] rounded-full border border-white/10 flex items-center justify-center pointer-events-none">
          <div className="w-[85%] h-[85%] rounded-full border border-dashed border-white/5 flex items-center justify-center animate-[spin_30s_infinite_linear]" />
          <div className="absolute w-[95%] h-[95%] rounded-full border border-dotted border-white/15 animate-[spin_50s_infinite_reverse_linear]" />
          
          {/* Digital crosshairs */}
          <div className="absolute w-6 h-[1px] bg-white/25 left-0" />
          <div className="absolute w-6 h-[1px] bg-white/25 right-0" />
          <div className="absolute h-6 w-[1px] bg-white/25 top-0" />
          <div className="absolute h-6 w-[1px] bg-white/25 bottom-0" />
        </div>
      </div>

      {/* 3. DYNAMIC CONVERSATIONAL LOG (Operator Q & AI response) */}
      <div className="w-full z-20 flex flex-col space-y-4 animate-[slideUp_0.6s_cubic-bezier(0.16,1,0.3,1)_forwards]">
        
        {/* Dynamic Q&A Panel */}
        <div className="hud-border p-5 rounded-lg bg-black/85 flex flex-col space-y-4 min-h-[160px] justify-center transition-all duration-300">
          
          {/* Operator Query */}
          {operatorQuery ? (
            <div className="flex items-start space-x-3 animate-[fadeIn_0.3s_ease-out]">
              <span className="hud-font text-[10px] bg-white/15 px-2 py-0.5 rounded text-white font-bold flex-shrink-0 mt-0.5">
                OPERATOR
              </span>
              <p className="text-slate-300 text-sm leading-relaxed font-medium">
                "{operatorQuery}"
              </p>
            </div>
          ) : (
            <div className="text-center text-slate-500 text-xs hud-font uppercase tracking-widest py-3 animate-pulse">
              Ask SurveX a question... e.g. "Is the reactor stable?"
            </div>
          )}

          {/* Divider if both exist */}
          {operatorQuery && <div className="border-t border-white/5 w-full" />}

          {/* AI Response */}
          {isTyping ? (
            <div className="flex items-center space-x-2 text-slate-400 hud-font text-xs">
              <Cpu className="w-3.5 h-3.5 text-white animate-spin" />
              <span className="animate-pulse">SurveX is processing neural pathways...</span>
            </div>
          ) : aiResponse ? (
            <div className="flex items-start space-x-3 animate-[fadeIn_0.5s_ease-out]">
              <span className="hud-font text-[10px] bg-white text-black px-2 py-0.5 rounded font-extrabold flex-shrink-0 mt-0.5">
                SURVEX
              </span>
              <p className="text-white text-sm leading-relaxed font-bold glow-text-white">
                {aiResponse}
              </p>
            </div>
          ) : null}
        </div>

        {/* Dynamic Mic Listening Status */}
        <div className="w-full flex items-center justify-center space-x-2 py-2">
          <div className={`w-8 h-8 rounded-full border border-white/10 flex items-center justify-center transition-all ${micStatus === 'LISTENING' ? 'bg-white/5 animate-pulse border-white/30' : ''}`}>
            <Mic className={`w-3.5 h-3.5 ${micStatus === 'LISTENING' ? 'text-white' : 'text-slate-500'}`} />
          </div>
          <span className="hud-font text-[9px] uppercase tracking-[0.25em] text-slate-500 font-bold">
            {micStatus === 'LISTENING' ? 'SYSTEM MIC ACTIVE - LISTENING' : 'VOICE MODE STANDBY'}
          </span>
        </div>

      </div>

    </div>
  );
};
export default Dashboard;
