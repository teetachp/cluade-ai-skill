---
name: pr-author
description: Prepare and open a pull request on GitHub with the gh CLI: branch, well-scoped commits (Conventional Commits), self-review, a PR description that follows the repo template, linked issue, labels and reviewers. Use when asked to "open a PR", "push this up", "commit and create a pull request", or to split work into reviewable PRs.
---

# PR author

A PR is a request for someone's time. Make it small, explain why, and prove it works.

## Before opening

1. **Branch**: never commit to `main`/`master`. Branch name `<type>/<short-slug>` (`feat/order-retry`, `fix/jwt-clock-skew`). If already on a feature branch, keep it.
2. **Self-review the diff**: `git diff main...HEAD`. Remove debug prints, unrelated formatting, secrets, generated files that should not be committed. If the diff mixes two concerns, split into two PRs.
3. **Run what CI runs**: tests, lint, type-check, build. Paste the summary in the PR. If something fails and you open the PR anyway, say so under "Known issues".
4. **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`), imperative mood, one logical change each. Squash fixups. End commit messages with any attribution line the session requires.

## Open the PR

```bash
git push -u origin HEAD
gh pr create --base main --title "<type>(<scope>): <summary ≤ 70 chars>" --body-file /tmp/pr-body.md \
  [--draft] [--label <label>] [--reviewer <user>] [--assignee @me]
```

Body: use `.github/PULL_REQUEST_TEMPLATE.md` if the repo has one; otherwise:

```
## Why
<the problem or the issue link: Closes #123>

## What
- <change 1>
- <change 2>

## How to verify
<commands or steps a reviewer can run; screenshots for UI>

## Risk / rollout
<migration? feature flag? backwards compatible? rollback plan>

## Checks
- [x] tests: <summary>
- [x] lint / typecheck
- [ ] docs updated (n/a)
```

Open as **draft** when CI has not run yet or the work is for early feedback; mark ready with `gh pr ready` once green.

## After opening

- Watch the first CI run: `gh pr checks --watch`. Fix red checks in follow-up commits; do not force-push over reviewed commits unless the repo prefers it.
- Respond to every review comment: fix it, or explain why not, and resolve the thread. Re-request review when done: `gh pr edit --add-reviewer <user>`.
- You open and update PRs; you do **not** approve or merge your own PR. Hand off to the `pr-reviewer` agent or a human.

## Rules

- Ask before pushing to a shared branch or a repository the user has not named in this conversation.
- Never include secrets, tokens, `.env` files or customer data in a diff or description.
- Keep PRs under ~400 changed lines where possible; stacked PRs beat one large one.
- Title and description in the repository's language (usually English), matching the existing PR style.
