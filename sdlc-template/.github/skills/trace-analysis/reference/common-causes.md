# Common failure patterns and where they usually point

| Symptom | Usual causes | First checks |
|---|---|---|
| `NullPointerException` / `TypeError: cannot read properties of undefined` / `AttributeError: 'NoneType'` | Optional value treated as present; API response shape changed; race on init | Which field is undefined? Trace it back to the producer; diff the producer's recent changes |
| `ECONNREFUSED`, `connection refused` | Dependency down, wrong host/port per environment, service not started yet | Env config for that environment; dependency health; startup order |
| `ETIMEDOUT`, `timeout`, `context deadline exceeded` | Slow downstream, missing index, lock contention, pool exhausted, DNS | Downstream latency graphs; slow query log; pool metrics; retries amplifying load |
| `too many connections`, `pool exhausted` | Connections not released; leak on error path; concurrency > pool size | Code paths that skip `finally`/`defer`; pool size vs worker count |
| `deadlock detected`, `Lock wait timeout` | Two transactions acquire rows in different order | Both statements' tables and order; shorten transactions; consistent ordering |
| `duplicate key value violates unique constraint` | Retry without idempotency; race in check-then-insert; sequence reset | Idempotency key; `INSERT ... ON CONFLICT`; who retries |
| `OOMKilled`, `OutOfMemoryError`, `heap out of memory` | Unbounded cache/list; loading full table; large file in memory; leak | Heap dump; what grows with request count; streaming instead of buffering |
| `CPU 100%`, latency rising with load | O(n²) on a growing list; regex backtracking; JSON of huge payload; GC thrash | Profile under load; recent change to a hot path |
| Works locally, fails in CI/prod | Env var missing; different timezone/locale; case-sensitive FS; different Node/Python version; network policy | Print config at startup (redacted); compare versions; check `.env.example` vs real |
| Flaky test | Order dependence; shared state; real time/randomness; network; port in use | Run alone vs in suite; seed randomness; freeze time; isolate state |
| `401`/`403` after deploy | Rotated secret; clock skew (JWT `nbf`/`exp`); wrong audience/issuer; CORS preflight | Decode the token; compare clocks; check issuer config |
| `500` with no stack trace | Error swallowed by catch; logger level; crash in error handler itself | Error middleware; `catch {}` blocks; process-level handlers |
| Data wrong but no error | Off-by-one; timezone conversion; float money; stale cache; eventual consistency read after write | Compare DB value vs displayed; cache TTL; replica lag |
| Intermittent `ECONNRESET` / `socket hang up` | Keep-alive mismatch; LB idle timeout shorter than client's; server restarted | LB idle timeout vs client keep-alive; deploy times |
| Migration failed / app boots with schema error | Migration ran partially; model and schema drift; wrong DB targeted | Migration table state; diff schema vs models |
| Message processed twice | At-least-once delivery without idempotent consumer; visibility timeout shorter than processing | Idempotency key; ack after commit; timeout vs p99 |
| Message never processed | Consumer group lag; poison message blocking partition; DLQ full | Lag metrics; DLQ; the first failing message |

## Reading order for a stack trace

1. Exception type and message (verbatim).
2. Innermost frame **in your code**.
3. `Caused by` chain to the bottom.
4. The request/trace id → surrounding log lines ±5 seconds.
5. Deploy/config change nearest before first occurrence.

## Useful commands

```bash
git log --since="3 days ago" --oneline -- path/to/area     # what changed
git log -S"functionName" --oneline                           # when a symbol changed
git bisect start && git bisect bad && git bisect good <tag>  # find the breaking commit
kubectl logs deploy/<svc> --since=30m | grep <request-id>
journalctl -u <svc> --since "1 hour ago"
grep -n "ERROR" app.log | cut -d' ' -f1-3 | uniq -c         # error rate by minute
```
