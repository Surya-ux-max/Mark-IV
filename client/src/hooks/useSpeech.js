/**
 * useSpeech.js — Web Speech API wrapper for STT + TTS.
 *
 * STT: SpeechRecognition (browser listens, sends text to server)
 * TTS: SpeechSynthesis (browser speaks server's response text)
 */

import { useCallback, useEffect, useRef, useState } from 'react';

export function useSpeech({ onTranscript, onSpeakStart, onSpeakEnd, isRobotAwake }) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);

  // ── STT Setup ─────────────────────────────────────────────────────────────
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-IN';
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onTranscript?.(transcript);
    };

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognitionRef.current = recognition;
  }, [onTranscript]);

  // ── Start Listening ───────────────────────────────────────────────────────
  const startListening = useCallback(() => {
    if (!isRobotAwake || isListening || isSpeaking) return;
    try {
      synthRef.current?.cancel(); // Stop any ongoing TTS first
      recognitionRef.current?.start();
    } catch (e) {
      console.warn('STT start error:', e);
    }
  }, [isRobotAwake, isListening, isSpeaking]);

  // ── Stop Listening ────────────────────────────────────────────────────────
  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    setIsListening(false);
  }, []);

  // ── Speak Text (TTS) ──────────────────────────────────────────────────────
  const speak = useCallback((text, onDone) => {
    if (!text || !synthRef.current) return;

    // Stop any current speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN';
    utterance.rate = 0.95;
    utterance.pitch = 1.05;
    utterance.volume = 1.0;

    // Try to pick a natural voice
    const voices = synthRef.current.getVoices();
    const preferred = voices.find(
      (v) => v.lang.startsWith('en') && v.name.includes('Female')
    ) || voices.find((v) => v.lang.startsWith('en'));
    if (preferred) utterance.voice = preferred;

    utterance.onstart = () => {
      setIsSpeaking(true);
      onSpeakStart?.();
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      onSpeakEnd?.();
      onDone?.();
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      onSpeakEnd?.();
    };

    synthRef.current.speak(utterance);
  }, [onSpeakStart, onSpeakEnd]);

  // ── Cancel TTS ────────────────────────────────────────────────────────────
  const cancelSpeech = useCallback(() => {
    synthRef.current?.cancel();
    setIsSpeaking(false);
  }, []);

  return {
    isListening,
    isSpeaking,
    startListening,
    stopListening,
    speak,
    cancelSpeech,
    isSupported: !!window.SpeechRecognition || !!window.webkitSpeechRecognition,
  };
}
