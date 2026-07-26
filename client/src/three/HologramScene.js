import * as THREE from 'three';
import { HologramCore } from './HologramCore';

/**
 * Object-Oriented Scene Manager Class encapsulating Three.js lifecycle, renderer,
 * camera, lighting, and pixel-dot text animations for the welcome intro.
 */
export class HologramScene {
  constructor(containerElement, initialPhase = 'HELMET_ASSEMBLING', maskImage = null, greetingText = "GOOD MORNING, SURYA") {
    this.container = containerElement;
    this.phase = initialPhase;
    this.maskImage = maskImage;
    this.greetingText = greetingText;
    this.time = 0;
    this.clock = new THREE.Clock();

    this.scene = null;
    this.camera = null;
    this.renderer = null;

    // Sub-modules
    this.core = null;

    // Meshes
    this.particles = null;

    // Text Particle coordinate pools
    this.survexPoints = [];
    this.greetingPoints = [];

    this.startPositions = null;
    this.survexPositions = null;
    this.greetingPositions = null;
    this.particleColors = null;

    // Animation trackers
    this.lerpProgress = 0;      // Start -> SurveX
    this.scanProgress = 0;      // SurveX -> Greeting
    this.dissolveProgress = 0;  // Greeting -> Reactor Core
    this.animationFrameId = null;

    this.init();
  }

  // Set up Three.js scene, camera, and render layers
  init() {
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;

    this.scene = new THREE.Scene();
    
    this.camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    this.camera.position.set(0, 0, 7.5);

    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(w, h);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // Minimal white lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    this.scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.5, 20);
    pointLight.position.set(0, 2, 5);
    this.scene.add(pointLight);

    // Generate text pixel coordinates
    this.survexPoints = this.generateTextPoints("SurveX", 400, 100, 52, 0.038);
    this.greetingPoints = this.generateTextPoints(this.greetingText, 600, 100, 26, 0.032);

    // Setup text points mesh
    this.setupTextPointsMesh();
    
    // Core AI Reactor setup (styled in white/grey)
    this.core = new HologramCore(this.scene);

    // Resize bind
    this.resizeHandler = this.onWindowResize.bind(this);
    window.addEventListener('resize', this.resizeHandler);

    // Start loop
    this.tick();
  }

