@AGENTS.md

Claude Code specifics: the lifecycle agents live in `.claude/agents/` and are invoked by describing the task ("use the architect agent to draw the order flow") or by letting the main session delegate. Skills in `.claude/skills/` load automatically when a task matches their description, or on request with `/<skill-name>`.
