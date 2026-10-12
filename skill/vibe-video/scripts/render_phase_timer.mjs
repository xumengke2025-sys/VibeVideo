import fs from 'node:fs';
import path from 'node:path';
import {performance} from 'node:perf_hooks';

// Wall-clock telemetry only. This does not assert that media was reviewed.
export function phaseTimer(out) {
  const began = performance.now();
  let current = null;
  const record = {started_at: new Date().toISOString(), status: 'running', phases: []};
  const flush = () => {
    record.elapsed_ms = Math.round(performance.now() - began);
    const file = path.join(out, 'phase-timings.json'), temp = file + '.tmp';
    fs.writeFileSync(temp, JSON.stringify(record, null, 2));
    fs.renameSync(temp, file);
  };
  function end() {
    if (!current) return;
    current.elapsed_ms = Math.round(performance.now() - current.clock);
    delete current.clock;
    current.ended_at = new Date().toISOString();
    record.phases.push(current);
    current = null;
  }
  return {
    start(name, details = {}) {end(); current = {name, ...details, started_at: new Date().toISOString(), clock: performance.now()}; record.active_phase = name; flush();},
    progress(details) {record.progress = {...details, at: new Date().toISOString()}; flush();},
    finish(status = 'complete') {end(); record.status = status; record.active_phase = null; flush();}
  };
}
