# Effect Lifecycle & Reactive Values

## Mental Model

Think **start sync / stop sync**, not mount / unmount.

```
mount        → setup
deps change  → cleanup (prev) → setup (next)
unmount      → cleanup
```

## Reactive Values

Reactive: props, state, context, and anything derived from them inside the component body.  
Not reactive: module-level constants, refs (`.current` is mutable but not tracked).

## Dependency Contract

The dep array declares what the Effect reads reactively — not a performance knob.

| Config | Meaning |
|---|---|
| `[a, b]` | Re-synchronize when `a` or `b` changes |
| `[]` | Synchronize once — reads no reactive values |
| *(omitted)* | Re-synchronize after every render — bug |

- Include every reactive value the Effect reads.
- Never add values the Effect doesn't read.
- Never suppress `react-hooks/exhaustive-deps` — fix the code.
- Wanting `[]` while reading props/state = stale closure bug, not a config choice.

## One Effect = One Synchronization Concern

Split Effects that handle unrelated external systems. Never merge for code-sharing.

```ts
// ❌
useEffect(() => {
  logVisit(roomId);
  const conn = createConnection(serverUrl, roomId);
  conn.connect();
  return () => conn.disconnect();
}, [serverUrl, roomId]);

// ✅
useEffect(() => { logVisit(roomId); }, [roomId]);

useEffect(() => {
  const conn = createConnection(serverUrl, roomId);
  conn.connect();
  return () => conn.disconnect();
}, [serverUrl, roomId]);
```

## Cleanup Correctness

Cleanup must fully undo what setup did. An Effect is correct if setup → cleanup → setup leaves the system in a valid state. Strict Mode verifies this by cycling the Effect on mount.

## Dep Instability Patterns

```ts
// ❌ object literal — new reference every render
useEffect(() => { ... }, [{ id }]);

// ❌ inline function — new reference every render
useEffect(() => { ... }, [() => handle()]);

// ❌ ref.current — not reactive; changes won't re-trigger the Effect
useEffect(() => { ... }, [ref.current]);

// ✅ primitives compared by value
useEffect(() => { ... }, [id, serverUrl]);
```

Move objects/functions **inside the Effect** or **hoist to module scope** to eliminate referential instability.