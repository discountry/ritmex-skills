---
name: debug
description: >
  Apply this skill whenever the user asks to debug, review, audit, or find problems in code — regardless of language or framework. Triggers include: "find bugs in this", "review my recent changes", "something is wrong but I don't know where", "check for security issues", "audit my commits", "why is this slow", "what am I missing in my tests", or any request to investigate correctness, safety, or performance. Prioritize recently modified files, staged changes, and the latest commits — the bug is almost always in what just changed.
license: MIT
---

# Debug Skill

> "Debugging is twice as hard as writing the code in the first place." — Brian Kernighan

Systematically surface logic flaws, latent bugs, performance bottlenecks, security vulnerabilities, and test gaps in existing code. Bias heavily toward **what recently changed** — most bugs live in the delta, not the stable baseline.

---

## Before Analyzing

1. **Orient to the diff** — ask for or examine: recent commits, staged changes, modified files. Fresh eyes on fresh code first.
2. **Understand the intent** — what is this code supposed to do? A bug is only a bug relative to expected behavior.
3. **Identify the blast radius** — where does this code touch? What depends on it?
4. **Don't assume the symptom is the problem** — the reported failure often points one layer away from the actual root cause.

---

## Analysis Dimensions

Work through each dimension. Not every dimension is equally relevant — weight by the nature of the code under review.

### Logic & Correctness
Off-by-one errors, wrong operator precedence, incorrect boundary conditions, inverted boolean logic, missed edge cases (empty input, zero, null/nil, maximum values), incorrect assumptions about ordering or uniqueness, race conditions in concurrent code.

### Latent Bugs
Code that works today but will break under different conditions: assumptions about data shape that aren't validated, silent failures from unchecked return values or ignored errors, state that can become inconsistent, error paths that swallow exceptions without logging or recovery.

### Performance
Unnecessary work inside loops, N+1 query patterns, missing indexes implied by query shape, repeated expensive computations that could be cached, unbounded growth (memory leaks, ever-growing collections), blocking calls on hot paths.

### Security
Injection vectors (SQL, command, template), unvalidated or unsanitized external input, authentication and authorization gaps, sensitive data in logs or error messages, insecure defaults, hardcoded secrets, over-broad permissions, missing rate limiting on exposed endpoints.

### Test Coverage Gaps
Happy path tested but edge cases absent, error paths untested, boundary values missing, mutable shared state between tests, tests that assert the wrong thing (passing for the wrong reason), missing regression tests for the exact scenario that just broke.

---

## High-Signal Patterns to Always Check

- **Error handling** — is every failure mode handled explicitly, or does it silently succeed/fail?
- **Trust boundaries** — where does untrusted data enter the system? Is it validated before use?
- **State mutation** — is shared mutable state accessed safely? Could two callers interfere?
- **Resource lifecycle** — are connections, file handles, locks always released, even on failure?
- **Type coercion / implicit conversion** — does the language allow surprising automatic conversions that could corrupt data?
- **Time and ordering** — does the code assume things happen in a specific order that isn't guaranteed?

---

## Root Cause Protocol

Don't stop at the symptom. For each issue found:

1. **What**: describe the specific flaw
2. **Why it's a problem**: the failure mode or impact
3. **Where it came from**: which change introduced it, if traceable
4. **Fix**: the minimal correct change — prefer targeted fixes over broad rewrites

---

## Output Format

1. **Summary** — one-line assessment of overall code health
2. **Issues** — ranked by severity (Critical → High → Medium → Low), each with: location, description, impact, fix
3. **Test gaps** — specific missing cases worth adding
4. **Positive observations** — note what is done well; debugging shouldn't only be adversarial

Scope large codebases to the changed surface area first. Expand to stable code only if the bug clearly originates there.
