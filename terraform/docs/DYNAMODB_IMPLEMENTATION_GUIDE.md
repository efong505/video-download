# DynamoDB Tables - Detailed Implementation Guide

## Overview
Step-by-step guide for creating the DynamoDB module and importing 28 existing tables into Terraform.

---

## Step 1: Gather Existing DynamoDB Table Information

### Commands to List All Tables

```bash
# List all DynamoDB tables
aws dynamodb list-tables

# Get table count
aws dynamodb list-tables --query 'length(TableNames)'

# Get detailed info for specific table
aws dynamodb describe-table --table-name articles

# Get table schema (keys and attributes)
aws dynamodb describe-table --table-name articles --query 'Table.[KeySchema,AttributeDefinitions,GlobalSecondaryIndexes]'

# Get billing mode
aws dynamodb describe-table --table-name articles --query 'Table.BillingModeSummary.BillingMode'

# Get TTL configuration
aws dynamodb describe-time-to-live --table-name rate-limits

# Get point-in-time recovery status
aws dynamodb describe-continuous-backups --table-name articles --query 'ContinuousBackupsDescription.PointInTimeRecoveryDescription.PointInTimeRecoveryStatus'
```

### Data Collected

**Total Tables**: 47

**Successfully Imported**: 28 (60%)

**Skipped (Complex Schemas)**: 19 (40%)

---

## Step 2: Analyze Table Schemas

### Simple Table Example: articles

```bash
aws dynamodb describe-table --table-name articles
```

**Output**:
```json
{
    "Table": {
        "TableName": "articles",
        "KeySchema": [
            {
                "AttributeName": "article_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "article_id",
                "AttributeType": "S"
            }
        ],
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        },
        "TableStatus": "ACTIVE"
    }
}
```

**Schema**: Simple hash key only

---

### Table with GSI Example: users

```bash
aws dynamodb describe-table --table-name users
```

**Output**:
```json
{
    "Table": {
        "TableName": "users",
        "KeySchema": [
            {
                "AttributeName": "user_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "email",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "email-index",
                "KeySchema": [
                    {
                        "AttributeName": "email",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            }
        ],
        "BillingModeSummary": {
            "BillingMode": "PAY_PER_REQUEST"
        }
    }
}
```

**Schema**: Hash key + GSI on email

---

### Table with TTL Example: rate-limits

```bash
aws dynamodb describe-time-to-live --table-name rate-limits
```

**Output**:
```json
{
    "TimeToLiveDescription": {
        "TimeToLiveStatus": "ENABLED",
        "AttributeName": "ttl"
    }
}
```

**Schema**: Hash key + TTL enabled

---

### Complex Table Example: video-analytics (Skipped)

```bash
aws dynamodb describe-table --table-name video-analytics
```

**Output**:
```json
{
    "Table": {
        "KeySchema": [
            {
                "AttributeName": "video_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "timestamp",
                "KeyType": "RANGE"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "video_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "timestamp",
                "AttributeType": "N"
            },
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "event_type",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user-index",
                "KeySchema": [
                    {
                        "AttributeName": "user_id",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "timestamp",
                        "KeyType": "RANGE"
                    }
                ]
            },
            {
                "IndexName": "event-index",
                "KeySchema": [
                    {
                        "AttributeName": "event_type",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "timestamp",
                        "KeyType": "RANGE"
                    }
                ]
            }
        ]
    }
}
```

**Schema**: Composite key (hash + range) + 2 GSIs with range keys

**Decision**: Too complex - Terraform would want to recreate. Skipped to protect data.

---

## Step 3: Create DynamoDB Module

### Directory Setup
```bash
mkdir -p terraform/modules/dynamodb
cd terraform/modules/dynamodb
```

### Create main.tf

**File**: `terraform/modules/dynamodb/main.tf`

