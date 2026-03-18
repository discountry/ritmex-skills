# When You Don't Need an Effect

## Derived State

```ts
// ❌
const [fullName, setFullName] = useState('');
useEffect(() => setFullName(first + ' ' + last), [first, last]);

// ✅
const fullName = first + ' ' + last;

// ✅ expensive → useMemo, not useEffect + useState
const visibleTodos = useMemo(() => getFiltered(todos, filter), [todos, filter]);
```

## State Reset on Identity Change

```ts
// ❌
useEffect(() => setComment(''), [userId]);

// ✅
<Profile key={userId} userId={userId} />
```

## Partial State Adjustment on Prop Change

```ts
// ❌
useEffect(() => setSelection(null), [items]);

// ✅ store ID; derive object during render
const [selectedId, setSelectedId] = useState<string | null>(null);
const selection = items.find(i => i.id === selectedId) ?? null;
```

## Shared Event Logic

```ts
// ❌
useEffect(() => {
  if (product.isInCart) showNotification(`Added ${product.name}!`);
}, [product]);

// ✅
function handleBuyClick() { addToCart(product); showNotification(`Added ${product.name}!`); }
function handleCheckoutClick() { handleBuyClick(); navigateTo('/checkout'); }
```

## User-Initiated POST Requests

```ts
// ❌
const [payload, setPayload] = useState(null);
useEffect(() => { if (payload) post('/api/register', payload); }, [payload]);

// ✅
function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  post('/api/register', { firstName, lastName });
}
```

## Effect Chains

```ts
// ❌
useEffect(() => { if (card?.gold) setGoldCount(c => c + 1); }, [card]);
useEffect(() => { if (goldCount > 3) setRound(r => r + 1); }, [goldCount]);

// ✅ compute all next state in one event handler
function handlePlaceCard(next: Card) {
  setCard(next);
  if (next.gold) {
    const nextCount = goldCount < 3 ? goldCount + 1 : 0;
    const nextRound = goldCount >= 3 ? round + 1 : round;
    setGoldCount(nextCount);
    setRound(nextRound);
    if (nextRound > 5) alert('Good game!');
  }
}
```

## One-Time App Initialization

```ts
// ❌ runs twice in Strict Mode
useEffect(() => { loadDataFromLocalStorage(); checkAuthToken(); }, []);

// ✅
if (typeof window !== 'undefined') {
  checkAuthToken();
  loadDataFromLocalStorage();
}
```

## Parent Notification / Two-State Synchronization

```ts
// ❌
useEffect(() => { onChange(isOn); }, [isOn, onChange]);

// ✅ update both in the same handler
function updateToggle(next: boolean) { setIsOn(next); onChange(next); }

// ✅ or make fully controlled — remove local state entirely
function Toggle({ isOn, onChange }: Props) { ... }
```

## Passing Data to Parent

```ts
// ❌ child fetches, pushes up via Effect
function Child({ onFetched }) {
  const data = useSomeAPI();
  useEffect(() => { if (data) onFetched(data); }, [data, onFetched]);
}

// ✅ parent fetches; passes data down as prop
function Parent() {
  const data = useSomeAPI();
  return <Child data={data} />;
}
```

## External Store Subscription

```ts
// ❌ manual Effect + useState
useEffect(() => {
  const update = () => setIsOnline(navigator.onLine);
  window.addEventListener('online', update);
  window.addEventListener('offline', update);
  return () => { window.removeEventListener('online', update); window.removeEventListener('offline', update); };
}, []);

// ✅
function useOnlineStatus() {
  return useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
}
```

## Data Fetching — Always Implement Cleanup

```ts
// ❌ race condition — stale responses can overwrite fresh ones
useEffect(() => {
  fetchResults(query, page).then(json => setResults(json));
}, [query, page]);

// ✅
useEffect(() => {
  let ignore = false;
  fetchResults(query, page).then(json => { if (!ignore) setResults(json); });
  return () => { ignore = true; };
}, [query, page]);
```

Prefer framework-level data fetching (React Query, SWR, Next.js, Remix) over raw Effects.