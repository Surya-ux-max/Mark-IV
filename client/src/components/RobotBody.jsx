/**
 * RobotBody.jsx — CSE Brain Bright User-Lovable Robot v7
 *
 * Bright Lovable Design Language:
 * - Polar White & Polished Silver Shell (#ffffff → #e2e8f0)
 * - Glossy Dark OLED Face Panel with High-Contrast Neon Cyan Eyes & Eyebrows
 * - Lovable Lavender/Violet Headphone Ears (#8b5cf6) with Pink Accent LEDs
 * - Interactive Dragging (Head, Arms, Torso) & Double-Tap Wake/Sleep support
 */

import { useEffect, useRef, useState } from 'react';
import './RobotBody.css';

/* ── State → Theme Palette ──────────────────────────────────── */
const THEMES = {
  SLEEPING:  { c: '#6366f1', g: 'rgba(99,102,241,0.45)',  dim: 0.75, hp: '#7c3aed' },
  IDLE:      { c: '#00e5ff', g: 'rgba(0,229,255,0.55)',  dim: 1.0,  hp: '#8b5cf6' },
  LISTENING: { c: '#2563eb', g: 'rgba(37,99,235,0.6)',   dim: 1.0,  hp: '#4f46e5' },
  THINKING:  { c: '#f59e0b', g: 'rgba(245,158,11,0.6)',   dim: 1.0,  hp: '#d97706' },
  SPEAKING:  { c: '#10b981', g: 'rgba(16,185,129,0.6)',   dim: 1.0,  hp: '#059669' },
  GREETING:  { c: '#ec4899', g: 'rgba(236,72,153,0.6)',   dim: 1.0,  hp: '#db2777' },
  OBSERVING: { c: '#00e5ff', g: 'rgba(0,229,255,0.5)',   dim: 1.0,  hp: '#8b5cf6' },
  ERROR:     { c: '#ef4444', g: 'rgba(239,68,68,0.6)',    dim: 1.0,  hp: '#dc2626' },
};

