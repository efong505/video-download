import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create newsletters table
try:
    newsletters_table = dynamodb.create_table(
        TableName='newsletters',
        KeySchema=[{'AttributeName': 'newsletter_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'newsletter_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print('Creating newsletters table...')
    newsletters_table.wait_until_exists()
    print('✓ newsletters table created')
except Exception as e:
    print(f'newsletters table: {e}')

# Create email_subscribers table
try:
    subscribers_table = dynamodb.create_table(
        TableName='email_subscribers',
        KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print('Creating email_subscribers table...')
    subscribers_table.wait_until_exists()
    print('✓ email_subscribers table created')
except Exception as e:
    print(f'email_subscribers table: {e}')

# Create newsletter_templates table
try:
    templates_table = dynamodb.create_table(
        TableName='newsletter_templates',
        KeySchema=[{'AttributeName': 'template_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'template_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print('Creating newsletter_templates table...')
    templates_table.wait_until_exists()
    print('✓ newsletter_templates table created')
except Exception as e:
    print(f'newsletter_templates table: {e}')

# Create newsletter_analytics table
try:
    analytics_table = dynamodb.create_table(
        TableName='newsletter_analytics',
        KeySchema=[{'AttributeName': 'tracking_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'tracking_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    print('Creating newsletter_analytics table...')
    analytics_table.wait_until_exists()
    print('✓ newsletter_analytics table created')
except Exception as e:
    print(f'newsletter_analytics table: {e}')

print('\nAll newsletter tables created successfully!')
