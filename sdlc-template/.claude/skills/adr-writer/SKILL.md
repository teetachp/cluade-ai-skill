---
name: adr-writer
description: Write or update an Architecture Decision Record (ADR): context, options considered with trade-offs, decision, consequences. Use when a design choice is being made (database, framework, API style, queue, auth, hosting, build vs buy), when asked "should we use X or Y", or when documenting why the code is the way it is.
---

# ADR writer

One decision per record, numbered, immutable once accepted (supersede instead of editing). Store in `docs/adr/NNNN-<slug>.md` using `docs/templates/adr.md`.

## Process

1. Find the next number (`ls docs/adr`), and check whether an existing ADR already covers or conflicts with this decision; if so, this one supersedes it and both link to each other.
2. State the **context**: the forces at play (requirements, constraints, team skills, deadlines, existing systems). Facts, not opinions.
3. List **2–4 real options**, including "do nothing / keep current". For each: how it works in one or two lines, pros, cons, cost/risk. Be honest about the option you do not prefer.
4. **Decision**: which option and the one or two reasons that actually decided it.
5. **Consequences**: what becomes easier, what becomes harder, what must be done now (migration, training, follow-up ADRs), and what would make you revisit.
6. Status: `Proposed` until the team agrees; then `Accepted`, later `Deprecated` or `Superseded by ADR-NNNN`.

## Rules

- A reader in two years should understand why without talking to anyone. Include dates, versions and links.
- No marketing language about tools; cite measured numbers or say "not measured".
- If the decision is reversible and cheap, say so and keep the ADR short; spend the words on the irreversible ones.
- When the user asks "X or Y?", answer with a recommendation and write the ADR as `Proposed`; do not just list trade-offs.
- Add a Mermaid diagram only when the structure is the point (e.g. sync vs event-driven); otherwise skip it.
