import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Send, History, Volume2, ArrowRight, Terminal } from 'lucide-react';
import MemoryDrawer from './MemoryDrawer';
import AudioControls from './AudioControls';

/**
 * Typewriter Text Component
 * Simulates a smooth character-by-character typewriter streaming effect
 * with a terminal cursor and clean, readable OS typography.
 */
const TypewriterOutput = ({ fullText, cleanTrace = [] }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isDone, setIsDone] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (!fullText) {
      setDisplayedText('');
      setIsDone(true);
      return;
    }

    setDisplayedText('');
    setIsDone(false);

    let currentIndex = 0;
    const stepLength = Math.max(1, Math.floor(fullText.length / 80));
    const intervalTime = 12;

    const timer = setInterval(() => {
      currentIndex += stepLength;
      if (currentIndex >= fullText.length) {
        setDisplayedText(fullText);
        setIsDone(true);
        clearInterval(timer);
      } else {
        setDisplayedText(fullText.slice(0, currentIndex));
      }
    }, intervalTime);

    return () => clearInterval(timer);
  }, [fullText]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [displayedText]);

  return (
    <div className="w-full max-w-2xl border border-[#1E1E1E] bg-[#0A0A0A] p-6 text-left shadow-2xl space-y-4 animate-[fadeIn_0.3s_ease-out]">
      <div className="flex justify-between items-center border-b border-[#1E1E1E] pb-2 text-[9px] hud-font text-[#9A9A9A] uppercase tracking-widest">
        <div className="flex items-center space-x-2">
          <Terminal className="w-3 h-3 text-white" />
          <span>SURVEX COGNITIVE OUTPUT</span>
        </div>
        {cleanTrace.length > 0 && (
          <div className="flex items-center space-x-1">
            <span>VIA:</span>
            {cleanTrace.map((ag, i) => (
              <span key={i} className="text-white font-bold bg-black border border-[#1E1E1E] px-1.5 py-0.5">
                {ag.replace('_', ' ').toUpperCase()}
              </span>
            ))}
          </div>
        )}
      </div>

      <div 
        ref={scrollRef}
        className="max-h-[320px] overflow-y-auto pr-2 scrollbar-thin text-sm md:text-base text-white leading-relaxed font-sans whitespace-pre-wrap tracking-wide"
      >
        {displayedText}
        {!isDone && (
          <span className="inline-block w-2 h-4 bg-white ml-1 align-middle animate-pulse" />
        )}
      </div>
    </div>
  );
};

export const Dashboard = ({
  operatorQuery,
  aiResponse,
  isTyping,
  micStatus,
  agentTrace = [],
  conversations = [],
  systemMetrics = { latency: "0.12s" },
  muted = false,
  toggleMute,
  onSubmitText,
  onSubmitVoice
}) => {
  const [mode, setMode] = useState('text');
  const [inputText, setInputText] = useState('');
  const [memoryDrawerOpen, setMemoryDrawerOpen] = useState(false);
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

  const cleanTrace = agentTrace.filter(a => a !== 'local_fallback' && a !== 'supervisor');

  return (
    <div className="w-full h-full bg-[#000000] text-white flex flex-col justify-between font-sans select-text relative">
      
      {/* Top Controls Strip */}
      <div className="w-full px-8 pt-4 flex justify-between items-center z-20">
        <div className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-widest">
          OPERATOR SESSION ACTIVE
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setMemoryDrawerOpen(true)}
            className="px-3 py-1.5 border border-[#1E1E1E] bg-black hover:border-white text-white text-[10px] hud-font uppercase font-bold tracking-wider transition-all flex items-center space-x-2 cursor-pointer"
          >
            <History className="w-3.5 h-3.5 text-[#9A9A9A]" />
            <span>SESSION MEMORY ({conversations.length})</span>
          </button>
          <AudioControls muted={muted} toggleMute={toggleMute} lastText={aiResponse} />
        </div>
      </div>

      {/* Main Center Area — Typewriter Streaming Output & Placeholder Input Below */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-4 max-w-4xl mx-auto w-full my-auto space-y-8">
        
        {/* CENTER TYPEWRITER STREAMING DISPLAY */}
        <div className="w-full flex flex-col items-center justify-center min-h-[200px]">
          {isTyping ? (
            <div className="flex flex-col items-center space-y-3">
              <div className="flex space-x-1.5 items-end">
                {[0, 1, 2, 3, 4].map(i => (
                  <div
                    key={i}
                    className="w-0.5 bg-white/70 rounded-full animate-[bounce_1s_ease-in-out_infinite]"
                    style={{ height: `${12 + (i % 3) * 8}px`, animationDelay: `${i * 0.1}s` }}
                  />
                ))}
              </div>
              <p className="hud-font text-xs text-[#9A9A9A] uppercase tracking-widest animate-pulse">
                SurveX is processing your request...
              </p>
            </div>
          ) : aiResponse ? (
            <TypewriterOutput fullText={aiResponse} cleanTrace={cleanTrace} />
          ) : (
            <div className="space-y-2 text-center">
              <h1 className="hud-font text-3xl md:text-5xl font-extrabold text-white tracking-wider uppercase">
                How can I help?
              </h1>
              <p className="hud-font text-xs text-[#9A9A9A] tracking-widest uppercase">
                Awaiting command or query from operator
              </p>
            </div>
          )}
        </div>

        {/* MIDDLE BELOW INPUT PLACEHOLDER & MODE TOGGLE */}
        <div className="w-full max-w-2xl space-y-4">
          
          {/* TEXT MODE INPUT */}
          {mode === 'text' && (
            <form onSubmit={handleFormSubmit} className="relative w-full">
              <input
                type="text"
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                placeholder="Type a command or ask a question..."
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

          {/* MODE TOGGLE BUTTONS */}
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

      </main>

      {/* Slide-out Session Memory Drawer */}
      <MemoryDrawer
        isOpen={memoryDrawerOpen}
        onClose={() => setMemoryDrawerOpen(false)}
        conversations={conversations}
      />

    </div>
  );
};

export default Dashboard;
