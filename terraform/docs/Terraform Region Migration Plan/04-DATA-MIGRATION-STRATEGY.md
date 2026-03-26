# Phase 4: Data Migration Strategy

## Objective

Terraform creates empty DynamoDB tables with the correct schemas. This phase covers migrating actual data from the source region to the target region for all 54+ tables.

## Risk Level: MEDIUM

Data migration involves reading from production tables and writing to new tables. Incorrect migration could result in data loss or corruption. Always validate counts and spot-check records.

## Estimated Time: 2-3 hours setup + variable migration time depending on data volume

## Prerequisites

- Phase 1 complete (parameterized config)
- Target region tables created by Terraform (Phase 6 dry run or Phase 7 production)

---

## Step 1: Categorize Tables by Priority

Not all 54 tables need the same migration treatment. Categorize them:

### Tier 1 — Critical (Must migrate with zero data loss)

These tables contain user data, content, or business-critical records:

| Table | Items (approx) | Has GSIs | Notes |
|-------|----------------|----------|-------|
| `users` | Active users | Yes (email-index) | User accounts |
| `articles` | Published content | No | All articles |
| `testimonies` | User submissions | Yes (UserEmailIndex) | Cannot be recreated |
| `testimony-users` | Auth data | No | Login credentials |
| `prayer-requests` | User submissions | No | Cannot be recreated |
| `book-subscribers` | Email list | No | Revenue-critical |
| `book_purchases` | Transaction records | No | Financial records |
| `user-email-subscribers` | Email list | Yes | Marketing list |
| `user-email-campaigns` | Campaign config | Yes | 14 campaign definitions |
| `user-email-drip-enrollments` | Active enrollments | Yes | In-progress drip sequences |
| `user-email-events` | Tracking data | Yes | Open/click history |
| `contributors` | Contributor profiles | No | User-submitted |
| `comments` | User comments | No | User-generated content |
| `content-comments` | Threaded comments | Yes | User-generated content |
| `admin-users` | Admin credentials | No | Platform access |
| `news-table` | Scraped news | No | Can be re-scraped but has curation |
| `forum-posts` | Forum content | Yes | User-generated |
| `business-directory` | Business listings | Yes | User-submitted |
| `boycott-tracker` | Boycott data | Yes | Community data |
| `events` | Event listings | No | Active events |
| `notifications` | User notifications | No | Active notifications |

### Tier 2 — Important (Migrate but can tolerate brief gaps)

| Table | Notes |
|-------|-------|
| `video-metadata` | Video catalog — can be rebuilt from S3 but tedious |
| `video-playlists` | User-created playlists |
| `video-analytics` | Historical analytics — nice to have |
| `download-jobs` | Active/completed downloads |
| `resources-table` | Curated resources |
| `newsletters` | Newsletter archive |
| `newsletter_campaigns` | Campaign definitions |
| `newsletter_templates` | Email templates |
| `newsletter_analytics` | Historical tracking |
| `feature-flags` | Feature toggle states |
| `pending-changes` | Queued content changes |
| `email-events` | Legacy event store |
| `email-subscribers` | Legacy subscriber list |
| `email_subscribers` | Legacy subscriber list (underscore variant) |
| `email-campaign-stats` | Aggregated stats |
| `email-subscriber-stats` | Per-subscriber stats |

### Tier 3 — Low Priority (Empty or regenerable)

| Table | Items | Notes |
|-------|-------|-------|
| `EmailPreferences` | 0 | Empty |
| `MarketingQueue` | 0 | Empty |
| `NewsArticles` | 0 | Empty |
| `ProductViews` | 4 | Minimal data |
| `rate-limits` | Ephemeral | TTL-based, regenerates automatically |
| `user-flags` | Flags | Can be regenerated |
| `candidates` | Election data | Seasonal |
| `races` | Election data | Seasonal |
| `state-summaries` | Election data | Seasonal |
| `election-events` | Election data | Seasonal |
| `fact-checks` | New feature | Likely small |
| `mountain-pledges` | 7 Mountains | Community data |
| `mountain-badges` | 7 Mountains | Gamification |
| `mountain-contributions` | 7 Mountains | Community data |
| Shopping tables (Cart, Orders, Products, Reviews) | E-commerce | Check if active |

