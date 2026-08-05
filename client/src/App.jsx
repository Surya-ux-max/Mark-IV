/**
 * App.jsx — Full-Body Layout for SurveX Virtual Robot (CSE Brain)
 */

import { useCallback, useEffect } from 'react';
import Background3D from './components/Background3D';
import RobotBody from './components/RobotBody';
import { useRobot } from './hooks/useRobot';
import { useSpeech } from './hooks/useSpeech';
import { useWebSocket } from './hooks/useWebSocket';
import './index.css';

const STATE_LABEL = {
  SLEEPING:  'SLEEPING',
  IDLE:      'STANDBY',
  LISTENING: 'LISTENING',
  THINKING:  'PROCESSING',
  SPEAKING:  'SPEAKING',
  GREETING:  'GREETING',
  OBSERVING: 'OBSERVING',
  ERROR:     'ERROR',
};

const STATE_COLOR = {
  SLEEPING:  '#3a5090',
  IDLE:      '#00e5ff',
  LISTENING: '#5599ff',
  THINKING:  '#ffbb00',
  SPEAKING:  '#00ffaa',
  GREETING:  '#cc77ff',
  OBSERVING: '#00e5ff',
  ERROR:     '#ff4455',
};

export default function App() {
  const robot = useRobot();
  const { connected, sessionId, send } = useWebSocket(robot.handleMessage);

  const speech = useSpeech({
    isRobotAwake: robot.isAwake,
    onTranscript: (text) => {
      robot.setTranscript(text);
      if (text && robot.isAwake) {
        send({ type: 'USER_MESSAGE', text, session_id: sessionId });
        send({ type: 'USER_STOPPED_SPEAKING' });
      }
    },
    onSpeakStart: () => send({ type: 'USER_STARTED_SPEAKING' }),
    onSpeakEnd: () => {},
  });

  useEffect(() => {
    robot.speakRef.current = (text, onDone) => {
      speech.speak(text, () => {
        send({ type: 'SPEAKING_DONE', session_id: sessionId });
        onDone?.();
      });
    };
  }, [speech.speak, send, sessionId]);

  const handleWakeToggle = useCallback(() => {
    if (robot.isAwake) {
      speech.cancelSpeech();
      send({ type: 'COMMAND', command: 'SLEEP' });
    } else {
      send({ type: 'COMMAND', command: 'WAKE_UP' });
    }
  }, [robot.isAwake, send, speech]);

  const handleMic = useCallback(() => {
    if (!robot.isAwake) return;
    if (speech.isListening) {
      speech.stopListening();
    } else {
      speech.cancelSpeech();
      speech.startListening();
      send({ type: 'USER_STARTED_SPEAKING', session_id: sessionId });
    }
  }, [robot.isAwake, speech, send, sessionId]);

  const color = STATE_COLOR[robot.robotState] || STATE_COLOR.IDLE;
  const label = STATE_LABEL[robot.robotState] || robot.robotState;

  return (
    <>
      {/* 3D Holographic Stage with Floating 3D Geometries & Interactive Mouse Parallax */}
      <Background3D robotState={robot.robotState} />

      <div className="bg-grid" />
      <div className="bg-radial" />

      <main className="app">

        {/* Header */}
        <div className="app-header">
          <div className="dept-title">Department of Computer Science &amp; Engineering</div>
          <div className="robot-name">CSE BRAIN</div>
        </div>

        {/* Status Badge */}
        <div
          className="status-badge"
          style={{ color, borderColor: `${color}60`, boxShadow: `0 0 24px ${color}25` }}
        >
          {robot.robotState === 'LISTENING' ? (
            <div className="listen-bars">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="listen-bar"
                  style={{ background: color, animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </div>
          ) : (
            <div className="status-dot" style={{ background: color, boxShadow: `0 0 10px ${color}` }} />
          )}
          {label}
        </div>

        {/* Full-Body Robot Stage */}
        <div className="robot-stage">
          <RobotBody
            robotState={robot.robotState}
            expression={robot.expression}
            emotion={robot.emotion}
            animationCue={robot.animationCue}
          />
        </div>

        {/* Response Panel */}
        <div
          className="response-panel"
          style={{ borderColor: `${color}25`, boxShadow: `0 0 35px ${color}12` }}
        >
          <div className="response-label">CSE BRAIN SAYS</div>
          <div className="response-text">
            {robot.transcript
              ? <span className="transcript-text">"{robot.transcript}"</span>
              : robot.lastResponse}
          </div>
          {robot.lastSources?.length > 0 && (
            <div className="sources-row">
              {robot.lastSources.map((s) => (
                <span key={s} className="source-chip">📚 {s}</span>
              ))}
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="controls-row">
          <div className="btn-row">
            {robot.isAwake && (
              <button
                id="mic-btn"
                className={`btn-mic ${speech.isListening ? 'listening' : ''}`}
                onClick={handleMic}
                title={speech.isListening ? 'Stop listening' : 'Start speaking'}
              >
                {speech.isListening ? '⏹' : '🎤'}
              </button>
            )}

            <button
              id="wake-btn"
              className={`btn-wake ${robot.isAwake ? 'btn-wake--awake' : 'btn-wake--sleep'}`}
              onClick={handleWakeToggle}
              disabled={!connected}
            >
              <div className={`conn-dot ${connected ? 'conn-dot--on' : 'conn-dot--off'}`} />
              {robot.isAwake ? '⏻ SLEEP' : '⏼ WAKE UP'}
            </button>
          </div>

          <div className="hint-text">
            {!connected
              ? '● CONNECTING TO SERVER...'
              : robot.isAwake
              ? speech.isListening
                ? '● LISTENING — SPEAK NOW'
                : '● TAP MIC OR SPEAK TO TALK'
              : '● TAP WAKE UP TO START'}
          </div>
        </div>

      </main>
    </>
  );
}
