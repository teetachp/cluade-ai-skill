---
name: spec-writer
description: Turn an idea, ticket or conversation into a concise spec: problem, goals/non-goals, user stories with acceptance criteria (Given/When/Then), scope, open questions, and a rough task breakdown. Use when asked for a PRD, spec, requirements, user stories, acceptance criteria, or "what should we build" before coding starts.
---

# Spec writer

A spec exists so that the builder, the reviewer and the tester agree on "done" before code is written. Keep it short enough to be read in five minutes; link out for detail.

## Process

1. **Read what exists**: the issue/ticket, related code, previous specs in `docs/specs/`, and the product's conventions. Reuse the team's terms.
2. **Ask at most 3 questions** if something blocks a correct spec (who is the user, what is the trigger, what is out of scope). Otherwise state your assumptions in the spec and move on.
3. **Write to `docs/specs/<yyyy-mm-dd>-<slug>.md`** using `docs/templates/spec.md`.
4. **Check** every acceptance criterion is testable (someone could write a failing test from it) and every goal has at least one criterion.

## Writing rules

- Problem first, solution second. If the problem statement does not mention a user and a pain, rewrite it.
- Goals are outcomes ("checkout completes in < 2 s p95"), not features ("add a cache").
- Non-goals are as important as goals; list what a reader might expect that you are deliberately not doing.
- User stories: `As a <role>, I want <action> so that <outcome>`. One behavior each.
- Acceptance criteria in Given/When/Then; include the unhappy paths (invalid input, permissions, timeouts, empty states).
- Mark anything unknown as **Open question** with an owner; never hide uncertainty in confident prose.
- Flag risks: data migration, backwards compatibility, security/privacy, performance, third-party dependencies.
- Size the work roughly (S/M/L) and list the first tasks; do not plan sprints.

## Hand-off

End with a "Next" line: which agent/skill takes over (architecture decision → `adr-writer`; diagrams → `mermaid-diagrams`/`er-diagram`; implementation → builder with `ponytail`; tests → `test-plan`).
