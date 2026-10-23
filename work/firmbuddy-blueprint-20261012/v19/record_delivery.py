from pathlib import Path
import json

R = Path(__file__).resolve().parent
B = R.parent
O = B / 'out/final-v19-mechanical-relief'
checks = json.loads((O / 'delivery-checks.json').read_text(encoding='utf-8'))
observations = {
    'video_sha256': checks['video_sha256'],
    'observer': '制作主角色，非独立审核',
    'actual_images_viewed': {
        'final-overview.jpg': [3, 18, 31, 38, 49, 62, 75, 87.5, 92, 101.6, 109, 117],
        'closing-sequence.jpg': [88, 88.4, 89.2, 89.6, 90.8, 91.6, 91.8, 92, 92.2, 92.8, 93.2, 94, 96, 97, 98, 99.2, 101.6, 102.2, 104, 106, 108, 110, 112, 114.4, 116.6, 119.6],
        'decoded_full_size': ['decoded-49.jpg', 'decoded-87.5.jpg', 'decoded-92.jpg'],
        'previously_viewed_final_render_sheets': ['opening-sequence.jpg', 'flow-sequence.jpg']
    },
    'findings': [
        '最终解码总览保留统一工程蓝图、来源业务卡、阶梯专家厅、产业定位、知识抽屉及同一A01档案。',
        '装配连续抽样呈现材料入档、压头接触、人工开闸与沟通记录回流；人工审阅标记未再被进料遮挡。',
        '49秒原尺寸帧确认九类业务专家及三位前景专家，87.5和92秒确认装配过程与结果。',
        '简短业务收益随每站动作呈现；没有虚构提效数字。'
    ],
    'limits': [
        '连续抽样和静帧不等于全片正常速度播放。',
        '未完整实际听音；响度与AAC对齐检查不等于听审。',
        '20.8–23.2秒业务卡转档案存在短暂淡化文字重叠。',
        '同纸二维摄影和斜投影，机械机构为业务流程的解释性隐喻。'
    ],
    'full_normal_speed_playback': False,
    'actual_listening': False,
    'independent_review': '沿用历史已用预算，无新增独立审核'
}
(O / 'observations.json').write_text(json.dumps(observations, ensure_ascii=False, indent=2), encoding='utf-8')
checks['observation'] = 'Completed producer image sampling; scope and limits in observations.json'
(O / 'delivery-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
(R / 'CHECKPOINT.md').write_text('''# V19 制作完成 · 2026-10-23

目标：机械感与动作解释业务减负，减少文字。
aspect_ratio=16:9；width=1920；height=1080；120秒；30fps；3600帧；纯音乐无配音。
delivery_mode=ai_review_once；历史预算已用，本轮零子代理，无新独立审核。

成片：out/final-v19-mechanical-relief/video.mp4。
源码包：FirmBuddy-source-v19-mechanical-relief.zip；打包结果见同成片目录source-package.json。
视频SHA256：80403e4033a9b2f9807a43a748df5beb3080c25dde5126f3da6bd0ff71463788。
最终源签名：ba6ce5555a2eba42ad4024c17355c216000eeac9bb88194fbe0f55ca891ff746。

完成：同一A01档案贯穿七站；滚轮归集、专家接力、丝杠定位、知识抽屉、连杆压头、人工开闸、记录回流。取消长段说明和上下双字幕，保留各站短标题与业务收益。九类专家、原式阶梯座谈、商机查询入口与减持示例关系保留。产品仓库只读，无虚构绩效数字。

工程验证：整片音视频完整解码、规格与哈希检查通过；11处AAC对齐均0采样偏移；V18原文件保护哈希一致。音乐约-14.97 LUFS/-1.50dBTP。相机接点和20.8–113秒每0.2秒档案安全区数值检查通过。

实际观察：初版概念34/50/75/91秒，修订92/117秒；88–100秒旧样段15时点抽样后修正进料遮挡。最终版重新渲染，实际看开头及中段连续抽样、88–119.6秒26时点连续抽样、MP4解码12帧总览及49/87.5/92秒原尺寸帧。最终进料未遮挡人工审阅标记。旧样段不冒充最终同源样段。

限制：未全片正常速度观看或完整实际听音，不宣称完整视听验收。20.8–23.2秒卡片转档案有短暂淡化文字重叠。准确范围见observations.json，工程证据见evidence.json和delivery-checks.json。

下一步：交付当前视频与源码，由用户反馈。无必需制作工作遗留，不启动新审核或创意返工。
''', encoding='utf-8')
checkpoint = B / 'CHECKPOINT.md'
text = checkpoint.read_text(encoding='utf-8')
start = text.index('## V19 ')
end = text.index('## V18 ', start)
section = '''## V19 机械减负工作流 · 2026-10-23 完成

- 120秒、1920×1080、30fps、3600帧、原创纯音乐无配音；delivery_mode=ai_review_once，历史预算已用，本轮零子代理。
- 同一A01客户档案沿连续机器：来源抽卡→滚轮归集→专家接力→产业定位→知识抽屉→准备包装配与人工开闸→沟通记录回流。减少长段文字，用动作配简短业务收益呈现减负。
- 成片：out/final-v19-mechanical-relief/video.mp4；源码包FirmBuddy-source-v19-mechanical-relief.zip。保留V18与产品仓库。
- 完整音视频解码、规格、哈希、11处AAC零采样偏移及V18保护检查通过；相机接点与档案安全区数值通过。
- 已看最终开头、中段、收尾连续抽样与MP4解码12帧总览及49/87.5/92秒原尺寸帧；装配进料遮挡已修正。未全片正常速度播放或完整听音，不宣称完整视听验收。
- 成片SHA256：80403e4033a9b2f9807a43a748df5beb3080c25dde5126f3da6bd0ff71463788；详细观察与边界见v19/CHECKPOINT.md及out/final-v19-mechanical-relief/observations.json。
- 下一步：交付后由用户反馈，无必需制作工作遗留。

'''
checkpoint.write_text(text[:start] + section + text[end:], encoding='utf-8')
print('Final observations and checkpoints recorded.')
