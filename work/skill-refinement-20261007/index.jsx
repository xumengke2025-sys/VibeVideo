import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {OpticalStudy} from './OpticalStudy';
registerRoot(()=> <Composition id="OpticalStudy" component={OpticalStudy} durationInFrames={300} width={1920} height={1080} fps={30}/>);
