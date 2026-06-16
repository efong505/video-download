import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Use default account (wrong account)
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam', region_name='us-east-1')

functions = [
    'media-bias-api',
    'fake-news-api',
    'corporate-wokeness-api',
    'political-corruption-api'
]

print("Deleting Lambda functions from wrong account (372110294325)...\n")

for func_name in functions:
    try:
        lambda_client.delete_function(FunctionName=func_name)
        print(f"✓ Deleted Lambda function: {func_name}")
    except lambda_client.exceptions.ResourceNotFoundException:
        print(f"⚠ Function {func_name} not found")
    except Exception as e:
        print(f"✗ Error deleting {func_name}: {e}")

# Delete IAM role
role_name = 'tracker-lambda-role'
print(f"\nDeleting IAM role: {role_name}...")

try:
    # Detach policies first
    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
    for policy in attached_policies['AttachedPolicies']:
        iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        print(f"  ✓ Detached policy: {policy['PolicyName']}")
    
    # Delete role
    iam_client.delete_role(RoleName=role_name)
    print(f"✓ Deleted IAM role: {role_name}")
except iam_client.exceptions.NoSuchEntityException:
    print(f"⚠ Role {role_name} not found")
except Exception as e:
    print(f"✗ Error deleting role: {e}")

print("\n✅ Cleanup complete")
