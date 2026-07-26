import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Send, Volume2, ArrowRight } from 'lucide-react';

const AGENT_BUTTONS = [
  { id: 'github', label: 'GITHUB', desc: 'Code Repositories & Commits' },
  { id: 'weather', label: 'WEATHER', desc: 'Forecast & Radar Metrics' },
  { id: 'search', label: 'SEARCH', desc: 'Tavily Neural Web Search' },
  { id: 'coding', label: 'CODING', desc: 'Scripts & Debug Terminal' },
  { id: 'memory', label: 'MEMORY', desc: 'Context & Profile Recall' },
  { id: 'email', label: 'EMAIL', desc: 'SMTP Inbox & Composition' },
  { id: 'calendar', label: 'CALENDAR', desc: 'Events & Agenda Schedule' },
  { id: 'system', label: 'SYSTEM', desc: 'OS Metrics & LangGraph Trace' },
  { id: 'browser', label: 'BROWSER', desc: 'Automation & Cache Cleaner' },
];

export const HomeWorkspace = ({
  operatorQuery,
  aiResponse,
  isTyping,
  micStatus,
  systemMetrics,
  onSubmitText,
  onSubmitVoice,
  onSelectAgent
}) => {
  const [mode, setMode] = useState('text'); // 'text' | 'voice'
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim()) {
      onSubmitText(inputText.trim());
      setInputText('');
    }
  };

  const startVoiceRecording = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch (_) {}
    }
    const rec = new SR();
    rec.lang = 'en-US';
    rec.continuous = false;
    rec.interimResults = true;

    rec.onstart = () => { setIsListening(true); setTranscript(''); };

    rec.onresult = (e) => {
      let interim = '', final = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        e.results[i].isFinal ? (final += t) : (interim += t);
      }
      setTranscript(final || interim);
    };

    rec.onend = () => {
      setIsListening(false);
      setTranscript(prev => {
        if (prev.trim()) {
          onSubmitVoice ? onSubmitVoice(prev.trim()) : onSubmitText(prev.trim());
        }
        return '';
      });
    };

    rec.onerror = () => { setIsListening(false); setTranscript(''); };

    recognitionRef.current = rec;
    rec.start();
  };

  const stopVoiceRecording = () => {
    try { recognitionRef.current?.stop(); } catch (_) {}
    setIsListening(false);
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between px-6 py-10 max-w-5xl mx-auto min-h-[calc(100vh-80px)] select-text font-sans">
      
      {/* Top Banner / Core Status */}
      <div className="w-full flex justify-between items-center text-[9px] hud-font text-slate-500 uppercase tracking-widest border-b border-[#1E1E1E] pb-3">
        <span>SURVEX COGNITIVE PLATFORM OS</span>
        <span>SUPERVISOR ROUTER: ACTIVE</span>
      </div>

      {/* Main Command Center Header & Input */}
      <div className="w-full max-w-2xl flex flex-col items-center text-center space-y-8 my-auto py-8">
        
        {/* Large Prompt Header */}
        <div className="space-y-2">
          <h1 className="hud-font text-3xl md:text-5xl font-extrabold text-white tracking-wider uppercase">
            How can I help?
          </h1>
          <p className="hud-font text-xs text-[#9A9A9A] tracking-widest uppercase">
            Type or speak a command to activate specialized agent workspaces
          </p>
        </div>

        {/* AI Output Box (if response is active) */}
        {(aiResponse || isTyping) && (
          <div className="w-full p-6 border border-[#1E1E1E] bg-[#0A0A0A] text-left space-y-3 animate-[fadeIn_0.3s_ease-out]">
            <div className="flex justify-between items-center text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
              <span>SURVEX OUTPUT</span>
              <span>{systemMetrics?.latency || '0.12s'}</span>
            </div>
            {isTyping ? (
              <p className="hud-font text-sm text-slate-400 animate-pulse uppercase tracking-widest">
                Analyzing intent and running agent graph...
              </p>
            ) : (
              <p className="text-white text-base font-medium leading-relaxed">
                {aiResponse}
              </p>
            )}
          </div>
        )}

        {/* Input Container */}
        <div className="w-full space-y-4">
          
          {/* TEXT MODE INPUT */}
          {mode === 'text' && (
            <form onSubmit={handleFormSubmit} className="relative w-full">
              <input
                type="text"
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                placeholder="Type something..."
                autoFocus
                className="w-full bg-[#0A0A0A] border border-[#1E1E1E] hover:border-white/30 focus:border-white px-5 py-4 text-sm text-white placeholder-[#9A9A9A] focus:outline-none transition-all hud-font font-medium tracking-wide shadow-inner"
              />
              <button
                type="submit"
                disabled={!inputText.trim()}
                className="absolute right-3 top-1/2 -translate-y-1/2 px-4 py-2 bg-white text-black hover:bg-slate-200 disabled:opacity-30 disabled:hover:bg-white text-xs hud-font font-bold uppercase tracking-wider transition-all cursor-pointer flex items-center space-x-1"
              >
                <span>Execute</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </form>
          )}

          {/* VOICE MODE INPUT */}
          {mode === 'voice' && (
            <div className="w-full p-6 border border-[#1E1E1E] bg-[#0A0A0A] flex flex-col items-center space-y-4">
              <button
                onClick={() => isListening ? stopVoiceRecording() : startVoiceRecording()}
                className={`w-16 h-16 rounded-full border-2 flex items-center justify-center transition-all cursor-pointer ${
                  isListening
                    ? 'border-white bg-white/20 animate-pulse'
                    : 'border-[#1E1E1E] bg-black hover:border-white hover:bg-white/10'
                }`}
              >
                {isListening ? <Mic className="w-7 h-7 text-white" /> : <MicOff className="w-7 h-7 text-[#9A9A9A]" />}
              </button>
              <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest">
                {isListening ? (transcript || "Listening to your voice...") : "Click microphone to speak"}
              </p>
            </div>
          )}

          {/* Mode Switcher Toggle */}
          <div className="flex justify-center items-center space-x-2">
            <button
              onClick={() => setMode('text')}
              className={`px-4 py-1.5 border text-[10px] hud-font uppercase tracking-widest font-bold transition-all cursor-pointer ${
                mode === 'text'
                  ? 'border-white bg-white text-black'
                  : 'border-[#1E1E1E] text-[#9A9A9A] hover:border-white/40 hover:text-white'
              }`}
            >
              Text Mode
            </button>
            <button
              onClick={() => setMode('voice')}
              className={`px-4 py-1.5 border text-[10px] hud-font uppercase tracking-widest font-bold transition-all cursor-pointer ${
                mode === 'voice'
                  ? 'border-white bg-white text-black'
                  : 'border-[#1E1E1E] text-[#9A9A9A] hover:border-white/40 hover:text-white'
              }`}
            >
              Voice Mode
            </button>
          </div>

        </div>

      </div>

      {/* Bottom Minimal Agent Buttons */}
      <div className="w-full space-y-3 pt-6 border-t border-[#1E1E1E]">
        <div className="flex justify-between items-center text-[9px] hud-font text-slate-500 uppercase tracking-widest">
          <span>SPECIALIZED AGENT WORKSPACES</span>
          <span>SELECT TO DIRECTLY SWITCH WORKSPACE</span>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-9 gap-2">
          {AGENT_BUTTONS.map(({ id, label }) => (
            <button
              key={id}
              onClick={() => onSelectAgent(id)}
              className="py-3 px-2 border border-[#1E1E1E] bg-[#0A0A0A] hover:border-white hover:bg-white/5 text-white hud-font text-xs font-bold uppercase tracking-wider text-center transition-all duration-200 cursor-pointer active:scale-95 group"
            >
              <span className="group-hover:tracking-widest transition-all">{label}</span>
            </button>
          ))}
        </div>
      </div>

    </div>
  );
};

export default HomeWorkspace;
