/**
 * RobotMouth.jsx — Animated mouth component.
 *
 * States:
 *  isSpeaking → Animated talking mouth
 *  isSleeping → Small closed "resting" line
 *  default   → Neutral slight curve
 */

import './RobotMouth.css';

export default function RobotMouth({ isSpeaking, isSleeping, stateColor }) {
  return (
    <div className={`mouth-container ${isSpeaking ? 'mouth-speaking' : ''} ${isSleeping ? 'mouth-sleeping' : ''}`}>
      {isSpeaking ? (
        /* Talking animation — bars of varying height */
        <div className="mouth-talking">
          {[...Array(7)].map((_, i) => (
            <div
              key={i}
              className="mouth-bar"
              style={{
                '--i': i,
                '--color': stateColor,
                animationDelay: `${i * 0.07}s`,
              }}
            />
          ))}
        </div>
      ) : isSleeping ? (
        /* Sleep — thin line */
        <div className="mouth-line mouth-line--sleep" style={{ background: stateColor }} />
      ) : (
        /* Default neutral smile */
        <svg
          width="60"
          height="20"
          viewBox="0 0 60 20"
          className="mouth-smile"
        >
          <path
            d="M 8 6 Q 30 18 52 6"
            stroke={stateColor}
            strokeWidth="2.5"
            fill="none"
            strokeLinecap="round"
            opacity="0.7"
          />
        </svg>
      )}
    </div>
  );
}
