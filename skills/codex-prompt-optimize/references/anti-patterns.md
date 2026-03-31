# Anti-Patterns

Common low-quality prompt patterns to detect and correct during optimization.

## Vague task framing

**Detect:** No specific action or target — "look at this", "check the code", "help me with auth."

**Correct:** Rewrite `<task>` with a concrete action, explicit scope, and done-state.

```
Bad:  "Take a look at this and let me know what you think."
Good: <task>Review this change for correctness and regression risks.</task>
```

---

## Missing output contract

**Detect:** No indication of what the answer should contain — "investigate and report back."

**Correct:** Add `structured_output_contract` or `compact_output_contract`.

```
Bad:  "Investigate and report back."
Good: <compact_output_contract>
      Return: 1. root cause  2. evidence  3. smallest safe next step
      </compact_output_contract>
```

---

## No follow-through default

**Detect:** Codex will stall asking routine clarifying questions instead of proceeding.

**Correct:** Add `default_follow_through_policy`.

```
Bad:  "Debug this failure."
Good: <default_follow_through_policy>
      Keep going until you have enough evidence. Only stop for safety-critical unknowns.
      </default_follow_through_policy>
```

---

## "Think harder" nudges instead of contracts

**Detect:** Attempting to improve quality through encouragement rather than structure — "be very thorough", "think step by step", "be smart about this."

**Correct:** Replace with `verification_loop` or `completeness_contract`.

```
Bad:  "Think harder and be very smart."
Good: <verification_loop>
      Verify the answer against task requirements before finalizing.
      </verification_loop>
```

---

## Multiple unrelated jobs in one prompt

**Detect:** Two or more tasks with different scopes, intent categories, or deliverables.

**Correct:** Split into separate prompts. Optimize and execute the first. Queue the rest.

```
Bad:  "Review this diff, fix the bug you find, update the docs, and suggest a roadmap."
Good: Run review first → fix prompt if needed → docs/roadmap as separate runs.
```

---

## Unsupported certainty

**Detect:** Demanding definitive answers about things that require investigation — "tell me exactly why production failed."

**Correct:** Add `grounding_rules` to frame claims against evidence.

```
Bad:  "Tell me exactly why production failed."
Good: <grounding_rules>
      Ground every claim in context or tool outputs. Label hypotheses clearly.
      </grounding_rules>
```

---

## Scope inflation

**Detect:** A simple task wrapped in broad language that invites unnecessary work — "refactor the entire backend", "clean up everything."

**Correct:** Narrow the `<task>` scope to the specific area that needs attention. Add `action_safety` to prevent drift.

```
Bad:  "Clean up everything in the project."
Good: <task>Clean up unused imports and dead code in src/api/.</task>
      <action_safety>Do not modify logic or rename public exports.</action_safety>
```

---

## Missing verification for risky tasks

**Detect:** Write-capable tasks (fix, implement, refactor) with no verification step.

**Correct:** Add `verification_loop` and, for implementation/fix, `completeness_contract`.

```
Bad:  "Fix the payment processing bug."
Good: <verification_loop>
      Verify the fix against the reported failure before finalizing.
      </verification_loop>
      <completeness_contract>
      Resolve fully. Check for edge cases and follow-on fixes.
      </completeness_contract>
```
