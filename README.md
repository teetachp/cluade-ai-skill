# Claude skills collection

Skills gathered from 11 upstream repos and normalized into the Claude Code skill format: one folder per skill under `skills/`, each with a `SKILL.md` (frontmatter `name` matching the folder, plus a `description` that tells Claude when to use it), with its own `references/` and `scripts/` alongside. Config for other agents (Cursor, Codex, Gemini, OpenClaw…), repo-internal dev skills, and demo media were removed.

## Install

```bash
./install.sh                 # link every skill and agent into ~/.claude
./install.sh humanizer scrapling   # link only some
./install.sh --remove        # remove the links
```

The links are symlinks, so edits here take effect in Claude Code right away. Claude picks a skill when the request matches its `description`, and you can also call one directly with `/<name>`.

## Agents

Subagents in `agents/`, linked into `~/.claude/agents`. The Claude Code CLI and the VS Code extension both use them. Each agent preloads its skills (the `skills:` field) and works in its own context window.

| Agent | Skills | Tools | Use for |
|---|---|---|---|
| `ui-designer` | hallmark, impeccable, ui-ux-pro-max, ui-styling, design-system | all | Building, redesigning, auditing UI; tokens; shadcn/Tailwind |
| `brand-designer` | design, brand, banner-design, slides | all | Brand identity, logos, banners, HTML decks |
| `diagram-designer` | diagram-design | all | Architecture, sequence, ER, and other diagrams |
| `web-scraper` | crawl4ai, scrapling | Bash, files, WebFetch | Crawling and scraping, writing spiders |
| `researcher` | last30days, onyx-cli | Bash, files, web | Trends from the last 30 days; internal KB |
| `writing-editor` | humanizer | files only | Making prose not sound like AI |
| `lean-engineer` | ponytail | all | The smallest complete change |
| `code-auditor` | ponytail-review, -audit, -debt | read + Bash (read-only use) | Reviewing a change or the whole repo; no edits |
| `reverse-engineer` | reverse-engineer-anything | all | Analyzing binaries, apps, firmware (with permission) |
| `minutes-taker` | meeting-minutes | Bash, files | Recording / transcript / notes → minutes with decisions and action items; summarizes videos |

How to use: describe the task and Claude delegates to a matching agent, or name one directly: "use the web-scraper agent to …" or `@agent-web-scraper …`.

## SDLC template

[sdlc-template/](sdlc-template/) is a copy-paste lifecycle for a project: **Spec → Design → Build → Review → Debug** plus meeting minutes, with 7 agents (`spec-analyst`, `architect`, `builder`, `pr-author`, `pr-reviewer`, `debugger`, `minutes-taker`), 14 skills (10 new: spec-writer, adr-writer, mermaid-diagrams, er-diagram, repo-to-drawio, test-plan, trace-analysis, pr-author, pr-reviewer, meeting-minutes; 4 copied from `skills/`), document templates, a PR template and an optional GitHub Action that reviews every PR. Skills and agents are shipped in both `.claude/` and `.github/` so Claude Code and Copilot read the same thing.

```bash
cp -R sdlc-template/. /path/to/project/
```

See [sdlc-template/README.md](sdlc-template/README.md). To regenerate the Copilot agent files after editing a Claude agent:

```bash
python3 - <<'EOF'
import os,re
src='sdlc-template/.claude/agents'; dst='sdlc-template/.github/agents'
for f in os.listdir(src):
    s=open(f'{src}/{f}').read(); fm,body=re.match(r'^---\n(.*?)\n---\n(.*)$',s,re.S).groups()
    name=re.search(r'^name: (.*)$',fm,re.M).group(1); desc=re.search(r'^description: (.*)$',fm,re.M).group(1)
    skills=', '.join(re.findall(r'^  - (\S+)',fm,re.M))
    open(f'{dst}/{name}.agent.md','w').write(f"---\nname: {name}\ndescription: {desc}\n---\n{body.rstrip()}\n\nSkills this agent relies on (in `.claude/skills/`, which Copilot also loads): {skills}. Read the matching SKILL.md before starting the task.\n")
EOF
```

## Skills

