#!/usr/bin/env bash
# Link skills (./skills) and subagents (./agents) into ~/.claude so Claude Code
# (CLI and the VS Code extension) loads them in every project.
# Usage: ./install.sh            link all skills and agents
#        ./install.sh name ...   link only the named skills/agents
#        ./install.sh --remove   remove links that point into this repo
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$ROOT/skills"
AGENTS_SRC="$ROOT/agents"
SKILLS_DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
AGENTS_DEST="${CLAUDE_AGENTS_DIR:-$HOME/.claude/agents}"
mkdir -p "$SKILLS_DEST" "$AGENTS_DEST"

if [[ "${1:-}" == "--remove" ]]; then
  for link in "$SKILLS_DEST"/* "$AGENTS_DEST"/*; do
    [[ -L "$link" && "$(readlink "$link")" == "$ROOT"/* ]] && rm "$link" && echo "removed $(basename "$link")"
  done
  exit 0
fi

link() {  # link <source> <target> <label>
  if [[ -e "$2" && ! -L "$2" ]]; then
    echo "skip $3 ($2 exists and is not a link)"; return
  fi
  ln -sfn "$1" "$2"
  echo "linked $3"
}

names=("$@")
if [[ ${#names[@]} -eq 0 ]]; then
  names=($(ls "$SKILLS_SRC") $(ls "$AGENTS_SRC" | sed 's/\.md$//'))
fi

for name in "${names[@]}"; do
  if [[ -f "$SKILLS_SRC/$name/SKILL.md" ]]; then
    link "$SKILLS_SRC/$name" "$SKILLS_DEST/$name" "skill $name"
  elif [[ -f "$AGENTS_SRC/$name.md" ]]; then
    link "$AGENTS_SRC/$name.md" "$AGENTS_DEST/$name.md" "agent $name"
  else
    echo "skip $name (no such skill or agent)"
  fi
done
