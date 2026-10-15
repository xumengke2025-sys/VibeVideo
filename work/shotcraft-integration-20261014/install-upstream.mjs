import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const task = path.dirname(fileURLToPath(import.meta.url));
const project = path.resolve(task, '../..');
const source = path.join(project, 'reference-sources/video-shotcraft-20261014');
const install = 'D:/Codex/skills/video-shotcraft';
const backup = path.join(task, 'before/video-shotcraft');
const commit = '13c74a707786872a18e3317e48c5c94011027620';
const sha = (p) => createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const actual = execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], {encoding: 'utf8'}).trim();
if (actual !== commit) throw new Error(`Unexpected source commit: ${actual}`);
if (fs.existsSync(backup)) throw new Error('Backup already exists; do not overwrite a previous upgrade');
if (path.resolve(backup).startsWith(path.resolve(task) + path.sep) === false) throw new Error('Backup outside task');
const oldFiles = [];
function inventory(dir, root, records) {
  for (const e of fs.readdirSync(dir, {withFileTypes: true})) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) inventory(p, root, records);
    else if (e.isFile()) records.push({path: path.relative(root, p).replaceAll('\\', '/'), sha256: sha(p), bytes: fs.statSync(p).size});
  }
}
inventory(install, install, oldFiles);
fs.mkdirSync(path.dirname(backup), {recursive: true});
// Both endpoints are explicit and the destination was checked against the task directory.
fs.renameSync(install, backup);
fs.mkdirSync(install, {recursive: true});
for (const e of fs.readdirSync(source)) {
  if (e === '.git') continue;
  fs.cpSync(path.join(source, e), path.join(install, e), {recursive: true});
}
const tracked = execFileSync('git', ['-C', source, 'ls-files', '-z'], {encoding: 'utf8'}).split('\0').filter(Boolean);
const upstream = tracked.map(p => ({path: p, sha256: sha(path.join(source, p)), bytes: fs.statSync(path.join(source, p)).size}));
const manifest = {repository: 'https://github.com/Vincentwei1021/video-shotcraft', commit, retrieved: '2026-10-14', license: 'Apache-2.0', source, install, backup, upstreamFiles: upstream, backupFiles: oldFiles};
fs.writeFileSync(path.join(task, 'installation.json'), JSON.stringify(manifest, null, 2) + '\n');
fs.writeFileSync(path.join(source, 'SOURCE.json'), JSON.stringify({repository: manifest.repository, commit, retrieved: manifest.retrieved, license: manifest.license}, null, 2) + '\n');
fs.copyFileSync(path.join(source, 'SKILL.md'), path.join(install, 'references/upstream-skill.md'));
console.log(JSON.stringify({commit, upstreamFiles: upstream.length, backupFiles: oldFiles.length, install, backup}));
