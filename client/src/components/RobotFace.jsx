/**
 * RobotFace.jsx — CSE Brain Face & Expression Display
 *
 * Dedicated Face-Only Component:
 * - Focuses 100% on facial expressions, eye emotions, and voice feedback.
 * - Eliminates body/torso/arms/legs.
 * - Large, crisp OLED screen with cyan digital eyes, independent eyebrows,
 *   camera dot, mouth display (SVG curves & 11-bar equalizer), and headphone ears.
 */

import { useEffect, useRef, useState } from 'react';
import './RobotFace.css';

/* ── State themes ───────────────────────────────────────────── */
const THEMES = {
  SLEEPING:  { c: '#3a5090', g: 'rgba(58,80,144,0.45)',  dim: 0.65, label: 'SLEEPING'  },
  IDLE:      { c: '#00e5ff', g: 'rgba(0,229,255,0.55)',  dim: 1.0,  label: 'STANDBY'   },
  LISTENING: { c: '#5599ff', g: 'rgba(85,153,255,0.65)', dim: 1.0,  label: 'LISTENING' },
  THINKING:  { c: '#ffbb00', g: 'rgba(255,187,0,0.6)',   dim: 1.0,  label: 'PROCESSING'},
  SPEAKING:  { c: '#00ffaa', g: 'rgba(0,255,170,0.6)',   dim: 1.0,  label: 'SPEAKING'  },
  GREETING:  { c: '#cc77ff', g: 'rgba(204,119,255,0.6)', dim: 1.0,  label: 'GREETING'  },
  OBSERVING: { c: '#00e5ff', g: 'rgba(0,229,255,0.5)',   dim: 1.0,  label: 'OBSERVING' },
  ERROR:     { c: '#ff4455', g: 'rgba(255,68,85,0.6)',   dim: 1.0,  label: 'ERROR'     },
};

/* ── Eye expressions ────────────────────────────────────────── */
const EYE_EXPR = {
  normal:      { h: 1.00, pupilY: 0,   browLift: 0,   browAngle: 0,  innerGlow: 0.85 },
  happy:       { h: 0.68, pupilY: 4,   browLift: -6,  browAngle: 6,  innerGlow: 1.00 },
  wide:        { h: 1.25, pupilY: -4,  browLift: -10, browAngle: 0,  innerGlow: 1.00 },
  excited:     { h: 1.20, pupilY: -2,  browLift: -8,  browAngle: 3,  innerGlow: 1.00 },
  sad:         { h: 0.58, pupilY: 6,   browLift: 6,   browAngle: -7, innerGlow: 0.45 },
  droopy:      { h: 0.50, pupilY: 8,   browLift: 7,   browAngle: -6, innerGlow: 0.40 },
  furrowed:    { h: 0.78, pupilY: 2,   browLift: 5,   browAngle: -9, innerGlow: 0.75 },
  look_up:     { h: 0.88, pupilY: -16, browLift: -4,  browAngle: 0,  innerGlow: 0.90 },
  raised_brow: { h: 1.00, pupilY: 0,   browLift: -8,  browAngle: 5,  innerGlow: 0.95 },
  confident:   { h: 0.86, pupilY: 0,   browLift: -3,  browAngle: 4,  innerGlow: 0.90 },
  closed:      { h: 0.04, pupilY: 0,   browLift: 0,   browAngle: 0,  innerGlow: 0.10 },
  squint:      { h: 0.42, pupilY: 2,   browLift: 3,   browAngle: -4, innerGlow: 0.60 },
};

/* ── Mouth curves ───────────────────────────────────────────── */
const MOUTH = {
  flat:         { type: 'line',  curve: 0    },
  smile:        { type: 'curve', curve: 18   },
  big_smile:    { type: 'curve', curve: 24   },
  frown:        { type: 'curve', curve: -14  },
  open_smile:   { type: 'open',  curve: 14   },
  slight_smile: { type: 'curve', curve: 8    },
  slight_frown: { type: 'curve', curve: -7   },
  talk:         { type: 'eq',    curve: 0    },
  open:         { type: 'open',  curve: 0    },
  attentive:    { type: 'curve', curve: 5    },
  thinking:     { type: 'curve', curve: -3   },
  proud:        { type: 'curve', curve: 20   },
  surprised:    { type: 'open',  curve: 4    },
  tired:        { type: 'curve', curve: -5   },
  sleeping:     { type: 'line',  curve: 0    },
};

