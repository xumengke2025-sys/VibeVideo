# FirmBuddy｜专业支持，随时在场

最新V4成片为 [out/final-v4-execution/video.mp4](out/final-v4-execution/video.mp4)，68秒、1920×1080横屏、30fps。三个场景各自显示输入、处理和结果；知识引用收敛服务建议，缺项进一步变成拜访提问。可编辑入口与使用说明见 [v4/README.md](v4/README.md)，源码包FirmBuddy-source-v4.zip。完整解码、画幅/时长/音轨与登记文字检查通过；实际观察及未完成听音范围见out/final-v4-execution/observations.json。

以下保留V3历史说明与入口。

V3为48秒，1920×1080横屏，30fps。开场明确拜访准备、业务答疑、商机查询三个使用入口；四排专家会场呈现数十位、多领域专家，六组知识档案呈现丰富知识库，六类成果与确认跟进体现商机经营全流程。调整明细见REVISION-V3.md。当前视频out/final-v3/video.mp4。

## 工程与预览

在本目录运行 `node server.mjs --serve`，浏览器打开 http://127.0.0.1:8768 。播放键同步音频，滑杆可定位任意时间。Chrome浏览器与Windows微软雅黑字体是当前渲染环境。

在本目录运行 `node render.mjs --mode=final --version=新版本名` 导出MP4。当前工程复用项目中已安装的playwright-core及Remotion FFmpeg，路径见render.mjs。更换电脑时须调整Chrome、Playwright和FFmpeg路径。源文件film.js为可编辑画面和字幕时间轴；音频源及实际时间信息在audio目录。

## 来源与声音

四张用户截图以线绘形态融入画面，原图和哈希保存在assets/reference。借鉴Lemo blueprint的蓝晒材质、描线与纸面相机，代码及MIT许可保存在vendor。参考实际查看范围为18秒静帧和16–20秒3fps连续采样，不声称看过全片。

旁白使用本机Windows SAPI合成，中文Huihui、英文品牌Zira。配乐为原创合成拨弦音型，含短促合成动作音效。音频统计和字幕时间对齐属于工程核对，不等同于实际听音。

## 内容边界

商机仅为待研判的标题级线索；资料显示来源、版本与引用关系；跟进任务在确认动作之后出现。不宣传自动成交、监管认证或未经确认的自动写入。没有修改FirmBuddy应用源码或业务数据。

delivery_mode: ai_review_once。V1的独立审核已使用本轮预算，记录仅对应V1哈希。V2为用户反馈修改，做工程及改动画面检查，没有重新开启全面独立审核；实际听音与实时播放感知未完成。历史V1保存在out/final-v1和FirmBuddy-source-v1.zip。
