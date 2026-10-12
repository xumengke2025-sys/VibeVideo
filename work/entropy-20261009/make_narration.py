"""Original Chinese narration script, public synthetic voice via edge-tts; no cloned human voice.
Measures actual durations with the verified ffprobe for downstream timeline fitting.
Generation does not imply listening acceptance."""
import asyncio, json, subprocess
from pathlib import Path
import edge_tts

ROOT = Path(__file__).parent
FFPROBE = 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe'
VOICE = 'zh-CN-YunxiNeural'
RATE = '+12%'
CUES = [
    {'id': 'c1', 'window': [0, 7], 'text': '粒子可以向右走，也可以向左走。那为什么，它们散开以后，却很少全部回到一边？'},
    {'id': 'c2', 'window': [7, 16], 'text': '我们用八个可区分的粒子，只记录它们在哪一侧。同样是左四、右四，具体是哪四个，可以完全不同。'},
    {'id': 'c3', 'window': [16, 30], 'text': '全部在左，只有一种归属排列。但左右各四，有七十种。宏观看起来一样，背后能对应的微观排列，却多得多。'},
    {'id': 'c4', 'window': [30, 42], 'text': '如果这些归属排列等可能，接近均匀的状态，就占了大多数。不过，恰好四比四只占百分之二十七左右。平衡附近，仍然会有波动。'},
    {'id': 'c5', 'window': [42, 53], 'text': '这里的规则没有偏爱左右，但从少见的集中状态出发，系统更容易进入排列更多的状态。它仍会波动，也并非绝不能回去。'},
    {'id': 'c6', 'window': [53, 60], 'text': '熵不只是看起来乱不乱。粒子数量巨大时，整体回到集中状态的机会极小，这就是熵增的统计含义。'},
]

def duration(path):
    out = subprocess.run([FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())

async def main():
    out = ROOT / 'narration'; out.mkdir(exist_ok=True)
    records = []
    for i, cue in enumerate(CUES):
        target = out / f'{i:02d}.mp3'
        if not target.exists() or target.stat().st_size < 1000:
            for attempt in range(4):
                try:
                    c = edge_tts.Communicate(cue['text'], VOICE, rate=RATE)
                    data = b''
                    async for chunk in c.stream():
                        if chunk['type'] == 'audio': data += chunk['data']
                    if data:
                        target.write_bytes(data); break
                except Exception as e:
                    print('retry', i, attempt, type(e).__name__, str(e)[:90], flush=True)
                    await asyncio.sleep(2.0)
            else:
                raise SystemExit(f'TTS failed for cue {i}')
        d = duration(target)
        records.append({'index': i, 'id': cue['id'], 'window': cue['window'], 'text': cue['text'],
                        'file': f'narration/{i:02d}.mp3', 'voice': VOICE, 'rate': RATE,
                        'synthetic': True, 'duration': round(d, 3)})
        print(f'VOICE {i+1}/{len(CUES)} {target.stat().st_size} bytes {d:.2f}s', flush=True)
    (ROOT / 'narration.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    total = sum(r['duration'] for r in records)
    print(f'total speech {total:.2f}s over windows', [c['window'] for c in CUES], flush=True)

if __name__ == '__main__':
    asyncio.run(main())
