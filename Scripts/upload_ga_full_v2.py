import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
summaries_table = dynamodb.Table("state-summaries")

ga_summary = """PASTE_GA_SUMMARY_HERE"""

summaries_table.put_item(Item={"state": "Georgia", "title": "Georgia 2026 Voter Guide", "content": ga_summary, "updated_at": "2025-01-22"})
print(f"GA: {len(ga_summary)} chars uploaded")