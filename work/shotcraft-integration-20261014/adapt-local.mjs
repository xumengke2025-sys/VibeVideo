import fs from 'node:fs';
import path from 'node:path';
const root = 'D:/Codex/skills/video-shotcraft';
const source = path.resolve('reference-sources/video-shotcraft-20261014');
const pending = new Map();
function change(relative, before, after) {
  const file = path.join(root, relative);
  const text = pending.get(file) ?? fs.readFileSync(path.join(source, relative), 'utf8').replaceAll('\r\n', '\n');
  if (!text.includes(before)) throw new Error(`Source mismatch: ${relative}`);
  pending.set(file, text.replace(before, after));
}
const demos = path.join(root, 'workbench/demosrc');
if (fs.lstatSync(demos).isFile()) {
  if (fs.readFileSync(demos, 'utf8').trim() !== '../demos') throw new Error('Unexpected Git link content');
  fs.unlinkSync(demos);
  fs.symlinkSync(path.join(root, 'demos'), demos, 'junction');
}
change('workbench/scripts/gen-index.mjs', 'const rel = relative(demosDir, p).replace(/\\.tsx$/, "");', 'const rel = relative(demosDir, p).replaceAll("\\\\", "/").replace(/\\.tsx$/, "");');
change('workbench/scripts/gen-index.mjs', 'import { dirname, extname, join, relative } from "node:path";', 'import { dirname, extname, join, relative } from "node:path";\nimport { linkLocal } from "./local-platform.mjs";');
change('workbench/scripts/gen-index.mjs', 'symlinkSync(target, linkPath);', 'linkLocal(target, linkPath);');
change('workbench/scripts/open.mjs', 'import { spawn, spawnSync } from "node:child_process";', 'import { spawn, spawnSync } from "node:child_process";\nimport { linkLocal } from "./local-platform.mjs";');
change('workbench/scripts/open.mjs', 'symlinkSync(srcDir, projLink);', 'linkLocal(srcDir, projLink);');
change('workbench/scripts/open.mjs', 'symlinkSync(join(publicSrc, e), join(pub, e));', 'linkLocal(join(publicSrc, e), join(pub, e));');
change('workbench/scripts/open.mjs', 'spawnSync("npm", ["install", "--ignore-scripts"], { cwd: wb, stdio: "inherit" })', 'spawnSync(process.platform === "win32" ? "npm.cmd" : "npm", ["install", "--ignore-scripts"], { cwd: wb, stdio: "inherit", shell: process.platform === "win32", windowsHide: true })');
change('workbench/scripts/open.mjs', 'if (process.platform === "win32") return false; // 无 ps；宁可不杀', `if (process.platform === "win32") {
    const r = spawnSync("powershell.exe", ["-NoProfile", "-Command", "(Get-CimInstance Win32_Process -Filter 'ProcessId = " + pid + "').CommandLine"], {encoding: "utf8", windowsHide: true});
    const command = (r.stdout ?? "").replaceAll("\\\\", "/");
    return r.status === 0 && command.includes(viteBin.replaceAll("\\\\", "/")) && command.includes("--port " + PORT);
  }`);
change('workbench/scripts/open.mjs', 'viteBin, "--port", String(PORT), "--strictPort"', 'viteBin, "--host", "127.0.0.1", "--port", String(PORT), "--strictPort"');
change('workbench/scripts/open.mjs', 'cwd: wb, detached: true, stdio: ["ignore", fd, fd],', 'cwd: wb, detached: true, windowsHide: true, stdio: ["ignore", fd, fd],');
change('workbench/vite.config.ts', 'import { spawn } from "node:child_process";', 'import { spawn } from "node:child_process";\n// @ts-ignore local platform helper is a Node-only module.\nimport { syncRenderPublic } from "./scripts/local-platform.mjs";');
const before = `            const rsync = spawn(
              "rsync",
              ["-aL", "--delete", "--exclude=cardpreviews", "public/", \`\${renderPublic}/\`],
              { cwd: root },
            );
            rsync.stderr.on("data", onChunk);
            rsync.on("close", (rc) => {
              if (rc !== 0) {
                dropProps();
                job.status = "error";
                job.lastLine = \`素材同步失败（rsync 退出码 \${rc}）：\${job.lastLine}\`;
                return;
              }
              const bin = path.join(root, "node_modules", ".bin", "remotion");
              const child = spawn(
                bin,
                [
                  "render",`;
const after = `            try {
              syncRenderPublic(root);
              const bin = path.join(root, "node_modules", "@remotion", "cli", "remotion-cli.js");
              const child = spawn(
                process.execPath,
                [
                  bin,
                  "render",`;
change('workbench/vite.config.ts', before, after);
change('workbench/vite.config.ts', '                { cwd: root },', '                { cwd: root, windowsHide: true },');
change('workbench/vite.config.ts', '              child.stdout.on("data", onChunk);', `              child.on("error", (error) => {
                dropProps(); job.status = "error"; job.lastLine = error.message;
              });
              child.stdout.on("data", onChunk);`);
change('workbench/vite.config.ts', '            });\n            send(200, { id });', `            } catch (error) {
              dropProps(); job.status = "error"; job.lastLine = String(error);
            }
            send(200, { id });`);
change('workbench/vite.config.ts', 'server: { port: 5198, strictPort: true }', 'server: { host: "127.0.0.1", port: 5198, strictPort: true }');
for (const [file, text] of pending) fs.writeFileSync(file, text);
console.log('Applied local Windows/path/export adapters; upstream checkout unchanged');
