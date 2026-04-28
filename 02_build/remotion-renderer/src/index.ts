import { registerRoot } from 'remotion';
import { FrictionFix } from './FrictionFix';
import { RadicalAttribution } from './RadicalAttribution';
import { SidecarComposition } from './SidecarComposition';
import { Composition } from 'remotion';

const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="SidecarB2B"
        component={SidecarComposition}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="FrictionFix"
        component={FrictionFix}
        durationInFrames={390}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          headline: 'Your phone rings 40 times a day',
          script: 'Every interruption costs you 23 minutes of focus...',
          varkStyle: 'read_write' as const,
          growthStage: 'sprout' as const,
          brandColor: '#e94560',
        }}
      />
      <Composition
        id="RadicalAttribution"
        component={RadicalAttribution}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          headline: 'The data says you lose 3 hours a day to friction',
          dataPoints: ['40 phone interruptions/day', '23 min recovery each',
                       '15.3 hours/week lost', '£780/week in billable time'],
          varkStyle: 'visual' as const,
          growthStage: 'grow' as const,
          brandColor: '#20B2AA',
        }}
      />
    </>
  );
};

registerRoot(RemotionRoot);
