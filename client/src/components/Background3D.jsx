/**
 * Background3D.jsx — Bright User-Lovable 3D Stage for CSE Brain
 *
 * Designed for light/bright backgrounds:
 * - Soft vibrant point lights matching state colors.
 * - Floating pastel glass-like polyhedrons & soft particle dust.
 * - Smooth interactive camera parallax.
 */

import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const STATE_COLORS = {
  SLEEPING:  0x6366f1, // Soft Indigo
  IDLE:      0x0284c7, // Sky Blue / Cyan
  LISTENING: 0x2563eb, // Royal Blue
  THINKING:  0xf59e0b, // Warm Amber
  SPEAKING:  0x10b981, // Emerald Green
  GREETING:  0xec4899, // Lovable Pink
  OBSERVING: 0x0284c7, // Cyan
  ERROR:     0xef4444, // Red
};

export default function Background3D({ robotState = 'IDLE' }) {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      60,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.z = 18;

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Lights for Bright Theme
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(STATE_COLORS[robotState] || 0x0284c7, 3, 40);
    pointLight1.position.set(6, 6, 8);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xa855f7, 2, 35);
    pointLight2.position.set(-6, -6, 6);
    scene.add(pointLight2);

    // Floating Pastel Polyhedrons
    const floatingGroup = new THREE.Group();
    const shapes = [];
    const geoms = [
      new THREE.IcosahedronGeometry(0.55, 0),
      new THREE.OctahedronGeometry(0.65, 0),
      new THREE.TetrahedronGeometry(0.45, 0),
    ];

    for (let i = 0; i < 14; i++) {
      const g = geoms[i % geoms.length];
      const mat = new THREE.MeshStandardMaterial({
        color: i % 2 === 0 ? (STATE_COLORS[robotState] || 0x0284c7) : 0xc084fc,
        metalness: 0.2,
        roughness: 0.1,
        transparent: true,
        opacity: 0.3,
        wireframe: i % 2 === 0,
      });
      const mesh = new THREE.Mesh(g, mat);

      const radius = 10 + Math.random() * 8;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);

      mesh.position.set(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi) - 6
      );

      mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);

      shapes.push({
        mesh,
        rotSpeedX: (Math.random() - 0.5) * 0.015,
        rotSpeedY: (Math.random() - 0.5) * 0.015,
        floatSpeed: 0.5 + Math.random() * 1.2,
        initialY: mesh.position.y,
      });
      floatingGroup.add(mesh);
    }
    scene.add(floatingGroup);

    // Particle Dust Field
    const particleCount = 800;
    const pPositions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      pPositions[i * 3 + 0] = (Math.random() - 0.5) * 45;
      pPositions[i * 3 + 1] = (Math.random() - 0.5) * 45;
      pPositions[i * 3 + 2] = (Math.random() - 0.5) * 35 - 5;
    }

    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPositions, 3));

    const pMat = new THREE.PointsMaterial({
      color: STATE_COLORS[robotState] || 0x0284c7,
      size: 0.09,
      transparent: true,
      opacity: 0.35,
    });

    const particles = new THREE.Points(pGeo, pMat);
    scene.add(particles);

    // Mouse Parallax
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (e) => {
      mouseX = (e.clientX - window.innerWidth / 2) * 0.0005;
      mouseY = (e.clientY - window.innerHeight / 2) * 0.0005;
    };
    window.addEventListener('mousemove', handleMouseMove);

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // Animation Loop
    let clock = new THREE.Clock();
    let animId;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();

      targetX += (mouseX - targetX) * 0.05;
      targetY += (mouseY - targetY) * 0.05;
      camera.position.x = targetX * 3;
      camera.position.y = -targetY * 3;
      camera.lookAt(scene.position);

      shapes.forEach((s) => {
        s.mesh.rotation.x += s.rotSpeedX;
        s.mesh.rotation.y += s.rotSpeedY;
        s.mesh.position.y = s.initialY + Math.sin(elapsed * s.floatSpeed) * 0.35;
      });

      particles.rotation.y = elapsed * 0.015;

      renderer.render(scene, camera);
    };

    animate();

    container._threeState = { pMat, pointLight1 };

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  useEffect(() => {
    const container = mountRef.current;
    if (!container || !container._threeState) return;

    const hexColor = STATE_COLORS[robotState] || 0x0284c7;
    const { pMat, pointLight1 } = container._threeState;

    if (pMat) pMat.color.setHex(hexColor);
    if (pointLight1) pointLight1.color.setHex(hexColor);
  }, [robotState]);

  return (
    <div
      ref={mountRef}
      style={{
        position: 'fixed',
        inset: 0,
        pointerEvents: 'none',
        zIndex: 0,
      }}
    />
  );
}