function Eye({ theme, expr, side, blinking }) {
  const { h, pupilY, browLift, browAngle, innerGlow } = expr;
  const dir = side === 'left' ? 1 : -1;
  const isClosed = h <= 0.08 || blinking;

  return (
    <div className="face-eye-unit">
      {/* Eyebrow LED Bar */}
      <div
        className="face-eyebrow"
        style={{
          background: theme.c,
          boxShadow: `0 0 12px ${theme.c}, 0 0 28px ${theme.g}`,
          transform: `translateY(${browLift}px) rotate(${browAngle * dir}deg)`,
          opacity: isClosed ? 0.3 : 0.9,
        }}
      />

      {/* Outer Metallic Eye Rim */}
      <div
        className="face-eye-socket"
        style={{
          boxShadow: `0 0 0 2px ${theme.c}45, 0 0 24px ${theme.g}, 0 4px 20px rgba(0,0,0,0.9)`,
        }}
      >
        {/* OLED Eye Screen */}
        <div
          className={`face-eye-oled ${isClosed ? 'face-eye-oled--closed' : ''}`}
          style={{ transform: `scaleY(${isClosed ? 0.04 : h})` }}
        >
          {isClosed ? (
            <div className="face-eye-sleep" style={{ background: `${theme.c}88` }} />
          ) : (
            <>
              {/* Cyan Pupil / Iris Glow */}
              <div
                className="face-eye-iris"
                style={{
                  background: `radial-gradient(ellipse 65% 60% at 50% 50%,
                    ${theme.c} 0%,
                    ${theme.c}dd 30%,
                    ${theme.c}44 65%,
                    rgba(0,0,0,0.98) 100%)`,
                  boxShadow: `0 0 30px ${theme.c}, 0 0 60px ${theme.g}`,
                  transform: `translateY(${pupilY}px)`,
                  opacity: innerGlow,
                }}
              />
              <div className="face-eye-pupil" style={{ transform: `translateY(${pupilY}px)` }} />
              <div className="face-eye-glint-large" />
              <div className="face-eye-glint-small" />
              <div className="face-eye-scanline" style={{ background: `${theme.c}30` }} />
              <div className="face-eye-pixel-grid" />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function Mouth({ theme, shape, speaking }) {
  const config = speaking ? MOUTH.talk : shape;
  const W = 100, H = 36, cx = W / 2;

  if (config.type === 'eq') {
    return (
      <div className="face-mouth-area face-mouth-eq">
        {[0.35, 0.65, 0.95, 1.0, 0.85, 0.95, 0.75, 0.55, 0.45, 0.75, 0.6, 0.4].map((h, i) => (
          <div
            key={i}
            className="face-eq-bar"
            style={{
              '--bh': h,
              background: `linear-gradient(180deg, ${theme.c}, ${theme.c}99)`,
              boxShadow: `0 0 8px ${theme.c}99`,
              animationDelay: `${i * 0.05}s`,
            }}
          />
        ))}
      </div>
    );
  }

  if (config.type === 'open') {
    const c = config.curve;
    return (
      <div className="face-mouth-area">
        <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} overflow="visible">
          <ellipse
            cx={cx} cy={H / 2 + 2}
            rx={28} ry={11 + c / 3}
            fill={`${theme.c}25`}
            stroke={theme.c}
            strokeWidth="2.5"
            style={{ filter: `drop-shadow(0 0 6px ${theme.c})` }}
          />
        </svg>
      </div>
    );
  }

  const c = config.curve;
  return (
    <div className="face-mouth-area">
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} overflow="visible">
        <path
          d={`M 12 ${H / 2 - c / 2} Q ${cx} ${H / 2 + c} ${W - 12} ${H / 2 - c / 2}`}
          stroke={theme.c}
          strokeWidth="3"
          fill="none"
          strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 6px ${theme.c})` }}
        />
      </svg>
    </div>
  );
}

function Headphone({ theme, side, listening }) {
  return (
    <div className={`face-hp face-hp--${side}`}>
      <div
        className="face-hp-cup"
        style={{
          background: `linear-gradient(${side === 'left' ? '135deg' : '225deg'}, #7755cc, #4433aa, #2a2060)`,
          boxShadow: listening
            ? `0 0 0 2.5px ${theme.c}70, 0 0 25px ${theme.g}, 0 6px 24px rgba(0,0,0,0.85)`
            : `0 6px 24px rgba(0,0,0,0.85), 0 0 0 1.5px rgba(255,255,255,0.08)`,
        }}
      >
        <div className="face-hp-grille">
          <div className="face-hp-ring r1" style={{ borderColor: `${theme.c}40` }} />
          <div className="face-hp-ring r2" style={{ borderColor: `${theme.c}25` }} />
          <div
            className={`face-hp-ring r3 ${listening ? 'r3--active' : ''}`}
            style={{
              borderColor: theme.c,
              boxShadow: listening ? `0 0 12px ${theme.c}` : 'none',
            }}
          />
        </div>
        <div
          className={`face-hp-led ${listening ? 'led--on' : ''}`}
          style={{ background: theme.c, boxShadow: listening ? `0 0 14px ${theme.c}` : 'none' }}
        />
      </div>
      <div className="face-hp-pad" />
    </div>
  );
}

