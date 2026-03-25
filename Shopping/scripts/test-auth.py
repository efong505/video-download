import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://ydq9xzya5d.execute-api.us-east-1.amazonaws.com/prod'

def call(method, url, data=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, body, headers, method=method)
    try:
        r = urllib.request.urlopen(req)
        return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

print('=== PUBLIC ENDPOINTS (should return 200) ===')
s, d = call('GET', f'{BASE}/products?action=list&limit=1')
print(f'  Products list: {s}')

s, d = call('GET', f'{BASE}/reviews?action=list&product_id=test')
print(f'  Reviews list: {s}')

s, d = call('GET', f'{BASE}/tracking?action=popular')
print(f'  Popular: {s}')

print()
print('=== PROTECTED ENDPOINTS WITHOUT AUTH (should return 401) ===')
s, d = call('GET', f'{BASE}/orders?action=list')
print(f'  Orders list: {s} - {d.get("error","")}')

s, d = call('POST', f'{BASE}/products?action=create', {'name':'test'})
print(f'  Product create: {s} - {d.get("error","")}')

s, d = call('POST', f'{BASE}/reviews?action=create', {'product_id':'test'})
print(f'  Review create: {s} - {d.get("error","")}')

s, d = call('GET', f'{BASE}/tracking?action=watchlist')
print(f'  Watchlist: {s} - {d.get("error","")}')

s, d = call('GET', f'{BASE}/marketing?action=stats')
print(f'  Marketing stats: {s} - {d.get("error","")}')

print()
print('=== GUEST ORDER (optional auth - should return 200 or 400) ===')
s, d = call('POST', f'{BASE}/orders?action=create', {
    'items': [{'product_id':'does-not-exist','name':'Test','price':1.00,'quantity':1}],
    'subtotal': 1.00, 'tax': 0.08, 'total': 1.08,
    'user_email': 'test@test.com', 'user_name': 'Test'
})
print(f'  Guest order: {s} - {d.get("error", d.get("order_id","ok"))}')

print()
print('=== AUTH TEST (register, login, test protected endpoints) ===')
AUTH_BASE = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth'

s, d = call('POST', f'{AUTH_BASE}?action=register', {'email': 'shoptest99@test.com', 'password': 'Test1234!', 'first_name': 'Shop', 'last_name': 'Tester', 'role': 'user'})
print(f'  Register: {s} - {d.get("message", d.get("error",""))}')

s, d = call('POST', f'{AUTH_BASE}?action=login', {'email': 'shoptest99@test.com', 'password': 'Test1234!'})
if s == 200 and d.get('token'):
    token = d['token']
    role = d.get('user',{}).get('role','')
    print(f'  Login: {s} - role={role}')

    s2, d2 = call('GET', f'{BASE}/orders?action=list', token=token)
    print(f'  Orders list (user auth): {s2} - {d2.get("count", d2.get("error",""))} orders')

    s2, d2 = call('GET', f'{BASE}/marketing?action=preferences-get', token=token)
    print(f'  Preferences (user auth): {s2}')

    s2, d2 = call('GET', f'{BASE}/marketing?action=stats', token=token)
    print(f'  Marketing stats (user, expect 403): {s2} - {d2.get("error","")}')

    s2, d2 = call('POST', f'{BASE}/products?action=create', {'name':'test'}, token=token)
    print(f'  Product create (user, expect 403): {s2} - {d2.get("error","")}')
else:
    print(f'  Login failed: {s} - {d}')

print()
print('Done!')
