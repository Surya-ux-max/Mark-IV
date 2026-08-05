/**
 * RobotEyes.jsx — Animated eyes component.
 *
 * States:
 *  SLEEPING  → Closed (horizontal lines)
 *  THINKING  → Pupils look up-right
 *  LISTENING → Wide/enlarged pupils
 *  SPEAKING  → Normal, slight squint
 *  IDLE      → Normal, with blink animation
 */

import './RobotEyes.css';

const EYE_CONFIGS = {
  SLEEPING: { closed: true, pupilSize: 0, squint: false },
  IDLE: { closed: false, pupilSize: 12, squint: false },
  LISTENING: { closed: false, pupilSize: 16, squint: false },
  THINKING: { closed: false, pupilSize: 10, squint: false, lookUp: true },
  SPEAKING: { closed: false, pupilSize: 11, squint: true },
  GREETING: { closed: false, pupilSize: 14, squint: true, happy: true },
  OBSERVING: { closed: false, pupilSize: 14, squint: false },
  ERROR: { closed: false, pupilSize: 8, squint: false },
};

function Eye({ config, stateColor, side }) {
  const { closed, pupilSize, squint, lookUp, happy } = config;
  const pupilOffset = lookUp ? { transform: 'translateY(-4px)' } : {};
  const happyOffset = side === 'left'
    ? { borderRadius: '50% 50% 40% 60%' }
    : { borderRadius: '50% 50% 60% 40%' };

  return (
    <div className={`eye-socket ${closed ? 'eye-socket--closed' : ''} ${squint ? 'eye-socket--squint' : ''}`}>
      {closed ? (
        <div className="eye-closed-line" style={{ background: stateColor }} />
      ) : (
        <>
          <div
            className={`eye-lens ${lookUp ? 'eye-lens--up' : ''}`}
            style={{
              ...(happy ? happyOffset : {}),
              borderColor: `${stateColor}40`,
            }}
          >
            <div
              className="pupil"
              style={{
                width: pupilSize,
                height: pupilSize,
                background: stateColor,
                boxShadow: `0 0 ${pupilSize}px ${stateColor}`,
                ...pupilOffset,
              }}
            />
            <div className="pupil-glint" />
          </div>
          {/* Scan line effect */}
          <div className="eye-scanline" style={{ borderColor: `${stateColor}20` }} />
        </>
      )}
    </div>
  );
}

export default function RobotEyes({ robotState, emotion, stateColor }) {
  const config = EYE_CONFIGS[robotState] || EYE_CONFIGS.IDLE;

  return (
    <div className={`eyes-row ${config.closed ? '' : 'eyes-row--blink'}`}>
      <Eye config={config} stateColor={stateColor} side="left" />
      <Eye config={config} stateColor={stateColor} side="right" />
    </div>
  );
}