export default function RobotFace({ robotState = 'IDLE', expression, emotion }) {
  const theme    = THEMES[robotState] || THEMES.IDLE;
  const isSleep  = robotState === 'SLEEPING';
  const isSpeak  = robotState === 'SPEAKING' || robotState === 'GREETING';
  const isThink  = robotState === 'THINKING';
  const isListen = robotState === 'LISTENING';
  const isExcited= robotState === 'GREETING';

  // Eye expression lookup
  const eyeKey = expression?.eye_shape
    ?? (isSleep ? 'closed' : isThink ? 'look_up' : isListen ? 'wide' : isSpeak ? 'happy' : isExcited ? 'excited' : 'normal');
  const eyeExpr = EYE_EXPR[eyeKey] || EYE_EXPR.normal;

  // Blinking loop
  const [blinking, setBlinking] = useState(false);
  useEffect(() => {
    if (isSleep) return;
    const schedBlink = () => {
      const wait = isExcited ? 1500 + Math.random() * 1500 : 3200 + Math.random() * 4000;
      return setTimeout(() => {
        setBlinking(true);
        setTimeout(() => setBlinking(false), 130);
        schedBlink();
      }, wait);
    };
    const t = schedBlink();
    return () => clearTimeout(t);
  }, [isSleep, isExcited]);

  // Mouth shape lookup
  const mouthKey = expression?.mouth
    ?? (isSleep ? 'sleeping' : isThink ? 'thinking' : isListen ? 'attentive' : isSpeak ? 'talk' : isExcited ? 'big_smile' : 'slight_smile');
  const mouthShape = MOUTH[mouthKey] || MOUTH.slight_smile;

  // Head tilt & float
  const tiltAngle = isThink ? -7 : isListen ? 4 : 0;

  return (
    <div
      className={`robot-face-root ${isSleep ? 'rf--sleep' : ''} ${isThink ? 'rf--think' : ''} ${isExcited ? 'rf--excited' : ''}`}
      style={{
        '--c': theme.c,
        '--g': theme.g,
        opacity: theme.dim,
      }}
    >
      {/* Background Halos */}
      <div className="rf-halo h1" />
      <div className="rf-halo h2" />

      {/* Headphone Arch Band */}
      <div className="rf-band-arc" />

      {/* Head Unit */}
      <div
        className={`rf-head-unit ${isSpeak ? 'rf-head-unit--bob' : ''}`}
        style={{ transform: `rotate(${tiltAngle}deg)` }}
      >
        <Headphone theme={theme} side="left" listening={isListen} />

        {/* Metallic Head Shell */}
        <div
          className="rf-head-shell"
          style={{
            boxShadow: `
              0 0 0 1.5px rgba(255,255,255,0.08),
              0 0 80px ${theme.g},
              0 0 160px ${theme.g}50,
              0 24px 70px rgba(0,0,0,0.85),
              inset 0 2px 0 rgba(255,255,255,0.1),
              inset 0 -3px 0 rgba(0,0,0,0.5)
            `,
          }}
        >
          {/* Top LED Stripe */}
          <div className="rf-top-led" style={{ background: `linear-gradient(90deg, transparent, ${theme.c}60, transparent)` }} />

          {/* OLED Screen Face */}
          <div
            className="rf-screen"
            style={{
              boxShadow: `inset 0 3px 25px rgba(0,0,0,0.98), 0 0 0 1.5px rgba(0,0,0,0.9)`,
            }}
          >
            {/* Camera Dot */}
            <div className="rf-camera" style={{ background: `${theme.c}95`, boxShadow: `0 0 8px ${theme.c}` }} />

            {/* Eyes Row */}
            <div className={`rf-eyes-row ${blinking ? 'rf-eyes-row--blink' : ''}`}>
              <Eye theme={theme} expr={eyeExpr} side="left"  blinking={blinking} />
              <Eye theme={theme} expr={eyeExpr} side="right" blinking={blinking} />
            </div>

            {/* Nose Dot Sensor */}
            <div className="rf-nose">
              <div className="rf-nose-dot" style={{ background: theme.c, boxShadow: `0 0 6px ${theme.c}` }} />
            </div>

            {/* Mouth */}
            <Mouth theme={theme} shape={mouthShape} speaking={isSpeak} />

            {/* Bottom Status LEDs */}
            <div className="rf-bottom-leds">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="rf-bled" style={{ background: `${theme.c}${isSpeak ? '90' : '35'}` }} />
              ))}
            </div>
          </div>

          {/* Chin Grille */}
          <div className="rf-chin">
            <div className="rf-chin-slits">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="rf-slit" />
              ))}
            </div>
          </div>
        </div>

        <Headphone theme={theme} side="right" listening={isListen} />
      </div>

      {/* Ground Reflection Glow */}
      <div className="rf-ground-glow" style={{ background: `radial-gradient(ellipse 80% 45%, ${theme.g} 0%, transparent 70%)` }} />

      {/* Thinking Orbiting Particles */}
      {isThink && (
        <div className="rf-think-particles">
          {[...Array(12)].map((_, i) => (
            <div key={i} className="rf-p" style={{ '--i': i, background: theme.c, boxShadow: `0 0 10px ${theme.c}` }} />
          ))}
        </div>
      )}

      {/* Speaking Sound Rings */}
      {isSpeak && (
        <div className="rf-speak-rings">
          {[0, 1, 2].map((i) => (
            <div key={i} className="rf-sr" style={{ '--i': i, borderColor: theme.c, boxShadow: `0 0 16px ${theme.g}` }} />
          ))}
        </div>
      )}
    </div>
  );
}
