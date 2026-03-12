---
name: refactor
description: >
  Apply this skill whenever the user asks to refactor, clean up, restructure, or improve existing code — regardless of language or framework. Triggers include: "refactor this", "clean up my code", "this file is too long", "this function is hard to read", "reduce duplication", "decouple this", "improve maintainability", "apply design patterns", or any request to improve code quality without changing observable behavior. Also trigger when reviewing code that has obvious smells: god files, deeply nested logic, long parameter lists, duplicated blocks, or functions exceeding ~30 lines.
---

# Refactor Skill

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler

Iteratively improve code for **readability, maintainability, and reusability** without breaking observable behavior. Apply the principles of *Refactoring* (Fowler), *Clean Code* (Martin), and *The Art of Readable Code* (Boswell & Foucher).

Refactoring is **not** rewriting. Change structure, not behavior.

---

## Before Touching Anything

1. Understand what the code actually does and where its boundaries are.
2. Identify the highest-pain smells — prioritize ruthlessly.
3. If tests are absent, flag it. Refactoring without a safety net is high-risk.
4. Propose an incremental plan. Never refactor everything in one pass.

---

## Core Principles

**SRP everywhere** — functions, classes, modules, files each own exactly one responsibility.

**Size as a signal, not a rule** — functions trending past ~30 lines and files past ~300 lines are worth questioning. But complexity varies: a genuinely complex algorithm may justify more lines than a simple utility. Use size as a prompt to ask "is this doing too much?" not as a threshold to mechanically split.

**Names over comments** — a name that requires a comment to explain is a name that needs replacing. Reserve comments for *why*, never *what*.

**DRY without fanaticism** — eliminate duplication by extracting shared abstractions, but never force unrelated concepts into one abstraction just because they look alike. The wrong abstraction is worse than duplication.

**Low coupling, high cohesion** — depend on abstractions, inject dependencies, keep things that change together physically together.

**Guard clauses over nesting** — return early, validate at the top, keep the happy path flat.

**No magic values** — every domain-meaningful literal gets a named constant.

---

## Refactoring Moves (Fowler Catalog)

Name the move when applying it — shared vocabulary improves code review:

| Move | Trigger |
|---|---|
| Extract Function | block has a describable singular purpose |
| Extract Variable | complex expression needs a name |
| Introduce Parameter Object | many related parameters travel together |
| Replace Conditional with Polymorphism | type-keyed branch chains |
| Decompose Conditional | boolean logic obscures intent |
| Separate Query from Modifier | function both returns and mutates |
| Move Function/Field | logic lives in the wrong module |
| Replace Magic Number with Constant | naked literal carries domain meaning |

---

## Code Smells → Fix

| Smell | Fix |
|---|---|
| God File / God Class | split by SRP |
| Long Function | Extract Function |
| Long Parameter List | Parameter Object / Builder |
| Duplicate Code | shared abstraction |
| Deep Nesting | guard clauses + Extract Function |
| Shotgun Surgery | consolidate; reduce coupling |
| Feature Envy | move logic to the data it needs |
| Dead Code | delete — git remembers |

---

## Design Patterns

Apply only when the problem genuinely exists. Preferred patterns for decoupling and flexibility: Strategy, Factory, Observer, Repository, Decorator, Command.

> Simpler is always preferred. A pattern without a problem is over-engineering. Real-world complexity sometimes justifies less abstraction, not more.

---

## Iterative Protocol

One smell → one fix → verify → commit (with the move name in the message) → repeat.

Never mix refactoring commits with feature commits.

---

## Output Format

1. **Diagnosis** — smells found, ranked by severity
2. **Plan** — moves to apply, in order
3. **Refactored Code** — before/after, clearly labeled
4. **Rationale** — one sentence per significant change
5. **Behavior preserved** — explicit confirmation

Scope large codebases to one module or function per response. Say so when doing this.
