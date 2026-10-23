import fs from 'node:fs';import{EVENTS,SHOTS,DURATION,FPS}from'./timeline.js';
fs.writeFileSync(new URL('./events.json',import.meta.url),JSON.stringify({DURATION,FPS,EVENTS,SHOTS},null,2));
