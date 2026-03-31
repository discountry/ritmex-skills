# Prompt Blocks

Reusable XML blocks for assembling optimized Codex prompts. Include only the blocks the task requires.

## Required Blocks

### `task`

Always include. The concrete job, scope, and done-state.

```xml
<task>
[Rewritten goal with scope, target files/modules, and done-state.]
</task>
```

### `default_follow_through_policy`

Always include. Prevents Codex from stalling on routine decisions.

```xml
<default_follow_through_policy>
Default to the most reasonable low-risk interpretation and keep going.
Only stop to ask when a missing detail changes correctness, safety, or triggers an irreversible action.
</default_follow_through_policy>
```

## Output Contracts

### `structured_output_contract`

Use when the response shape matters — fixes, reviews, research.

```xml
<structured_output_contract>
Return:
1. [primary deliverable]
2. [evidence or touched files]
3. [verification performed]
4. [residual risks or follow-ups]
</structured_output_contract>
```

### `compact_output_contract`

Use for diagnosis or quick answers where structured format is overkill.

```xml
<compact_output_contract>
Return a compact result with:
1. most likely root cause
2. evidence
3. smallest safe next step
</compact_output_contract>
```

## Completion and Verification

### `completeness_contract`

Use for implementation, fix, or refactor tasks that should not stop early.

```xml
<completeness_contract>
Resolve the task fully before stopping.
Do not stop at the first plausible answer.
Check for follow-on fixes, edge cases, or cleanup needed.
</completeness_contract>
```

### `verification_loop`

Use whenever correctness matters.

```xml
<verification_loop>
Before finalizing, verify the result against the task requirements and changed files.
If a check fails, revise instead of reporting the first draft.
</verification_loop>
```

## Grounding and Context

### `missing_context_gating`

Use when Codex might otherwise guess missing facts.

```xml
<missing_context_gating>
Do not guess missing repository facts.
If required context is absent, retrieve it with tools or state exactly what remains unknown.
</missing_context_gating>
```

### `grounding_rules`

Use for review, research, or root-cause analysis.

```xml
<grounding_rules>
Ground every claim in the provided context or tool outputs.
Do not present inferences as facts. Label hypotheses clearly.
</grounding_rules>
```

### `citation_rules`

Use for research or recommendation tasks.

```xml
<citation_rules>
Back important claims with explicit references to inspected sources. Prefer primary sources.
</citation_rules>
```

## Safety and Scope

### `action_safety`

Use for any write-capable or potentially broad task.

```xml
<action_safety>
Keep changes tightly scoped to the stated task.
Avoid unrelated refactors, renames, or cleanup unless required for correctness.
</action_safety>
```

## Depth and Exploration

### `research_mode`

Use for comparisons, recommendations, or exploration tasks.

```xml
<research_mode>
Separate observed facts, reasoned inferences, and open questions.
Prefer breadth first, then depth only where evidence changes the recommendation.
</research_mode>
```

### `dig_deeper_nudge`

Use for review and adversarial inspection.

```xml
<dig_deeper_nudge>
After finding the first plausible issue, check for second-order failures, empty-state behavior,
retries, stale state, and rollback paths before finalizing.
</dig_deeper_nudge>
```
