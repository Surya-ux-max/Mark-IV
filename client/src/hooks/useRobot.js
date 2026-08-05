/**
 * useRobot.js — Top-level robot state management hook.
 *
 * Handles all WS message types including new EXPRESSION_CHANGED.
 */

import { useCallback, useRef, useState } from 'react';

export const ROBOT_STATES = {
  SLEEPING:  'SLEEPING',
  IDLE:      'IDLE',
  LISTENING: 'LISTENING',
  THINKING:  'THINKING',
  SPEAKING:  'SPEAKING',
  GREETING:  'GREETING',
  OBSERVING: 'OBSERVING',
  ERROR:     'ERROR',
};

const INITIAL_STATE = {
  robotState:   ROBOT_STATES.SLEEPING,
  emotion:      'NEUTRAL',
  isAwake:      false,
  lastResponse: '',
  lastSources:  [],
  animationCue: null,
  expression:   null,   // full expression descriptor from server
  transcript:   '',
};

export function useRobot() {
  const [state, setState] = useState(INITIAL_STATE);
  const speakRef       = useRef(null);
  const onSpeakDoneRef = useRef(null);

  const handleMessage = useCallback((msg) => {
    switch (msg.type) {

      case 'WELCOME':
        setState((s) => ({
          ...s,
          robotState: msg.state || ROBOT_STATES.SLEEPING,
          isAwake:    msg.state !== ROBOT_STATES.SLEEPING,
        }));
        break;

      case 'STATE_CHANGED':
        setState((s) => ({
          ...s,
          robotState: msg.state,
          emotion:    msg.emotion || s.emotion,
          isAwake:    msg.is_awake ?? msg.state !== ROBOT_STATES.SLEEPING,
        }));
        break;

      case 'ROBOT_RESPONSE':
        setState((s) => ({
          ...s,
          lastResponse: msg.text,
          lastSources:  msg.sources || [],
          transcript:   '',
        }));
        speakRef.current?.(msg.text, () => {
          onSpeakDoneRef.current?.();
        });
        break;

      case 'EMOTION_CHANGED':
        setState((s) => ({ ...s, emotion: msg.emotion }));
        break;

      case 'EXPRESSION_CHANGED':
        // Full expression descriptor from face controller
        setState((s) => ({ ...s, expression: msg }));
        break;

      case 'ANIMATION_CUE':
        setState((s) => ({
          ...s,
          animationCue: {
            animation:  msg.animation,
            target:     msg.target,
            params:     msg.params || {},
            frames:     msg.frames || [],
            duration_ms: msg.duration_ms,
          },
        }));
        // Auto-clear cue after it plays
        setTimeout(() => {
          setState((s) => ({ ...s, animationCue: null }));
        }, (msg.duration_ms || 2000) + 100);
        break;

      default:
        break;
    }
  }, []);

  const setTranscript    = useCallback((t) => setState((s) => ({ ...s, transcript: t })), []);
  const clearAnimCue     = useCallback(()  => setState((s) => ({ ...s, animationCue: null })), []);

  return {
    ...state,
    handleMessage,
    setTranscript,
    clearAnimCue,
    speakRef,
    onSpeakDoneRef,
  };
}
