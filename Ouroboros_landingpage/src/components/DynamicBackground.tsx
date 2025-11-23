import { useEffect, useRef } from 'react';

export function DynamicBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const setCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);

    // Particle system for neural network effect
    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;
      alpha: number;

      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1;
        this.alpha = Math.random() * 0.5 + 0.2;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      }

      draw() {
        if (!ctx) return;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200, 150, 255, ${this.alpha})`;
        ctx.fill();
      }
    }

    // Create particles
    const particles: Particle[] = [];
    const particleCount = 100;
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    // Animation loop
    let animationFrame: number;
    let time = 0;

    const animate = () => {
      time += 0.005;
      
      // Clear canvas with fade effect
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particles.forEach(particle => {
        particle.update();
        particle.draw();
      });

      // Draw connections between close particles
      particles.forEach((p1, i) => {
        particles.slice(i + 1).forEach(p2 => {
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 150) {
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            const alpha = (1 - distance / 150) * 0.3;
            ctx.strokeStyle = `rgba(180, 130, 255, ${alpha})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        });
      });

      // Draw Ouroboros-inspired spiral energy
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const maxRadius = Math.max(canvas.width, canvas.height) * 0.6;

      for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        const offset = (time + i * 2) % (Math.PI * 2);
        for (let angle = 0; angle < Math.PI * 4; angle += 0.1) {
          const radius = (angle / (Math.PI * 4)) * maxRadius;
          const x = centerX + Math.cos(angle + offset) * radius;
          const y = centerY + Math.sin(angle + offset) * radius;
          
          if (angle === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        const alpha = 0.03 + Math.sin(time * 2 + i) * 0.02;
        ctx.strokeStyle = `rgba(220, 180, 255, ${alpha})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      animationFrame = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', setCanvasSize);
      cancelAnimationFrame(animationFrame);
    };
  }, []);

  return (
    <>
      {/* Animated gradient background layers */}
      <div className="fixed inset-0 z-0">
        {/* Base gradient */}
        <div 
          className="absolute inset-0 animate-gradient-shift"
          style={{
            background: 'radial-gradient(ellipse at 20% 30%, rgba(147, 51, 234, 0.4) 0%, transparent 50%), radial-gradient(ellipse at 80% 70%, rgba(219, 39, 119, 0.3) 0%, transparent 50%), radial-gradient(ellipse at 50% 50%, rgba(59, 130, 246, 0.2) 0%, transparent 50%), linear-gradient(135deg, #1a0b2e 0%, #16213e 25%, #0f3460 50%, #533483 75%, #7b2cbf 100%)',
          }}
        />
        
        {/* Layered moving gradients */}
        <div 
          className="absolute inset-0 opacity-60 animate-gradient-rotate"
          style={{
            background: 'radial-gradient(circle at 30% 50%, rgba(168, 85, 247, 0.4) 0%, transparent 50%)',
          }}
        />
        <div 
          className="absolute inset-0 opacity-40 animate-gradient-rotate-reverse"
          style={{
            background: 'radial-gradient(circle at 70% 50%, rgba(236, 72, 153, 0.3) 0%, transparent 50%)',
          }}
        />
        
        {/* Shimmer effect */}
        <div 
          className="absolute inset-0 opacity-30 animate-shimmer"
          style={{
            background: 'linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%)',
            backgroundSize: '200% 200%',
          }}
        />
      </div>

      {/* Particle canvas overlay */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 z-0 pointer-events-none"
        style={{ opacity: 0.8 }}
      />

      {/* Vignette effect */}
      <div 
        className="fixed inset-0 z-0 pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.4) 100%)',
        }}
      />
    </>
  );
}
