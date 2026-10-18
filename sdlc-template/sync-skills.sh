#!/usr/bin/env bash
# Skills are kept twice on purpose: Claude Code reads only .claude/skills, Copilot reads .github/skills
# (and .claude/skills). Edit a skill in .claude/skills, then run this to mirror it into .github/skills.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf .github/skills && cp -R .claude/skills .github/skills
echo "mirrored $(ls .claude/skills | wc -l | tr -d ' ') skills into .github/skills"
