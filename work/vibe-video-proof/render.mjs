import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const root = path.dirname(fileURLToPath(import.meta.url));
const serveUrl = await bundle({entryPoint: path.join(root, 'index.jsx'), publicDir: path.join(root, 'public')});
const composition = await selectComposition({serveUrl, id: 'CodeMotionStudy'});
let renderProgress = -1;
await renderMedia({
  serveUrl, composition, outputLocation: path.join(root, 'out', 'code-motion-study.mp4'),
  codec: 'h264', crf: 18, x264Preset: 'veryfast', concurrency: 1,
  ffmpegOverride: ({args}) => {
    const result = [...args];
    result.splice(result.length - 1, 0, '-threads:v', '1', '-x264-params', 'threads=1:lookahead_threads=1');
    return result;
  },
  onProgress: ({progress}) => {
    const percent = Math.floor(progress * 100);
    if (percent % 20 === 0 && percent !== renderProgress) {console.log(`Render ${percent}%`); renderProgress = percent;}
  },
});
console.log(path.join(root, 'out', 'code-motion-study.mp4'));
