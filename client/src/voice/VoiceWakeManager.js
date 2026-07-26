// Object-Oriented Voice manager encapsulating SpeechRecognition command loop and permissions
export class VoiceWakeManager {
  constructor({ onListening, onHeard, onStatusChange, onCommand }) {
    this.onListening = onListening || (() => {});
    this.onHeard = onHeard || (() => {});
    this.onStatusChange = onStatusChange || (() => {});
    this.onCommand = onCommand || (() => {});
    this.recognition = null;
    this.status = 'STANDBY'; // STANDBY, AWAITING_PERMISSION, LISTENING, HEARD, ERROR, NOT_SUPPORTED, PERMISSION_DENIED
    this.mode = 'WAKE'; // WAKE, COMMAND
  }

  // Instantiates the browser SpeechRecognition object (if supported)
  init() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      this.updateStatus('NOT_SUPPORTED');
      return false;
    }

    try {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';

      this.recognition.onstart = () => {
        this.updateStatus('LISTENING');
        this.onListening();
      };

      this.recognition.onerror = (e) => {
        console.warn("VoiceWakeManager SpeechRecognition error:", e);
        if (e.error === 'not-allowed') {
          this.updateStatus('PERMISSION_DENIED');
        } else {
          this.updateStatus('ERROR');
        }
      };

      this.recognition.onend = () => {
        // Auto-restart if we are still active
        if (this.status === 'LISTENING') {
          try { this.recognition.start(); } catch(err) {}
        }
      };

      this.recognition.onresult = (event) => {
        const lastResultIndex = event.results.length - 1;
        const text = event.results[lastResultIndex][0].transcript.trim();
        console.log(`VoiceWakeManager heard in [${this.mode}] mode:`, text);

        if (this.mode === 'WAKE') {
          const lowerText = text.toLowerCase();
          if (
            lowerText.includes('wake up survex') || 
            lowerText.includes('wake up') || 
            lowerText.includes('survex') || 
            lowerText.includes('surve x')
          ) {
            this.updateStatus('HEARD');
            this.onHeard();
            // Switch mode to COMMAND to capture subsequent dialog queries
            this.mode = 'COMMAND';
            this.updateStatus('LISTENING');
          }
        } else if (this.mode === 'COMMAND') {
          this.onCommand(text);
        }
      };

      this.updateStatus('STANDBY');
      return true;
    } catch (err) {
      console.error("Failed to initialize SpeechRecognition:", err);
      this.updateStatus('NOT_SUPPORTED');
      return false;
    }
  }

  // Set command vs wake mode
  setMode(mode) {
    this.mode = mode;
  }

  // Start listening directly
  startListeningDirectly() {
    this.status = 'LISTENING';
    if (this.recognition) {
      try {
        this.recognition.start();
      } catch (e) {
        // already active
      }
    }
  }

  // Explicitly prompt device for microphone stream permission
  enable() {
    if (this.status === 'NOT_SUPPORTED') return;

    this.updateStatus('AWAITING_PERMISSION');

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // Stop stream immediately to release hardware
        stream.getTracks().forEach(track => track.stop());

        // Now safe to start SpeechRecognition
        if (!this.recognition) {
          this.init();
        }

        this.startListeningDirectly();
      })
      .catch(err => {
        console.error("VoiceWakeManager microphone denied:", err);
        this.updateStatus('PERMISSION_DENIED');
      });
  }

  // Stop recognition
  stop() {
    this.status = 'STANDBY';
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
    }
  }

  // Update status string
  updateStatus(newStatus) {
    this.status = newStatus;
    this.onStatusChange(newStatus);
  }
}
export default VoiceWakeManager;
