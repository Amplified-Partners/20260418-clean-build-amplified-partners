import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';

export const SidecarComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // The Advertising Base Level: Slow Dolly-In + Rack Focus = Control & Relief

  // 1. The Slow Dolly-In (Control & Inevitability)
  // Scale goes from 1.0 to 1.15 over the entire 300 frames. 
  // This continuous, methodical move signals authority.
  const cameraScale = interpolate(frame, [0, 300], [1, 1.15], {
    extrapolateRight: 'clamp',
  });

  // 2. The Rack Focus (Relief from Chaos)
  // Background blur starts at 0, and smoothly slams to 24px just before Sidecar enters.
  const backgroundBlur = spring({
    frame: Math.max(0, frame - 15),
    fps,
    config: { damping: 200 },
  });
  const blurAmount = interpolate(backgroundBlur, [0, 1], [0, 24]);
  const bgOpacity = interpolate(backgroundBlur, [0, 1], [1, 0.3]);

  // 3. Sidecar Entry (The Solution arrives)
  const sidecarEntrance = spring({
    frame: Math.max(0, frame - 30),
    fps,
    config: { damping: 14, mass: 0.9 }, // Slight weight to make it feel grounded
  });
  const sidecarTranslateX = interpolate(sidecarEntrance, [0, 1], [400, 0]);
  const sidecarOpacity = interpolate(sidecarEntrance, [0, 1], [0, 1]);

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a', overflow: 'hidden' }}>
      
      {/* The Camera Layer */}
      <AbsoluteFill style={{ transform: `scale(${cameraScale})` }}>
        
        {/* The Chaotic Background (Simulated CRM / Desktop Noise) */}
        <AbsoluteFill style={{ 
          backgroundImage: 'url("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: `blur(${blurAmount}px)`,
          opacity: bgOpacity,
        }} />

        {/* The Sidecar UI Container */}
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'flex-end', padding: '80px' }}>
          
          {/* The Sidecar Vertical Ribbon */}
          <div style={{
            width: '420px',
            background: 'rgba(15, 15, 20, 0.85)',
            backdropFilter: 'blur(24px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '16px',
            padding: '36px',
            display: 'flex',
            flexDirection: 'column',
            gap: '28px',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05) inset',
            color: 'white',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            transform: `translateX(${sidecarTranslateX}px)`,
            opacity: sidecarOpacity,
          }}>
            
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', paddingBottom: '16px' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#3b82f6', boxShadow: '0 0 15px #3b82f6' }} />
              <div style={{ fontWeight: 700, letterSpacing: '0.1em', fontSize: '16px', color: '#f3f4f6' }}>SIDECAR</div>
            </div>

            {/* The Note (Pick-to-Light) */}
            <div style={{ borderLeft: '4px solid #3b82f6', paddingLeft: '20px' }}>
              <div style={{ color: '#60a5fa', fontWeight: 700, fontSize: '13px', letterSpacing: '0.05em', marginBottom: '12px' }}>
                CONTEXT SWITCH PREVENTED
              </div>
              <div style={{ fontSize: '19px', lineHeight: 1.5, fontWeight: 500, color: '#f8fafc', marginBottom: '28px' }}>
                Sarah just quoted the Jesmond job. Mirror quote amount (£450) to Xero?
              </div>

              {/* The Binary Choice */}
              <div style={{ display: 'flex', gap: '16px' }}>
                <div style={{
                  flex: 1, background: '#2563eb', padding: '16px', borderRadius: '8px', 
                  textAlign: 'center', fontWeight: 700, letterSpacing: '0.05em', fontSize: '15px',
                  boxShadow: '0 4px 20px rgba(37, 99, 235, 0.4)'
                }}>
                  YES
                </div>
                <div style={{
                  flex: 1, background: 'rgba(255,255,255,0.05)', padding: '16px', borderRadius: '8px', 
                  textAlign: 'center', fontWeight: 700, letterSpacing: '0.05em', color: '#10b981', fontSize: '15px',
                  border: '1px solid rgba(16, 185, 129, 0.3)'
                }}>
                  NO
                </div>
              </div>
            </div>

          </div>
        </AbsoluteFill>

      </AbsoluteFill>
    </AbsoluteFill>
  );
};