```hcl
# DynamoDB Table
resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = var.billing_mode
  hash_key     = var.hash_key
  range_key    = var.range_key

  # Attributes (only for keys and GSI keys)
  dynamic "attribute" {
    for_each = var.attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  # Global Secondary Indexes
  dynamic "global_secondary_index" {
    for_each = var.global_secondary_indexes
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.hash_key
      range_key       = lookup(global_secondary_index.value, "range_key", null)
      projection_type = global_secondary_index.value.projection_type
      
      # Only for PROVISIONED billing mode
      read_capacity  = var.billing_mode == "PROVISIONED" ? lookup(global_secondary_index.value, "read_capacity", null) : null
      write_capacity = var.billing_mode == "PROVISIONED" ? lookup(global_secondary_index.value, "write_capacity", null) : null
    }
  }

  # TTL Configuration
  dynamic "ttl" {
    for_each = var.ttl_enabled ? [1] : []
    content {
      enabled        = true
      attribute_name = var.ttl_attribute_name
    }
  }

  # Point-in-time Recovery
  point_in_time_recovery {
    enabled = var.point_in_time_recovery
  }

  tags = var.tags

  lifecycle {
    prevent_destroy = true
  }
}
```

**Data Source**: 
- DynamoDB table schemas from `aws dynamodb describe-table`
- TTL configs from `aws dynamodb describe-time-to-live`
- PITR status from `aws dynamodb describe-continuous-backups`

### Create variables.tf

**File**: `terraform/modules/dynamodb/variables.tf`

```hcl
variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "billing_mode" {
  description = "Billing mode (PROVISIONED or PAY_PER_REQUEST)"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "hash_key" {
  description = "Hash key attribute name"
  type        = string
}

variable "range_key" {
  description = "Range key attribute name (optional)"
  type        = string
  default     = null
}

variable "attributes" {
  description = "List of attribute definitions (only for keys and GSI keys)"
  type = list(object({
    name = string
    type = string
  }))
}

variable "global_secondary_indexes" {
  description = "List of global secondary indexes"
  type = list(object({
    name            = string
    hash_key        = string
    range_key       = optional(string)
    projection_type = string
    read_capacity   = optional(number)
    write_capacity  = optional(number)
  }))
  default = []
}

variable "ttl_enabled" {
  description = "Enable TTL for the table"
  type        = bool
  default     = false
}

variable "ttl_attribute_name" {
  description = "Attribute name for TTL"
  type        = string
  default     = "ttl"
}

variable "point_in_time_recovery" {
  description = "Enable point-in-time recovery"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to the table"
  type        = map(string)
  default     = {}
}
```

### Create outputs.tf

**File**: `terraform/modules/dynamodb/outputs.tf`

```hcl
output "table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.this.name
}

output "table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.this.arn
}

output "table_id" {
  description = "ID of the DynamoDB table"
  value       = aws_dynamodb_table.this.id
}
```

---

## Step 4: Use Module in Production Environment

### Simple Table: articles

**File**: `terraform/environments/prod/main.tf`

```hcl
module "dynamodb_articles" {
  source = "../../modules/dynamodb"

  table_name   = "articles"
  hash_key     = "article_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "article_id", type = "S" }
  ]

  point_in_time_recovery = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

### Table with GSI: users

```hcl
module "dynamodb_users" {
  source = "../../modules/dynamodb"

  table_name   = "users"
  hash_key     = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "email", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "email-index"
      hash_key        = "email"
      projection_type = "ALL"
    }
  ]

  point_in_time_recovery = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

### Table with TTL: rate-limits

```hcl
module "dynamodb_rate_limits" {
  source = "../../modules/dynamodb"

  table_name   = "rate-limits"
  hash_key     = "rate_key"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "rate_key", type = "S" }
  ]

  ttl_enabled        = true
  ttl_attribute_name = "ttl"

  point_in_time_recovery = true

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

**Data Source**: Values from Step 2 AWS CLI output

---

## Step 5: Import Existing Tables

### Initialize Terraform
```bash
cd terraform/environments/prod
terraform init
```

### Import Simple Table
```bash
terraform import module.dynamodb_articles.aws_dynamodb_table.this articles
```

**Output**:
```
module.dynamodb_articles.aws_dynamodb_table.this: Importing from ID "articles"...
module.dynamodb_articles.aws_dynamodb_table.this: Import complete!
```

### Import Table with GSI
```bash
terraform import module.dynamodb_users.aws_dynamodb_table.this users
```

### Import All 28 Tables

```bash
# Script to import all successfully configured tables
TABLES=(
  "articles"
  "users"
  "news-table"
  "comments"
  "video-metadata"
  "resources-table"
  "contributors"
  "rate-limits"
  "download-jobs"
  "video-playlists"
  "book-subscribers"
  "book_purchases"
  "notifications"
  "events"
  "prayer-requests"
  "testimonies"
  "testimony-users"
  "candidates"
  "races"
  "state-summaries"
  "election-events"
  "email-subscribers"
  "email-events"
  "newsletters"
  "newsletter_campaigns"
  "newsletter_templates"
  "newsletter_analytics"
  "user-email-subscribers"
)

