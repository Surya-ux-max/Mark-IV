import React, { useState, useEffect, useRef } from 'react';
import { 
  Volume2, VolumeX, RefreshCw, Clock 
} from 'lucide-react';

// Import OOP managers
import { audioSynth } from './audio/AudioSynth';
import { VoiceWakeManager } from './voice/VoiceWakeManager';
import { HologramScene } from './three/HologramScene';

// Import UI components
import { InitialScreen } from './components/InitialScreen';
import { Dashboard } from './components/Dashboard';

// Cinematic phases
const PHASE = {
  INITIAL: 'INITIAL',
  HELMET_ASSEMBLING: 'HELMET_ASSEMBLING',
  HELMET_SCANNING: 'HELMET_SCANNING',
  HELMET_AWAKEN: 'HELMET_AWAKEN',
  HELMET_DISSOLVING: 'HELMET_DISSOLVING',
  DASHBOARD_ACTIVE: 'DASHBOARD_ACTIVE'
};

function App() {
  const [phase, setPhase] = useState(PHASE.INITIAL);
  const [muted, setMuted] = useState(false);
  const [userInteracted, setUserInteracted] = useState(false);
  const [micStatus, setMicStatus] = useState('STANDBY');
  const [maskImage, setMaskImage] = useState(null);

  // Conversational state variables
  const [operatorQuery, setOperatorQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const [voiceFinished, setVoiceFinished] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Dynamic greeting based on time of day
  const getGreetingText = () => {
    const hr = currentTime.getHours();
    if (hr >= 5 && hr < 12) return "Good morning, Surya.";
    if (hr >= 12 && hr < 17) return "Good afternoon, Surya.";
    if (hr >= 17 && hr < 22) return "Good evening, Surya.";
    return "Hello, Surya. Systems active.";
  };
  const greetingText = getGreetingText();

  // OOP Managers references
  const voiceManagerRef = useRef(null);
  const sceneManagerRef = useRef(null);
  const canvasContainerRef = useRef(null);

  // System time clock tick
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Load mask image asset dynamically
  useEffect(() => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = "/mask/image.png";
    img.onload = () => {
      setMaskImage(img);
    };
  }, []);

  // Handle voice commands dynamically
  const handleVoiceCommand = (text) => {
    if (!text.trim()) return;
    
    setOperatorQuery(text);
    setAiResponse('');
    setIsTyping(true);

    let reply = "";
    const query = text.toLowerCase();

    // Context response router
    if (query.includes('who are you') || query.includes('your name') || query.includes('who is this')) {
      reply = "I am SurveX, your cognitive operating system core interface.";
    } else if (query.includes('reactor') || query.includes('core') || query.includes('stable') || query.includes('status')) {
      reply = "The thermonuclear core is operating at 24 million Kelvin. Magnetic fields are fully balanced at 99.87% sync load.";
    } else if (query.includes('analyze') || query.includes('project') || query.includes('code') || query.includes('repository')) {
      reply = "Project architecture analyzed. 1,805 modules active. The file structure is fully refactored, decoupled, and compiled with zero errors.";
    } else if (query.includes('latency') || query.includes('ping') || query.includes('speed')) {
      reply = "Latency is clear at 0.12 milliseconds. High-frequency neural bands are fully calibrated.";
    } else if (query.includes('hello') || query.includes('hi') || query.includes('hey')) {
      reply = "Hello, Surya. Systems are fully loaded and listening. What can I assist you with today?";
    } else if (query.includes('time') || query.includes('date')) {
      const now = new Date();
      reply = `The local host time is currently ${now.toLocaleTimeString(undefined, {hour: '2-digit', minute: '2-digit'})} on ${now.toLocaleDateString(undefined, {weekday: 'long', month: 'long', day: 'numeric'})}.`;
    } else {
      reply = `Analyzing request: "${text}". Running neural query arrays. All cognitive pipelines are stable.`;
    }

    // Delay response to simulate processing typewriter effect
    setTimeout(() => {
      setIsTyping(false);
      setAiResponse(reply);
      if (!muted) {
        audioSynth.speak(reply);
      }
    }, 1000);
  };

  // Handle voice wake word triggers
  const triggerVoiceWake = () => {
    setUserInteracted(true);
    setMicStatus('HEARD');
    if (!muted) {
      audioSynth.playWakeChime();
    }
    // Mute mic immediately during intro to isolate the wake-word
    if (voiceManagerRef.current) {
      voiceManagerRef.current.stop();
    }
    // Launch unified text particles intro instantly
    setTimeout(() => {
      setPhase(PHASE.HELMET_ASSEMBLING);
      if (!muted) {
        audioSynth.startAmbient();
      }
    }, 50);
  };

  // Launch manually via button click
  const launchSystem = () => {
    setUserInteracted(true);
    setPhase(PHASE.HELMET_ASSEMBLING);
    if (!muted) {
      audioSynth.startAmbient();
    }
    // Mute mic during intro
    if (voiceManagerRef.current) {
      voiceManagerRef.current.stop();
    }
  };

  // Explicit voice request activation
  const enableVoiceControl = () => {
    if (voiceManagerRef.current) {
      voiceManagerRef.current.enable();
    }
  };

  const toggleMute = () => {
    setMuted(!muted);
  };

  // Reboot state managers clean
  const rebootSystem = () => {
    window.speechSynthesis.cancel();
    audioSynth.stopAmbient();
    
    if (voiceManagerRef.current) {
      voiceManagerRef.current.stop();
      voiceManagerRef.current.setMode('WAKE');
    }
    if (sceneManagerRef.current) {
      sceneManagerRef.current.destroy();
      sceneManagerRef.current = null;
    }

    setPhase(PHASE.INITIAL);
    setUserInteracted(false);
    setVoiceFinished(false);
    setOperatorQuery('');
    setAiResponse('');
    setIsTyping(false);

    // Reinitialize speech manager
    setTimeout(() => {
      if (voiceManagerRef.current) {
        voiceManagerRef.current.init();
      }
    }, 200);
  };

  // 1. Instantiate OOP Voice Manager on mount
  useEffect(() => {
    const manager = new VoiceWakeManager({
      onListening: () => setMicStatus('LISTENING'),
      onHeard: () => triggerVoiceWake(),
      onStatusChange: (status) => setMicStatus(status),
      onCommand: (text) => handleVoiceCommand(text)
    });
    
    manager.init();
    voiceManagerRef.current = manager;

    return () => {
      if (voiceManagerRef.current) {
        voiceManagerRef.current.stop();
      }
    };
  }, []);

  // 2. Instantiate OOP Three.js HologramScene Manager
  useEffect(() => {
    if (!userInteracted || !canvasContainerRef.current) return;

    const sceneManager = new HologramScene(canvasContainerRef.current, phase, maskImage, greetingText.toUpperCase());
    sceneManagerRef.current = sceneManager;

    return () => {
      if (sceneManagerRef.current) {
        sceneManagerRef.current.destroy();
        sceneManagerRef.current = null;
      }
    };
  }, [userInteracted, maskImage, greetingText]);

  // Sync Phase changes to Three.js manager
  useEffect(() => {
    if (sceneManagerRef.current) {
      sceneManagerRef.current.setPhase(phase);
    }
  }, [phase]);

  // 3. Cinematic Phase Transitions (Unified manual/voice intro)
  useEffect(() => {
    if (phase !== PHASE.HELMET_ASSEMBLING) return;

    // Transition from brand SurveX text -> Greeting text after 4.5s
    const timer1 = setTimeout(() => {
      setPhase(PHASE.HELMET_SCANNING);
    }, 4500);

    return () => clearTimeout(timer1);
  }, [phase]);

  useEffect(() => {
    if (phase !== PHASE.HELMET_SCANNING) return;

    if (!muted) audioSynth.playLaser(2.0);

    // Transition from morph to vocal greetings trigger after 3s
    const timer2 = setTimeout(() => {
      setPhase(PHASE.HELMET_AWAKEN);
    }, 3000);

    return () => clearTimeout(timer2);
  }, [phase]);

  useEffect(() => {
    if (phase !== PHASE.HELMET_AWAKEN) return;

    if (!muted) {
      audioSynth.speak(greetingText + " All systems are online.", () => setVoiceFinished(true));
    } else {
      const timer3 = setTimeout(() => setVoiceFinished(true), 2500);
      return () => clearTimeout(timer3);
    }
  }, [phase, greetingText]);

  // Trigger dissolve into AI core after greeting ends
  useEffect(() => {
    if (voiceFinished && phase === PHASE.HELMET_AWAKEN) {
      setPhase(PHASE.HELMET_DISSOLVING);
    }
  }, [voiceFinished, phase]);

  // Dissolve to active dashboard
  useEffect(() => {
    if (phase === PHASE.HELMET_DISSOLVING) {
      const timer4 = setTimeout(() => {
        setPhase(PHASE.DASHBOARD_ACTIVE);
        // Force command mode on voice manager
        if (voiceManagerRef.current) {
          voiceManagerRef.current.setMode('COMMAND');
          voiceManagerRef.current.startListeningDirectly();
        }
      }, 2500);
      return () => clearTimeout(timer4);
    }
  }, [phase]);

  return (
    <div className="relative min-h-screen w-screen bg-black text-white overflow-hidden holo-scanlines select-none font-sans flex flex-col">
      {/* Background Subtle Grid */}
      <div className="absolute inset-0 cyber-grid opacity-25 pointer-events-none z-0" />

      {/* Streaming futuristic lines */}
      {phase === PHASE.DASHBOARD_ACTIVE && (
        <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
          <div className="absolute left-[15%] top-0 w-[1px] h-full bg-gradient-to-b from-transparent via-white/10 to-transparent animate-[sweepVertical_12s_infinite_linear]" />
          <div className="absolute left-[80%] top-0 w-[1px] h-full bg-gradient-to-b from-transparent via-white/10 to-transparent animate-[sweepVertical_8s_infinite_linear]" />
          <div className="absolute top-[25%] left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent animate-[sweepHorizontal_10s_infinite_linear]" />
        </div>
      )}

      {/* Status Bar */}
      <header className="relative z-50 flex items-center justify-between px-6 py-4 border-b border-white/5 bg-black/60 backdrop-blur-md font-sans">
        <div className="flex items-center space-x-3">
          <div className="relative flex items-center justify-center w-5 h-5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-white opacity-75 animate-ping"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-white"></span>
          </div>
          <span className="hud-font tracking-[0.25em] text-xs font-bold uppercase text-slate-400">
            SURVEX // COGNITIVE PLATFORM OS
          </span>
        </div>

        {/* Global Utilities */}
        <div className="flex items-center space-x-6 font-sans">
          <div className="hud-font text-[10px] text-slate-400 uppercase tracking-widest hidden sm:flex items-center space-x-2">
            <Clock className="w-3.5 h-3.5 text-white mr-1" />
            <span>{currentTime.toLocaleTimeString()}</span>
            <span className="mx-2 text-white/10">|</span>
            <span>SYSTEM: ONLINE</span>
          </div>

          <div className="flex items-center space-x-2">
            <button 
              onClick={toggleMute}
              className="p-1.5 rounded border border-white/10 bg-white/5 hover:border-white/30 hover:text-white transition-all cursor-pointer"
              title={muted ? "Unmute sounds" : "Mute sounds"}
            >
              {muted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>
            
            {phase !== PHASE.INITIAL && (
              <button 
                onClick={rebootSystem}
                className="p-1.5 rounded border border-white/10 bg-white/5 hover:border-white/30 hover:text-white transition-all cursor-pointer flex items-center space-x-1 hud-font text-[10px] uppercase font-bold tracking-wider"
              >
                <RefreshCw className="w-3.5 h-3.5 animate-[spin_4s_infinite_linear]" />
                <span className="hidden md:inline">REBOOT</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main stage canvas container */}
      <main className="relative flex-1 w-full flex items-center justify-center z-10">

        {/* PHASE 1: INITIAL MIC & MANUAL CONTROL SCREEN */}
        {phase === PHASE.INITIAL && (
          <InitialScreen 
            micStatus={micStatus} 
            enableVoiceControl={enableVoiceControl} 
            launchSystem={launchSystem} 
          />
        )}

        {/* 3D WEBGL HOLOGRAPHIC CANVAS CONTAINER */}
        {userInteracted && (
          <div className="absolute inset-0 w-full h-full z-10 pointer-events-none">
            <div ref={canvasContainerRef} className="w-full h-full pointer-events-auto" />
          </div>
        )}

        {/* DISSOLVED TRANSITION */}
        {phase === PHASE.HELMET_DISSOLVING && (
          <div className="absolute bottom-12 left-1/2 -translate-x-1/2 text-center z-20 hud-font text-xs text-slate-400 uppercase tracking-[0.3em] animate-pulse">
            Projecting central core reactor dashboard...
          </div>
        )}

        {/* FINAL CYBERSECURITY COMMAND CENTER DASHBOARD */}
        {phase === PHASE.DASHBOARD_ACTIVE && (
          <Dashboard 
            operatorQuery={operatorQuery}
            aiResponse={aiResponse}
            isTyping={isTyping}
            micStatus={micStatus}
          />
        )}

      </main>

      {/* Footer information details */}
      <footer className="relative z-50 py-3 px-6 border-t border-white/5 bg-black/60 backdrop-blur-md flex flex-col md:flex-row items-center justify-between text-slate-500 text-[10px] uppercase tracking-widest font-sans">
        <div className="flex items-center space-x-2 mb-2 md:mb-0">
          <span>OPERATOR: <span className="text-white font-semibold">SURYA</span></span>
          <span className="text-white/10">|</span>
          <span>LOCATION: <span className="text-white font-semibold">WORKSPACE_HOST</span></span>
        </div>
        <div className="flex items-center space-x-4">
          <span>SURVEX COGNITIVE CORE [ACTIVE]</span>
          <span className="text-white/10">|</span>
          <span>© 2026 SURVEX OS INC. ALL SYSTEMS ACTIVE.</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
