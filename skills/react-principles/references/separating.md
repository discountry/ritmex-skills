# Separating Events from Effects

## The Distinction

|  | Event Handler | Effect |
|---|---|---|
| Trigger | Specific user interaction | Component displayed / deps changed |
| Reactive | No — runs once per gesture | Yes — re-runs on every dep change |
| Intent | Respond to what the user *did* | Stay synchronized with external system |

## Decision Rule

> **Why does this code run?**
> - User did X → **event handler**
> - Component must stay in sync → **Effect**

If the answer is "because some state changed," trace further: that state change originated from either a user gesture or a render. Route accordingly.

## Antipattern: Event Logic Inside an Effect

```ts
// ❌ fires on page load and every re-render where isInCart is true
useEffect(() => {
  if (product.isInCart) showNotification(`Added ${product.name}!`);
}, [product]);

// ✅ fires only on the user's gesture
function handleBuyClick() {
  addToCart(product);
  showNotification(`Added ${product.name}!`);
}
```

## Antipattern: Shared Logic Routed Through State + Effect

```ts
// ❌ auxiliary state just to share code between handlers
const [payload, setPayload] = useState(null);
useEffect(() => { if (payload) post('/api/register', payload); }, [payload]);

// ✅ extract a function; call it from each handler directly
function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  post('/api/register', { firstName, lastName });
}
```

## `useEffectEvent` — Non-Reactive Reads Inside Effects

Use when a value inside an Effect must always be current but **must not trigger re-synchronization**.

```ts
// ❌ theme in deps causes reconnect on every theme change
useEffect(() => {
  const conn = createConnection(serverUrl, roomId);
  conn.on('connected', () => showNotification('Connected!', theme));
  conn.connect();
  return () => conn.disconnect();
}, [serverUrl, roomId, theme]);

// ✅ theme is read non-reactively; Effect only re-syncs on serverUrl/roomId change
const onConnected = useEffectEvent(() => {
  showNotification('Connected!', theme);
});

useEffect(() => {
  const conn = createConnection(serverUrl, roomId);
  conn.on('connected', onConnected);
  conn.connect();
  return () => conn.disconnect();
}, [serverUrl, roomId]);
```

### Rules for Effect Events

- Only call them from **inside Effects** — never from JSX or other hooks.
- Never pass them as props or arguments to other components/hooks.
- Never list them in dependency arrays.

## Never Suppress

`// eslint-disable-next-line react-hooks/exhaustive-deps` hides stale-closure bugs.
Non-reactive reads → `useEffectEvent`, not suppression.