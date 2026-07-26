import React, { useState } from 'react';
import { Volume2, VolumeX, Play, Pause, RotateCcw } from 'lucide-react';
import { audioSynth } from '../audio/AudioSynth';

export const AudioControls = ({ muted, toggleMute, lastText = "" }) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePauseResume = () => {
    if (window.speechSynthesis.speaking) {
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
        setIsPlaying(true);
      } else {
        window.speechSynthesis.pause();
        setIsPlaying(false);
      }
    }
  };

  const handleReplay = () => {
    if (lastText && !muted) {
      audioSynth.speak(lastText);
      setIsPlaying(true);
    }
  };

  return (
    <div className="flex items-center space-x-2 border border-[#1E1E1E] bg-[#0A0A0A] px-3 py-1.5 font-sans">
      <span className="hud-font text-[9px] text-[#9A9A9A] uppercase tracking-widest mr-1 hidden sm:inline">
        VOICE CONTROLS
      </span>
      
      <button
        onClick={handleReplay}
        className="p-1 border border-[#1E1E1E] hover:border-white text-[#9A9A9A] hover:text-white transition-all cursor-pointer"
        title="Replay Voice Output"
      >
        <RotateCcw className="w-3.5 h-3.5" />
      </button>

      <button
        onClick={handlePauseResume}
        className="p-1 border border-[#1E1E1E] hover:border-white text-[#9A9A9A] hover:text-white transition-all cursor-pointer"
        title="Pause / Resume Speech"
      >
        {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
      </button>

      <button
        onClick={toggleMute}
        className="p-1 border border-[#1E1E1E] hover:border-white text-[#9A9A9A] hover:text-white transition-all cursor-pointer"
        title={muted ? "Unmute" : "Mute"}
      >
        {muted ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-white" />}
      </button>
    </div>
  );
};

export default AudioControls;
