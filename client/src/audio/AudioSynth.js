// Object-Oriented Audio Synthesizer class using Web Audio API and Speech Synthesis API
export class AudioSynth {
  constructor() {
    this.ctx = null;
    this.ambientOsc = null;
    this.ambientFilter = null;
    this.ambientGain = null;
  }

  // Initialize the audio context
  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Starts the low-frequency ambient electronic background hum
  startAmbient() {
    this.init();
    if (this.ambientOsc) return;

    try {
      this.ambientGain = this.ctx.createGain();
      this.ambientGain.gain.setValueAtTime(0.0, this.ctx.currentTime);
      this.ambientGain.gain.linearRampToValueAtTime(0.12, this.ctx.currentTime + 3);

      this.ambientFilter = this.ctx.createBiquadFilter();
      this.ambientFilter.type = 'lowpass';
      this.ambientFilter.frequency.setValueAtTime(150, this.ctx.currentTime);

      const osc1 = this.ctx.createOscillator();
      osc1.type = 'sawtooth';
      osc1.frequency.setValueAtTime(55, this.ctx.currentTime); // A1 note

      const osc2 = this.ctx.createOscillator();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(55.5, this.ctx.currentTime); // slightly detuned

      osc1.connect(this.ambientFilter);
      osc2.connect(this.ambientFilter);
      this.ambientFilter.connect(this.ambientGain);
      this.ambientGain.connect(this.ctx.destination);

      osc1.start();
      osc2.start();

      this.ambientOsc = [osc1, osc2];
    } catch (e) {
      console.warn("Failed to start ambient audio:", e);
    }
  }

  // Stops the ambient hum with a clean fade-out
  stopAmbient() {
    if (this.ambientGain && this.ctx) {
      try {
        const now = this.ctx.currentTime;
        this.ambientGain.gain.cancelScheduledValues(now);
        this.ambientGain.gain.setValueAtTime(this.ambientGain.gain.value, now);
        this.ambientGain.gain.linearRampToValueAtTime(0.0, now + 1.5);
        
        setTimeout(() => {
          if (this.ambientOsc) {
            this.ambientOsc.forEach(osc => {
              try { osc.stop(); } catch(e) {}
            });
            this.ambientOsc = null;
          }
          this.ambientGain = null;
          this.ambientFilter = null;
        }, 1600);
      } catch (e) {
        console.warn("Failed to stop ambient audio:", e);
      }
    }
  }

