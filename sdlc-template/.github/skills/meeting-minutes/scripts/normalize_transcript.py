#!/usr/bin/env python3
"""Normalize a meeting transcript into plain text with [HH:MM:SS] Speaker: lines.

Accepts .vtt (Zoom, Teams, Google Meet, YouTube), .srt, whisper .json, or .txt.
Merges consecutive cues from the same speaker and strips cue noise, so the agent reads
one clean file instead of thousands of 2-second fragments.

    normalize_transcript.py transcript.vtt > transcript.clean.txt
    normalize_transcript.py transcript.json --every 60   # a timestamp at least every 60 s
"""
import argparse
import json
import re
import sys

TIME = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})|(\d{1,2}):(\d{2})[.,](\d{3})")
SPEAKER = re.compile(r"^(?:<v\s+([^>]+)>|([A-Z][\w .'-]{0,40}?):\s)")


def to_sec(m):
    g = m.groups()
    if g[0] is not None:
        return int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
    return int(g[4]) * 60 + int(g[5]) + int(g[6]) / 1000


def fmt(sec):
    sec = int(sec)
    return f"[{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}]"


def parse_cues(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        data = json.loads(text)
        for s in data.get("segments", []):
            yield float(s["start"]), (s.get("speaker") or ""), s["text"].strip()
        return
    if not re.search(r"-->", text):  # plain text
        yield 0.0, "", text.strip()
        return
    blocks = re.split(r"\n\s*\n", text)
    for b in blocks:
        lines = [l for l in b.strip().splitlines() if l.strip()]
        idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if idx is None:
            continue
        m = TIME.search(lines[idx])
        start = to_sec(m) if m else 0.0
        body = " ".join(lines[idx + 1:])
        body = re.sub(r"<(?!v\s)[^>]+>", "", body)  # drop tags except <v Speaker>
        sp = ""
        sm = SPEAKER.match(body)
        if sm:
            sp = (sm.group(1) or sm.group(2)).strip()
            body = body[sm.end():]
        body = re.sub(r"</v>", "", body).strip()
        if body:
            yield start, sp, body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--every", type=int, default=30, help="seconds between timestamps when the speaker does not change")
    a = ap.parse_args()

    out, cur_sp, cur_start, buf, last_stamp = [], None, 0.0, [], -1e9
    for start, sp, body in parse_cues(a.path):
        new_speaker = sp != cur_sp
        if new_speaker or start - last_stamp >= a.every:
            if buf:
                out.append(f"{fmt(cur_start)} {cur_sp + ': ' if cur_sp else ''}{' '.join(buf)}")
            cur_sp, cur_start, buf, last_stamp = sp, start, [], start
        buf.append(body)
    if buf:
        out.append(f"{fmt(cur_start)} {cur_sp + ': ' if cur_sp else ''}{' '.join(buf)}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
