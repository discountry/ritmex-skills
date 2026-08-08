---
name: how-to-use-effect
description: >
  Write, review, and debug `useEffect` correctly. Use whenever touching React code that
  contains an Effect — authoring a new one, reviewing a diff that includes one, or debugging
  symptoms like a spinner that never resolves, UI stuck in a loading/pending/verifying phase,
  a button permanently disabled, an Effect that fires twice or loops forever, a fetch race
  condition, a cleanup that cancels the wrong request, a stale closure reading old props/state,
  or a `react-hooks/exhaustive-deps` warning. Also use for setInterval / setTimeout /
  subscriptions / AbortController inside Effects, StrictMode double-invocation questions,
  multi-step async flows and state machines driven by Effects, and any .tsx/.jsx/.ts/.js file
  where `useEffect`, `useLayoutEffect`, or a custom hook wrapping them appears.
---

# How to use useEffect

An Effect **synchronizes a component with an external system**. It is not a lifecycle hook,
not a place to sequence a workflow, and not a state machine driver.

For the "should this be an Effect at all?" decision table (derived state, event logic, Effect
chains, parent notification, one-time init), use the **`react-principles`** skill. This skill
covers what that one does not: **the mechanics of an Effect body once you have decided you
need one** — where correct-looking code from the docs silently deadlocks.

---

## Gate: three questions before writing an Effect

1. **Can it be computed during render?** → compute it. No state, no Effect.
2. **Does it run because the user did something?** → event handler.
3. **Does it run because the component is on screen and must track something outside React?**
   → Effect. Everything else is a misuse.

---

## The five invariants

Every Effect you write or approve must satisfy all five. They are checkable mechanically.

| # | Invariant | How to check |
|---|---|---|
| 1 | **The body never sets state that is in its own dep array** | Intersect deps with every `setX` in the body, including inside `.then`, `await` continuations, and timer callbacks. Intersection must be empty. |
| 2 | **One Effect = one synchronization process** | If the body does two things (time *and* network, subscribe *and* fetch), split it. |
| 3 | **Cleanup mirrors setup** | Every resource acquired has exactly one release. No cleanup-only Effects. |
| 4 | **setup → cleanup → setup is indistinguishable from setup** | Dry-run StrictMode. If the second setup returns early or the work never completes, it is broken. |
| 5 | **Every non-terminal state has a guaranteed exit** | For each state the UI treats as "busy", trace at least one code path to a terminal state on both success and failure. |

Invariant 1 is the one that produces the worst bugs, and it is not stated anywhere in the
official docs. It is derived below.

---

## Trap 1 — The self-cancelling Effect

**The single most damaging `useEffect` bug, and it looks exactly like the documented pattern.**

```tsx
// ❌ BROKEN — permanently stuck in "verifying"
useEffect(() => {
  if (phase !== "waiting") return;
  let cancelled = false;

  const verify = async () => {
    setPhase("verifying");              // (a) writes a value that is in this Effect's deps
    const res = await fetch("/api/...");// (b) React re-renders → deps changed → cleanup runs
    if (cancelled) return;              // (c) cleanup set cancelled = true → own result dropped
    setPhase("ready");                  // (d) never reached. UI hangs forever.
  };

  const timer = setInterval(() => { if (countdownDone()) verify(); }, 250);
  return () => { cancelled = true; clearInterval(timer); };
}, [phase]);
```

The `cancelled` / `ignore` flag is the correct race-condition guard **only when the deps are
inputs that change from outside** (`query`, `roomId`, `url`, `userId`). There, "cleanup ran"
truthfully implies "a newer Effect run is superseding me, so my result is stale."

When the dep is state that the Effect body itself writes, that implication is false. "Cleanup
ran" now means "I advanced my own state," and the guard discards the response the flow was
waiting for. The Effect cancels itself. `tsc` passes, ESLint passes, the deps array is
exhaustive and honest — and the UI deadlocks.

**Test to apply, every time:**

> When this cleanup fires, is a replacement Effect run *guaranteed* to redo this work?
> If no — the `ignore` guard is wrong here.

**Fix: split the state machine so no Effect writes its own deps.** One Effect per phase; each
one ends by handing off to the next.

```tsx
// ✅ Effect A owns the countdown only. Its exit is a handoff.
useEffect(() => {
  if (phase !== "waiting") return;
  const tick = () => {
    const left = Math.max(0, Math.ceil((deadlineRef.current - Date.now()) / 1000));
    setRemaining(left);                       // `remaining` is NOT in deps — safe
    if (left === 0) { clearInterval(timer); setPhase("verifying"); }
  };
  const timer = setInterval(tick, 250);
  tick();
  return () => clearInterval(timer);
}, [phase]);

// ✅ Effect B owns the request only. Its cleanup now fires only when the request's own
//    result changed the phase, or the component unmounted — both correct times to ignore.
useEffect(() => {
  if (phase !== "verifying") return;
  let cancelled = false;

  (async () => {
    try {
      const res = await fetch("/api/...");
      if (cancelled) return;
      if (!res.ok) throw new Error("FAILED");
      const data = await res.json();
      if (cancelled) return;
      setAccessPath(data.path);
      setPhase("ready");
    } catch {
      if (cancelled) return;
      setPhase("error");                      // Invariant 5: failure has an exit too
    }
  })();

  return () => { cancelled = true; };
}, [phase, itemId]);
```

