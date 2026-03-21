import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('feature-flags')

# Scan the table
response = table.scan()
items = response.get('Items', [])

print(f'Found {len(items)} feature flags in the table:')
print()

if len(items) == 0:
    print('Table is empty. Adding default election_system flag...')
    table.put_item(
        Item={
            'feature_id': 'election_system',
            'enabled': True,
            'name': 'Election Tracking System',
            'description': '50-state election coverage with candidates, races, and voter guides. Seasonal feature active during election cycles.',
            'admin_only_access': True,
            'seasonal': True,
            'volunteer_dependent': True,
            'min_volunteers_required': 10,
            'active_volunteers': 0,
            'season_start': '2025-01-01T00:00:00Z',
            'season_end': '2026-11-30T23:59:59Z',
            'disable_reason': '',
            'volunteer_signup_url': '/apply-correspondent.html',
            'created_at': '2025-01-15T00:00:00Z',
            'updated_at': '2025-01-15T00:00:00Z',
            'updated_by': 'system'
        }
    )
    print('[SUCCESS] Default election_system flag created!')
else:
    for item in items:
        print(f"Feature ID: {item.get('feature_id')}")
        print(f"  Name: {item.get('name')}")
        print(f"  Enabled: {item.get('enabled')}")
        print(f"  Seasonal: {item.get('seasonal')}")
        print(f"  Volunteer Dependent: {item.get('volunteer_dependent')}")
        print(f"  Min Volunteers: {item.get('min_volunteers_required')}")
        print()

print('[SUCCESS] Feature flags table is ready!')
