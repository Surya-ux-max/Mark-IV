import React from 'react';
import { Cpu, Zap, RefreshCw } from 'lucide-react';

/**
 * Clean minimalist launch screen showing circular soundwave radar and activation controls.
 */
export const InitialScreen = ({ micStatus, enableVoiceControl, launchSystem }) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 z-30 max-w-xl">
      {/* Soundwave Visualizer Radar */}
      <div className="w-28 h-28 rounded-full border border-white/10 flex flex-col items-center justify-center mb-8 relative">
        <div className={`absolute inset-0 rounded-full border ${micStatus === 'LISTENING' ? 'border-white/40 animate-ping' : 'border-white/5'}`} />
        <div className="absolute inset-2 rounded-full border border-white/5 flex items-center justify-center">
          {micStatus === 'LISTENING' ? (
            <div className="flex items-end justify-center space-x-1 h-9">
              <div className="voice-bar voice-bar-1" />
              <div className="voice-bar voice-bar-2" />
              <div className="voice-bar voice-bar-3" />
              <div className="voice-bar voice-bar-4" />
              <div className="voice-bar voice-bar-5" />
            </div>
          ) : micStatus === 'HEARD' ? (
            <Zap className="w-8 h-8 text-white animate-bounce" />
          ) : micStatus === 'AWAITING_PERMISSION' ? (
            <RefreshCw className="w-8 h-8 text-white animate-[spin_2s_infinite_linear]" />
          ) : (
            <Cpu className="w-8 h-8 text-white/50" />
          )}
        </div>
      </div>

      <h1 className="text-4xl md:text-5xl font-light tracking-[0.35em] uppercase text-white mb-3">
        SURVEX <span className="font-extrabold text-white/60">OS</span>
      </h1>
      <p className="hud-font text-[9px] uppercase text-slate-500 tracking-[0.4em] mb-12">
        INTELLIGENT KERNEL INTERFACE
      </p>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full px-4">
        {micStatus === 'STANDBY' && (
          <button 
            onClick={enableVoiceControl}
            className="w-full sm:w-auto px-8 py-4 rounded border-2 border-white text-white hover:bg-white hover:text-black cursor-pointer transition-all duration-300 hud-font text-xs uppercase tracking-[0.25em] font-bold shadow-lg shadow-white/5 active:scale-95 animate-pulse"
          >
            ENABLE VOICE WAKE WORD
          </button>
        )}
        
        <button 
          onClick={launchSystem}
          className="w-full sm:w-auto px-8 py-4 rounded border-2 border-white/20 hover:border-white text-white bg-transparent hover:bg-white/5 cursor-pointer transition-all duration-300 hud-font text-xs uppercase tracking-[0.25em] font-bold active:scale-95"
        >
          INITIALIZE CORE MANUALLY
        </button>
      </div>
    </div>
  );
};
export default InitialScreen;