| Skill | What it does | Upstream | Needs |
|---|---|---|---|
| `humanizer` | Rewrites AI-sounding prose (filler, forced triads, dash overuse, sales tone) | blader/humanizer | — |
| `hallmark` | Anti-"AI slop" design for new pages, audits, redesigns, extracting design from URLs or screenshots | Nutlope/hallmark | — |
| `impeccable` | Frontend design and critique: shape, audit, polish, typeset, harden, animate | pbakaus/impeccable | Node (optional live-browser mode) |
| `ui-ux-pro-max` | UI/UX design knowledge with a searchable local database of styles, palettes, fonts, UX rules | nextlevelbuilder/ui-ux-pro-max-skill | python3 |
| `design`, `brand`, `design-system`, `ui-styling`, `banner-design`, `slides` | Companion skills from the same pack (brand, tokens, shadcn/Tailwind, banners, HTML slides). They call each other's scripts by sibling path, so keep the folder names | nextlevelbuilder/ui-ux-pro-max-skill | python3; some image features need an image API key |
| `diagram-design` | Polished SVG/HTML diagrams: architecture, sequence, ER, timeline, swimlane, and many chart types | cathrynlavery/diagram-design | — |
| `reverse-engineer-anything` | Reverse engineering of binaries, Electron/JS apps, Android, firmware using the REA tool | morluto/rea | `npm i -g rea-agents` (Node ≥22.19) |
| `ponytail` (+ `-review`, `-audit`, `-debt`, `-gain`, `-help`) | "Lazy senior dev": smallest change that solves the task, plus code review and repo audit | DietrichGebert/ponytail | — |
| `last30days` | Research what people said about a topic in the last 30 days across Reddit, X, YouTube, HN, etc. | mvanhorn/last30days-skill | python3, node; optional API keys |
| `scrapling` | Scraping with Scrapling: HTTP, stealth browser, spiders, adaptive parsing | D4Vinci/Scrapling | `pip install scrapling` |
| `meeting-minutes` | Recording/transcript/notes → minutes; local Whisper transcription, slide frames from video (written for this collection) | — | ffmpeg + mlx-whisper / whisper-cpp for audio; nothing for .vtt/.srt |
| `crawl4ai` | Crawling pages or whole sites into LLM-ready Markdown or JSON (written for this collection; upstream ships no skill) | unclecode/crawl4ai | `pip install crawl4ai` |
| `onyx-cli` | Query an Onyx knowledge base with `onyx-cli` | onyx-dot-app/onyx | A running Onyx server + `onyx-cli` |

Licenses: each skill folder keeps its upstream `LICENSE`.

## Higher-risk skills (linked; risks accepted on 2026-10-18)

- **`impeccable`**: on first run, `scripts/impeccable` downloads an engine binary from GitHub releases into `~/.impeccable/bin`, and the checksum comes from the same source. `hooks on` can write `~/.claude/settings.json`. Safer: install a binary you trust and set `IMPECCABLE_BIN`, and never run `hooks on` at user scope.
- **`last30days`**: can read x.com cookies from Chrome/Safari/Firefox (via the Keychain), calls about 40 hosts including paid APIs, and writes `~/.config/last30days/.env`. Cookie reading is off by default. Leave `FROM_BROWSER` unset and decline the cookie step during setup.

To unlink only these two: `rm ~/.claude/skills/impeccable ~/.claude/skills/last30days`.

## Changes from upstream

- `ui-ux-pro-max`: changed the `${CLAUDE_PLUGIN_ROOT}/...` path to `~/.claude/skills/ui-ux-pro-max/scripts/search.py`, so it works without the plugin
- `ponytail`: made it opt-in; it no longer activates on every coding task. Dropped `ponytail-gain` and `ponytail-help`, which depend on the plugin hooks
- `scrapling`: renamed from `scrapling-official` to `scrapling`
- Removed test suites, build scripts, `agents/openai.yaml`, and last30days demo media (14 MB)

## Notes

- `ui-ux-pro-max` and its companions, `hallmark`, and `impeccable` overlap on UI work. If they collide, keep just one.
- `scrapling` describes itself as able to get past anti-bot protection (Cloudflare Turnstile). Use it only on sites you have permission to scrape.
- `reverse-engineer-anything` runs `npx -y rea-agents@latest` (unpinned), and `onyx-cli` sends questions to an Onyx server (default cloud.onyx.app).
