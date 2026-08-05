/**
 * Robot.jsx — Animated SVG robot avatar.
 *
 * State → Visual mapping:
 *   SLEEPING  → Eyes closed, dim blue glow, slow breathing
 *   IDLE      → Eyes open, cyan glow, gentle idle sway
 *   LISTENING → Eyes wide, blue glow, ear pulse rings
 *   THINKING  → Pupils look up-right, amber glow, spinning particles
 *   SPEAKING  → Mouth animates, green glow, voice waves
 *   GREETING  → Eyes happy, purple glow, wave animation
 *   ERROR     → Eyes red, red glow
 */

import { useEffect, useRef } from 'react';
import RobotEyes from './RobotEyes';
import RobotMouth from './RobotMouth';
import './Robot.css';

const STATE_COLORS = {
  SLEEPING: '#1a2540',
  IDLE: '#00d4ff',
  LISTENING: '#0066ff',
  THINKING: '#ff9500',
  SPEAKING: '#00ff88',
  GREETING: '#aa66ff',
  OBSERVING: '#00d4ff',
  ERROR: '#ff3366',
};

export default function Robot({ robotState, emotion, animationCue, onAnimationEnd }) {
  const color = STATE_COLORS[robotState] || STATE_COLORS.IDLE;
  const isSleeping = robotState === 'SLEEPING';
  const isListening = robotState === 'LISTENING';
  const isThinking = robotState === 'THINKING';
  const isSpeaking = robotState === 'SPEAKING' || robotState === 'GREETING';

  return (
    <div
      className={`robot-avatar robot-avatar--${robotState.toLowerCase()}`}
      style={{ '--state-color': color }}
    >
      {/* Outer glow rings */}
      <div className="glow-ring glow-ring--outer" />
      <div className="glow-ring glow-ring--mid" />

      {/* Ear sensors */}
      <div className={`ear ear--left ${isListening ? 'ear--active' : ''}`}>
        <div className="ear-dot" />
        {isListening && <div className="ear-pulse" />}
      </div>
      <div className={`ear ear--right ${isListening ? 'ear--active' : ''}`}>
        <div className="ear-dot" />
        {isListening && <div className="ear-pulse" />}
      </div>

      {/* Main robot head */}
      <div className="robot-head">
        {/* Top antenna */}
        <div className="antenna">
          <div className="antenna-stem" />
          <div className={`antenna-light ${isListening ? 'antenna-light--active' : ''}`} />
        </div>

        {/* Face panel */}
        <div className="robot-face">
          {/* Forehead visor stripe */}
          <div className="forehead-stripe">
            <div className="stripe-line" />
          </div>

          {/* Eyes */}
          <RobotEyes
            robotState={robotState}
            emotion={emotion}
            stateColor={color}
          />

          {/* Nose sensor dot */}
          <div className="nose-sensor">
            <div className="nose-dot" style={{ background: color }} />
          </div>

          {/* Mouth */}
          <RobotMouth
            isSpeaking={isSpeaking}
            isSleeping={isSleeping}
            stateColor={color}
          />
        </div>

        {/* Chin detail */}
        <div className="chin-detail">
          <span className="chin-text">CSE · SURVEX</span>
        </div>
      </div>

      {/* Thinking particles */}
      {isThinking && (
        <div className="thinking-particles">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="particle" style={{ '--i': i }} />
          ))}
        </div>
      )}

      {/* Voice waves when speaking */}
      {isSpeaking && (
        <div className="voice-waves">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="voice-wave" style={{ '--i': i }} />
          ))}
        </div>
      )}
    </div>
  );
}
