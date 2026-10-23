// Remotion CLI（Studio / 渲染导出）打包配置：与 vite.config.ts 的 @proj/@demos 策略保持一致。
// 未链接成片工程时自动落到 proj-stub 降级实现；symlinks:false 让符号链接按
// 虚拟路径解析，裸导入落回本工程 node_modules（避免 react/remotion 双实例）。
import { existsSync } from "node:fs";
import path from "node:path";
import { Config } from "@remotion/cli/config";

const proj = path.resolve(
  process.cwd(),
  existsSync(path.resolve(process.cwd(), "proj", "workbench.ts")) ? "proj" : "proj-stub",
);

Config.overrideWebpackConfig((c) => ({
  ...c,
  resolve: {
    ...c.resolve,
    symlinks: false,
    alias: {
      ...(c.resolve?.alias ?? {}),
      "@proj": proj,
      "@demos": path.resolve(process.cwd(), "demosrc"),
    },
  },
}));

// 与 template/remotion.config.ts 同口径：jpeg 帧、ANGLE GL（three/WebGL 镜头要它）、并发 4
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setChromiumOpenGlRenderer("angle");
Config.setConcurrency(process.platform === 'win32' ? 1 : 4);
// Avoid FFmpeg auto-allocating an encoder thread for every logical CPU on
// shared Windows hosts. Input decoding, filters and output encoding are bounded.
if (process.platform === 'win32') Config.overrideFfmpegCommand(({args}) => [
  '-threads', '1', '-filter_threads', '1',
  ...args.slice(0,-1), '-threads', '1', args[args.length-1],
]);
// Optional reuse of a locally installed/cached browser; unset uses Remotion's default.
if (process.env.SHOTCRAFT_BROWSER_EXECUTABLE) Config.setBrowserExecutable(process.env.SHOTCRAFT_BROWSER_EXECUTABLE);
