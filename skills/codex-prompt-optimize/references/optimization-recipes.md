# Optimization Recipes

End-to-end examples of transforming raw user input into optimized Codex prompts.

## Fix — Vague scope (ask)

**Raw:** "fix the auth"

**Analysis:**
- Intent: Fix
- Scope: **missing** — which auth module? which bug?
- Constraints: check AGENTS.md
- Done-State: **missing**

**Action:** Scope is uninferrable. Ask one question:

> Which auth issue? (e.g., login failure, token expiry, permission error — or point me to the error log)

---

## Refactor — Broad scope (infer + optimize)

**Raw:** "refactor the backend to be cleaner"

**Analysis:**
- Intent: Refactor
- Scope: "backend" — broad but inferable from repo structure
- Constraints: inferable from AGENTS.md
- Done-State: "cleaner" — vague, infer concrete criteria

**Optimized:**

```xml
<task>
Refactor the backend source under src/api/ to reduce duplication and improve readability.
Preserve all existing behavior and public API contracts. Done when: no logic changes, existing
tests still pass, no function exceeds 30 lines.
</task>

<default_follow_through_policy>
Default to the most reasonable low-risk interpretation and keep going.
Only stop to ask when a missing detail changes correctness or triggers an irreversible action.
</default_follow_through_policy>

<completeness_contract>
Resolve the task fully before stopping.
Check for follow-on cleanup needed for a consistent result.
</completeness_contract>

<verification_loop>
Before finalizing, verify that all existing tests pass and no public API surface changed.
</verification_loop>

<action_safety>
Keep changes tightly scoped. Do not rename public exports, change config, or modify tests.
</action_safety>
```

---

## Diagnosis — No scope (ask)

**Raw:** "make it faster"

**Analysis:**
- Intent: Diagnosis (performance)
- Scope: **missing**
- Constraints: **missing**
- Done-State: "faster" — unmeasurable

**Action:** Scope is uninferrable. Ask one question:

> What is slow? (e.g., a specific endpoint, page load, build step, test suite — or share a timing/profile)

---

## Review — Scope inferable (optimize)

**Raw:** "review the PR"

**Analysis:**
- Intent: Review
- Scope: inferable (current branch diff)
- Constraints: check AGENTS.md
- Done-State: inferable (review output)

**Optimized:**

```xml
<task>
Review the current branch changes against the base branch for correctness and regression risks.
</task>

<structured_output_contract>
Return:
1. Findings ordered by severity (Critical → High → Medium → Low)
2. Supporting evidence for each finding
3. Suggested next steps
</structured_output_contract>

<grounding_rules>
Ground every claim in the diff or tool outputs.
If a point is an inference, label it clearly.
</grounding_rules>

<dig_deeper_nudge>
Check for second-order failures, empty-state handling, retries, stale state, and rollback paths.
</dig_deeper_nudge>

<verification_loop>
Before finalizing, verify that each finding is material and actionable.
</verification_loop>
```

---

## Implementation — Clear enough after rewrite (minimal blocks)

**Raw:** "add a health check endpoint"

**Analysis:**
- Intent: Implementation
- Scope: inferable (API layer, e.g., src/api/routes/)
- Constraints: inferable from AGENTS.md (framework, conventions)
- Done-State: inferable (endpoint responds 200, test added)

**Optimized:**

```xml
<task>
Add a GET /health endpoint that returns 200 with {"status": "ok"}.
Add it to the existing route file in src/api/routes/. Add a test.
Done when: endpoint responds correctly and test passes.
</task>

<default_follow_through_policy>
Default to the most reasonable low-risk interpretation and keep going.
Only stop to ask when a missing detail changes correctness or triggers an irreversible action.
</default_follow_through_policy>

<action_safety>
Keep changes tightly scoped. Do not refactor existing routes.
</action_safety>
```

Note: `<task>` was clear enough after rewriting — `completeness_contract` and `verification_loop` omitted because the task is trivially verifiable.

---

## Mixed asks — Split

**Raw:** "fix the login bug, add dark mode, and update the deps"

**Analysis:** Three unrelated tasks mixed into one prompt.

**Action:** Split into three. Optimize and execute the first:

```xml
<task>
Fix the login bug. [Scope and details from investigation or clarifying question.]
</task>
```

Queue "add dark mode" and "update deps" as follow-up tasks.