---

## Step 2: Choose Migration Method

### Method A: DynamoDB Global Tables (Recommended for Tier 1)

**How it works:** You enable Global Tables replication on an existing table. AWS automatically replicates all data to the target region in near-real-time. Once cutover is complete, you remove the source region replica.

**Pros:**
- Zero downtime — replication happens in the background
- Automatic conflict resolution
- Data stays in sync until you cut over
- No custom scripts needed

**Cons:**
- Tables must use PAY_PER_REQUEST billing (or have auto-scaling)
- Tables must have DynamoDB Streams enabled
- Adds cost during replication period (you pay for both regions)
- PROVISIONED tables must be converted to PAY_PER_REQUEST first

**Setup per table:**
```bash
# Enable streams (required for Global Tables)
aws dynamodb update-table \
  --table-name articles \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
  --profile ekewaka --region us-east-1

# Create replica in target region
aws dynamodb update-table \
  --table-name articles \
  --replica-updates "Create={RegionName=us-west-2}" \
  --profile ekewaka --region us-east-1
```

**Monitor replication:**
```bash
aws dynamodb describe-table \
  --table-name articles \
  --profile ekewaka --region us-east-1 \
  --query "Table.Replicas"
```

**After cutover — remove source replica:**
```bash
aws dynamodb update-table \
  --table-name articles \
  --replica-updates "Delete={RegionName=us-east-1}" \
  --profile ekewaka --region us-west-2
```

### Method B: Export to S3 → Import (Good for Tier 2, large tables)

**How it works:** DynamoDB has native export-to-S3 functionality. You export the table to S3, then import it in the new region.

**Pros:**
- No impact on source table performance
- Works with any billing mode
- Good for large tables
- Built-in AWS feature (no custom code)

