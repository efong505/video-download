import boto3

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')

# Create feature-flags table
table = dynamodb.create_table(
    TableName='feature-flags',
    KeySchema=[
        {
            'AttributeName': 'feature_id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'feature_id',
            'AttributeType': 'S'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)

print('Creating feature-flags table...')
table.wait_until_exists()
print('[SUCCESS] Table created successfully!')

# Insert default election system flag
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
print('\nFeature Flag Details:')
print('- Feature ID: election_system')
print('- Status: Enabled')
print('- Seasonal: Yes (Jan 2025 - Nov 2026)')
print('- Volunteer Dependent: Yes (min 10 volunteers)')
print('- Admin Access: Always available to admins')