  // Generates 2D text outline pixel coordinates using HTML5 Canvas
  generateTextPoints(text, width, height, fontSize, scale) {
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    // Clean modern Sans-serif font
    ctx.font = `bold ${fontSize}px system-ui, -apple-system, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, width / 2, height / 2);

    const imgData = ctx.getImageData(0, 0, width, height).data;
    const points = [];

    // Scan pixel alphas to form outline dots
    for (let y = 0; y < height; y += 2) { // step by 2 for a clean pixelated grid effect
      for (let x = 0; x < width; x += 2) {
        const idx = (y * width + x) * 4;
        const a = imgData[idx + 3];
        if (a > 128) {
          const px = (x - width / 2) * scale;
          const py = (height / 2 - y) * scale;
          const pz = (Math.random() - 0.5) * 0.03;
          points.push({ x: px, y: py, z: pz });
        }
      }
    }
    return points.length > 0 ? points : [{ x: 0, y: 0, z: 0 }];
  }

  // Setup main particle system
  setupTextPointsMesh() {
    const pCount = 3800; // constant density
    this.particleCount = pCount;

    this.startPositions = new Float32Array(pCount * 3);
    this.survexPositions = new Float32Array(pCount * 3);
    this.greetingPositions = new Float32Array(pCount * 3);
    this.particleColors = new Float32Array(pCount * 3);

    // 1. Start positions (scattered random particles far away)
    for (let i = 0; i < pCount; i++) {
      this.startPositions[i * 3] = (Math.random() - 0.5) * 15;
      this.startPositions[i * 3 + 1] = (Math.random() - 0.5) * 15;
      this.startPositions[i * 3 + 2] = (Math.random() - 0.5) * 15;

      // Color: pure white
      this.particleColors[i * 3] = 1.0;
      this.particleColors[i * 3 + 1] = 1.0;
      this.particleColors[i * 3 + 2] = 1.0;
    }

    // 2. Map SurveX text target coordinates
    for (let i = 0; i < pCount; i++) {
      const pt = this.survexPoints[i % this.survexPoints.length];
      this.survexPositions[i * 3] = pt.x;
      this.survexPositions[i * 3 + 1] = pt.y;
      this.survexPositions[i * 3 + 2] = pt.z;
    }

    // 3. Map greeting text target coordinates
    for (let i = 0; i < pCount; i++) {
      const pt = this.greetingPoints[i % this.greetingPoints.length];
      this.greetingPositions[i * 3] = pt.x;
      this.greetingPositions[i * 3 + 1] = pt.y;
      this.greetingPositions[i * 3 + 2] = pt.z;
    }

    // Buffer geometry compilation
    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(this.startPositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(this.particleColors, 3));

    // Custom pixel-dot circular texture programmatically
    const c = document.createElement('canvas');
    c.width = 16;
    c.height = 16;
    const ctx = c.getContext('2d');
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.3, 'rgba(255, 255, 255, 0.7)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 16, 16);
    const particleTexture = new THREE.CanvasTexture(c);
    particleTexture.needsUpdate = true;

    // Bigger particle size to match dot grid design
    const particleMat = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      map: particleTexture,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    this.particles = new THREE.Points(particleGeo, particleMat);
    this.scene.add(this.particles);
  }

  // Handle browser resize
  onWindowResize() {
    if (!this.container || !this.renderer) return;
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h);
  }

  // Set cinematic state phase
  setPhase(newPhase) {
    this.phase = newPhase;
  }

  // Rendering ticks
  tick() {
    this.animationFrameId = requestAnimationFrame(this.tick.bind(this));
    
    const time = this.clock.getElapsedTime();
    const delta = this.clock.getDelta();
    this.time = time;

    const mockAudioLevel = Math.max(0, Math.sin(time * 8) * 0.15 + 0.1);

    // Fast-track snapping if phase is scanning/awaken but assembly was skipped (voice wake trigger)
    if ((this.phase === 'HELMET_SCANNING' || this.phase === 'HELMET_AWAKEN') && this.lerpProgress < 1.0) {
      this.lerpProgress = 1.0;
    }

    const posAttr = this.particles.geometry.attributes.position;

    // PHASE 1: Morph to "SurveX" Text
    if (this.phase === 'HELMET_ASSEMBLING') {
      this.lerpProgress = Math.min(1.0, this.lerpProgress + 0.007); // quicker assembly
      const easeVal = Math.pow(this.lerpProgress, 2.0);

      for (let i = 0; i < posAttr.count; i++) {
        const sx = this.startPositions[i * 3];
        const sy = this.startPositions[i * 3 + 1];
        const sz = this.startPositions[i * 3 + 2];

        const tx = this.survexPositions[i * 3];
        const ty = this.survexPositions[i * 3 + 1];
        const tz = this.survexPositions[i * 3 + 2];

        posAttr.array[i * 3] = THREE.MathUtils.lerp(sx, tx, easeVal);
        posAttr.array[i * 3 + 1] = THREE.MathUtils.lerp(sy, ty, easeVal);
        posAttr.array[i * 3 + 2] = THREE.MathUtils.lerp(sz, tz, easeVal);
      }
      posAttr.needsUpdate = true;

      // Keep camera static and focused
      this.camera.position.set(0, 0, 7.5);
      this.camera.lookAt(0, 0, 0);
    }

    // PHASE 2: Morph from "SurveX" to "GOOD MORNING, SURYA"
    else if (this.phase === 'HELMET_SCANNING') {
      this.scanProgress = Math.min(1.0, this.scanProgress + 0.015);
      const easeVal = Math.pow(this.scanProgress, 1.8);

      for (let i = 0; i < posAttr.count; i++) {
        const sx = this.survexPositions[i * 3];
        const sy = this.survexPositions[i * 3 + 1];
        const sz = this.survexPositions[i * 3 + 2];

        const tx = this.greetingPositions[i * 3];
        const ty = this.greetingPositions[i * 3 + 1];
        const tz = this.greetingPositions[i * 3 + 2];

        posAttr.array[i * 3] = THREE.MathUtils.lerp(sx, tx, easeVal);
        posAttr.array[i * 3 + 1] = THREE.MathUtils.lerp(sy, ty, easeVal);
        posAttr.array[i * 3 + 2] = THREE.MathUtils.lerp(sz, tz, easeVal);
      }
      posAttr.needsUpdate = true;

      this.camera.position.set(0, 0, 7.5);
      this.camera.lookAt(0, 0, 0);
    }

    // PHASE 3: Hold greeting text
    else if (this.phase === 'HELMET_AWAKEN') {
      // Ensure points are fully greeting-aligned
      for (let i = 0; i < posAttr.count; i++) {
        posAttr.array[i * 3] = this.greetingPositions[i * 3];
        posAttr.array[i * 3 + 1] = this.greetingPositions[i * 3 + 1];
        posAttr.array[i * 3 + 2] = this.greetingPositions[i * 3 + 2];
      }
      posAttr.needsUpdate = true;

      this.camera.position.set(0, 0, 7.5);
      this.camera.lookAt(0, 0, 0);
    }

    // PHASE 4: Dissolve points into central core
    else if (this.phase === 'HELMET_DISSOLVING') {
      this.dissolveProgress = Math.min(1.0, this.dissolveProgress + 0.018);

      // Scale Core reactor up from center
      this.core.setScale(this.dissolveProgress);
      this.core.update(time, false, 0);

      // Melt text particles into core orbit paths
      for (let i = 0; i < posAttr.count; i++) {
        const gx = this.greetingPositions[i * 3];
        const gy = this.greetingPositions[i * 3 + 1];
        const gz = this.greetingPositions[i * 3 + 2];

        const radius = 0.55 + (i % 15) * 0.12;
        const theta = (i * 0.1) + (time * (0.8 + (i % 5) * 0.1));
        const rx = radius * Math.cos(theta);
        const ry = (i % 2 === 0 ? 1 : -1) * ((i % 10) * 0.15) * Math.sin(time + i);
        const rz = radius * Math.sin(theta);

        posAttr.array[i * 3] = THREE.MathUtils.lerp(gx, rx, this.dissolveProgress);
        posAttr.array[i * 3 + 1] = THREE.MathUtils.lerp(gy, ry, this.dissolveProgress);
        posAttr.array[i * 3 + 2] = THREE.MathUtils.lerp(gz, rz, this.dissolveProgress);
      }
      posAttr.needsUpdate = true;
      this.particles.material.opacity = THREE.MathUtils.lerp(0.9, 0.4, this.dissolveProgress);

      this.camera.position.set(0, 0, 7.5);
      this.camera.lookAt(0, 0, 0);
    }

    // PHASE 5: Dashboard active
    else if (this.phase === 'DASHBOARD_ACTIVE') {
      this.core.update(time, true, mockAudioLevel);

      // Spin particles around core reactor
      for (let i = 0; i < posAttr.count; i++) {
        const radius = 0.65 + (i % 20) * 0.08;
        const speed = 0.6 + (i % 8) * 0.2;
        const theta = (i * 0.12) + (time * speed);
        
        posAttr.array[i * 3] = radius * Math.cos(theta);
        posAttr.array[i * 3 + 1] = Math.sin(time * 0.5 + i) * 0.6;
        posAttr.array[i * 3 + 2] = radius * Math.sin(theta);
      }
      posAttr.needsUpdate = true;
      this.particles.material.opacity = 0.25;

      this.camera.position.x = Math.sin(time * 0.15) * 0.5;
      this.camera.position.y = Math.cos(time * 0.1) * 0.3;
      this.camera.position.z = 6.2;
      this.camera.lookAt(0, 0, 0);
    }

    this.renderer.render(this.scene, this.camera);
  }

  // Cleanup to prevent memory leaks
  destroy() {
    window.removeEventListener('resize', this.resizeHandler);
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.renderer) {
      if (this.container && this.renderer.domElement) {
        try {
          this.container.removeChild(this.renderer.domElement);
        } catch(e) {}
      }
      this.renderer.dispose();
    }
  }
}
export default HologramScene;
