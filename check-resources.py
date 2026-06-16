import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

RESOURCES_API = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

res = requests.get(f'{RESOURCES_API}?action=list')
all_resources = res.json()

print("\n=== MUSIC RESOURCES ===")
music = [r for r in all_resources if any('music' in str(c).lower() for c in (r.get('category', []) if isinstance(r.get('category'), list) else [r.get('category', '')]))]
for m in music:
    print(f"Name: {m.get('name')}")
    print(f"  Category: {m.get('category')}")
    print(f"  Subcategory: {m.get('subcategory', 'MISSING')}")
    print()

print("\n=== LITERATURE RESOURCES ===")
lit = [r for r in all_resources if any('literature' in str(c).lower() or 'book' in str(c).lower() for c in (r.get('category', []) if isinstance(r.get('category'), list) else [r.get('category', '')]))]
for l in lit:
    print(f"Name: {l.get('name')}")
    print(f"  Category: {l.get('category')}")
    print(f"  Subcategory: {l.get('subcategory', 'MISSING')}")
    print()

print("\n=== VISUAL ARTS RESOURCES ===")
arts = [r for r in all_resources if any('visual' in str(c).lower() or 'art' in str(c).lower() for c in (r.get('category', []) if isinstance(r.get('category'), list) else [r.get('category', '')]))]
for a in arts:
    print(f"Name: {a.get('name')}")
    print(f"  Category: {a.get('category')}")
    print(f"  Subcategory: {a.get('subcategory', 'MISSING')}")
    print()
