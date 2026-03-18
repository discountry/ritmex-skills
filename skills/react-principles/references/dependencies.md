# Managing Effect Dependencies

Dependencies are a **consequence of code, not a choice**. Never omit a reactive value the Effect reads. Fix the code to need fewer deps; don't misrepresent what the Effect reads.

> Suppressing `react-hooks/exhaustive-deps` is always wrong — it hides stale-closure bugs.

## Strategies to Reduce Dependencies

### Hoist static values outside the component

```ts
// ❌ object recreated each render → Effect re-runs every render
function C() {
  const options = { serverUrl, roomId };
  useEffect(() => connect(options), [options]);
}

// ✅ module-level constant — not reactive, not a dep
const OPTIONS = { serverUrl: 'https://example.com', roomId: 'general' };
function C() {
  useEffect(() => connect(OPTIONS), []);
}
```

### Compute non-reactive values inside the Effect

```ts
// ❌ url is a dep solely because it's declared in component body
const url = `wss://example.com/${roomId}`;
useEffect(() => connect(url), [url]);

// ✅ compute inside — only the primitive roomId is a dep
useEffect(() => {
  const url = `wss://example.com/${roomId}`;
  connect(url);
}, [roomId]);
```

### Use functional updaters to remove state deps

```ts
// ❌ messages must be listed as a dep
useEffect(() => {
  socket.on('msg', msg => setMessages([...messages, msg]));
}, [messages]);

// ✅ updater reads previous state — messages is no longer a dep
useEffect(() => {
  socket.on('msg', msg => setMessages(prev => [...prev, msg]));
}, []);
```

### Use `useEffectEvent` for non-reactive reads

When a value must always be current inside an Effect but must not cause re-synchronization, wrap it in `useEffectEvent` (see `separating.md`).

```ts
// ❌ theme in deps causes reconnect on every theme change
useEffect(() => {
  const conn = connect(roomId);
  conn.on('connected', () => showNotification('Connected!', theme));
  return () => conn.disconnect();
}, [roomId, theme]);

// ✅ theme read non-reactively via Effect Event
const onConnected = useEffectEvent(() => showNotification('Connected!', theme));
useEffect(() => {
  const conn = connect(roomId);
  conn.on('connected', onConnected);
  return () => conn.disconnect();
}, [roomId]);
```

## Object & Function Dep Instability

New reference on every render → Effect re-runs on every render.

| Scenario | Solution |
|---|---|
| Object/function only used inside Effect | Define it inside the Effect |
| Object has extractable primitive fields | Destructure; list primitives as deps |
| Truly static (never changes) | Hoist outside the component |
| Must read latest value without re-triggering | `useEffectEvent` |

## Long Dep Array = Design Smell

A sprawling dep array means the Effect handles multiple unrelated concerns. Split into separate Effects with tight, cohesive dep sets.

```ts
// ❌
useEffect(() => {
  logVisit(roomId);
  const conn = connect(serverUrl, roomId);
  return () => conn.disconnect();
}, [roomId, serverUrl, logConfig, theme, userId]);

// ✅
useEffect(() => { logVisit(roomId, logConfig, userId); }, [roomId, logConfig, userId]);
useEffect(() => {
  const conn = connect(serverUrl, roomId);
  return () => conn.disconnect();
}, [serverUrl, roomId]);
```

## Never

```ts
// eslint-disable-next-line react-hooks/exhaustive-deps  ← always wrong
```