  // Futuristic wake confirmation chime (double beep major interval)
  playWakeChime() {
    this.init();
    try {
      const now = this.ctx.currentTime;
      
      // Chime 1 (Lower Note)
      const osc1 = this.ctx.createOscillator();
      const gain1 = this.ctx.createGain();
      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(523.25, now); // C5
      gain1.gain.setValueAtTime(0.08, now);
      gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.3);
      osc1.connect(gain1);
      gain1.connect(this.ctx.destination);
      osc1.start(now);
      osc1.stop(now + 0.35);

      // Chime 2 (Higher Note, delayed)
      const osc2 = this.ctx.createOscillator();
      const gain2 = this.ctx.createGain();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(783.99, now + 0.08); // G5
      gain2.gain.setValueAtTime(0.08, now + 0.08);
      gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.08 + 0.4);
      osc2.connect(gain2);
      gain2.connect(this.ctx.destination);
      osc2.start(now + 0.08);
      osc2.stop(now + 0.08 + 0.45);
    } catch (e) {}
  }

  // Quick system tick sound (for keyboard log feeds)
  playTick(frequency = 1200, duration = 0.03) {
    this.init();
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(frequency, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(frequency * 0.4, this.ctx.currentTime + duration);

      gain.gain.setValueAtTime(0.02, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {}
  }

  // Mechanical lock/snapping parts chime
  playLock(delay = 0) {
    this.init();
    try {
      const now = this.ctx.currentTime + delay;
      // High pitch metallic ping
      const oscMetal = this.ctx.createOscillator();
      const gainMetal = this.ctx.createGain();
      
      oscMetal.type = 'triangle';
      oscMetal.frequency.setValueAtTime(800, now);
      oscMetal.frequency.exponentialRampToValueAtTime(100, now + 0.15);

      gainMetal.gain.setValueAtTime(0.08, now);
      gainMetal.gain.exponentialRampToValueAtTime(0.0001, now + 0.15);

      oscMetal.connect(gainMetal);
      gainMetal.connect(this.ctx.destination);
      oscMetal.start(now);
      oscMetal.stop(now + 0.16);

      // Low mechanical thud
      const oscThud = this.ctx.createOscillator();
      const gainThud = this.ctx.createGain();
      
      oscThud.type = 'sine';
      oscThud.frequency.setValueAtTime(110, now);
      oscThud.frequency.linearRampToValueAtTime(40, now + 0.2);

      gainThud.gain.setValueAtTime(0.12, now);
      gainThud.gain.exponentialRampToValueAtTime(0.0001, now + 0.25);

      oscThud.connect(gainThud);
      gainThud.connect(this.ctx.destination);
      oscThud.start(now);
      oscThud.stop(now + 0.26);
    } catch (e) {}
  }

  // Sweeping laser scanner sound
  playLaser(duration = 2.0) {
    this.init();
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const filter = this.ctx.createBiquadFilter();
      const gain = this.ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(200, now);
      osc.frequency.linearRampToValueAtTime(450, now + duration * 0.5);
      osc.frequency.linearRampToValueAtTime(180, now + duration);

      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(800, now);
      filter.frequency.exponentialRampToValueAtTime(1800, now + duration * 0.5);
      filter.frequency.exponentialRampToValueAtTime(600, now + duration);
      filter.Q.setValueAtTime(8, now);

      gain.gain.setValueAtTime(0.0, now);
      gain.gain.linearRampToValueAtTime(0.04, now + 0.2);
      gain.gain.linearRampToValueAtTime(0.04, now + duration - 0.2);
      gain.gain.linearRampToValueAtTime(0.0, now + duration);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now);
      osc.stop(now + duration + 0.1);
    } catch (e) {}
  }

  // Deep low-frequency energy pulse when eyes light up
  playAwakenPulse() {
    this.init();
    try {
      const now = this.ctx.currentTime;

      // Primary deep sub-bass drop
      const oscBase = this.ctx.createOscillator();
      const gainBase = this.ctx.createGain();
      
      oscBase.type = 'sine';
      oscBase.frequency.setValueAtTime(90, now);
      oscBase.frequency.exponentialRampToValueAtTime(28, now + 2.0);

      gainBase.gain.setValueAtTime(0.0, now);
      gainBase.gain.linearRampToValueAtTime(0.35, now + 0.15); // sharp build-up
      gainBase.gain.exponentialRampToValueAtTime(0.0001, now + 2.5);

      oscBase.connect(gainBase);
      gainBase.connect(this.ctx.destination);
      oscBase.start(now);
      oscBase.stop(now + 2.6);

      // Mid-frequency synth buzz to give it a cinematic, electrical texture
      const oscBuzz = this.ctx.createOscillator();
      const filterBuzz = this.ctx.createBiquadFilter();
      const gainBuzz = this.ctx.createGain();

      oscBuzz.type = 'sawtooth';
      oscBuzz.frequency.setValueAtTime(110, now);
      
      filterBuzz.type = 'lowpass';
      filterBuzz.frequency.setValueAtTime(150, now);
      filterBuzz.frequency.exponentialRampToValueAtTime(1200, now + 0.15); // flash cut-off open
      filterBuzz.frequency.exponentialRampToValueAtTime(60, now + 1.2);    // sweep down

      gainBuzz.gain.setValueAtTime(0.0, now);
      gainBuzz.gain.linearRampToValueAtTime(0.18, now + 0.12);
      gainBuzz.gain.exponentialRampToValueAtTime(0.0001, now + 1.8);

      oscBuzz.connect(filterBuzz);
      filterBuzz.connect(gainBuzz);
      gainBuzz.connect(this.ctx.destination);

      oscBuzz.start(now);
      oscBuzz.stop(now + 1.9);

      // White noise explosion for energy shockwave
      const bufferSize = this.ctx.sampleRate * 1.5;
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }

      const noiseSource = this.ctx.createBufferSource();
      noiseSource.buffer = buffer;

      const noiseFilter = this.ctx.createBiquadFilter();
      noiseFilter.type = 'bandpass';
      noiseFilter.frequency.setValueAtTime(1000, now);
      noiseFilter.frequency.exponentialRampToValueAtTime(80, now + 1.5);
      noiseFilter.Q.setValueAtTime(3, now);

      const noiseGain = this.ctx.createGain();
      noiseGain.gain.setValueAtTime(0.0, now);
      noiseGain.gain.linearRampToValueAtTime(0.08, now + 0.08);
      noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);

      noiseSource.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(this.ctx.destination);

      noiseSource.start(now);
      noiseSource.stop(now + 1.6);

    } catch (e) {
      console.warn("Failed to play awaken pulse:", e);
    }
  }

  // Voice greeting: "Good morning, Surya. All systems are online."
  speakGreeting(callback) {
    if (!('speechSynthesis' in window)) {
      console.warn("Speech synthesis not supported in this browser.");
      if (callback) callback();
      return;
    }

    try {
      window.speechSynthesis.cancel();

      const text = "Good morning, Surya. All systems are online.";
      const utterance = new SpeechSynthesisUtterance(text);
      
      const voices = window.speechSynthesis.getVoices();
      let selectedVoice = null;
      
      const voicePriorities = [
        'google uk english male',
        'google us english male',
        'microsoft david',
        'en-gb',
        'en-us',
        'en'
      ];

      for (let priority of voicePriorities) {
        selectedVoice = voices.find(v => v.name.toLowerCase().includes(priority) || v.lang.toLowerCase().includes(priority));
        if (selectedVoice) break;
      }

      if (selectedVoice) {
        utterance.voice = selectedVoice;
      }

      utterance.pitch = 0.85; // slightly lower pitch
      utterance.rate = 0.88;  // slightly slower pacing (Jarvis style)
      utterance.volume = 1.0;

      utterance.onend = () => {
        if (callback) callback();
      };

      utterance.onerror = (e) => {
        console.warn("Speech utterance error:", e);
        if (callback) callback();
      };

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("Speech synthesis failed:", e);
      if (callback) callback();
    }
  }

  // Speak arbitrary text dynamically
  speak(text, callback) {
    if (!('speechSynthesis' in window)) {
      console.warn("Speech synthesis not supported.");
      if (callback) callback();
      return;
    }

    try {
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);
      const voices = window.speechSynthesis.getVoices();
      let selectedVoice = null;
      
      const voicePriorities = [
        'google uk english male',
        'google us english male',
        'microsoft david',
        'en-gb',
        'en-us',
        'en'
      ];

      for (let priority of voicePriorities) {
        selectedVoice = voices.find(v => v.name.toLowerCase().includes(priority) || v.lang.toLowerCase().includes(priority));
        if (selectedVoice) break;
      }

      if (selectedVoice) {
        utterance.voice = selectedVoice;
      }

      utterance.pitch = 0.85;
      utterance.rate = 0.88;
      utterance.volume = 1.0;

      utterance.onend = () => {
        if (callback) callback();
      };

      utterance.onerror = () => {
        if (callback) callback();
      };

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn("Speech synthesis error:", e);
      if (callback) callback();
    }
  }
}

// Export singleton instance
export const audioSynth = new AudioSynth();
