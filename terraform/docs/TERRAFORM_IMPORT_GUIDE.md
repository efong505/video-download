# Terraform Import Guide — Bringing AWS Resources Under Management

> **Profile:** Always use `--profile ekewaka` (account 371751795928)
> **Working Directory:** `cd c:\Users\Ed\Documents\Programming\AWS\Downloader\terraform\environments\prod`
> **Terraform Version:** 1.14.6

---

## Table of Contents

1. [Migrate State Locking from DynamoDB to S3-Native](#1-migrate-state-locking)
2. [General Workflow for Importing Resources](#2-general-workflow)
3. [DynamoDB Tables](#3-dynamodb-tables)
4. [Lambda Functions](#4-lambda-functions)
5. [SQS Queues](#5-sqs-queues)
6. [SNS Topics](#6-sns-topics)
7. [API Gateway Endpoints](#7-api-gateway-endpoints)
8. [Cleanup — Deciding What NOT to Manage](#8-cleanup)
9. [Live vs State Audit — How to Find What's Missing](#9-live-vs-state-audit)
10. [Priority Import Plan](#10-priority-import-plan)
11. [Case Study — comments-api vs comments-handler](#11-case-study-comments)

---

## 1. Migrate State Locking from DynamoDB to S3-Native {#1-migrate-state-locking}

### Background

Your current backend uses a DynamoDB table (`terraform-state-lock`) for state locking. Since Terraform 1.10+, S3 supports native locking via `use_lockfile = true`, eliminating the need for DynamoDB.

Your version (1.14.6) fully supports this.

### ⚠️ CRITICAL: This Lock Table Is Shared by 4 Projects

The `terraform-state-lock` DynamoDB table is used by **4 separate Terraform projects**. You MUST migrate ALL of them before deleting the table, or the un-migrated projects will break.

| # | S3 Bucket | State Key | Local Project Path | Status |
|---|-----------|-----------|-------------------|--------|
| 1 | `techcross-terraform-state` | `prod/terraform.tfstate` | `c:\Users\Ed\Documents\Programming\AWS\Downloader\terraform\environments\prod\` | Active (490KB state, many resources) |
| 2 | `techcross-terraform-state` | `ministry-platform/terraform.tfstate` | Not found locally — abandoned project | Empty (0 resources, 181 bytes) |
| 3 | `ed-terraform-remote-backend` | `terraform/tfstate.tfstate` | `c:\Users\Ed\Documents\Post Graduation\Projects\Terraform\backend\` | Active |
| 4 | `terraform-state-mumbai-practice` | `practice-mumbai/terraform.tfstate` | `c:\Users\Ed\Documents\Programming\AWS\Multi-Region-Practice\terraform\environments\practice-mumbai\` | Active |

### How I Found These Projects

You can discover which projects share the lock table by scanning it:

```cmd
aws dynamodb scan --table-name terraform-state-lock --profile ekewaka --region us-east-1 --output json
```

Each item's `LockID` contains the S3 bucket + state key path. The `-md5` suffix entries are digest records (not active locks).

To find the local project files, search for `.tf` files referencing the table:

```cmd
powershell -Command "Get-ChildItem -Path 'c:\Users\Ed\Documents' -Recurse -Filter '*.tf' -ErrorAction SilentlyContinue | ForEach-Object { $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue; if ($content -match 'terraform-state-lock') { $_.FullName } }"
```

### Step 1: Back Up ALL State Files

Before touching anything, download local copies of every state file that uses this lock table:

```cmd
mkdir state-backups

aws s3 cp s3://techcross-terraform-state/prod/terraform.tfstate ./state-backups/prod.tfstate.backup --profile ekewaka

aws s3 cp s3://techcross-terraform-state/ministry-platform/terraform.tfstate ./state-backups/ministry-platform.tfstate.backup --profile ekewaka

aws s3 cp s3://ed-terraform-remote-backend/terraform/tfstate.tfstate ./state-backups/ed-backend.tfstate.backup --profile ekewaka

aws s3 cp s3://terraform-state-mumbai-practice/practice-mumbai/terraform.tfstate ./state-backups/mumbai-practice.tfstate.backup --profile ekewaka
```

Verify all 4 backups exist:

```cmd
dir state-backups
```

Keep these safe. If anything goes wrong, restore with:

```cmd
aws s3 cp ./state-backups/prod.tfstate.backup s3://techcross-terraform-state/prod/terraform.tfstate --profile ekewaka
```

(Same pattern for the other 3.)

### Step 2: Verify No Active Locks

```cmd
aws dynamodb scan --table-name terraform-state-lock --profile ekewaka --region us-east-1 --output json
```

You should only see items with `-md5` suffix in the `LockID`. Those are digest records, NOT active locks. An active lock would have a `LockID` without `-md5` and an `Info` field with a timestamp.

If there IS an active lock and you're sure no one else is running:

```cmd
terraform force-unlock <LOCK_ID>
```

### Step 3: Migrate Project 1 — Prod (Main Platform)

```cmd
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\terraform\environments\prod
```

Edit `main.tf`, change the backend from:

```hcl
backend "s3" {
  bucket         = "techcross-terraform-state"
  key            = "prod/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

To:

```hcl
backend "s3" {
  bucket       = "techcross-terraform-state"
  key          = "prod/terraform.tfstate"
  region       = "us-east-1"
  encrypt      = true
  use_lockfile = true
}
```

Then re-initialize:

```cmd
terraform init -migrate-state
```

Terraform will ask: `Do you want to migrate all workspaces to "s3"?` — type `yes`.

Verify:

```cmd
terraform plan
```

If the plan runs without errors, Project 1 is migrated. ✅

### Step 4: Migrate Project 2 — Ministry Platform (Abandoned)

This state file has 0 resources — it's an empty/abandoned project. The `.tf` files aren't on your machine anymore. You have two options:

**Option A: Just delete the state file (recommended since it's empty):**

```cmd
aws s3 rm s3://techcross-terraform-state/ministry-platform/terraform.tfstate --profile ekewaka
```

**Option B: If you want to keep it, create a temporary directory and migrate:**

```cmd
mkdir c:\temp\ministry-platform-migrate
cd c:\temp\ministry-platform-migrate
```

Create a minimal `main.tf`:

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket       = "techcross-terraform-state"
    key          = "ministry-platform/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "ekewaka"
}
```

Then:

```cmd
terraform init -migrate-state
```

Type `yes` when prompted. Then clean up the temp directory.

Project 2 done. ✅

### Step 5: Migrate Project 3 — Post Graduation Terraform Backend

```cmd
cd "c:\Users\Ed\Documents\Post Graduation\Projects\Terraform\backend"
```

Edit `backend.tf`, change from:

```hcl
backend "s3" {
  bucket         = "ed-terraform-remote-backend"
  key            = "terraform/tfstate.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

To:

```hcl
backend "s3" {
  bucket       = "ed-terraform-remote-backend"
  key          = "terraform/tfstate.tfstate"
  region       = "us-east-1"
  encrypt      = true
  use_lockfile = true
}
```

Then:

```cmd
terraform init -migrate-state
terraform plan
```

Project 3 done. ✅

### Step 6: Migrate Project 4 — Mumbai Practice

```cmd
cd c:\Users\Ed\Documents\Programming\AWS\Multi-Region-Practice\terraform\environments\practice-mumbai
```

Edit `main.tf`, change the backend from:

```hcl
backend "s3" {
  bucket         = "terraform-state-mumbai-practice"
  key            = "practice-mumbai/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

To:

```hcl
backend "s3" {
  bucket       = "terraform-state-mumbai-practice"
  key          = "practice-mumbai/terraform.tfstate"
  region       = "us-east-1"
  encrypt      = true
  use_lockfile = true
}
```

Then:

```cmd
terraform init -migrate-state
terraform plan
```

Project 4 done. ✅

### Step 7: Delete the DynamoDB Lock Table

Only do this AFTER all 4 projects are migrated and verified:

```cmd
aws dynamodb delete-table --table-name terraform-state-lock --profile ekewaka --region us-east-1
```

Verify it's gone:

```cmd
aws dynamodb describe-table --table-name terraform-state-lock --profile ekewaka --region us-east-1 2>&1
```

You should see a `ResourceNotFoundException`. The table is gone and you're fully on S3-native locking. 🎉

### Rollback Plan

If something goes wrong at any point:

1. Restore the backend block in the affected project to use `dynamodb_table = "terraform-state-lock"`
2. If the DynamoDB table was already deleted, recreate it:
   ```cmd
   aws dynamodb create-table --table-name terraform-state-lock --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --profile ekewaka --region us-east-1
   ```
3. Run `terraform init -migrate-state` again in the affected project
4. If a state file got corrupted, restore from backup:
   ```cmd
   aws s3 cp ./state-backups/prod.tfstate.backup s3://techcross-terraform-state/prod/terraform.tfstate --profile ekewaka
   ```

---

## 2. General Workflow for Importing Resources {#2-general-workflow}

For every resource you want to bring under Terraform management:

1. **Discover** — Use AWS CLI to list what exists
2. **Describe** — Get the exact configuration of the resource
3. **Write HCL** — Add the module/resource block to `main.tf`
4. **Import** — Tell Terraform "this HCL block maps to this existing AWS resource"
5. **Plan** — Verify Terraform sees no changes (meaning your HCL matches reality)
6. **Fix drift** — If the plan shows changes, update your HCL to match what's in AWS

### Key Commands

```cmd
# Import a resource into state
terraform import <TERRAFORM_ADDRESS> <AWS_RESOURCE_ID>

# Plan only a specific module (limits blast radius)
terraform plan -target=module.<MODULE_NAME>

# Full plan after all imports
terraform plan
```

### Tips

- Always use `-target` when importing to avoid accidentally touching other resources
- If `terraform plan` shows "will be updated in-place", your HCL doesn't match AWS — fix the HCL
- If it shows "will be created", you forgot to import
- If it shows "will be destroyed", something is in state that shouldn't be — use `terraform state rm` to remove it



---

## 3. DynamoDB Tables {#3-dynamodb-tables}

### How to Discover Missing Tables

```cmd
aws dynamodb list-tables --profile ekewaka --region us-east-1 --output text
```

### How to Describe Any Table

```cmd
aws dynamodb describe-table --table-name TABLE_NAME --profile ekewaka --region us-east-1 --query "Table.{Name:TableName,KeySchema:KeySchema,BillingMode:BillingModeSummary.BillingMode,Attributes:AttributeDefinitions,GSIs:GlobalSecondaryIndexes}" --output json
```

### Missing Tables — Platform Related

These are production tables that should be in Terraform. Add each block to `main.tf`, then import.

#### 3.1 mountain-pledges

```hcl
module "dynamodb_mountain_pledges" {
  source = "../../modules/dynamodb"

  table_name   = "mountain-pledges"
  hash_key     = "user_id"
  range_key    = "mountain"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_mountain_pledges.aws_dynamodb_table.this mountain-pledges
terraform plan -target=module.dynamodb_mountain_pledges
```

#### 3.2 mountain-badges

```hcl
module "dynamodb_mountain_badges" {
  source = "../../modules/dynamodb"

  table_name   = "mountain-badges"
  hash_key     = "badge_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "badge_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "user-index"
      hash_key        = "user_id"
      range_key       = "mountain"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_mountain_badges.aws_dynamodb_table.this mountain-badges
terraform plan -target=module.dynamodb_mountain_badges
```

#### 3.3 mountain-contributions

```hcl
module "dynamodb_mountain_contributions" {
  source = "../../modules/dynamodb"

  table_name   = "mountain-contributions"
  hash_key     = "contribution_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "contribution_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "mountain", type = "S" },
    { name = "contribution_date", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "user-index"
      hash_key        = "user_id"
      range_key       = "contribution_date"
      projection_type = "ALL"
    },
    {
      name            = "mountain-index"
      hash_key        = "mountain"
      range_key       = "contribution_date"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_mountain_contributions.aws_dynamodb_table.this mountain-contributions
terraform plan -target=module.dynamodb_mountain_contributions
```

#### 3.4 admin-users

```hcl
module "dynamodb_admin_users" {
  source = "../../modules/dynamodb"

  table_name   = "admin-users"
  hash_key     = "username"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "username", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_admin_users.aws_dynamodb_table.this admin-users
terraform plan -target=module.dynamodb_admin_users
```

#### 3.5 content-comments

```hcl
module "dynamodb_content_comments" {
  source = "../../modules/dynamodb"

  table_name   = "content-comments"
  hash_key     = "content_id"
  range_key    = "comment_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "content_id", type = "S" },
    { name = "comment_id", type = "S" },
    { name = "created_at", type = "N" }
  ]

  global_secondary_indexes = [
    {
      name            = "CreatedAtIndex"
      hash_key        = "content_id"
      range_key       = "created_at"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_content_comments.aws_dynamodb_table.this content-comments
terraform plan -target=module.dynamodb_content_comments
```

#### 3.6 feature-flags

```hcl
module "dynamodb_feature_flags" {
  source = "../../modules/dynamodb"

  table_name   = "feature-flags"
  hash_key     = "feature_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "feature_id", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_feature_flags.aws_dynamodb_table.this feature-flags
terraform plan -target=module.dynamodb_feature_flags
```

#### 3.7 pending-changes

```hcl
module "dynamodb_pending_changes" {
  source = "../../modules/dynamodb"

  table_name   = "pending-changes"
  hash_key     = "change_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "change_id", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_pending_changes.aws_dynamodb_table.this pending-changes
terraform plan -target=module.dynamodb_pending_changes
```

#### 3.8 user-flags

```hcl
module "dynamodb_user_flags" {
  source = "../../modules/dynamodb"

  table_name   = "user-flags"
  hash_key     = "flagId"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "flagId", type = "S" },
    { name = "userEmail", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "UserEmailIndex"
      hash_key        = "userEmail"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_user_flags.aws_dynamodb_table.this user-flags
terraform plan -target=module.dynamodb_user_flags
```

#### 3.9 email-campaign-stats

```hcl
module "dynamodb_email_campaign_stats" {
  source = "../../modules/dynamodb"

  table_name   = "email-campaign-stats"
  hash_key     = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "campaign_id", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_email_campaign_stats.aws_dynamodb_table.this email-campaign-stats
terraform plan -target=module.dynamodb_email_campaign_stats
```

#### 3.10 email-subscriber-stats

```hcl
module "dynamodb_email_subscriber_stats" {
  source = "../../modules/dynamodb"

  table_name   = "email-subscriber-stats"
  hash_key     = "subscriber_email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "subscriber_email", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_email_subscriber_stats.aws_dynamodb_table.this email-subscriber-stats
terraform plan -target=module.dynamodb_email_subscriber_stats
```

#### 3.11 email_subscribers (underscore variant)

```hcl
module "dynamodb_email_subscribers_v2" {
  source = "../../modules/dynamodb"

  table_name   = "email_subscribers"
  hash_key     = "email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "email", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_email_subscribers_v2.aws_dynamodb_table.this email_subscribers
terraform plan -target=module.dynamodb_email_subscribers_v2
```

#### 3.12 newsletter_analytics

```hcl
module "dynamodb_newsletter_analytics" {
  source = "../../modules/dynamodb"

  table_name   = "newsletter_analytics"
  hash_key     = "tracking_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "tracking_id", type = "S" }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_newsletter_analytics.aws_dynamodb_table.this newsletter_analytics
terraform plan -target=module.dynamodb_newsletter_analytics
```

#### 3.13 user-email-campaigns

```hcl
module "dynamodb_user_email_campaigns" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-campaigns"
  hash_key     = "user_id"
  range_key    = "campaign_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "campaign_id", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_user_email_campaigns.aws_dynamodb_table.this user-email-campaigns
terraform plan -target=module.dynamodb_user_email_campaigns
```

#### 3.14 user-email-drip-enrollments

```hcl
module "dynamodb_user_email_drip_enrollments" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-drip-enrollments"
  hash_key     = "user_id"
  range_key    = "enrollment_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "enrollment_id", type = "S" },
    { name = "status", type = "S" },
    { name = "subscriber_email", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    },
    {
      name            = "email-index"
      hash_key        = "user_id"
      range_key       = "subscriber_email"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_user_email_drip_enrollments.aws_dynamodb_table.this user-email-drip-enrollments
terraform plan -target=module.dynamodb_user_email_drip_enrollments
```

#### 3.15 user-email-events

```hcl
module "dynamodb_user_email_events" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-events"
  hash_key     = "user_id"
  range_key    = "event_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "event_id", type = "S" },
    { name = "campaign_id", type = "S" },
    { name = "subscriber_email", type = "S" },
    { name = "timestamp", type = "N" }
  ]

  global_secondary_indexes = [
    {
      name            = "campaign-index"
      hash_key        = "campaign_id"
      range_key       = "timestamp"
      projection_type = "ALL"
    },
    {
      name            = "email-index"
      hash_key        = "subscriber_email"
      range_key       = "timestamp"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_user_email_events.aws_dynamodb_table.this user-email-events
terraform plan -target=module.dynamodb_user_email_events
```

#### 3.16 forum-posts

```hcl
module "dynamodb_forum_posts" {
  source = "../../modules/dynamodb"

  table_name   = "forum-posts"
  hash_key     = "post_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "post_id", type = "S" },
    { name = "mountain", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "mountain-index"
      hash_key        = "mountain"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_forum_posts.aws_dynamodb_table.this forum-posts
terraform plan -target=module.dynamodb_forum_posts
```

#### 3.17 business-directory

```hcl
module "dynamodb_business_directory" {
  source = "../../modules/dynamodb"

  table_name   = "business-directory"
  hash_key     = "business_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "business_id", type = "S" },
    { name = "category", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "category-index"
      hash_key        = "category"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_business_directory.aws_dynamodb_table.this business-directory
terraform plan -target=module.dynamodb_business_directory
```

#### 3.19 boycott-tracker

> **Note:** This table uses PROVISIONED billing (5 RCU / 5 WCU), not PAY_PER_REQUEST. The DynamoDB module now supports `read_capacity` and `write_capacity` variables for this.

```hcl
module "dynamodb_boycott_tracker" {
  source = "../../modules/dynamodb"

  table_name     = "boycott-tracker"
  hash_key       = "boycott_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attributes = [
    { name = "boycott_id", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "status"
      range_key       = null
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_boycott_tracker.aws_dynamodb_table.this boycott-tracker
terraform plan -target=module.dynamodb_boycott_tracker
```

> **Tip:** If you'd rather switch this to PAY_PER_REQUEST (the table has 0 items), just use `billing_mode = "PAY_PER_REQUEST"` and omit the capacity settings. Terraform will update it in-place.

#### 3.20 user-email-subscribers

```hcl
module "dynamodb_user_email_subscribers" {
  source = "../../modules/dynamodb"

  table_name   = "user-email-subscribers"
  hash_key     = "user_id"
  range_key    = "subscriber_email"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "user_id", type = "S" },
    { name = "subscriber_email", type = "S" },
    { name = "status", type = "S" }
  ]

  global_secondary_indexes = [
    {
      name            = "status-index"
      hash_key        = "user_id"
      range_key       = "status"
      projection_type = "ALL"
    }
  ]
}
```

Import:
```cmd
terraform import module.dynamodb_user_email_subscribers.aws_dynamodb_table.this user-email-subscribers
terraform plan -target=module.dynamodb_user_email_subscribers
```

### Tables to Skip (Demo/Learning — Not Platform)

These exist in AWS but are likely demo/practice tables. Don't add them to Terraform unless you want to manage them:

- `Cards`, `Cart`, `DemoTable`, `FindingEtsyDoc`, `NewsArticles`, `Orders`, `Products`, `Reviews`
- `StorageFiles`, `StorageUsers`, `Templates`, `Users` (capital U), `WebsiteConfigs`
- `saas-tf-lock-table` (separate project)



---

## 4. Lambda Functions {#4-lambda-functions}

### How to Discover Missing Functions

```cmd
aws lambda list-functions --profile ekewaka --region us-east-1 --query "Functions[].FunctionName" --output table
```

### How to Describe Any Function

```cmd
aws lambda get-function-configuration --function-name FUNCTION_NAME --profile ekewaka --region us-east-1 --query "{Runtime:Runtime,Handler:Handler,MemorySize:MemorySize,Timeout:Timeout,Layers:Layers[].Arn}" --output json
```

### Import Pattern for Lambda

Each Lambda module creates a function + optionally an alias. You need to import both:

```cmd
terraform import module.MODULE_NAME.aws_lambda_function.this FUNCTION_NAME
terraform import "module.MODULE_NAME.aws_lambda_alias.this[0]" FUNCTION_NAME:live
terraform plan -target=module.MODULE_NAME
```

> **Note:** The alias import uses quotes because of the `[0]` index. If the function doesn't have a `live` alias in AWS, set `create_alias = false` and skip the alias import.

### How to Check If a Function Has a "live" Alias

```cmd
aws lambda get-alias --function-name FUNCTION_NAME --name live --profile ekewaka --region us-east-1 2>&1
```

If it returns an error like "Function not found", the alias doesn't exist — use `create_alias = false`.

### Missing Lambda Functions — Platform Related

#### 4.1 mountains-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_mountains_api" {
  source = "../../modules/lambda"

  function_name = "mountains-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

#### 4.2 newsletter_api

```hcl
module "lambda_newsletter_api" {
  source = "../../modules/lambda"

  function_name = "newsletter_api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.3 digest_generator

```hcl
module "lambda_digest_generator" {
  source = "../../modules/lambda"

  function_name = "digest_generator"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.4 scheduled-publisher

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_scheduled_publisher" {
  source = "../../modules/lambda"

  function_name = "scheduled-publisher"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

#### 4.5 feature-flags-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_feature_flags_api" {
  source = "../../modules/lambda"

  function_name = "feature-flags-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

#### 4.6 auto-cache-monitor

```hcl
module "lambda_auto_cache_monitor" {
  source = "../../modules/lambda"

  function_name = "auto-cache-monitor"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.7 playlists-api

```hcl
module "lambda_playlists_api" {
  source = "../../modules/lambda"

  function_name = "playlists-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.8 comments-handler

```hcl
module "lambda_comments_handler" {
  source = "../../modules/lambda"

  function_name = "comments-handler"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.9 contact-form-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_contact_form_api" {
  source = "../../modules/lambda"

  function_name = "contact-form-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

#### 4.10 email-subscription-handler

```hcl
module "lambda_email_subscription_handler" {
  source = "../../modules/lambda"

  function_name = "email-subscription-handler"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.11 email-drip-processor

```hcl
module "lambda_email_drip_processor" {
  source = "../../modules/lambda"

  function_name = "email-drip-processor"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.12 manual-email-sender

```hcl
module "lambda_manual_email_sender" {
  source = "../../modules/lambda"

  function_name = "manual-email-sender"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.13 ses-event-processor

```hcl
module "lambda_ses_event_processor" {
  source = "../../modules/lambda"

  function_name = "ses-event-processor"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 256
  timeout       = 60
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.14 article-meta-tags-edge (Lambda@Edge)

```hcl
module "lambda_article_meta_tags_edge" {
  source = "../../modules/lambda"

  function_name = "article-meta-tags-edge"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 5
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

#### 4.15 user-email-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_user_email_api" {
  source = "../../modules/lambda"

  function_name = "user-email-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

#### 4.16 forum-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_forum_api" {
  source = "../../modules/lambda"

  function_name = "forum-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_forum_api.aws_lambda_function.this forum-api
terraform plan -target=module.lambda_forum_api
```

#### 4.17 business-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_business_api" {
  source = "../../modules/lambda"

  function_name = "business-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_business_api.aws_lambda_function.this business-api
terraform plan -target=module.lambda_business_api
```

#### 4.18 book-delivery-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_book_delivery_api" {
  source = "../../modules/lambda"

  function_name = "book-delivery-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_book_delivery_api.aws_lambda_function.this book-delivery-api
terraform plan -target=module.lambda_book_delivery_api
```

#### 4.19 boycott-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_boycott_api" {
  source = "../../modules/lambda"

  function_name = "boycott-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_boycott_api.aws_lambda_function.this boycott-api
terraform plan -target=module.lambda_boycott_api
```

#### 4.20 tracking-api

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_tracking_api" {
  source = "../../modules/lambda"

  function_name = "tracking-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 15
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_tracking_api.aws_lambda_function.this tracking-api
terraform plan -target=module.lambda_tracking_api
```

#### 4.21 email-sender

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_email_sender" {
  source = "../../modules/lambda"

  function_name = "email-sender"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_email_sender.aws_lambda_function.this email-sender
terraform plan -target=module.lambda_email_sender
```

#### 4.22 NewsScraperLambda

> **No live alias** — use `create_alias = false`

```hcl
module "lambda_news_scraper" {
  source = "../../modules/lambda"

  function_name = "NewsScraperLambda"
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 512
  timeout       = 300
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = false

  environment_variables = {}
}
```

Import:
```cmd
terraform import module.lambda_news_scraper.aws_lambda_function.this NewsScraperLambda
terraform plan -target=module.lambda_news_scraper
```

#### 4.23–4.27 Testimony Functions (Node.js)

> **Note:** Your Lambda module currently works with Python (placeholder.zip). These Node.js functions use different handlers. The module should still work since it ignores `filename` changes via lifecycle rules, but verify after import.

```hcl
module "lambda_testimony_auth" {
  source = "../../modules/lambda"

  function_name = "testimony-auth"
  runtime       = "nodejs22.x"
  handler       = "auth.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_testimony_crud" {
  source = "../../modules/lambda"

  function_name = "testimony-crud"
  runtime       = "nodejs22.x"
  handler       = "testimony.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_testimony_admin" {
  source = "../../modules/lambda"

  function_name = "testimony-admin"
  runtime       = "nodejs22.x"
  handler       = "admin.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_testimony_email_sharing" {
  source = "../../modules/lambda"

  function_name = "testimony-email-sharing"
  runtime       = "nodejs22.x"
  handler       = "email-sharing.handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

module "lambda_testimony_email_ses" {
  source = "../../modules/lambda"

  function_name = "testimony-email-ses"
  runtime       = "nodejs22.x"
  handler       = "email-ses.handler"
  memory_size   = 128
  timeout       = 3
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}
```

Import all testimony functions:
```cmd
terraform import module.lambda_testimony_auth.aws_lambda_function.this testimony-auth
terraform import module.lambda_testimony_crud.aws_lambda_function.this testimony-crud
terraform import module.lambda_testimony_admin.aws_lambda_function.this testimony-admin
terraform import module.lambda_testimony_email_sharing.aws_lambda_function.this testimony-email-sharing
terraform import module.lambda_testimony_email_ses.aws_lambda_function.this testimony-email-ses
```

### Lambda Functions to Skip (Demo/Learning)

- `ffmpegLambda`, `musicFunction`, `pollyFunctionTest`, `TrackPollyUsage`, `blue-green-demo`
- `createTempate`, `bible-lesson-to-audio`
- `recipe-scrapter`, `recipe-scraper`, `recipe-scraper-lambda`
- `video-url-generator`
- `products-api`, `orders-api`, `reviews-api`, `storage_api`, `subscription_api` (e-commerce demo)



---

## 5. SQS Queues {#5-sqs-queues}

### How to Discover Queues

```cmd
aws sqs list-queues --profile ekewaka --region us-east-1 --output text
```

### How to Describe Any Queue

```cmd
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/QUEUE_NAME --attribute-names All --profile ekewaka --region us-east-1 --query "Attributes.{VisibilityTimeout:VisibilityTimeout,MessageRetention:MessageRetentionPeriod,MaxMessageSize:MaximumMessageSize,RedrivePolicy:RedrivePolicy}" --output json
```

### Import Pattern for SQS (using your sqs-queue-with-dlq module)

Your module creates BOTH a main queue and a DLQ automatically. The DLQ is named `{queue_name}-dlq`. You need to import both:

```cmd
terraform import module.MODULE_NAME.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/QUEUE_NAME
terraform import module.MODULE_NAME.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/QUEUE_NAME-dlq
terraform plan -target=module.MODULE_NAME
```

### Module Variables Reference

Your `sqs-queue-with-dlq` module accepts:
- `queue_name` (required) — name of the main queue
- `visibility_timeout` (default: 30) — seconds
- `message_retention` (default: 345600 = 4 days) — seconds, applies to BOTH main and DLQ
- `max_receive_count` (default: 3) — failures before sending to DLQ

### Missing SQS Queues — Platform Related

#### 5.1 video-processing-queue

```hcl
module "sqs_video_processing" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "video-processing-queue"
  visibility_timeout = 900
  message_retention  = 345600
  max_receive_count  = 3
}
```

Import:
```cmd
terraform import module.sqs_video_processing.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-queue
terraform import module.sqs_video_processing.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-dlq
terraform plan -target=module.sqs_video_processing
```

#### 5.2 thumbnail-generation-queue

```hcl
module "sqs_thumbnail_generation" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "thumbnail-generation-queue"
  visibility_timeout = 300
  message_retention  = 86400
  max_receive_count  = 3
}
```

Import:
```cmd
terraform import module.sqs_thumbnail_generation.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/thumbnail-generation-queue
terraform import module.sqs_thumbnail_generation.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/thumbnail-generation-dlq
terraform plan -target=module.sqs_thumbnail_generation
```

> **Note:** The DLQ in AWS has `message_retention = 1209600` (14 days) but your module sets the DLQ retention to the same value as the main queue. After import, `terraform plan` will likely show drift on the DLQ retention. You have two options:
> 1. Accept the drift and let Terraform update the DLQ retention to match the main queue
> 2. Update the module to support separate DLQ retention (better long-term)

#### 5.3 email-queue

```hcl
module "sqs_email" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "email-queue"
  visibility_timeout = 60
  message_retention  = 172800
  max_receive_count  = 5
}
```

Import:
```cmd
terraform import module.sqs_email.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/email-queue
terraform import module.sqs_email.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/email-dlq
terraform plan -target=module.sqs_email
```

#### 5.4 email-notification-queue

```hcl
module "sqs_email_notification" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "email-notification-queue"
  visibility_timeout = 60
  message_retention  = 345600
  max_receive_count  = 3
}
```

Import:
```cmd
terraform import module.sqs_email_notification.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/email-notification-queue
terraform import module.sqs_email_notification.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/email-notification-queue-dlq
terraform plan -target=module.sqs_email_notification
```

#### 5.5 analytics-queue

```hcl
module "sqs_analytics" {
  source = "../../modules/sqs-queue-with-dlq"

  queue_name         = "analytics-queue"
  visibility_timeout = 30
  message_retention  = 86400
  max_receive_count  = 2
}
```

Import:
```cmd
terraform import module.sqs_analytics.aws_sqs_queue.main https://sqs.us-east-1.amazonaws.com/371751795928/analytics-queue
terraform import module.sqs_analytics.aws_sqs_queue.dlq https://sqs.us-east-1.amazonaws.com/371751795928/analytics-dlq
terraform plan -target=module.sqs_analytics
```

### Standalone Queues (No DLQ Pairing in Module)

These queues exist without a matching `-dlq` suffix, or their DLQ name doesn't match the module's convention. You may need raw `aws_sqs_queue` resources instead of the module:

- `email-sending-queue` — standalone, no DLQ
- `NewsScraperQueue` / `NewsScraperDLQ` — DLQ name doesn't match `{name}-dlq` convention

### SQS Queues to Skip (Demo/Learning)

- `DemoQue`, `DemoQueue.fifo`, `TestQue.fifo`
- `order-processing-queue` + DLQ, `payment-processing-queue` + DLQ, `inventory-update-queue` + DLQ (e-commerce demo)
- `my-textract-completion-queue`

---

## 6. SNS Topics {#6-sns-topics}

### How to Discover Topics

```cmd
aws sns list-topics --profile ekewaka --region us-east-1 --query "Topics[].TopicArn" --output table
```

### How to See Subscriptions

```cmd
aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:371751795928:TOPIC_NAME --profile ekewaka --region us-east-1 --output json
```

### Import Pattern for SNS

```cmd
terraform import module.MODULE_NAME.aws_sns_topic.this arn:aws:sns:us-east-1:371751795928:TOPIC_NAME
terraform plan -target=module.MODULE_NAME
```

> **Important:** Your SNS module only supports `email` subscriptions. The `ses-email-events` topic has a `lambda` subscription — you'll need a raw `aws_sns_topic_subscription` resource for that one.

### Missing SNS Topics — Platform Related

#### 6.1 platform-critical-alerts

Subscriptions: email to `<email>`, SMS to `<phone>`

```hcl
module "sns_platform_critical_alerts" {
  source = "../../modules/sns-topic"

  topic_name      = "platform-critical-alerts"
  email_addresses = ["<email>"]

  tags = {
    Environment = "production"
    Purpose     = "Critical platform alerts"
  }
}
```

> **Note:** The SMS subscription can't be managed by your current module (it only supports email). You'd need to add a raw resource or extend the module.

Import:
```cmd
terraform import module.sns_platform_critical_alerts.aws_sns_topic.this arn:aws:sns:us-east-1:371751795928:platform-critical-alerts
terraform plan -target=module.sns_platform_critical_alerts
```

#### 6.2 video-download-notifications

```hcl
module "sns_video_download_notifications" {
  source = "../../modules/sns-topic"

  topic_name      = "video-download-notifications"
  email_addresses = ["<email>"]

  tags = {
    Environment = "production"
    Purpose     = "Video download completion alerts"
  }
}
```

Import:
```cmd
terraform import module.sns_video_download_notifications.aws_sns_topic.this arn:aws:sns:us-east-1:371751795928:video-download-notifications
terraform plan -target=module.sns_video_download_notifications
```

#### 6.3 ses-bounces

```hcl
module "sns_ses_bounces" {
  source = "../../modules/sns-topic"

  topic_name      = "ses-bounces"
  email_addresses = ["<email>"]

  tags = {
    Environment = "production"
    Purpose     = "SES bounce notifications"
  }
}
```

Import:
```cmd
terraform import module.sns_ses_bounces.aws_sns_topic.this arn:aws:sns:us-east-1:371751795928:ses-bounces
terraform plan -target=module.sns_ses_bounces
```

#### 6.4 ses-email-events

This topic has a Lambda subscription (not email), so use a raw resource:

```hcl
resource "aws_sns_topic" "ses_email_events" {
  name = "ses-email-events"

  tags = {
    Environment = "production"
    Purpose     = "SES event processing"
  }
}

resource "aws_sns_topic_subscription" "ses_email_events_lambda" {
  topic_arn = aws_sns_topic.ses_email_events.arn
  protocol  = "lambda"
  endpoint  = module.lambda_ses_event_processor.function_arn
}
```

Import:
```cmd
terraform import aws_sns_topic.ses_email_events arn:aws:sns:us-east-1:371751795928:ses-email-events
terraform plan -target=aws_sns_topic.ses_email_events
```

#### 6.5 surveillance-alerts

```hcl
module "sns_surveillance_alerts" {
  source = "../../modules/sns-topic"

  topic_name      = "surveillance-alerts"
  email_addresses = ["<email>"]

  tags = {
    Environment = "production"
    Purpose     = "Security surveillance alerts"
  }
}
```

Import:
```cmd
terraform import module.sns_surveillance_alerts.aws_sns_topic.this arn:aws:sns:us-east-1:371751795928:surveillance-alerts
terraform plan -target=module.sns_surveillance_alerts
```

### SNS Topics to Skip (Demo/Learning)

- `DemoTopic`, `MyFirstTopic`
- `PollyUsageAlerts`, `PollyUsageAlertsv2`
- `my-textract-completion-topic`

---

## 7. API Gateway Endpoints {#7-api-gateway-endpoints}

### Missing Endpoint on Unified API

The `events_api` Lambda is defined but has no API Gateway integration. Add:

```hcl
module "api_events" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "events"
  http_method          = "ANY"
  lambda_function_name = module.lambda_events_api.function_name
  lambda_function_arn  = module.lambda_events_api.function_arn
  enable_cors          = true
}
```

> **Note:** If this endpoint already exists in AWS on the unified API, you'll need to import the API Gateway resource and method. If it doesn't exist yet, just `terraform apply -target=module.api_events` to create it.

### Standalone API Gateways (Not on Unified API)

These are separate REST APIs that exist independently. Bringing them under Terraform would require separate `api-gateway` module blocks for each. Consider whether you want to consolidate them into the unified API or manage them separately:

| API Name | API ID | Decision Needed |
|----------|--------|-----------------|
| mountains-api | lcmogvl3v2 | Consolidate into unified API? |
| prayer-api | cayl9dmtaf | Already has `/prayer` on unified API — may be duplicate |
| contributors-api | hzursivfuk | Already has `/contributors` on unified API — may be duplicate |
| video-downloader-api | j3w8kgqlvi | Already has `/download` on unified API — may be duplicate |
| user-email-api | olmcyxwc1a | Add to unified API as `/user-email`? |
| Book Delivery API | k2zbtkeh67 | Keep separate or consolidate? |
| MyTestimony API | wm234jgiv3 | Keep separate (different project)? |
| NewsScraperAPI | xi6azy9cp9 | Keep separate? |
| shopping-api | ydq9xzya5d | Demo — skip? |
| MyMusicAPI | sljzs4mmue | Demo — skip? |
| video-api | wfeds5lejb | Legacy — may be replaced by unified API |
| recipe-scraper-api | 1lgppg87fe | Demo — skip? |

---

## 8. Cleanup — Deciding What NOT to Manage {#8-cleanup}

Not everything in your AWS account needs to be in Terraform. Here's a decision framework:

### Manage in Terraform (Production)
- All Lambda functions that serve the platform (APIs, processors, handlers)
- All DynamoDB tables used by the platform
- SQS queues used in production workflows
- SNS topics for alerts and event processing
- The unified API Gateway and its integrations
- S3 buckets used by the platform (`my-video-downloads-bucket`, `lambda-code-ekewaka`)
- CloudFront, ACM, Route53 (already managed)

### Don't Manage (Demo/Learning)
- Demo DynamoDB tables: `Cards`, `Cart`, `DemoTable`, `Products`, `Orders`, etc.
- Demo Lambda functions: `musicFunction`, `pollyFunctionTest`, `blue-green-demo`, etc.
- Demo SQS queues: `DemoQue`, `TestQue.fifo`, e-commerce queues
- Demo SNS topics: `DemoTopic`, `MyFirstTopic`, Polly topics
- Demo API Gateways: `MyMusicAPI`, `shopping-api`, `recipe-scraper-api`
- Infrastructure tables: `saas-tf-lock-table` (separate project)

### Recommended Order of Operations

1. **State locking migration** (Section 1) — do this first, it's independent
2. **DynamoDB tables** (Section 3) — safest to start with, no side effects
3. **Lambda functions** (Section 4) — import one at a time, verify with plan
4. **SQS queues** (Section 5) — watch for DLQ retention drift
5. **SNS topics** (Section 6) — watch for subscription types your module doesn't support
6. **API Gateway** (Section 7) — most complex, do last
7. **Full plan** — after all imports, run `terraform plan` with no target to see the full picture

### After Each Import Session

Always run a full plan to check for unexpected changes:

```cmd
terraform plan
```

And commit your `main.tf` changes to git:

```cmd
git add terraform/environments/prod/main.tf
git commit -m "terraform: import [RESOURCE_TYPE] into state"
```


---

## 9. Live vs State Audit — How to Find What's Missing {#9-live-vs-state-audit}

Before importing resources, you need to know what's in AWS but NOT in Terraform state. This section teaches you the methodology.

### The Core Concept

Terraform only knows about resources in its state file. When you run `terraform plan`, it compares your HCL against the state file (after refreshing state from AWS). Resources that exist in AWS but aren't in state are **invisible** to Terraform — it will try to create duplicates if you add HCL without importing first.

### Step 1: List What Terraform Knows

```cmd
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\terraform\environments\prod
terraform state list
```

This outputs every resource address Terraform is tracking. Filter by type:

```cmd
terraform state list | findstr "dynamodb"
terraform state list | findstr "lambda"
terraform state list | findstr "sqs"
terraform state list | findstr "sns"
```

### Step 2: List What AWS Has

For each resource type, use AWS CLI:

```cmd
REM DynamoDB
aws dynamodb list-tables --profile ekewaka --region us-east-1 --output text

REM Lambda
aws lambda list-functions --profile ekewaka --region us-east-1 --query "Functions[].FunctionName" --output text

REM SQS
aws sqs list-queues --profile ekewaka --region us-east-1 --output text

REM SNS
aws sns list-topics --profile ekewaka --region us-east-1 --query "Topics[].TopicArn" --output text

REM API Gateway
aws apigateway get-rest-apis --profile ekewaka --region us-east-1 --query "items[].{id:id,name:name}" --output table

REM S3
aws s3 ls --profile ekewaka
```

### Step 3: Compare the Two Lists

Manually compare the outputs. Anything in AWS but NOT in `terraform state list` is unmanaged. For a quick count:

```cmd
REM Count DynamoDB tables in state (use PowerShell — cmd find is unreliable with pipes)
powershell -Command "(terraform state list | Select-String 'dynamodb').Count"

REM Count DynamoDB tables in AWS
aws dynamodb list-tables --profile ekewaka --region us-east-1 --query "TableNames | length(@)"
```

### Audit Results (as of latest session)

| Resource Type | Live in AWS | In Terraform State | Gap |
|---------------|-------------|-------------------|-----|
| Lambda Functions | 62 | 22 | ~40 unmanaged |
| DynamoDB Tables | 63 | 31 | ~32 unmanaged |
| API Gateways | 13 | 2 | 11 unmanaged |
| SQS Queues | 23 | 8 | 15 unmanaged |
| SNS Topics | 10 | 1 | 9 unmanaged |
| S3 Buckets | 31 | 1 | 30 unmanaged |

> **Note:** Not all gaps need to be closed. Many are demo/learning resources (see Section 8). The Priority Import Plan (Section 10) tells you which ones matter.

### Step 4: Describe Each Missing Resource

Once you identify a missing resource, get its exact config before writing HCL:

```cmd
REM DynamoDB — get schema, GSIs, billing mode
aws dynamodb describe-table --table-name TABLE_NAME --profile ekewaka --region us-east-1 --query "Table.{Name:TableName,KeySchema:KeySchema,BillingMode:BillingModeSummary.BillingMode,Attributes:AttributeDefinitions,GSIs:GlobalSecondaryIndexes}" --output json

REM Lambda — get runtime, handler, memory, timeout, layers
aws lambda get-function-configuration --function-name FUNCTION_NAME --profile ekewaka --region us-east-1 --query "{Runtime:Runtime,Handler:Handler,MemorySize:MemorySize,Timeout:Timeout,Layers:Layers[].Arn}" --output json

REM Lambda — check if it has a "live" alias (determines create_alias setting)
aws lambda get-alias --function-name FUNCTION_NAME --name live --profile ekewaka --region us-east-1 2>&1

REM SQS — get all attributes
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/371751795928/QUEUE_NAME --attribute-names All --profile ekewaka --region us-east-1 --output json

REM SNS — get subscriptions
aws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:us-east-1:371751795928:TOPIC_NAME --profile ekewaka --region us-east-1 --output json
```

### Batch Alias Check for Lambda

To check ALL Lambda functions for a `live` alias at once (useful when importing many):

```cmd
for %f in (forum-api business-api scheduled-publisher book-delivery-api mountains-api contact-form-api feature-flags-api user-email-api) do @aws lambda get-alias --function-name %f --name live --profile ekewaka --region us-east-1 2>&1 | findstr /c:"FunctionName" /c:"ResourceNotFoundException"
```

If you see `ResourceNotFoundException`, that function has no alias — use `create_alias = false` in the HCL block.

---

## 10. Priority Import Plan {#10-priority-import-plan}

Based on the audit, here's what to import and in what order. Priority is based on: is it actively used by the platform? Does the frontend call it? Would losing it break something?

### Priority 1 — CRITICAL (Active Platform Features)

These are called by the live frontend or support core platform functionality.

| Resource | Type | Why Critical | Section |
|----------|------|-------------|---------|
| `mountains-api` | Lambda | Powers all 7 mountain hub pages (API ID `lcmogvl3v2`) | 4.1 |
| `forum-api` | Lambda | Powers forum.html discussions | 4.16 |
| `business-api` | Lambda | Powers business directory | 4.17 |
| `scheduled-publisher` | Lambda | Auto-publishes scheduled articles | 4.4 |
| `book-delivery-api` | Lambda | Book delivery feature (API ID `k2zbtkeh67`) | 4.18 |
| `boycott-api` | Lambda | Powers boycott tracker page | 4.19 |
| `comments-handler` | Lambda | Already in main.tf — just applied | 4.8 |
| `mountain-pledges` | DynamoDB | Stores user pledges for mountains | 3.1 |
| `mountain-badges` | DynamoDB | Stores earned badges | 3.2 |
| `mountain-contributions` | DynamoDB | Tracks user contributions | 3.3 |
| `forum-posts` | DynamoDB | Forum discussion data | 3.16 |
| `business-directory` | DynamoDB | Business listings | 3.17 |
| `boycott-tracker` | DynamoDB | Boycott tracker data | 3.19 |
| `content-comments` | DynamoDB | Article/video comments | 3.5 |
| `admin-users` | DynamoDB | Admin authentication | 3.4 |
| `pending-changes` | DynamoDB | Content moderation queue | 3.7 |

### Priority 2 — HIGH (Supporting Infrastructure)

Important but not immediately user-facing, or have workarounds.

| Resource | Type | Why High | Section |
|----------|------|---------|---------|
| `user-email-api` | Lambda | User email campaign management | 4.15 |
| `feature-flags-api` | Lambda | Feature flag toggles | 4.5 |
| `tracking-api` | Lambda | Analytics/tracking | 4.20 |
| `email-sender` | Lambda | Email sending | 4.21 |
| `contact-form-api` | Lambda | Contact form submissions | 4.9 |
| `feature-flags` | DynamoDB | Feature flag data | 3.6 |
| `user-email-campaigns` | DynamoDB | Email campaign data | 3.13 |
| `user-email-subscribers` | DynamoDB | Email subscriber lists | 3.18 |
| `user-email-drip-enrollments` | DynamoDB | Drip campaign enrollments | 3.14 |
| `user-email-events` | DynamoDB | Email event tracking | 3.15 |
| `video-processing-queue` | SQS | Video processing pipeline | 5.1 |
| `thumbnail-generation-queue` | SQS | Thumbnail generation pipeline | 5.2 |
| `email-queue` | SQS | Email sending pipeline | 5.3 |
| `platform-critical-alerts` | SNS | Critical alert notifications | 6.1 |
| `video-download-notifications` | SNS | Download completion alerts | 6.2 |
| `ses-bounces` | SNS | Email bounce handling | 6.3 |
| `ses-email-events` | SNS | SES event processing (Lambda sub) | 6.4 |

### Priority 3 — LOW (Nice to Have)

Functional but lower risk. Import when you have time.

| Resource | Type | Notes |
|----------|------|-------|
| `testimony-*` (5 functions) | Lambda | Testimony feature — Node.js functions | 4.19–4.23 |
| `newsletter_api` | Lambda | Newsletter system | 4.2 |
| `digest_generator` | Lambda | Newsletter digest | 4.3 |
| `email-subscription-handler` | Lambda | Email subscription | 4.10 |
| `email-drip-processor` | Lambda | Drip campaigns | 4.11 |
| `manual-email-sender` | Lambda | Manual email sends | 4.12 |
| `ses-event-processor` | Lambda | SES event processing | 4.13 |
| `NewsScraperLambda` | Lambda | News scraping pipeline | 4.22 |
| `auto-cache-monitor` | Lambda | Cache monitoring | 4.6 |
- `NewsScraperQueue` / `NewsScraperDLQ` | SQS | News scraper pipeline |
| `email-notification-queue` | SQS | Email notifications | 5.4 |
| `analytics-queue` | SQS | Analytics pipeline | 5.5 |
| `surveillance-alerts` | SNS | Security alerts | 6.5 |
| `email-campaign-stats` | DynamoDB | Campaign analytics | 3.9 |
| `email-subscriber-stats` | DynamoDB | Subscriber analytics | 3.10 |
| `email_subscribers` | DynamoDB | Legacy subscriber table | 3.11 |
| `newsletter_analytics` | DynamoDB | Newsletter tracking | 3.12 |
| `user-flags` | DynamoDB | User flag data | 3.8 |

### Skip (Demo/Learning — Don't Import)

- **Lambda:** `ffmpegLambda`, `musicFunction`, `pollyFunctionTest`, `TrackPollyUsage`, `blue-green-demo`, `createTempate`, `bible-lesson-to-audio`, `recipe-scrapter`, `recipe-scraper`, `recipe-scraper-lambda`, `video-url-generator`, `products-api`, `orders-api`, `reviews-api`, `storage_api`, `subscription_api`, `comments-api` (dead — zero invocations)
- **DynamoDB:** `Cards`, `Cart`, `DemoTable`, `FindingEtsyDoc`, `NewsArticles`, `Orders`, `Products`, `ProductViews`, `Reviews`, `StorageFiles`, `StorageUsers`, `Templates`, `Users`, `WatchList`, `WebsiteConfigs`, `saas-tf-lock-table`, `terraform-state-lock`
- **SQS:** `DemoQue`, `DemoQueue.fifo`, `TestQue.fifo`, `order-processing-queue`, `payment-processing-queue`, `inventory-update-queue` (+ their DLQs)
- **SNS:** `DemoTopic`, `MyFirstTopic`, `PollyUsageAlerts`, `PollyUsageAlertsv2`, `my-textract-completion-topic`
- **API Gateway:** `MyMusicAPI`, `shopping-api`, `recipe-scraper-api`

### Recommended Workflow

1. Pick a priority tier (start with Priority 1)
2. For each resource: add HCL block to `main.tf` → `terraform import` → `terraform plan -target` → fix drift
3. After importing all resources in a tier, run full `terraform plan` to check for surprises
4. Commit to git: `git commit -m "terraform: import priority 1 resources"`
5. Move to next tier

---

## 11. Case Study — comments-api vs comments-handler {#11-case-study-comments}

This is a real example of investigating drift between Terraform state and live AWS. It demonstrates the detective work needed when things don't match up.

### The Problem

`main.tf` had a Lambda called `comments-api` with an API Gateway integration pointing to `/comments`. But when checking AWS, the actual API Gateway route for `/comments` pointed to a DIFFERENT function: `comments-handler`.

### Investigation Steps

#### 1. Check what API Gateway actually routes to

```cmd
aws apigateway get-integration --rest-api-id diz6ceeb22 --resource-id RESOURCE_ID --http-method ANY --profile ekewaka --region us-east-1
```

The `uri` field in the response contains the Lambda ARN. It pointed to `comments-handler`, not `comments-api`.

#### 2. Check if both functions exist

```cmd
aws lambda get-function-configuration --function-name comments-api --profile ekewaka --region us-east-1
aws lambda get-function-configuration --function-name comments-handler --profile ekewaka --region us-east-1
```

Both existed! Different handlers:
- `comments-api`: `index.lambda_handler`
- `comments-handler`: `lambda_function.lambda_handler` (with email notification support)

#### 3. Check which one is actually being called

```cmd
REM Check invocation metrics for the last 6 weeks
aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=comments-api --start-time 2025-05-01T00:00:00Z --end-time 2025-06-15T00:00:00Z --period 86400 --statistics Sum --profile ekewaka --region us-east-1

aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=comments-handler --start-time 2025-05-01T00:00:00Z --end-time 2025-06-15T00:00:00Z --period 86400 --statistics Sum --profile ekewaka --region us-east-1
```

Result: `comments-api` had **zero** invocations. `comments-handler` had active traffic.

#### 4. Check git history for context

```cmd
git log --all --oneline -- "**/comments*"
```

Found that `comments-handler` was built first (commit `82cd74a`), and `comments-api` was created later for a standalone API Gateway (`l10alau5g3`) that has since been deleted.

#### 5. Check the frontend

Search the frontend code for which endpoint it calls:

```cmd
powershell -Command "Get-ChildItem -Path '.' -Recurse -Include '*.html','*.js' | Select-String -Pattern 'comments' -Encoding UTF8 | Select-Object -Property Filename,LineNumber,Line"
```

Frontend calls `/prod/comments` on the unified API (`diz6ceeb22`), which routes to `comments-handler`.

### The Fix

1. Removed `comments-api` from `main.tf` (it was the wrong function)
2. Added `comments-handler` with correct config
3. Updated the API Gateway integration to reference `comments-handler`
4. Ran `terraform state rm` to detach the old `comments-api` from state (doesn't delete from AWS)
5. Ran `terraform plan` — clean result: 3 add, 3 change, 2 destroy (all safe)

### Lessons Learned

- **Don't trust the HCL blindly.** The state file and HCL said `comments-api`, but AWS was actually using `comments-handler`.
- **Check CloudWatch invocations** to see which function is actually being called. Zero invocations = dead code.
- **Check git history** to understand why two similar resources exist.
- **Check the frontend** to see what the user actually hits.
- **`terraform state rm`** is your friend — it detaches a resource from state without deleting it from AWS. Safe way to clean up state mismatches.

### Key Commands Used

```cmd
REM Detach a resource from state (does NOT delete from AWS)
terraform state rm module.lambda_comments_api.aws_lambda_function.this
terraform state rm "module.lambda_comments_api.aws_lambda_alias.this[0]"

REM Verify it's gone from state
terraform state list | findstr "comments"

REM Check the plan is clean
terraform plan
```

### Standalone API Gateways Still Active

During this investigation, we also discovered that the frontend references **18 different API Gateway IDs**. Many standalone APIs are still called directly alongside the unified API:

| Standalone API | API ID | Called From |
|---------------|--------|------------|
| mountains-api | `lcmogvl3v2` | All 7 mountain hub pages |
| prayer-api | `cayl9dmtaf` | prayer-wall.html |
| contributors-api | `hzursivfuk` | contributors.html |
| video-downloader-api | `j3w8kgqlvi` | download pages |
| user-email-api | `olmcyxwc1a` | email management pages |
| Book Delivery API | `k2zbtkeh67` | book delivery feature |
| MyTestimony API | `wm234jgiv3` | testimony pages |

These are NOT on the unified API (`diz6ceeb22`) — they're separate REST APIs with their own deployments. Consolidating them is a future project. For now, they need to be imported as-is or left unmanaged.
