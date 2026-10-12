# FirmBuddy｜一次客户拜访的行动蓝图

60秒，1920×1080横屏，30fps。蓝晒图纸上的连续流程：客户拜访→商机线索→专家会商→资料查证→拜访策略包与确认跟进→企业全生命周期。

## 工程与预览

在本目录运行 `node server.mjs --serve`，浏览器打开 http://127.0.0.1:8768 。播放键同步音频，滑杆可定位任意时间。Chrome浏览器与Windows微软雅黑字体是当前渲染环境。

在本目录运行 `node render.mjs --mode=final --version=新版本名` 导出MP4。当前工程复用项目中已安装的playwright-core及Remotion FFmpeg，路径见render.mjs。更换电脑时须调整Chrome、Playwright和FFmpeg路径。源文件film.js为可编辑画面和字幕时间轴；音频源及实际时间信息在audio目录。

## 来源与声音

四张用户截图以线绘形态融入画面，原图和哈希保存在assets/reference。借鉴Lemo blueprint的蓝晒材质、描线与纸面相机，代码及MIT许可保存在vendor。参考实际查看范围为18秒静帧和16–20秒3fps连续采样，不声称看过全片。

旁白使用本机Windows SAPI合成，中文Huihui、英文品牌Zira。配乐为原创合成拨弦音型，含短促合成动作音效。音频统计和字幕时间对齐属于工程核对，不等同于实际听音。

## 内容边界

上市制造企业和15:00拜访为演示情境。商机仅为待研判的标题级线索；资料显示来源、版本与引用关系；跟进任务在确认动作之后出现。不宣传自动成交、监管认证或未经确认的自动写入。没有修改FirmBuddy应用源码或业务数据。

delivery_mode: ai_review_once。审核结果及实际覆盖见qa目录；工具不支持的听音、实时播放须保留为未完成。
