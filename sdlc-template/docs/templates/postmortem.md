# Postmortem: <short title>

Blameless. The goal is to understand the system, not to find who to blame.

| | |
|---|---|
| Date of incident | <yyyy-mm-dd> |
| Duration | <start–end UTC>, <n> min |
| Severity | SEV1 / SEV2 / SEV3 |
| Author | |
| Status | Draft / Reviewed |

## Summary

Two or three sentences: what broke, who was affected, how it was resolved.

## Impact

- Users / customers affected:
- Requests failed / data affected:
- Revenue / SLA:

## Timeline (UTC)

| Time | Event |
|---|---|
| 09:02 | Alert fired: ... |
| 09:05 | On-call acknowledged |
| 09:10 | Rollback of <deploy> started |
| 09:15 | Error rate back to baseline |

## Root cause

What actually caused it, with file/config references. Distinguish the trigger (the deploy, the traffic spike) from the underlying cause (the missing timeout, the unindexed query).

## Contributing factors

- Why it was not caught earlier (tests, review, staging)
- Why detection took as long as it did
- Why mitigation took as long as it did

## What went well

- 

## Action items

| Action | Type (prevent / detect / mitigate) | Owner | Due | Status |
|---|---|---|---|---|

## Lessons

What we now know about the system that we did not before.