for table in "${TABLES[@]}"; do
  # Convert table name to module name (replace hyphens with underscores)
  module_name=$(echo "$table" | tr '-' '_')
  echo "Importing $table as module.dynamodb_${module_name}..."
  terraform import "module.dynamodb_${module_name}.aws_dynamodb_table.this" "$table"
done
```

---

## Step 6: Handle Complex Tables

### Attempt to Import Complex Table

```bash
# Try to import video-analytics
terraform import module.dynamodb_video_analytics.aws_dynamodb_table.this video-analytics
```

### Run Terraform Plan
```bash
terraform plan
```

**Output**:
```
Terraform will perform the following actions:

  # module.dynamodb_video_analytics.aws_dynamodb_table.this must be replaced
-/+ resource "aws_dynamodb_table" "this" {
      ~ global_secondary_index {
          # Configuration doesn't match AWS exactly
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.
```

**Problem**: Terraform wants to RECREATE the table (destroy + create)

### Prevent Destroy Blocks Recreation

```
Error: Instance cannot be destroyed

  on ../../modules/dynamodb/main.tf line 50:
  50:   lifecycle {
  51:     prevent_destroy = true
  52:   }

Resource has lifecycle.prevent_destroy set, but the plan calls for this
resource to be destroyed.
```

**Result**: `prevent_destroy` protects data by blocking the recreation

### Decision: Skip Complex Tables

**Tables Skipped** (19 total):
- Tables with composite keys (hash + range)
- Tables with multiple GSIs
- Tables with GSIs that have range keys
- Tables with complex attribute definitions

**Reason**: Risk of data loss outweighs benefit of Terraform management

---

## Step 7: Verify Import

### Run Terraform Plan
```bash
terraform plan
```

**Expected Output**:
```
No changes. Your infrastructure matches the configuration.
```

**If there are changes**, common issues:

### Issue 1: Attribute Mismatch
```
# Plan shows:
~ attribute {
    + name = "extra_attribute"
    + type = "S"
  }

# Problem: Only define attributes used in keys or GSIs
# Solution: Remove extra attributes from Terraform config
```

### Issue 2: GSI Projection Type
```
# Plan shows:
~ global_secondary_index {
    ~ projection_type = "KEYS_ONLY" -> "ALL"
  }

# Solution: Update projection_type in main.tf
projection_type = "KEYS_ONLY"
```

### Issue 3: TTL Status
```
# Plan shows:
~ ttl {
    ~ enabled = false -> true
  }

# Solution: Check actual TTL status
aws dynamodb describe-time-to-live --table-name rate-limits

# Update Terraform config to match
ttl_enabled = true  # or false
```

---

## Step 8: Test Terraform Control

### Make a Small Change
```hcl
# Enable PITR for articles table
point_in_time_recovery = true  # Changed from false
```

### Apply Change
```bash
terraform apply
```

**Output**:
```
Terraform will perform the following actions:

  # module.dynamodb_articles.aws_dynamodb_table.this will be updated in-place
  ~ resource "aws_dynamodb_table" "this" {
      ~ point_in_time_recovery {
          ~ enabled = false -> true
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

### Verify in AWS
```bash
aws dynamodb describe-continuous-backups --table-name articles --query 'ContinuousBackupsDescription.PointInTimeRecoveryDescription.PointInTimeRecoveryStatus'
```

**Output**: `"ENABLED"`

---

## Step 9: Verify Data Protection

### Attempt to Destroy Table
```bash
terraform destroy -target=module.dynamodb_articles.aws_dynamodb_table.this
```

**Output**:
```
Error: Instance cannot be destroyed

Resource module.dynamodb_articles.aws_dynamodb_table.this has
lifecycle.prevent_destroy set, but the plan calls for this resource to be
destroyed.
```

**Result**: `prevent_destroy` successfully protects data

---

## Key Learnings

### DynamoDB Attributes
- **Only define attributes used in keys or GSIs**
- DynamoDB is schemaless - other attributes don't need to be defined
- Common mistake: Defining all attributes (causes Terraform drift)

### Global Secondary Indexes
- **Must define all GSI key attributes** in `attributes` block
- **Projection type**: ALL, KEYS_ONLY, or INCLUDE
- **Billing mode**: PAY_PER_REQUEST doesn't need capacity settings

### TTL Configuration
- **Separate resource** in Terraform (not part of table definition)
- **Attribute name** must match DynamoDB configuration
- **Can be enabled/disabled** without recreating table

### Point-in-Time Recovery
- **Recommended for production** tables
- **Enables restore** to any point in last 35 days
- **No performance impact**

### Prevent Destroy
- **Critical for data protection**
- **Blocks accidental deletion** via Terraform
- **Must be removed** before intentional deletion

---

## Common Pitfalls

**Pitfall 1: Defining non-key attributes**
- **Problem**: Terraform shows constant drift
- **Solution**: Only define attributes used in keys or GSIs

**Pitfall 2: GSI capacity for PAY_PER_REQUEST**
- **Problem**: Terraform error about capacity settings
- **Solution**: Don't set read_capacity/write_capacity for PAY_PER_REQUEST

**Pitfall 3: Complex table import**
- **Problem**: Terraform wants to recreate table
- **Solution**: Skip complex tables or carefully match exact AWS configuration

**Pitfall 4: Forgetting prevent_destroy**
- **Problem**: Risk of accidental data loss
- **Solution**: Always add `prevent_destroy = true` lifecycle rule

---

## Terraform State

After import, state contains:

```json
{
  "resources": [
    {
      "module": "module.dynamodb_articles",
      "type": "aws_dynamodb_table",
      "name": "this",
      "instances": [
        {
          "attributes": {
            "name": "articles",
            "hash_key": "article_id",
            "billing_mode": "PAY_PER_REQUEST",
            "attribute": [
              {
                "name": "article_id",
                "type": "S"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Note**: State stores schema, not actual table data

---

## Troubleshooting

### Issue: Plan shows attribute changes
**Solution**: Only define attributes used in keys or GSIs, remove others

### Issue: GSI configuration mismatch
**Solution**: Get exact GSI config from AWS and match in Terraform

### Issue: TTL shows as changed
**Solution**: Check actual TTL status with `describe-time-to-live` and update config

### Issue: Table recreation required
**Solution**: Skip table or carefully match exact AWS configuration

### Issue: Can't delete table
**Solution**: Remove `prevent_destroy` lifecycle rule first (intentional protection)

---

## Tables Successfully Imported (28)

| Table Name | Schema Type | Special Features |
|-----------|-------------|------------------|
| articles | Simple hash | PITR |
| users | Hash + GSI | Email index |
| news-table | Simple hash | PITR |
| comments | Simple hash | PITR |
| video-metadata | Simple hash | PITR |
| resources-table | Simple hash | PITR |
| contributors | Simple hash | PITR |
| rate-limits | Simple hash | TTL enabled |
| download-jobs | Simple hash | PITR |
| video-playlists | Simple hash | PITR |
| book-subscribers | Simple hash | PITR |
| book_purchases | Simple hash | PITR |
| notifications | Simple hash | PITR |
| events | Simple hash | PITR |
| prayer-requests | Simple hash | PITR |
| testimonies | Hash + GSI | User index |
| testimony-users | Simple hash | PITR |
| candidates | Simple hash | PITR |
| races | Simple hash | PITR |
| state-summaries | Simple hash | PITR |
| election-events | Simple hash | PITR |
| email-subscribers | Simple hash | PITR |
| email-events | Simple hash | PITR |
| newsletters | Simple hash | PITR |
| newsletter_campaigns | Simple hash | PITR |
| newsletter_templates | Simple hash | PITR |
| newsletter_analytics | Simple hash | PITR |
| user-email-subscribers | Simple hash | PITR |

---

## Related Files
- [DynamoDB Module](../../modules/dynamodb/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
