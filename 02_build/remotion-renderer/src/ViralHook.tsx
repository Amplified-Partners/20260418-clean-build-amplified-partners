import { AbsoluteFill, Sequence, spring, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const ViralHook: React.FC<{
  hookText: string;
  scriptText: string;
  ctaText: string;
  brandColor?: string;
}> = ({
  hookText = "Are you making this mistake?",
  scriptText = "Most businesses lose 20% of leads by not following up in 4 hours. Our logic fixes that.",
  ctaText = "Reply PUDDING to see the math.",
  brandColor = "#2563eb",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animations
  const hookOpacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const hookY = spring({ frame, fps, config: { damping: 12 } });

  const scriptOpacity = interpolate(frame, [90, 105], [0, 1], { extrapolateRight: 'clamp' });
  
  const ctaOpacity = interpolate(frame, [300, 315], [0, 1], { extrapolateRight: 'clamp' });
  const ctaScale = spring({ frame: Math.max(0, frame - 300), fps, config: { damping: 12 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f0f14', color: 'white', fontFamily: 'Inter, sans-serif', padding: '60px 40px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
      
      {/* 0-4s: Hook */}
      <Sequence from={0} durationInFrames={120}>
        <div style={{ opacity: hookOpacity, transform: `translateY(${50 - hookY * 50}px)`, fontSize: '72px', fontWeight: 800, textAlign: 'center', color: brandColor, lineHeight: 1.1 }}>
          {hookText}
        </div>
      </Sequence>

      {/* 3s-15s: Script */}
      <Sequence from={90} durationInFrames={360}>
        <div style={{ opacity: scriptOpacity, fontSize: '48px', fontWeight: 500, textAlign: 'center', marginTop: '80px', color: '#e5e7eb', lineHeight: 1.4 }}>
          {scriptText}
        </div>
      </Sequence>

      {/* 10s-15s: CTA */}
      <Sequence from={300} durationInFrames={150}>
        <AbsoluteFill style={{ justifyContent: 'flex-end', paddingBottom: '120px', alignItems: 'center' }}>
          <div style={{ opacity: ctaOpacity, transform: `scale(${ctaScale})`, backgroundColor: brandColor, padding: '30px 50px', borderRadius: '20px', fontSize: '56px', fontWeight: 800, textAlign: 'center', boxShadow: '0 20px 40px rgba(0,0,0,0.5)' }}>
            {ctaText}
          </div>
        </AbsoluteFill>
      </Sequence>

    </AbsoluteFill>
  );
};
