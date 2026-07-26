import React from 'react';
import { Settings, Volume2, Sliders, Shield } from 'lucide-react';

export const SettingsWorkspace = ({ muted, toggleMute }) => {
  return (
    <div className="w-full h-full p-8 max-w-6xl mx-auto space-y-8 select-text font-sans text-white">
      
      {/* Header */}
      <div className="border-b border-[#1E1E1E] pb-4 flex justify-between items-end">
        <div>
          <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-[0.25em]">SYSTEM CONFIGURATION</span>
          <h1 className="hud-font text-4xl font-extrabold uppercase tracking-wider text-white mt-1">SETTINGS</h1>
        </div>
        <div className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest text-right">
          <span>SURVEX OS v4.0</span><br />
          <span>CONFIG FILE: LOCAL ENV</span>
        </div>
      </div>

      {/* Settings Options */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Audio Synth Preferences */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">AUDIO SYNTHESIS & VOICE OUTPUT</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 border border-[#1E1E1E] bg-black">
              <div>
                <p className="text-xs font-bold text-white uppercase">Voice Response Output</p>
                <p className="hud-font text-[10px] text-[#9A9A9A]">Speak AI responses simultaneously with text display</p>
              </div>
              <button
                onClick={toggleMute}
                className="px-4 py-2 border border-white text-xs hud-font uppercase font-bold text-white bg-white/10 hover:bg-white hover:text-black transition-all"
              >
                {muted ? 'MUTED' : 'ACTIVE'}
              </button>
            </div>
          </div>
        </div>

        {/* Neural LLM Configuration */}
        <div className="p-6 border border-[#1E1E1E] bg-[#0A0A0A] space-y-4">
          <h3 className="hud-font text-xs text-white font-bold uppercase tracking-widest">NEURAL LLM CONFIGURATION</h3>
          <div className="space-y-3 hud-font text-xs">
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">PRIMARY LLM</span>
              <span className="text-white font-bold">Groq / llama-3.1-8b-instant</span>
            </div>
            <div className="p-3 border border-[#1E1E1E] bg-black flex justify-between">
              <span className="text-[#9A9A9A]">TEMPERATURE</span>
              <span className="text-white font-bold">0.7 (Conversational) / 0.1 (Routing)</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};

export default SettingsWorkspace;