/* ── Eye expressions ────────────────────────────────────────── */
const EYE_EXPR = {
  normal:      { h: 1.00, pupilY: 0,   browLift: 0,   browAngle: 0,  innerGlow: 0.90 },
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

/* ── Mouth profiles ─────────────────────────────────────────── */
const MOUTH = {
  flat:         { type: 'line',  curve: 0    },
  smile:        { type: 'curve', curve: 16   },
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

/* ── Arm Poses ──────────────────────────────────────────────── */
const DEFAULT_ARM_POSE = {
  SLEEPING:  { ls: 3,  rs: 3,  le: 5,  re: 5  },
  IDLE:      { ls: 8,  rs: -8, le: 4,  re: 4  },
  LISTENING: { ls: 18, rs: 18, le: 40, re: 40 },
  THINKING:  { ls: 15, rs: 48, le: 25, re: 84 },
  SPEAKING:  { ls: 32, rs: 32, le: 22, re: 22 },
  GREETING:  { ls: 10, rs: 88, le: 10, re: 18 },
  OBSERVING: { ls: 10, rs: -10,le: 4,  re: 4  },
  ERROR:     { ls: 0,  rs: 0,  le: 0,  re: 0  },
};

function Eye({ theme, expr, side, blinking }) {
  const { h, pupilY, browLift, browAngle, innerGlow } = expr;
  const dir = side === 'left' ? 1 : -1;
  const isClosed = h <= 0.08 || blinking;

  return (
    <div className="fb-eye-unit">
      <div
        className="fb-eyebrow"
        style={{
          background: theme.c,
          boxShadow: `0 0 10px ${theme.c}, 0 0 22px ${theme.g}`,
          transform: `translateY(${browLift}px) rotate(${browAngle * dir}deg)`,
          opacity: isClosed ? 0.3 : 0.95,
        }}
      />
      <div
        className="fb-eye-socket"
        style={{
          boxShadow: `0 0 0 1.5px ${theme.c}40, 0 0 20px ${theme.g}, 0 4px 16px rgba(0,0,0,0.9)`,
        }}
      >
        <div
          className={`fb-eye-oled ${isClosed ? 'fb-eye-oled--closed' : ''}`}
          style={{ transform: `scaleY(${isClosed ? 0.04 : h})` }}
        >
          {isClosed ? (
            <div className="fb-eye-sleep" style={{ background: `${theme.c}88` }} />
          ) : (
            <>
              <div
                className="fb-eye-iris"
                style={{
                  background: `radial-gradient(ellipse 65% 60% at 50% 50%,
                    ${theme.c} 0%,
                    ${theme.c}dd 30%,
                    ${theme.c}44 65%,
                    rgba(0,0,0,0.98) 100%)`,
                  boxShadow: `0 0 24px ${theme.c}, 0 0 50px ${theme.g}`,
                  transform: `translateY(${pupilY}px)`,
                  opacity: innerGlow,
                }}
              />
              <div className="fb-eye-pupil" style={{ transform: `translateY(${pupilY}px)` }} />
              <div className="fb-eye-glint-large" />
              <div className="fb-eye-glint-small" />
              <div className="fb-eye-scanline" style={{ background: `${theme.c}25` }} />
              <div className="fb-eye-pixel-grid" />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function Mouth({ theme, shape, speaking }) {
  const config = speaking ? MOUTH.talk : shape;
  const W = 80, H = 28, cx = W / 2;

  if (config.type === 'eq') {
    return (
      <div className="fb-mouth-area fb-mouth-eq">
        {[0.35, 0.65, 0.95, 1.0, 0.85, 0.95, 0.75, 0.55, 0.45, 0.75].map((h, i) => (
          <div
            key={i}
            className="fb-eq-bar"
            style={{
              '--bh': h,
              background: `linear-gradient(180deg, ${theme.c}, ${theme.c}99)`,
              boxShadow: `0 0 6px ${theme.c}99`,
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
      <div className="fb-mouth-area">
        <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} overflow="visible">
          <ellipse
            cx={cx} cy={H / 2 + 2}
            rx={22} ry={8 + c / 3}
            fill={`${theme.c}25`}
            stroke={theme.c}
            strokeWidth="2"
            style={{ filter: `drop-shadow(0 0 5px ${theme.c})` }}
          />
        </svg>
      </div>
    );
  }

  const c = config.curve;
  return (
    <div className="fb-mouth-area">
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} overflow="visible">
        <path
          d={`M 10 ${H / 2 - c / 2} Q ${cx} ${H / 2 + c} ${W - 10} ${H / 2 - c / 2}`}
          stroke={theme.c}
          strokeWidth="2.5"
          fill="none"
          strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 5px ${theme.c})` }}
        />
      </svg>
    </div>
  );
}

function Headphone({ theme, side, listening }) {
  return (
    <div className={`fb-hp fb-hp--${side}`}>
      <div
        className="fb-hp-cup"
        style={{
          background: `linear-gradient(${side === 'left' ? '135deg' : '225deg'}, #a855f7, #7c3aed, #4c1d95)`,
          boxShadow: listening
            ? `0 0 0 2.5px ${theme.c}70, 0 0 20px ${theme.g}, 0 6px 20px rgba(0,0,0,0.15)`
            : `0 6px 20px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.8)`,
        }}
      >
        <div className="fb-hp-grille">
          <div className="fb-hp-ring r1" style={{ borderColor: `${theme.c}50` }} />
          <div className="fb-hp-ring r2" style={{ borderColor: `${theme.c}30` }} />
          <div
            className={`fb-hp-ring r3 ${listening ? 'r3--active' : ''}`}
            style={{
              borderColor: theme.c,
              boxShadow: listening ? `0 0 10px ${theme.c}` : 'none',
            }}
          />
        </div>
        <div
          className={`fb-hp-led ${listening ? 'led--on' : ''}`}
          style={{ background: theme.c, boxShadow: listening ? `0 0 12px ${theme.c}` : 'none' }}
        />
      </div>
      <div className="fb-hp-pad" />
    </div>
  );
}

export default function RobotBody({ robotState = 'IDLE', expression, emotion, animationCue, onDoubleTap }) {
  const theme     = THEMES[robotState] || THEMES.IDLE;
  const isSleep   = robotState === 'SLEEPING';
  const isSpeak   = robotState === 'SPEAKING' || robotState === 'GREETING';
  const isThink   = robotState === 'THINKING';
  const isListen  = robotState === 'LISTENING';
  const isExcited = robotState === 'GREETING';

  // Eye & Expression
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

  // Mouth shape
  const mouthKey = expression?.mouth
    ?? (isSleep ? 'sleeping' : isThink ? 'thinking' : isListen ? 'attentive' : isSpeak ? 'talk' : isExcited ? 'big_smile' : 'slight_smile');
  const mouthShape = MOUTH[mouthKey] || MOUTH.slight_smile;

  // Drag & Interactive Pose State
  const [headRotation, setHeadRotation] = useState({ rotX: 0, rotY: 0 });
  const [torsoLean, setTorsoLean] = useState({ leanX: 0, leanY: 0 });
  const [armOffsets, setArmOffsets] = useState({
    lShoulderOffset: 0,
    rShoulderOffset: 0,
    lElbowOffset: 0,
    rElbowOffset: 0,
  });

  const [arms, setArms]     = useState(DEFAULT_ARM_POSE.IDLE);
  const [waving, setWaving] = useState(false);
  const [celeb, setCeleb]   = useState(false);
  const timerRef = useRef(null);

  const [dragTarget, setDragTarget] = useState(null);
  const dragStartRef = useRef({ x: 0, y: 0 });
  const lastTapRef = useRef(0);
  const clickTimeoutRef = useRef(null);

  useEffect(() => {
    setArms(DEFAULT_ARM_POSE[robotState] || DEFAULT_ARM_POSE.IDLE);
    setWaving(false);
    setCeleb(false);
  }, [robotState]);

  useEffect(() => {
    if (!animationCue) return;
    const a = (animationCue.animation || '').toUpperCase();
    clearTimeout(timerRef.current);
    if (a.includes('WAVE')) {
      setWaving(true);
      timerRef.current = setTimeout(() => setWaving(false), 2400);
    } else if (a.includes('CELEBRAT')) {
      setCeleb(true);
      timerRef.current = setTimeout(() => setCeleb(false), 2600);
    } else if (a.includes('THINKING')) {
      setArms({ ls: 15, rs: 48, le: 25, re: 84 });
      timerRef.current = setTimeout(() => setArms(DEFAULT_ARM_POSE[robotState] || DEFAULT_ARM_POSE.IDLE), 4000);
    } else if (a.includes('OPEN_ARMS')) {
      setArms({ ls: 75, rs: 75, le: 18, re: 18 });
      timerRef.current = setTimeout(() => setArms(DEFAULT_ARM_POSE[robotState] || DEFAULT_ARM_POSE.IDLE), 2600);
    }
  }, [animationCue, robotState]);

  const startDrag = (target, e) => {
    e.stopPropagation();
    setDragTarget(target);
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    dragStartRef.current = { x: clientX, y: clientY };
  };

  useEffect(() => {
    const handleMove = (e) => {
      if (!dragTarget) return;
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const deltaX = clientX - dragStartRef.current.x;
      const deltaY = clientY - dragStartRef.current.y;

      if (dragTarget === 'head') {
        setHeadRotation((prev) => ({
          rotY: Math.max(-25, Math.min(25, prev.rotY + deltaX * 0.4)),
          rotX: Math.max(-15, Math.min(15, prev.rotX + deltaY * 0.3)),
        }));
      } else if (dragTarget === 'torso') {
        setTorsoLean((prev) => ({
          leanX: Math.max(-15, Math.min(15, prev.leanX + deltaX * 0.3)),
          leanY: Math.max(-10, Math.min(10, prev.leanY + deltaY * 0.2)),
        }));
      } else if (dragTarget === 'rArm') {
        setArmOffsets((prev) => ({
          ...prev,
          rShoulderOffset: Math.max(-60, Math.min(120, prev.rShoulderOffset - deltaY * 0.8)),
          rElbowOffset: Math.max(-40, Math.min(80, prev.rElbowOffset + deltaX * 0.5)),
        }));
      } else if (dragTarget === 'lArm') {
        setArmOffsets((prev) => ({
          ...prev,
          lShoulderOffset: Math.max(-60, Math.min(120, prev.lShoulderOffset - deltaY * 0.8)),
          lElbowOffset: Math.max(-40, Math.min(80, prev.lElbowOffset - deltaX * 0.5)),
        }));
      }

      dragStartRef.current = { x: clientX, y: clientY };
    };

    const stopDrag = () => setDragTarget(null);

    if (dragTarget) {
      window.addEventListener('mousemove', handleMove);
      window.addEventListener('mouseup', stopDrag);
      window.addEventListener('touchmove', handleMove);
      window.addEventListener('touchend', stopDrag);
    }
    return () => {
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('mouseup', stopDrag);
      window.removeEventListener('touchmove', handleMove);
      window.removeEventListener('touchend', stopDrag);
    };
  }, [dragTarget]);

  const handleRobotDoubleClick = (e) => {
    e.stopPropagation();
    if (onDoubleTap) onDoubleTap();
  };

  const handleTouchEnd = (e) => {
    const now = Date.now();
    if (now - lastTapRef.current < 300) {
      e.preventDefault();
      if (onDoubleTap) onDoubleTap();
    }
    lastTapRef.current = now;
  };

  const handleResetPose = () => {
    setHeadRotation({ rotX: 0, rotY: 0 });
    setTorsoLean({ leanX: 0, leanY: 0 });
    setArmOffsets({ lShoulderOffset: 0, rShoulderOffset: 0, lElbowOffset: 0, rElbowOffset: 0 });
  };

  const rShoulder = (celeb ? 142 : waving ? 86 : arms.rs) + armOffsets.rShoulderOffset;
  const lShoulder = (celeb ? 142 : arms.ls) + armOffsets.lShoulderOffset;
  const rElbow    = (waving ? 20 : celeb ? 25 : arms.re) + armOffsets.rElbowOffset;
  const lElbow    = (celeb ? 25 : arms.le) + armOffsets.lElbowOffset;

  const tiltAngle = (isThink ? -6 : isListen ? 3 : 0) + headRotation.rotY;

  const isCustomPosed =
    headRotation.rotX !== 0 ||
    headRotation.rotY !== 0 ||
    torsoLean.leanX !== 0 ||
    torsoLean.leanY !== 0 ||
    armOffsets.rShoulderOffset !== 0 ||
    armOffsets.lShoulderOffset !== 0;

  return (
    <div
      className={`fb-root ${isSleep ? 'fb--sleep' : ''} ${isThink ? 'fb--think' : ''} ${isExcited ? 'fb--excited' : ''}`}
      style={{
        '--c': theme.c,
        '--g': theme.g,
        opacity: theme.dim,
        transform: `rotate(${torsoLean.leanX * 0.5}deg) translateY(${torsoLean.leanY}px)`,
      }}
      onDoubleClick={handleRobotDoubleClick}
      onTouchEnd={handleTouchEnd}
    >
      {/* Soft Ambient Light Halo */}
      <div className="fb-halo h1" />

      {/* Headphone Arc Band */}
      <div className="fb-band-arc" />

      {/* HEAD */}
      <div
        className={`fb-head-unit ${isSpeak ? 'fb-head-unit--bob' : ''} interactive-part`}
        style={{
          transform: `rotate(${tiltAngle}deg) translateY(${headRotation.rotX}px)`,
          cursor: dragTarget === 'head' ? 'grabbing' : 'grab',
        }}
        onMouseDown={(e) => startDrag('head', e)}
        onTouchStart={(e) => startDrag('head', e)}
        onClick={() => {
          clearTimeout(clickTimeoutRef.current);
          clickTimeoutRef.current = setTimeout(() => {
            setWaving(true);
            setTimeout(() => setWaving(false), 2000);
          }, 250);
        }}
        title="Double-tap to Wake/Sleep! Drag to tilt head."
      >
        <Headphone theme={theme} side="left" listening={isListen} />

        {/* Polar White Head Shell */}
        <div
          className="fb-head-shell"
          style={{
            boxShadow: `
              0 16px 40px rgba(0,40,90,0.12),
              0 0 40px ${theme.g},
              inset 0 2px 0 #ffffff,
              inset 0 -2px 0 rgba(0,0,0,0.06)
            `,
          }}
        >
          <div className="fb-top-led" style={{ background: `linear-gradient(90deg, transparent, ${theme.c}70, transparent)` }} />

          <div
            className="fb-screen"
            style={{ boxShadow: `inset 0 2px 20px rgba(0,0,0,0.95), 0 0 0 1.5px rgba(0,0,0,0.9)` }}
          >
            <div className="fb-camera" style={{ background: `${theme.c}95`, boxShadow: `0 0 8px ${theme.c}` }} />

            <div className={`fb-eyes-row ${blinking ? 'fb-eyes-row--blink' : ''}`}>
              <Eye theme={theme} expr={eyeExpr} side="left"  blinking={blinking} />
              <Eye theme={theme} expr={eyeExpr} side="right" blinking={blinking} />
            </div>

            <div className="fb-nose">
              <div className="fb-nose-dot" style={{ background: theme.c, boxShadow: `0 0 6px ${theme.c}` }} />
            </div>

            <Mouth theme={theme} shape={mouthShape} speaking={isSpeak} />

            <div className="fb-bottom-leds">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="fb-bled" style={{ background: `${theme.c}${isSpeak ? '90' : '35'}` }} />
              ))}
            </div>
          </div>

          <div className="fb-chin">
            <div className="fb-chin-slits">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="fb-slit" />
              ))}
            </div>
          </div>
        </div>

        <Headphone theme={theme} side="right" listening={isListen} />
      </div>

      {/* NECK */}
      <div className="fb-neck-wrap">
        <div className="fb-neck-ring fb-neck-ring--top" style={{ borderColor: `${theme.c}30` }} />
        <div className="fb-neck-core" />
        <div className="fb-neck-ring fb-neck-ring--bot" style={{ borderColor: `${theme.c}30` }} />
      </div>

      {/* TORSO & ARMS */}
      <div className="fb-torso-row">
        {/* LEFT ARM */}
        <div
          className="fb-arm fb-arm--left interactive-part"
          style={{
            transform: `rotate(${-lShoulder}deg)`,
            transformOrigin: 'top center',
            cursor: dragTarget === 'lArm' ? 'grabbing' : 'grab',
          }}
          onMouseDown={(e) => startDrag('lArm', e)}
          onTouchStart={(e) => startDrag('lArm', e)}
          title="Drag to move left arm!"
        >
          <div className="fb-shoulder" style={{ background: theme.c, boxShadow: `0 0 12px ${theme.g}` }} />
          <div className="fb-arm-upper" style={{ borderColor: `${theme.c}25` }}>
            <div className="fb-arm-stripe" style={{ background: `${theme.c}50` }} />
          </div>
          <div className="fb-elbow" style={{ borderColor: `${theme.c}45`, background: `#cbd5e1` }} />
          <div
            className="fb-arm-lower"
            style={{ transform: `rotate(${lElbow}deg)`, transformOrigin: 'top center', borderColor: `${theme.c}25` }}
          >
            <div className="fb-wrist" style={{ borderColor: `${theme.c}35` }} />
            <div className="fb-hand" style={{ borderColor: `${theme.c}50`, background: `${theme.c}12` }}>
              {[...Array(4)].map((_, i) => (
                <div key={i} className="fb-finger" style={{ background: `#ffffff`, borderColor: `${theme.c}40` }} />
              ))}
              <div className="fb-thumb" style={{ background: `#ffffff`, borderColor: `${theme.c}40` }} />
            </div>
          </div>
        </div>

        {/* TORSO */}
        <div
          className="fb-torso interactive-part"
          style={{
            boxShadow: `
              0 16px 40px rgba(0,40,90,0.1),
              0 0 30px ${theme.g}20,
              inset 0 2px 0 #ffffff,
              inset 0 -2px 0 rgba(0,0,0,0.06)
            `,
            cursor: dragTarget === 'torso' ? 'grabbing' : 'grab',
          }}
          onMouseDown={(e) => startDrag('torso', e)}
          onTouchStart={(e) => startDrag('torso', e)}
          title="Drag to lean body!"
        >
          <div className="fb-chest-top" style={{ background: `linear-gradient(90deg, transparent, ${theme.c}30, transparent)` }} />

          <div
            className="fb-chest-core"
            style={{
              borderColor: theme.c,
              boxShadow: `0 0 20px ${theme.c}80, 0 0 45px ${theme.g}, inset 0 0 15px ${theme.c}20`,
            }}
          >
            <div
              className="fb-core-fill"
              style={{
                background: `radial-gradient(circle, ${theme.c} 0%, ${theme.c}88 35%, ${theme.c}22 65%, transparent 100%)`,
              }}
            />
            <div className="fb-core-ring" style={{ borderColor: `${theme.c}70` }} />
          </div>

          <div className={`fb-chest-eq ${isSpeak ? 'fb-chest-eq--active' : ''}`}>
            {[0.4, 0.7, 1.0, 0.6, 0.9, 0.5, 0.8, 0.6].map((h, i) => (
              <div
                key={i}
                className="fb-ceq"
                style={{
                  '--bh': h,
                  background: `linear-gradient(180deg, ${theme.c}, ${theme.c}77)`,
                  animationDelay: `${i * 0.06}s`,
                }}
              />
            ))}
          </div>

          <div className="fb-torso-badge" style={{ color: `#64748b` }}>
            CSE·BRAIN·MK4
          </div>
        </div>

        {/* RIGHT ARM */}
        <div
          className={`fb-arm fb-arm--right ${waving ? 'fb-arm--wave' : ''} ${celeb ? 'fb-arm--celeb' : ''} interactive-part`}
          style={{
            transform: `rotate(${rShoulder}deg)`,
            transformOrigin: 'top center',
            cursor: dragTarget === 'rArm' ? 'grabbing' : 'grab',
          }}
          onMouseDown={(e) => startDrag('rArm', e)}
          onTouchStart={(e) => startDrag('rArm', e)}
          title="Drag to move right arm!"
        >
          <div className="fb-shoulder" style={{ background: theme.c, boxShadow: `0 0 12px ${theme.g}` }} />
          <div className="fb-arm-upper" style={{ borderColor: `${theme.c}25` }}>
            <div className="fb-arm-stripe" style={{ background: `${theme.c}50` }} />
          </div>
          <div className="fb-elbow" style={{ borderColor: `${theme.c}45`, background: `#cbd5e1` }} />
          <div
            className="fb-arm-lower"
            style={{ transform: `rotate(${-rElbow}deg)`, transformOrigin: 'top center', borderColor: `${theme.c}25` }}
          >
            <div className="fb-wrist" style={{ borderColor: `${theme.c}35` }} />
            <div className="fb-hand" style={{ borderColor: `${theme.c}50`, background: `${theme.c}12` }}>
              {[...Array(4)].map((_, i) => (
                <div key={i} className="fb-finger" style={{ background: `#ffffff`, borderColor: `${theme.c}40` }} />
              ))}
              <div className="fb-thumb" style={{ background: `#ffffff`, borderColor: `${theme.c}40` }} />
            </div>
          </div>
        </div>
      </div>

      {/* HIP CONNECTOR */}
      <div className="fb-hip-bar" style={{ borderColor: `${theme.c}30`, background: `#e2e8f0` }}>
        <div className="fb-hip-leds">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="fb-hled" style={{ background: `${theme.c}${isSleep ? '30' : '75'}` }} />
          ))}
        </div>
      </div>

      {/* LEGS & FEET */}
      <div className="fb-legs-row">
        <div className={`fb-leg ${isSpeak || isExcited ? 'fb-leg--bounce' : ''}`}>
          <div className="fb-leg-hip" style={{ background: theme.c, boxShadow: `0 0 8px ${theme.g}` }} />
          <div className="fb-leg-upper" style={{ borderColor: `${theme.c}25` }}>
            <div className="fb-leg-stripe" style={{ background: `${theme.c}50` }} />
          </div>
          <div className="fb-knee" style={{ borderColor: `${theme.c}40`, background: `#cbd5e1` }} />
          <div className="fb-leg-lower" style={{ borderColor: `${theme.c}20` }} />
          <div className="fb-foot" style={{ borderColor: `${theme.c}45`, background: `#ffffff` }}>
            <div className="fb-foot-led" style={{ background: theme.c, boxShadow: `0 0 10px ${theme.c}` }} />
          </div>
        </div>

        <div className={`fb-leg ${isSpeak || isExcited ? 'fb-leg--bounce fb-leg--bounce-r' : ''}`}>
          <div className="fb-leg-hip" style={{ background: theme.c, boxShadow: `0 0 8px ${theme.g}` }} />
          <div className="fb-leg-upper" style={{ borderColor: `${theme.c}25` }}>
            <div className="fb-leg-stripe" style={{ background: `${theme.c}50` }} />
          </div>
          <div className="fb-knee" style={{ borderColor: `${theme.c}35`, background: `#cbd5e1` }} />
          <div className="fb-leg-lower" style={{ borderColor: `${theme.c}20` }} />
          <div className="fb-foot" style={{ borderColor: `${theme.c}45`, background: `#ffffff` }}>
            <div className="fb-foot-led" style={{ background: theme.c, boxShadow: `0 0 10px ${theme.c}` }} />
          </div>
        </div>
      </div>

      {/* GROUND GLOW */}
      <div className="fb-ground-glow" style={{ background: `radial-gradient(ellipse 80% 45%, ${theme.g} 0%, transparent 70%)` }} />

      {/* Reset Pose Button */}
      {isCustomPosed && (
        <button
          className="reset-pose-btn"
          onClick={handleResetPose}
          style={{ borderColor: theme.c, color: theme.c }}
        >
          ↺ RESET POSE
        </button>
      )}

      {/* Thinking particles */}
      {isThink && (
        <div className="fb-think-cloud">
          {[...Array(10)].map((_, i) => (
            <div key={i} className="fb-tp" style={{ '--i': i, background: theme.c, boxShadow: `0 0 8px ${theme.c}` }} />
          ))}
        </div>
      )}

      {/* Speaking rings */}
      {isSpeak && (
        <div className="fb-speak-rings">
          {[0, 1, 2].map((i) => (
            <div key={i} className="fb-sr" style={{ '--i': i, borderColor: theme.c, boxShadow: `0 0 12px ${theme.g}` }} />
          ))}
        </div>
      )}
    </div>
  );
}
