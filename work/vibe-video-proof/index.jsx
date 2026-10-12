import React from 'react';
import {Composition, registerRoot, staticFile} from 'remotion';
import {CodeMotionStudy} from './CodeMotionStudy.jsx';

const Root = () => <Composition
  id="CodeMotionStudy"
  component={CodeMotionStudy}
  durationInFrames={360}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{soundSrc: staticFile('proof-score.wav')}}
/>;
registerRoot(Root);
