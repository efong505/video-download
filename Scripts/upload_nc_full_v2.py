import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
summaries_table = dynamodb.Table("state-summaries")

nc_summary = """PASTE_NC_SUMMARY_HERE"""

summaries_table.put_item(Item={"state": "North Carolina", "title": "North Carolina 2026 Voter Guide", "content": nc_summary, "updated_at": "2025-01-22"})
print(f"NC: {len(nc_summary)} chars uploaded")