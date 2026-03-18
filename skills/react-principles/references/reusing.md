# Reusing Logic with Custom Hooks

## Extract When

- The same Effect + state pattern recurs across components.
- An Effect is complex enough to obscure the component's intent.
- You need a declarative, domain-specific API that hides Effect internals.
- You need a stable abstraction boundary for future migration (e.g., raw `fetch` → React Query).

Don't extract prematurely. Wait for a clear, recurring pattern.

## Design Rules

- **Name for the domain**: `useOnlineStatus`, `useChatRoom`, `useData` — not `useEffectWithFetch`.
- **Parameters are reactive**: the hook re-executes every render; internal Effects re-synchronize automatically when params change.
- **Minimal surface area**: expose only what callers need; don't leak internal setters or implementation details.
- **Cleanup ownership**: if the hook opens a connection or subscription, it closes it. Callers never manage teardown.
- Each caller gets **independent state** — hooks share logic, not state instances.

## Reactive Parameters

```ts
function useChatRoom({ serverUrl, roomId }: Options) {
  useEffect(() => {
    const conn = createConnection(serverUrl, roomId);
    conn.connect();
    return () => conn.disconnect();
  }, [serverUrl, roomId]);
}
```

## Data Fetching Pattern

```ts
function useData<T>(url: string): T | null {
  const [data, setData] = useState<T | null>(null);
  useEffect(() => {
    let ignore = false;
    fetch(url)
      .then(res => res.json())
      .then((json: T) => { if (!ignore) setData(json); });
    return () => { ignore = true; };
  }, [url]);
  return data;
}
```

## External Store Pattern

```ts
function useOnlineStatus(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine,
    () => true
  );
}
```

## Composing Hooks

Hooks compose naturally — a hook may call other hooks. Each composed hook manages its own lifecycle independently.

```ts
function useAuth() {
  const isOnline = useOnlineStatus();
  const user = useData<User>('/api/me');
  return { user, isOnline };
}
```

## Anti-patterns

- **Hooks that only rename `useEffect`** with one cosmetic option — zero abstraction value.
- **Passing `useEffectEvent` references** out of a hook or into sibling hooks.
- **Hooks as a workaround** for suppressed dep linter violations.
- **Exposing mutable refs** — encapsulate behind stable callback APIs.
- **Shared state via custom hook** — shared state belongs in context or an external store, not a custom hook.