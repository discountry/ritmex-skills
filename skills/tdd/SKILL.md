---
name: tdd
description: >
  Apply when the task requires implementing net-new behavior — features, modules, endpoints, integrations, or any additive change. Drives development through strict red-green-refactor with test-first slicing and deterministic verification.
---

# TDD Skill

Strict red-green-refactor for all net-new behavior. Test-first, one behavior slice at a time.

---

## Constraints

- **Test-first** — no production code without a failing test that demands it.
- **Minimal diff** — no unrelated refactors, renames, or formatting churn.
- **Deterministic** — control time, randomness, I/O, and concurrency via seams/fakes.
- **Fail fast** — no silent error swallowing without a test proving the intent.

---

## Cycle

Per behavior slice, execute the canonical red-green-refactor loop:

1. **Red** — one test, failing for the right reason. Name encodes behavior + condition.
2. **Green** — minimum production code to pass. No speculative abstraction (Rule of Three).
3. **Refactor** — remove duplication, tighten names, simplify flow. Behavior unchanged.
4. **Verify** — run smallest relevant target first, then full suite. Report commands + outcomes.

---

## Output

- **Intent**: one sentence.
- **Test slices**: 3-7 bullets, ordered.
- **Changes**: tests added/updated + production code, by file.
- **Verification**: commands + pass/fail.
- **Risks**: contract changes, flaky-test vectors, uncovered boundaries.
