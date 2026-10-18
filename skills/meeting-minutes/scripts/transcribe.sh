#!/usr/bin/env bash
# Transcribe a meeting recording (video, audio, or a YouTube/Drive/Zoom share URL) to text with timestamps.
#
#   transcribe.sh <file-or-url> [-o outdir] [-l lang] [-m model]
#
# Output in outdir (default ./minutes-work/<basename>/):
#   audio.wav        16 kHz mono audio (ffmpeg)
#   transcript.txt   plain text
#   transcript.srt   with timestamps
#
# Backends, first found wins:  mlx_whisper (Apple Silicon, fastest)  >  whisper-cli (whisper.cpp)  >  whisper (openai-whisper)
# Nothing is installed by this script. If no backend exists it prints the install commands and exits 2.
set -euo pipefail

usage() { sed -n '2,14p' "$0"; exit 1; }
[[ $# -ge 1 ]] || usage

INPUT="$1"; shift
OUT=""; LANG_OPT=""; MODEL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o) OUT="$2"; shift 2;;
    -l) LANG_OPT="$2"; shift 2;;
    -m) MODEL="$2"; shift 2;;
    *) usage;;
  esac
done

export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"   # pipx and Homebrew installs
need() { command -v "$1" >/dev/null 2>&1; }

# 1. Resolve the input to a local media file
if [[ "$INPUT" =~ ^https?:// ]]; then
  need yt-dlp || { echo "URL input needs yt-dlp:  brew install yt-dlp   (or: pipx install yt-dlp)"; exit 2; }
  base="$(yt-dlp --get-id "$INPUT" 2>/dev/null || echo download)"
  OUT="${OUT:-minutes-work/$base}"; mkdir -p "$OUT"
  echo "downloading audio with yt-dlp…"
  yt-dlp -q -x --audio-format m4a -o "$OUT/source.%(ext)s" "$INPUT"
  MEDIA="$OUT/source.m4a"
else
  [[ -f "$INPUT" ]] || { echo "no such file: $INPUT"; exit 1; }
  base="$(basename "${INPUT%.*}")"
  OUT="${OUT:-minutes-work/$base}"; mkdir -p "$OUT"
  MEDIA="$INPUT"
fi

# 2. Extract 16 kHz mono wav
need ffmpeg || { echo "ffmpeg is required:  brew install ffmpeg"; exit 2; }
WAV="$OUT/audio.wav"
if [[ ! -f "$WAV" ]]; then
  echo "extracting audio…"
  ffmpeg -loglevel error -y -i "$MEDIA" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WAV"
fi
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WAV" 2>/dev/null | cut -d. -f1 || echo "?")
echo "audio: $WAV (${dur}s)"

# 3. Transcribe
if need mlx_whisper; then
  MODEL="${MODEL:-mlx-community/whisper-large-v3-turbo}"
  echo "backend: mlx_whisper ($MODEL)"
  mlx_whisper "$WAV" --model "$MODEL" --output-dir "$OUT" --output-name transcript --output-format all \
    ${LANG_OPT:+--language "$LANG_OPT"} >/dev/null
elif need whisper-cli; then
  MODEL="${MODEL:-${WHISPER_CPP_MODEL:-}}"
  [[ -f "$MODEL" ]] || { echo "whisper-cli needs a model file: pass -m /path/ggml-large-v3-turbo.bin or set WHISPER_CPP_MODEL"; exit 2; }
  echo "backend: whisper.cpp ($MODEL)"
  whisper-cli -m "$MODEL" -f "$WAV" -otxt -osrt -of "$OUT/transcript" ${LANG_OPT:+-l "$LANG_OPT"} >/dev/null
elif need whisper; then
  MODEL="${MODEL:-turbo}"
  echo "backend: openai-whisper ($MODEL)"
  whisper "$WAV" --model "$MODEL" --output_dir "$OUT" --output_format all ${LANG_OPT:+--language "$LANG_OPT"} >/dev/null
  for f in "$OUT"/audio.*; do case "$f" in *.wav) ;; *) mv "$f" "$OUT/transcript.${f##*.}";; esac; done
else
  cat <<'EOF'
No transcription backend found. Install one (ask the user first):

  Apple Silicon (recommended, runs locally):   pipx install mlx-whisper      # or: pip install mlx-whisper
  Any machine, local:                          brew install whisper-cpp && download a model:
      curl -L -o ~/.cache/ggml-large-v3-turbo.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
      export WHISPER_CPP_MODEL=~/.cache/ggml-large-v3-turbo.bin
  Python, slower:                              pipx install openai-whisper

All of them need ffmpeg:  brew install ffmpeg
EOF
  exit 2
fi

[[ -f "$OUT/transcript.txt" ]] || { echo "transcription produced no transcript.txt in $OUT"; ls "$OUT"; exit 1; }
words=$(wc -w < "$OUT/transcript.txt" | tr -d ' ')
echo "done: $OUT/transcript.txt ($words words), $OUT/transcript.srt"
