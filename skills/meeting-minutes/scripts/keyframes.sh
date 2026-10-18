#!/usr/bin/env bash
# Extract slide/screen-share frames from a meeting video so the agent can read what was shown.
#
#   keyframes.sh <video> [-o outdir] [-t scene-threshold] [-n max-frames]
#
# Writes outdir/frame-HHMMSS.jpg for every scene change (default threshold 0.25) plus one frame
# every 60 s as a fallback, capped at max-frames (default 40). Requires ffmpeg.
set -euo pipefail

VIDEO="${1:?usage: keyframes.sh <video> [-o outdir] [-t threshold] [-n max]}"; shift
OUT="minutes-work/$(basename "${VIDEO%.*}")/frames"; THR=0.25; MAX=40
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o) OUT="$2"; shift 2;;
    -t) THR="$2"; shift 2;;
    -n) MAX="$2"; shift 2;;
    *) echo "unknown option $1"; exit 1;;
  esac
done
command -v ffmpeg >/dev/null || { echo "ffmpeg is required:  brew install ffmpeg"; exit 2; }
[[ -f "$VIDEO" ]] || { echo "no such file: $VIDEO"; exit 1; }
mkdir -p "$OUT"

# timestamps of scene changes + every 60s (-fps_mode replaced -vsync in ffmpeg 5.1)
if ffmpeg -hide_banner -h full 2>/dev/null | grep -- '-fps_mode' >/dev/null; then VFR=(-fps_mode vfr); else VFR=(-vsync vfr); fi
ts=$(ffmpeg -loglevel info -i "$VIDEO" -vf "select='gt(scene,$THR)+eq(mod(n\,1500)\,0)',showinfo" "${VFR[@]}" -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | awk '!seen[int($1)]++' | head -n "$MAX")
[[ -n "$ts" ]] || { echo "ffmpeg found no frames; run without -loglevel to see the error"; exit 1; }

count=0
for t in $ts; do
  name=$(printf "frame-%02d%02d%02d.jpg" $((${t%.*}/3600)) $(((${t%.*}%3600)/60)) $((${t%.*}%60)))
  ffmpeg -loglevel error -y -ss "$t" -i "$VIDEO" -frames:v 1 -vf "scale=1280:-2" -q:v 3 "$OUT/$name"
  count=$((count+1))
done
echo "wrote $count frames to $OUT (threshold $THR, max $MAX)"
