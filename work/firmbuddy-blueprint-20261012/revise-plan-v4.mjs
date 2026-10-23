import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const read = (object, appear, readable, leave) => ({object, appear, readable, leave});
const shot = (id, start, end, intent, states, action, camera, reads, voiceover, sound, risks) => ({
  id, start, end, intent,
  states: {establish: states[0], action: states[1], result: states[2]},
  action, camera, reads, voiceover, sound, risks,
});
const plan = {
  status: 'planned_not_rendered', revision: '2026-10-13-plan-review',
  duration: 68, fps: 30, width: 1920, height: 1080,
  delivery_mode: 'ai_review_once', review_budget: 'previous_round_already_used',
  treatment: 'ANIMATION-PLAN-V4.md', facts: 'product-reassessment-20261013.json',
  reference_commit: 'e3cb16f63768c68693ff0e15171d6e755457cc32',
  core_memories: ['专业分工', '知识有据', '持续经营'],
  scenario_ids: {S: '查商机', A: '问业务', V: '备拜访'},
  constraints: [
    '三种场景可独立进入，每种均显示新输入、处理和结果；示例议题相同不等于强制工作流',
    '装配关系在请求前成立；当前只表现可见范围内检索，不表现自动装配或训练',
    '全部示例资料和回答持续标记流程示例，不伪造真实公告、法规、来源ID或在线运行结果',
    '用户确认跟进行动不等于客户确认需求；任务写入与专家会商分开',
    '同一张蓝晒图纸，无人物、手或人影；屏幕文字按投影字号校准',
  ],
  shots: [
    shot('position-and-input', 0, 6, '开场认清服务对象和三个独立入口', [0, 3, 3.5],
      '品牌定位从首帧可见，三个入口与一句查商机输入落定',
      '固定中近景，先定位后问题', [
        read('FirmBuddy／券商客户经营·AI专家平台', 0, 0, 6),
        read('查商机／问业务／备拜访；谁值得先跟进？', 3, 3.5, 6),
      ], '券商客户经营，查商机、问业务、备拜访，都能从一句问题开始。',
      '轻笔触建立入口，避免三次重击', [[3, 3.5]]),
    shot('candidate-signals', 6, 15, '查询和监测发现待核实线索', [6, 7, 12.5],
      '双轨资料带筛出扩产披露示例，保留来源端口与待核实状态',
      '6–9秒扫描，9秒后以停读为主', [
        read('查询／监测', 6, 9, 12),
        read('扩产相关披露·流程示例／待核实', 12, 12.5, 15),
      ], '主动查询，也能监测市场和客户名单，从变化中发现待核实的线索。',
      '扫描细擦，选中轻落定', [[7, 9]]),
    shot('expert-work-branches', 15, 24, '数十位专家按专业分工，商机场景获得结果', [15, 17, 21],
      '广场先显规模，行业／财务／资本运作三席依次展开职责，收束到候选与待核实问题',
      '广场转三分支近景，21秒停读结果', [
        read('数十位AI专家', 15, 15.2, 17.5),
        read('行业·看扩产逻辑', 17, 17.5, 21),
        read('财务·查资金安排', 18, 18.5, 21),
        read('资本运作·研判服务方向', 19, 19.5, 22),
        read('候选线索＋待核实问题', 21, 21.5, 24),
      ], '数十位AI专家按专业分工，复杂问题协作研判，找出服务方向和待核实问题。',
      '三次错开接合，收束减音', [[17, 21]]),
    shot('question-with-evidence', 24, 36, '独立业务答疑，证据让服务假设收敛为核实问题', [24, 27, 33],
      '新输入后单专家检索已配备知识；示例资料只给扩产计划，资金安排未提供；引用返回，融资服务？收敛为先确认资金来源与缺口',
      '短匹配切入新输入，固定剖面展开，结论时停机', [
        read('有扩产计划，就有融资需求吗？', 24, 24.5, 27),
        read('知识库／专家已装配（既有关系）', 27, 27.5, 30),
        read('示例资料：扩产计划；资金安排未提供', 30, 30.5, 33),
        read('先确认资金来源与缺口', 33, 33.5, 36),
      ], '有疑问，直接问。专家检索已配备的知识，带着依据回答：有扩产计划，还要确认资金来源与缺口。',
      '纸页轻擦，证据回接一声，结论留静', [[27, 36]]),
    shot('visit-preparation', 36, 46, '独立拜访输入形成具体提问与策略包', [36, 39, 42],
      '新输入准备拜访；资金安排缺项同形对齐成资金怎么安排？；展开落地时间、决策参与者，保留目标／话术／材料页签',
      '短匹配切换输入，固定看缺项变提问，42秒后停读', [
        read('帮我准备这次拜访', 36, 36.5, 39),
        read('资金怎么安排？', 39, 40, 46),
        read('何时落地？／谁参与决策？', 41, 42, 46),
      ], '准备拜访，把信息缺口变成具体提问，再组织目标、话术和材料。',
      '纸页折展，提问成形轻落定', [[39, 42]]),
    shot('followup-feedback', 46, 55, '确认跟进后记录反馈，诊断推进下一步', [46, 47.5, 52],
      '先用户确认，再建立待跟进任务；跟进后时间标识下，资金安排尚未明确的示例记录经诊断得到补问资金计划',
      '确认停机，反馈短回流，52秒固定读结果', [
        read('确认跟进→待跟进任务', 46, 47, 49),
        read('跟进后·示例记录：资金安排尚未明确', 49, 49.5, 52),
        read('下一步：补问资金计划', 52, 52.5, 55),
      ], '确认后进入跟进。记录带回商机诊断，找出卡点，调整下一步。',
      '确认轻点击，反馈细笔声', [[47.5, 50]]),
    shot('capability-index', 55, 61, '三场景属于更广泛的客户经营能力', [55, 55.2, 58.5],
      '后退一级显示两组功能，先查询／答疑／拜访，再诊断／陪练／经营计划，原路径保留',
      '55–55.5秒短退后固定，以对比度切换两组重点', [
        read('商机查询／业务答疑／拜访准备', 55, 55.5, 58),
        read('商机诊断／销售陪练／经营计划', 58, 58.5, 61),
      ], '从商机查询到诊断、陪练和经营计划，支持持续的客户经营。',
      '短纸擦，两组各一次轻提示', [[55, 58.5]]),
    shot('lifecycle-reveal', 61, 68, '三阶段服务范围与品牌主张落定', [61, 61.2, 64.5],
      '同纸面再退一级，三阶段外框展开；业务条线降为结构，标题栏写入品牌与价值主张',
      '61–64.5秒拉远，64.5–68秒完全停住', [
        read('上市前／上市中／上市后', 62, 64.5, 68),
        read('FirmBuddy·把业务问题，变成有依据的行动', 64, 64.5, 68),
      ], '覆盖企业全生命周期，把业务问题，变成有依据的行动。',
      '克制收束，尾音自然衰减', [[61, 65]]),
  ],
  connections: [
    {time: 6, kind: 'path_follow', anchor: '查商机输入引线', window: [5, 7]},
    {time: 15, kind: 'causal_link', anchor: '扩产议题与来源端口', window: [14, 16]},
    {time: 24, kind: 'match_cut_new_request', anchor: '同一扩产议题；问业务新输入', window: [23, 25]},
    {time: 36, kind: 'match_cut_new_request', anchor: '资金安排缺项；拜访新输入', window: [35, 37]},
    {time: 46, kind: 'confirmation_gate', anchor: '策略包跟进端口', window: [45, 48]},
    {time: 55, kind: 'world_reveal_level_1', anchor: '下一步与原三场景结果', window: [54, 56]},
    {time: 61, kind: 'world_reveal_level_2', anchor: '功能索引与原路径', window: [60, 65]},
  ],
};