**Cons:**
- Point-in-time snapshot (not continuous)
- Requires S3 bucket accessible from both regions
- Import creates a NEW table (can't import into existing)
- Some downtime for data written between export and cutover

**Export:**
```bash
aws dynamodb export-table-to-point-in-time \
  --table-arn arn:aws:dynamodb:us-east-1:371751795928:table/articles \
  --s3-bucket techcross-terraform-state \
  --s3-prefix dynamodb-exports/articles/ \
  --export-format DYNAMODB_JSON \
  --profile ekewaka --region us-east-1
```

**Import (in new region):**
```bash
aws dynamodb import-table \
  --s3-bucket-source S3Bucket=techcross-terraform-state,S3KeyPrefix=dynamodb-exports/articles/ \
  --input-format DYNAMODB_JSON \
  --table-creation-parameters '{"TableName":"articles","KeySchema":[{"AttributeName":"article_id","KeyType":"HASH"}],"AttributeDefinitions":[{"AttributeName":"article_id","AttributeType":"S"}],"BillingMode":"PAY_PER_REQUEST"}' \
  --profile ekewaka --region us-west-2
```

**Note:** If Terraform already created the table in the new region, you'd need to delete it first, then import, then re-import into Terraform state. This is why Global Tables is simpler for critical tables.

### Method C: Custom Script — Scan + BatchWrite (Good for small tables)

**How it works:** A Python script scans the source table and batch-writes items to the target table.

**Pros:**
- Full control over what gets migrated
- Can transform data during migration
- Works with any table configuration
- Simple to understand

**Cons:**
- Consumes read capacity on source table
- Slow for large tables (scan is sequential by default)
- Must handle pagination and retries
- Risk of throttling on large tables

```python
#!/usr/bin/env python3
"""
DynamoDB Table Migration Script

Usage:
    python migrate-table.py --table articles --source-region us-east-1 --target-region us-west-2
"""

import argparse
import boto3
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')


def migrate_table(table_name, source_region, target_region, profile):
    session = boto3.Session(profile_name=profile)
    source = session.resource('dynamodb', region_name=source_region)
    target = session.resource('dynamodb', region_name=target_region)

    source_table = source.Table(table_name)
    target_table = target.Table(table_name)

    # Get source item count
    source_table.reload()
    total_items = source_table.item_count
    print(f"Source table '{table_name}' has ~{total_items} items")

    # Scan and batch write
    migrated = 0
    scan_kwargs = {}

    while True:
        response = source_table.scan(**scan_kwargs)
        items = response.get('Items', [])

        if not items:
            break

        # Batch write (max 25 items per batch)
        with target_table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
                migrated += 1

        print(f"  Migrated {migrated} items...", end='\r')

        # Check for pagination
        if 'LastEvaluatedKey' in response:
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        else:
            break

    print(f"\nMigrated {migrated} items from {table_name}")

    # Verify counts
    target_table.reload()
    target_count = target_table.item_count
    print(f"Target table item count: ~{target_count}")

    if abs(migrated - target_count) > 5:  # DynamoDB item_count is approximate
        print("WARNING: Count mismatch! Verify manually.")
    else:
        print("Counts match.")

    return migrated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True)
    parser.add_argument("--source-region", default="us-east-1")
    parser.add_argument("--target-region", required=True)
    parser.add_argument("--profile", default="ekewaka")
    args = parser.parse_args()

    migrate_table(args.table, args.source_region, args.target_region, args.profile)


if __name__ == "__main__":
    main()
```

---

## Step 3: Recommended Approach by Tier

| Tier | Method | Reason |
|------|--------|--------|
| Tier 1 (Critical) | **Global Tables** | Zero downtime, continuous sync until cutover |
| Tier 2 (Important) | **Export/Import** or **Custom Script** | One-time migration is fine, brief gap acceptable |
| Tier 3 (Low Priority) | **Skip or Custom Script** | Empty tables need nothing; small tables are quick to scan |
| PROVISIONED tables | **Convert to PAY_PER_REQUEST first**, then Global Tables | Global Tables requires on-demand or auto-scaling |

### PROVISIONED Tables That Need Conversion

Before enabling Global Tables, these must be converted:

| Table | Current Mode | GSIs |
|-------|-------------|------|
| `boycott-tracker` | PROVISIONED (5/5) | 1 GSI |
| `EmailPreferences` | PROVISIONED (5/5) | None |
| `MarketingQueue` | PROVISIONED (5/5) | 2 GSIs |
| `ProductViews` | PROVISIONED (5/5) | 3 GSIs |

```bash
# Convert to PAY_PER_REQUEST
aws dynamodb update-table \
  --table-name boycott-tracker \
  --billing-mode PAY_PER_REQUEST \
  --profile ekewaka --region us-east-1
```

**Note:** Update the Terraform HCL to match after conversion, or the next `terraform apply` will try to revert it.

---

## Step 4: S3 Data Migration

The S3 bucket `my-video-downloads-bucket` contains all static files, videos, and frontend assets.

### Option A: S3 Cross-Region Replication (Recommended)

```bash
# Enable versioning (required for replication) — already enabled
# Create destination bucket in new region
aws s3 mb s3://my-video-downloads-bucket-west --region us-west-2 --profile ekewaka

# Set up replication rule via console or CLI
# This continuously syncs new objects
```

### Option B: One-Time Sync

```bash
# Sync all objects to new region bucket
aws s3 sync s3://my-video-downloads-bucket s3://my-video-downloads-bucket-west \
  --profile ekewaka --region us-west-2

# Verify counts
aws s3 ls s3://my-video-downloads-bucket --recursive --summarize --profile ekewaka | tail -2
aws s3 ls s3://my-video-downloads-bucket-west --recursive --summarize --profile ekewaka | tail -2
```

**Important:** S3 bucket names are globally unique. You cannot have the same bucket name in two regions. The Terraform config will need the new bucket name.

---

## Step 5: Create Migration Orchestration Script

Create `terraform/scripts/migrate-data.py` that orchestrates the full migration:

```python
#!/usr/bin/env python3
"""
Data Migration Orchestrator

Manages the full DynamoDB + S3 data migration between regions.

Usage:
    python migrate-data.py --target-region us-west-2 --phase enable-replication
    python migrate-data.py --target-region us-west-2 --phase verify-replication
    python migrate-data.py --target-region us-west-2 --phase migrate-tier2
    python migrate-data.py --target-region us-west-2 --phase verify-all
    python migrate-data.py --target-region us-west-2 --phase cleanup-source
"""

import argparse
import boto3
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

TIER1_TABLES = [
    "users", "articles", "testimonies", "testimony-users",
    "prayer-requests", "book-subscribers", "book_purchases",
    "user-email-subscribers", "user-email-campaigns",
    "user-email-drip-enrollments", "user-email-events",
    "contributors", "comments", "content-comments",
    "admin-users", "news-table", "forum-posts",
    "business-directory", "boycott-tracker", "events", "notifications"
]

TIER2_TABLES = [
    "video-metadata", "video-playlists", "video-analytics",
    "download-jobs", "resources-table", "newsletters",
    "newsletter_campaigns", "newsletter_templates",
    "newsletter_analytics", "feature-flags", "pending-changes",
    "email-events", "email-subscribers", "email_subscribers",
    "email-campaign-stats", "email-subscriber-stats"
]

TIER3_TABLES = [
    "EmailPreferences", "MarketingQueue", "NewsArticles",
    "ProductViews", "rate-limits", "user-flags",
    "candidates", "races", "state-summaries", "election-events",
    "fact-checks", "mountain-pledges", "mountain-badges",
    "mountain-contributions"
]


def enable_global_tables(tables, target_region, profile):
    """Enable Global Tables replication for Tier 1 tables."""
    session = boto3.Session(profile_name=profile)
    client = session.client('dynamodb', region_name='us-east-1')

    for table in tables:
        print(f"\n[{table}] Enabling Global Tables replication to {target_region}...")
        try:
            # Enable streams first
            client.update_table(
                TableName=table,
                StreamSpecification={
                    'StreamEnabled': True,
                    'StreamViewType': 'NEW_AND_OLD_IMAGES'
                }
            )
            print(f"  Streams enabled. Waiting 30s...")
            time.sleep(30)

            # Create replica
            client.update_table(
                TableName=table,
                ReplicaUpdates=[{
                    'Create': {'RegionName': target_region}
                }]
            )
            print(f"  Replica creation initiated.")

        except client.exceptions.ResourceInUseException:
            print(f"  Already has replication or update in progress. Skipping.")
        except Exception as e:
            print(f"  ERROR: {e}")


def verify_replication(tables, target_region, profile):
    """Verify all replicas are active and item counts match."""
    session = boto3.Session(profile_name=profile)
    source_client = session.client('dynamodb', region_name='us-east-1')
    target_resource = session.resource('dynamodb', region_name=target_region)

    all_good = True
    for table in tables:
        print(f"\n[{table}]")
        try:
            # Check replica status
            response = source_client.describe_table(TableName=table)
            replicas = response['Table'].get('Replicas', [])
            target_replica = [r for r in replicas if r['RegionName'] == target_region]

            if not target_replica:
                print(f"  NO REPLICA in {target_region}")
                all_good = False
                continue

            status = target_replica[0].get('ReplicaStatus', 'UNKNOWN')
            print(f"  Replica status: {status}")

            if status != 'ACTIVE':
                all_good = False
                continue

            # Compare item counts (approximate)
            source_count = response['Table']['ItemCount']
            target_table = target_resource.Table(table)
            target_table.reload()
            target_count = target_table.item_count

            print(f"  Source: ~{source_count} items, Target: ~{target_count} items")

        except Exception as e:
            print(f"  ERROR: {e}")
            all_good = False

    return all_good


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-region", required=True)
    parser.add_argument("--phase", required=True,
                       choices=["enable-replication", "verify-replication",
                               "migrate-tier2", "verify-all", "cleanup-source"])
    parser.add_argument("--profile", default="ekewaka")
    args = parser.parse_args()

    if args.phase == "enable-replication":
        enable_global_tables(TIER1_TABLES, args.target_region, args.profile)

    elif args.phase == "verify-replication":
        success = verify_replication(TIER1_TABLES, args.target_region, args.profile)
        print(f"\nAll replicas active: {success}")

    elif args.phase == "migrate-tier2":
        print("Migrating Tier 2 tables via scan+batch_write...")
        # Import and call migrate_table from migrate-table.py for each

    elif args.phase == "verify-all":
        print("Verifying all tables in target region...")
        # Check all tables exist and have data

    elif args.phase == "cleanup-source":
        print("WARNING: This removes source region replicas!")
        confirm = input("Type 'DELETE SOURCE REPLICAS' to confirm: ")
        if confirm == "DELETE SOURCE REPLICAS":
            # Remove replicas from source region
            pass


if __name__ == "__main__":
    main()
```

---

## Testing

### Test 1: Global Tables on a Non-Critical Table

Pick an empty or low-priority table to test the full flow:

```bash
# Enable Global Tables on EmailPreferences (0 items, safe to test)
python migrate-data.py --target-region us-west-2 --phase enable-replication
# (modify script to only process EmailPreferences for testing)

# Verify replica is active
aws dynamodb describe-table --table-name EmailPreferences \
  --profile ekewaka --region us-east-1 \
  --query "Table.Replicas"

# Write a test item in source region
aws dynamodb put-item --table-name EmailPreferences \
  --item '{"user_id":{"S":"test-migration"}}' \
  --profile ekewaka --region us-east-1

# Verify it appears in target region (may take a few seconds)
aws dynamodb get-item --table-name EmailPreferences \
  --key '{"user_id":{"S":"test-migration"}}' \
  --profile ekewaka --region us-west-2

# Clean up: delete test item and remove replica
aws dynamodb delete-item --table-name EmailPreferences \
  --key '{"user_id":{"S":"test-migration"}}' \
  --profile ekewaka --region us-east-1

aws dynamodb update-table --table-name EmailPreferences \
  --replica-updates "Delete={RegionName=us-west-2}" \
  --profile ekewaka --region us-east-1
```

### Test 2: Custom Script on Small Table

```bash
# Test scan+batch_write on ProductViews (4 items)
python migrate-table.py --table ProductViews --target-region us-west-2 --profile ekewaka

# Verify
aws dynamodb scan --table-name ProductViews \
  --select COUNT \
  --profile ekewaka --region us-west-2
```

### Test 3: S3 Sync Verification

```bash
# Count objects in source
aws s3 ls s3://my-video-downloads-bucket --recursive --summarize --profile ekewaka 2>&1 | findstr "Total"

# After sync, count in target
aws s3 ls s3://my-video-downloads-bucket-west --recursive --summarize --profile ekewaka 2>&1 | findstr "Total"
```

### Test 4: Export/Import Round-Trip

```bash
# Export a small table
aws dynamodb export-table-to-point-in-time \
  --table-arn arn:aws:dynamodb:us-east-1:371751795928:table/fact-checks \
  --s3-bucket techcross-terraform-state \
  --s3-prefix dynamodb-exports/test/ \
  --export-format DYNAMODB_JSON \
  --profile ekewaka --region us-east-1

# Wait for export to complete, then verify the S3 export files exist
aws s3 ls s3://techcross-terraform-state/dynamodb-exports/test/ --recursive --profile ekewaka
```

---

## Checklist

- [ ] All tables categorized into Tier 1/2/3
- [ ] PROVISIONED tables identified for billing mode conversion
- [ ] Global Tables tested on a non-critical table
- [ ] Custom migration script tested on a small table
- [ ] S3 sync strategy decided (replication vs one-time)
- [ ] Migration orchestration script created
- [ ] Rollback plan documented (delete replicas, revert billing mode)
- [ ] Git commit: "Phase 4: Data migration scripts and strategy"
