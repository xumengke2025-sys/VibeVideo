#!/usr/bin/env bash
# Contact sheet of every beat, sampled 0.2 s after each beat by frame number.
#   tools/beat-sheet.sh <video> <fps> <first-scene-start> <scene-count> <out.jpg>
set -euo pipefail
video=$1 fps=$2 start=$3 count=$4 out=$5
sel=""
for ((s = 0; s < count; s++)); do for b in 0 1 2 3 4 5 6 7; do
  n=$(python3 -c "print(round(($start + $s*2 + $b*0.25 + 0.2) * $fps))")
  sel+="eq(n\\,$n)+"
done; done
ffmpeg -loglevel error -y -i "$video" -vf "select='${sel%+}',scale=640:-1,tile=4x$((count * 2))" -frames:v 1 "$out"