const md = fs.readFileSync(path.join(root, plan.treatment), 'utf8');
const assert = (test, message) => {if (!test) throw new Error(message);};
let cursor = 0;
for (const s of plan.shots) {
  assert(s.start === cursor && s.end > s.start, `shot continuity: ${s.id}`);
  assert(Number.isInteger(s.start * plan.fps) && Number.isInteger(s.end * plan.fps), `frame alignment: ${s.id}`);
  const values = [s.start, ...Object.values(s.states), s.end];
  assert(values.every((v, i) => i === 0 || v >= values[i - 1]), `state order: ${s.id}`);
  for (const r of s.reads) {
    assert(s.start <= r.appear && r.appear <= r.readable && r.readable < r.leave && r.leave <= s.end, `read window: ${s.id}/${r.object}`);
  }
  for (const [a, b] of s.risks) assert(s.start <= a && a < b && b <= s.end, `risk window: ${s.id}`);
  assert(md.includes(`| ${s.start}–${s.end}秒 |`), `markdown time mismatch: ${s.id}`);
  assert(md.includes(s.voiceover), `markdown narration mismatch: ${s.id}`);
  cursor = s.end;
}
assert(cursor === plan.duration, 'duration');
assert(plan.connections.length === plan.shots.length - 1, 'connection count');
plan.connections.forEach((c, i) => {
  assert(c.time === plan.shots[i].end, 'connection boundary');
  assert(c.window[0] < c.time && c.time < c.window[1], 'connection window');
});
const verification = {
  scope: 'Plan structure only; no rendered picture, playback or listening validation.',
  revision: plan.revision, duration: plan.duration, frames: plan.duration * plan.fps,
  shots: plan.shots.length, read_windows: plan.shots.reduce((n, s) => n + s.reads.length, 0),
  connections: plan.connections.length,
  checked: ['continuous timeline', 'frame alignment', 'ordered states', 'bounded reads and risks', 'connection boundaries', 'markdown timing and exact narration parity'],
  narration_estimates: plan.shots.map(s => ({id: s.id, han_characters_per_second: +((s.voiceover.match(/\p{Script=Han}/gu) || []).length / (s.end - s.start)).toFixed(2)})),
  remaining: ['actual narration timing', 'projected text density', 'dynamic causality and pacing', 'render and sound'],
};
fs.writeFileSync(path.join(root, 'plan-v4.json'), JSON.stringify(plan, null, 2) + '\n');
fs.writeFileSync(path.join(root, 'plan-v4-verification.json'), JSON.stringify(verification, null, 2) + '\n');
console.log(JSON.stringify(verification, null, 2));
