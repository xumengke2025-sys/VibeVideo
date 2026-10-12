"""Independent combinatorial verification for the entropy film. Python-side, no reuse of film code.
Enumerates all 2^8 arrangements, groups by left count, and verifies every number shown on screen."""
import json, math
from pathlib import Path

OUT = Path(__file__).parent / 'out' / 'audit'; OUT.mkdir(parents=True, exist_ok=True)
N = 8
failures = []

# 1) enumerate all 256 side assignments
arr = {}
for mask in range(1 << N):
    k = bin(mask).count('1')
    arr.setdefault(k, []).append(mask)
counts = [len(arr[k]) for k in range(N + 1)]
expected = [math.comb(N, k) for k in range(N + 1)]

if counts != expected: failures.append(f'counts {counts} != comb {expected}')
if sum(counts) != 256: failures.append('sum != 256')
if counts[3] + counts[4] + counts[5] != 182: failures.append('near-uniform != 182')
if counts[0] + counts[8] != 2: failures.append('merged one-side != 2')
if len(set(arr[4])) != 70: failures.append('arrangements for k=4 not distinct')

A = 0b00001111  # left {1,2,3,4}
B = (1 << 0) | (1 << 2) | (1 << 4) | (1 << 6)  # left {1,3,5,7}
idxA, idxB = arr[4].index(A), arr[4].index(B)
if A not in arr[4] or B not in arr[4]: failures.append('A or B not in k=4 list')

# 2) probabilities used on screen
p44 = counts[4] / 256
p_near = (counts[3] + counts[4] + counts[5]) / 256

report = {
    'scope': 'Independent combinatorial verification (Python math.comb). Not a runtime substitute.',
    'particles': N, 'total_arrangements': sum(counts),
    'counts_by_left_k': counts, 'comb_expected': expected,
    'arrangements_defining_left_side': {str(k): arr[k] for k in range(N + 1)},
    'k4_distinct': len(set(arr[4])), 'k4_list': arr[4],
    'probabilities': {'4:4': round(p44, 4), 'near_uniform_345': round(p_near, 4),
                      '4:4_percent': round(p44 * 100, 2), 'near_uniform_percent': round(p_near * 100, 2)},
    'A_mask': A, 'B_mask': B, 'A_index_in_k4': idxA, 'B_index_in_k4': idxB,
    'checks': {'counts_match_comb': counts == expected, 'sum_256': sum(counts) == 256,
               'near_uniform_182': (counts[3] + counts[4] + counts[5]) == 182,
               'merged_ends_2': (counts[0] + counts[8]) == 2, 'k4_distinct_70': len(set(arr[4])) == 70},
    'failures': failures}
(OUT / 'counts-evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'ok': not failures, 'counts': counts, 'p44_percent': report['probabilities']['4:4_percent'],
                  'near_uniform_percent': report['probabilities']['near_uniform_percent'],
                  'idxA': idxA, 'idxB': idxB, 'failures': failures}, ensure_ascii=False))
raise SystemExit(1 if failures else 0)
