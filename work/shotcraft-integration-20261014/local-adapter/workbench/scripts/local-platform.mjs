// Local VibeVideo adapter. Upstream originals remain in the fixed source checkout.
import fs from 'node:fs';
import path from 'node:path';

export function linkLocal(target, destination) {
  const resolved = path.resolve(path.dirname(destination), target);
  const directory = fs.statSync(resolved).isDirectory();
  if (directory) {
    fs.symlinkSync(process.platform === 'win32' ? resolved : target, destination,
      process.platform === 'win32' ? 'junction' : 'dir');
  } else {
    // File symlinks require extra privileges on Windows; refreshed copies are sufficient.
    if (process.platform === 'win32') fs.copyFileSync(resolved, destination);
    else fs.symlinkSync(target, destination, 'file');
  }
}

export function syncRenderPublic(workbench) {
  const root = fs.realpathSync(workbench);
  const destination = path.resolve(root, '.render-public');
  if (path.dirname(destination) !== root || path.basename(destination) !== '.render-public') {
    throw new Error('Render-public destination is outside this workbench');
  }
  // Never follow a replaced output link during cleanup.
  if (fs.existsSync(destination) && fs.lstatSync(destination).isSymbolicLink()) {
    throw new Error('Render-public destination must be a private directory');
  }
  fs.rmSync(destination, {recursive: true, force: true});
  fs.mkdirSync(destination, {recursive: true});
  const publicDir = path.join(root, 'public');
  for (const name of fs.readdirSync(publicDir)) {
    if (name === 'cardpreviews' || name.startsWith('.')) continue;
    const source = path.join(publicDir, name);
    if (!fs.existsSync(source)) continue;
    fs.cpSync(source, path.join(destination, name), {recursive: true, dereference: true});
  }
  return destination;
}
