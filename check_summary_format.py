import boto3
import sys

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Get state from command line or prompt
if len(sys.argv) > 1:
    state = sys.argv[1]
else:
    state = input("Enter state name: ").strip()

print(f"Checking summary format for {state}...\n")

try:
    summary = summaries_table.get_item(Key={'state': state})['Item']
    
    content = summary['content']
    
    print(f"Title: {summary['title']}")
    print(f"Content length: {len(content)} characters")
    print(f"\nFirst 100 characters (text only):")
    print("=" * 80)
    # Remove emojis for display
    text_only = ''.join(c for c in content[:200] if ord(c) < 128)
    print(text_only)
    print("=" * 80)
    
    # Check format
    if content.startswith('<'):
        print("\n✓ Format: HTML")
    elif content.startswith('#') or '##' in content[:100]:
        print("\n✓ Format: Markdown")
    else:
        print("\n⚠ Format: Plain text (no markdown detected)")
    
    # Check for markdown indicators
    has_headers = '##' in content or '###' in content
    has_bold = '**' in content
    has_lists = '\n- ' in content or '\n* ' in content
    has_emojis = any(ord(c) > 127 for c in content[:1000])
    
    print(f"\nMarkdown indicators:")
    print(f"  Headers (##): {has_headers}")
    print(f"  Bold (**): {has_bold}")
    print(f"  Lists (- or *): {has_lists}")
    print(f"  Emojis: {has_emojis}")
    
except Exception as e:
    print(f"Error: {e}")
