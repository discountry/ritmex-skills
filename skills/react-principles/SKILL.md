---
name: react-principles
description: React best practices for component design, state management, and Effect discipline. Use when writing, reviewing, or refactoring React components, custom hooks, or any .ts/.tsx/.js/.jsx file that uses React.
---

# React Development Principles

## Component Model

- Components are pure functions: `(props, state) → JSX`. Render must be side-effect-free.
- One-way data flow: parent → child via props, child → parent via callbacks.
- Never mutate state or props in-place.

## Thinking in React: Design Process

1. **Hierarchy** — decompose by SRP; one component, one concern. Map data model shape to component tree.
2. **Static first** — props only, no state, until the skeleton renders correctly.
3. **Minimal state** — DRY: if it's derivable, it's not state.
4. **Ownership** — hoist state to the closest common ancestor of all consumers.
5. **Inverse flow** — pass setters/handlers down; children call them on interaction.

### What is NOT state

- Computable from existing state or props → derive during render
- Passed in as a prop
- Unchanged over time

Prefer storing IDs/primitives; derive full objects at render time.

## Effect Discipline

`useEffect` is for **synchronizing with external systems** only — DOM APIs, network connections, third-party widgets, browser subscriptions. It is not a lifecycle hook and not a data-transformation pipeline.

### Deciding when to write an Effect

> **Why does this code run?**
> - Because the user did something → **event handler**
> - Because the component must stay in sync with something external → **Effect**

### Unnecessary Effects — replace with:

| Antipattern | Correct approach |
|---|---|
| Derived state via `useEffect` + `useState` | Compute during render; `useMemo` if expensive |
| State reset on prop change via Effect | `key` prop |
| Partial state adjustment on prop change | Store primitive ID; derive object during render |
| Shared event logic routed through state+Effect | Extract a plain function; call from event handlers |
| User-initiated POST in Effect | Move directly into the event handler |
| Effect chains (A → Effect → B → Effect → C) | Compute all next state in one event handler |
| Parent notification via Effect | Call both setters in the same event handler; or lift state |
| Pushing data up to parent via Effect | Parent fetches; passes data down as prop |
| One-time app init in component Effect | Module-level or `didInit` guard outside component |
| External store subscription via Effect | `useSyncExternalStore` |
| Data fetch without cleanup | `ignore` flag cleanup; prefer framework data-fetching |

### Effect rules

- Every reactive value the Effect reads must be in its dependency array.
- Never suppress `react-hooks/exhaustive-deps` — fix the code.
- Every resource acquired in setup must be released in cleanup.
- One Effect = one synchronization concern. Split unrelated concerns.
- Think **start sync / stop sync**, not mount / unmount.

## Key Heuristics

1. If it's computable at render time — compute it. No state, no Effect.
2. If it runs because the user did X — it's an event handler.
3. If it runs because the component is visible — it's an Effect.
4. If two state variables drift out of sync — lift state or derive one from the other.
5. If the dep array is long — the Effect does too much; split it.
6. If you want to suppress the deps linter — redesign instead.

## Supporting Reference Files

Load these files when deeper guidance is needed for the specific topic at hand:

- **Eliminating unnecessary Effects** (derived state, event logic, Effect chains, data fetching): see [references/not-need.md](references/not-need.md)
- **Effect lifecycle, reactive values, and dependency contract**: see [references/lifecycle.md](references/lifecycle.md)
- **Distinguishing event handlers from Effects, and using `useEffectEvent`**: see [references/separating.md](references/separating.md)
- **Strategies to reduce and stabilize Effect dependencies**: see [references/dependencies.md](references/dependencies.md)
- **Extracting reusable logic into custom hooks**: see [references/reusing.md](references/reusing.md)