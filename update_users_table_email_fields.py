import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')

TIER_LIMITS = {
    'free': {
        'email_subscriber_limit': 0,
        'email_monthly_limit': 0
    },
    'premium': {
        'email_subscriber_limit': 500,
        'email_monthly_limit': 1000
    },
    'pro': {
        'email_subscriber_limit': 5000,
        'email_monthly_limit': 10000
    },
    'enterprise': {
        'email_subscriber_limit': 999999,
        'email_monthly_limit': 50000
    }
}

print("Scanning users table...")
response = users_table.scan()
users = response['Items']

print(f"Found {len(users)} users")

for user in users:
    user_id = user['user_id']
    tier = user.get('subscription_tier', 'free')
    limits = TIER_LIMITS.get(tier, TIER_LIMITS['free'])
    
    print(f"Updating {user.get('email', user_id)} ({tier})...")
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email_subscriber_limit = :sub_limit, email_monthly_limit = :send_limit, email_subscribers_count = :zero, email_sent_this_month = :zero',
        ExpressionAttributeValues={
            ':sub_limit': limits['email_subscriber_limit'],
            ':send_limit': limits['email_monthly_limit'],
            ':zero': 0
        }
    )

print("\n✅ All users updated with email quota fields!")
