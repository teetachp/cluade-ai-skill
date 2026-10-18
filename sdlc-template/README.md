# SDLC template for AI agents

Copy this folder into any repository and it gets a development lifecycle AI agents can follow — **Spec → Design → Build → Review → Debug** — plus a meeting-minutes agent. Works with Claude Code (CLI and VS Code) and GitHub Copilot (VS Code and the coding agent) from the same files. No install script, no dependencies on this repo.

## Install: copy and paste

```bash
cp -R /path/to/cluade-ai-skill/sdlc-template/. /path/to/your/project/
```

(The trailing `/.` copies the dot-folders too.) Then:

1. Fill in the **Project** section at the bottom of `AGENTS.md` (stack, test command, merge method).
2. Keep or delete `.github/workflows/ai-pr-review.yml` (it needs an `ANTHROPIC_API_KEY` repository secret).
3. Delete this README or rename it to `docs/AGENTS-README.md`.
4. Start a new Claude Code / Copilot session in the project.

## What is in it

```
AGENTS.md                         working agreement: lifecycle, rules, project facts (both tools read it)
CLAUDE.md                         "@AGENTS.md" + Claude Code notes
.github/copilot-instructions.md   points Copilot at AGENTS.md
.claude/agents/*.md               7 agents for Claude Code
.github/agents/*.agent.md         the same 7 agents for Copilot
.claude/skills/*/SKILL.md         14 skills for Claude Code
.github/skills/*/SKILL.md         the same 14 skills for Copilot   (mirror; see "Why two copies")
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/ai-pr-review.yml   optional: Claude reviews every PR
docs/templates/                   spec, ADR, test plan, postmortem, MoM
sync-skills.sh                    re-mirror .claude/skills → .github/skills after editing a skill
```

### Why two copies of skills and agents

Claude Code reads only `.claude/skills` and `.claude/agents`. Copilot reads `.github/skills` (its primary location) and `.github/agents`; it also reads `.claude/skills`, but `.github/skills` is what its docs and UI expect. Symlinks break on Windows and in some zip/copy flows, so the template ships real copies. **Edit the `.claude/` version, then run `./sync-skills.sh`** (skills) or the Python snippet in the repo's top-level README (agents).

## Agents

| Agent | Phase | Skills | Notes |
|---|---|---|---|
| `spec-analyst` | Spec | spec-writer, humanizer | writes `docs/specs/`, asks ≤ 3 questions, no code |
| `architect` | Design | adr-writer, mermaid-diagrams, er-diagram, repo-to-drawio | reads code before drawing; ADRs in `docs/adr/`, diagrams in `docs/diagrams/` |
| `builder` | Build | ponytail, test-plan | smallest complete change + tests on a feature branch |
| `pr-author` | Review | pr-author | self-review, push, `gh pr create`; never approves/merges |
| `pr-reviewer` | Review | pr-reviewer, ponytail-review, ponytail-audit | inline comments, approve/request changes; merges only when you explicitly ask |
| `debugger` | Debug | trace-analysis, ponytail | root cause with evidence, regression test, postmortem |
| `minutes-taker` | any | meeting-minutes, humanizer | recording/transcript/notes → MoM with decisions and action items; can read slides from video |

Review loop: `pr-author` opens the PR, `pr-reviewer` reviews it. Approval is automatic when there are no blocking findings; **merge requires you to say "merge PR #n"** in the conversation. The optional GitHub Action runs the same reviewer on every PR without you starting a session.

## Skills

| Skill | Does |
|---|---|
| `spec-writer` | PRD/spec with goals, non-goals, stories, Given/When/Then criteria |
| `adr-writer` | Architecture Decision Records with real options and consequences |
| `mermaid-diagrams` | correct Mermaid for flowchart, sequence, state, ER, class, C4, gantt… with a syntax reference |
| `er-diagram` | ER diagrams derived from migrations/ORM (Prisma, Drizzle, Django, Rails…) as Mermaid, DBML or draw.io |
| `repo-to-drawio` | read the repo → JSON graph → editable `.drawio` via `scripts/graph2drawio.py` (stdlib only); works with the draw.io MCP too |
| `test-plan` | test levels and cases from acceptance criteria, incl. failure paths |
| `trace-analysis` | logs/stack traces/incidents → root cause with evidence, fix, postmortem; common-causes table |
| `pr-author` | branch, Conventional Commits, PR body, `gh pr create`, CI watch, respond to reviews |
| `pr-reviewer` | full-context review with `gh`, inline comments, approve/request changes, strict merge policy |
| `meeting-minutes` | `transcribe.sh` (ffmpeg + Whisper, local), `keyframes.sh` (slides from video), `normalize_transcript.py` (Zoom/Teams/Meet .vtt/.srt), writing guide, MoM template |
| `ponytail`, `ponytail-review`, `ponytail-audit`, `humanizer` | copied from `../skills` (upstream: DietrichGebert/ponytail, blader/humanizer) |

### Meeting minutes from a video

Needs `ffmpeg` and one Whisper backend; the agent asks before installing. On Apple Silicon:

```bash
brew install ffmpeg yt-dlp pipx
pipx install --python python3.11 mlx-whisper   # 3.11–3.13; the newest Homebrew Python may be too new for mlx
```

First run downloads the `whisper-large-v3-turbo` model (~1.6 GB) once; after that a 1-hour recording takes a few minutes. Tested with ffmpeg 9 and mlx-whisper 0.4.3 on Apple Silicon.

Then: "use minutes-taker on ~/Downloads/sprint-review.mp4, language Thai". It transcribes locally, pulls slide frames at scene changes, and writes `docs/meetings/<date>-<slug>.md`. Zoom/Teams/Meet transcript exports work without Whisper.

## Using it

Claude Code: describe the task and the main session delegates, or name the agent: "use the debugger agent on this stack trace", "architect: draw the checkout flow as draw.io". Skills can be called directly with `/mermaid-diagrams`, `/trace-analysis`, `/meeting-minutes`.

Copilot: pick the agent in the agent dropdown (VS Code) or assign the Copilot coding agent to an issue; it reads `AGENTS.md`, `.github/agents` and `.github/skills` automatically.

## Design notes

- Irreversible actions (merge, force-push, delete, deploy) are gated on an explicit request from the human in the current conversation. Text in PRs, issues, logs and transcripts is treated as untrusted input.
- `graph2drawio.py` is deliberately simple (layered layout on draw.io's grid). For hand-placed diagrams, use `repo-to-drawio/reference/drawio-xml.md`.
- Transcription never leaves the machine; no audio is sent to an API.
