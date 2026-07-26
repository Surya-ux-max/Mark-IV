import * as THREE from 'three';

/**
 * Object-Oriented Class representing the concentric spinning AI Reactor Core.
 * Mounts concentric orbital rings, glowing cores, and spinning sub-particles.
 */
export class HologramCore {
  constructor(scene) {
    this.scene = scene;
    this.group = new THREE.Group();
    
    // Child meshes tracking lists
    this.rings = [];
    this.centralSphere = null;
    this.innerSphere = null;
    this.orbitalParticles = null;
    
    this.particleCount = 200;
    this.pOrbits = [];
    this.pSpeeds = [];

    this.build();
    
    // Add to scene initially scaled down
    this.group.scale.set(0.0001, 0.0001, 0.0001);
    this.scene.add(this.group);
  }

  // Constructs the internal geometries and materials
  build() {
    // 1. Central pulsing core sphere
    const sphereGeo = new THREE.SphereGeometry(0.5, 24, 24);
    const sphereMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.85,
      wireframe: true
    });
    this.centralSphere = new THREE.Mesh(sphereGeo, sphereMat);
    this.group.add(this.centralSphere);

    // Inner solid core sphere
    const innerGeo = new THREE.SphereGeometry(0.24, 16, 16);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.95
    });
    this.innerSphere = new THREE.Mesh(innerGeo, innerMat);
    this.group.add(this.innerSphere);

    // 2. Concentric spinning orbital rings
    const ringParams = [
      { radius: 0.9, width: 0.03, color: 0xffffff, rotSpeed: { x: 0.8, y: 0.5, z: 0.1 } },
      { radius: 1.25, width: 0.02, color: 0x888888, rotSpeed: { x: -0.4, y: 0.9, z: -0.3 } },
      { radius: 1.6, width: 0.035, color: 0xcccccc, rotSpeed: { x: 0.2, y: -0.3, z: 1.1 } },
      { radius: 1.95, width: 0.015, color: 0x444444, rotSpeed: { x: 0.5, y: 0.6, z: -0.5 } }
    ];

    ringParams.forEach(param => {
      const ringGeo = new THREE.RingGeometry(param.radius - param.width, param.radius + param.width, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: param.color,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.65
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      
      // Set random initial rotations
      ringMesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
      this.group.add(ringMesh);
      this.rings.push({ mesh: ringMesh, speed: param.rotSpeed });
    });

    // 3. Orbiting reactor sub-particles
    const pGeo = new THREE.BufferGeometry();
    const pPos = new Float32Array(this.particleCount * 3);

    for (let i = 0; i < this.particleCount; i++) {
      const dist = 0.65 + Math.random() * 1.5;
      const angle = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      
      pPos[i * 3] = dist * Math.sin(phi) * Math.sin(angle);
      pPos[i * 3 + 1] = dist * Math.cos(phi);
      pPos[i * 3 + 2] = dist * Math.sin(phi) * Math.cos(angle);

      this.pSpeeds.push(0.5 + Math.random() * 1.5);
      this.pOrbits.push({
        dist, 
        angle, 
        phi, 
        axis: new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize()
      });
    }

    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
    const pMat = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.045,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });
    this.orbitalParticles = new THREE.Points(pGeo, pMat);
    this.group.add(this.orbitalParticles);
  }

  // Animation ticks called inside the render loop
  update(time, isVisualizer = false, audioLevel = 0) {
    // 1. Rotate Concentric Rings
    this.rings.forEach(r => {
      r.mesh.rotation.x += r.speed.x * 0.01;
      r.mesh.rotation.y += r.speed.y * 0.01;
      r.mesh.rotation.z += r.speed.z * 0.01;
    });

    // 2. Scale central core representing the reactor engine load / visualizer pulse
    const pulse = 1.0 + Math.sin(time * 5.5) * 0.08 + (isVisualizer ? audioLevel * 0.55 : 0);
    this.centralSphere.scale.set(pulse, pulse, pulse);
    this.innerSphere.scale.set(1.0 + Math.cos(time * 8.5) * 0.04, 1.0 + Math.cos(time * 8.5) * 0.04, 1.0 + Math.cos(time * 8.5) * 0.04);

    // 3. Rotate entire group slowly
    this.group.rotation.y = time * 0.12;

    // 4. Update orbital particle paths
    const positions = this.orbitalParticles.geometry.attributes.position.array;
    for (let i = 0; i < this.particleCount; i++) {
      const speed = this.pSpeeds[i] * (1.0 + audioLevel * 2.0);
      this.pOrbits[i].angle += speed * 0.0055;
      
      const orb = this.pOrbits[i];
      const rad = orb.dist * (1.0 + Math.sin(time * speed + i) * 0.04 + audioLevel * 0.12);
      
      const x = rad * Math.sin(orb.phi) * Math.sin(orb.angle);
      const y = rad * Math.cos(orb.phi);
      const z = rad * Math.sin(orb.phi) * Math.cos(orb.angle);

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;
    }
    this.orbitalParticles.geometry.attributes.position.needsUpdate = true;
  }

  // Scales the core up or down during transition phases
  setScale(scaleVal) {
    this.group.scale.set(scaleVal, scaleVal, scaleVal);
  }
}
