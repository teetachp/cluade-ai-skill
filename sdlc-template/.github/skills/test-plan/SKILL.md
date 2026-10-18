---
name: test-plan
description: Derive a test plan from a spec, PR or feature: what to test at which level (unit, integration, e2e, contract, performance), the concrete cases including edge and failure paths, test data, and what to automate vs check manually. Use when asked "how should we test this", for a QA plan, to find missing test coverage for a change, or to write the tests for acceptance criteria.
---

# Test plan

## 1. Start from behavior, not code

Collect the acceptance criteria (spec, issue, PR description). If none exist, write 3–6 one-line behaviors from reading the code and confirm them in the report as assumptions.

## 2. Pick the level per behavior

| Level | Use for | Avoid for |
|---|---|---|
| Unit | pure logic, branching, validation, calculations | anything that mostly exercises a framework |
| Integration | DB queries, repositories, HTTP handlers with a real test DB, message handlers | UI flows |
| Contract | APIs consumed by other teams/services (OpenAPI, Pact) | internal functions |
| E2E | the 3–5 money paths (sign-up, checkout, core workflow) | every edge case |
| Performance | hot paths with an SLO, migrations on large tables | code without a stated target |
| Security | authz on every new endpoint, input validation, secrets | — |

Prefer the lowest level that can prove the behavior. One e2e test per critical path, many unit tests per branch.

## 3. Enumerate cases

For each behavior write cases as `Given / When / Then`, covering:
- happy path
- boundaries (0, 1, max, empty, unicode, very long, negative, past/future dates, timezone edges)
- invalid input and the exact error returned
- permissions (wrong user, wrong tenant, expired token)
- failure of dependencies (DB down, timeout, 429, partial failure, duplicate message)
- concurrency where it matters (double submit, two workers)
- idempotency of retries
- migration: up, down, with existing data

Mark each case `auto` or `manual` and name the test file it goes in. Use the repo's existing test framework and fixtures; do not introduce a new one.

## 4. Test data

Say where data comes from (factories, fixtures, seeded DB) and how it is isolated (transaction rollback, unique prefixes, fresh container). No production data.

## 5. Output

Write `docs/test-plans/<slug>.md` with: scope, out of scope, levels, case table (`id | behavior | given/when/then | level | auto/manual | file`), test data, risks, and a "coverage gaps" section if reviewing an existing change. When asked to implement, write the automated tests from the table in the order: unit → integration → e2e, running each as you go, and report pass/fail honestly.