Both Effects still list `phase` in their deps — that is required and correct. What changed is
that **neither writes `phase` while an async continuation of its own run is still pending.**
Effect A's write happens synchronously in a timer callback with nothing awaiting behind it;
Effect B's writes happen after the last `await`, so the cleanup they trigger has nothing left
to cancel.

---

## Trap 2 — `didRun` refs as guards

```tsx
// ❌ breaks under StrictMode and after any legitimate re-run
if (startedRef.current) return;
startedRef.current = true;
```

The dev-mode setup → cleanup → setup cycle hits the early return on the second setup, so the
work never happens (violates invariant 4). A ref guard also silently defeats a real re-run
after a dep genuinely changed.

If an Effect needs "run once," that requirement belongs to the **dep array**, not to a ref.
Let the Effect own its lifecycle and let cleanup undo the first run. Reserve module-level
`didInit` flags for true once-per-app-load work (`checkAuthToken()`), never per-component.

---

## Trap 3 — Interval plus state in deps

```tsx
// ❌ resets the interval on every tick
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, [count]);

// ✅ updater function removes the dep entirely
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

Same shape as Trap 1 — the body writes its own dep — but the failure is a churning interval
rather than a deadlock. Whenever the next value derives from the previous, pass the updater.

---

## Trap 4 — Reading fresh values without reacting to them

Every reactive value the body reads must be a dep. To read the *latest* value without
re-running, do not lie to the linter — move that read into an Effect Event
(`useEffectEvent`, stable since React 19.2):

```tsx
const onVisit = useEffectEvent(visitedUrl => {
  logVisit(visitedUrl, shoppingCart.length);   // reads latest cart, non-reactively
});

useEffect(() => { onVisit(url); }, [url]);     // ✅ Effect Events are never deps
```

Never write `// eslint-disable-next-line react-hooks/exhaustive-deps` to make a warning go
away. If the deps feel wrong, the code shape is wrong: move objects/functions inside the
Effect, hoist non-reactive constants out of the component, use an updater, or use an Effect
Event.

---

## Trap 5 — Cleanup that does not mirror setup

Cleanup runs before **every** re-run with changed deps, not only on unmount. Cleanup logic
with no corresponding setup logic is a code smell. Cleanup that tears down more than its own
setup created (clearing shared state, aborting a controller owned by another Effect) breaks
the next run.

---

## Audit procedure

Run this on every Effect you write, and on every Effect in a diff you are reviewing.

1. **List the deps.** List every `setX` reachable from the body — including inside `await`
   continuations, `.then`, `setTimeout`/`setInterval` callbacks, and event listeners.
2. **Intersect the two lists.** Non-empty → go to step 3. Empty → skip to step 5.
3. **Trace the self-cancel.** Write out: setup → body calls `setX` → React commits → cleanup
   runs → new setup runs. Then ask: *does the async work started by run #1 still have a path
   to completion, or does run #2 early-return while run #1's result is discarded?* If the
   latter, you have Trap 1. Split the Effect.
4. **Confirm the split.** After splitting, every `setState` on a dep must be either synchronous
   in the body/timer callback, or after the final `await` of that run.
5. **Dry-run StrictMode.** setup → cleanup → setup. Is the observable outcome identical to a
   single setup? Watch for ref guards, counters, and non-idempotent side effects.
6. **Check every `await` boundary.** For each one, ask what happens if cleanup ran during it.
   Both branches must leave the UI in a state the user can act on.
7. **Enumerate terminal states.** For each state the UI renders as busy (spinner, `disabled`,
   a modal that blocks `onOpenChange`), find the code path out on success *and* on failure.
   A busy state with no exit is a deadlock waiting for a slow network.
8. **Check the lockout.** If the UI disables cancel/close during a phase, that phase must have
   a guaranteed exit — otherwise a single dropped response traps the user with no recovery.

---

## Verifying

Type-checking and linting cannot see any of these bugs — the broken code in Trap 1 passes
both. An Effect fix is verified only by **running the flow end to end** and observing the
terminal state: drive the real UI (browser automation, or the app itself), and separately
exercise the API/external system to confirm which side actually failed.

When a symptom is "stuck in a pending state," check the client state machine before suspecting
the server. Deadlocks in Effects present exactly like a hung request.
