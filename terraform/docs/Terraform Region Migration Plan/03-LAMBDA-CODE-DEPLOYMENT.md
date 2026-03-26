# Phase 3: Lambda Code Deployment Pipeline

## Objective

Currently, Terraform manages Lambda function *configuration* (runtime, memory, timeout, role) but ignores the actual code via `lifecycle { ignore_changes = [filename, source_code_hash] }`. This means after Terraform creates empty Lambda shells in a new region, you need a reliable way to deploy code to all 48 functions.

This phase creates a repeatable, scriptable deployment pipeline that works in any region.

## Risk Level: LOW

The deployment script targets existing functions. If a deployment fails, the previous code version remains active.

## Estimated Time: 3-4 hours

## Prerequisites

- All Lambda source code is accessible locally or in a known repository
- AWS CLI configured with `ekewaka` profile

---

## Current Lambda Code Locations

Before building the pipeline, you need to inventory where each Lambda's source code lives. Based on the project structure:

```
Downloader/
├── articles_api/          → articles-api
├── auth_api/              → auth-api (maybe)
├── lambda_functions/      → various functions
├── ...
```

### Step 1: Create a Lambda Source Code Inventory

Create `terraform/scripts/lambda-inventory.json`:

```json
{
  "functions": [
    {
      "name": "admin-api",
      "source_dir": "../../admin_api",
      "handler": "index.lambda_handler",
      "runtime": "python3.12"
    },
    {
      "name": "articles-api",
      "source_dir": "../../articles_api",
      "handler": "index.lambda_handler",
      "runtime": "python3.12"
    },
    {
      "name": "auth-api",
      "source_dir": "../../auth_api",
      "handler": "index.lambda_handler",
      "runtime": "python3.12"
    }
  ]
}
```

You'll need to fill this out for all 48 functions. To discover the current source paths:

```powershell
# List all Lambda function directories in the project
Get-ChildItem -Path "c:\Users\Ed\Documents\Programming\AWS\Downloader" -Directory |
  Where-Object { $_.Name -match "api|lambda|handler|processor|sender|scraper" } |
  Select-Object Name, FullName
```

---

## Step 2: Create the Deployment Script

Create `terraform/scripts/deploy-lambdas.py`:

```python
#!/usr/bin/env python3
"""
Lambda Code Deployment Script

Deploys Lambda function code to any AWS region.

Usage:
    python deploy-lambdas.py --region us-east-1 --profile ekewaka
    python deploy-lambdas.py --region us-west-2 --profile ekewaka --function articles-api
    python deploy-lambdas.py --region us-east-1 --profile ekewaka --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')  # Windows emoji fix

SCRIPT_DIR = Path(__file__).parent
INVENTORY_FILE = SCRIPT_DIR / "lambda-inventory.json"
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Downloader/


def load_inventory():
    """Load the Lambda function inventory."""
    with open(INVENTORY_FILE) as f:
        return json.load(f)["functions"]


def create_zip(source_dir, function_name):
    """Create a deployment zip from the source directory."""
    source_path = PROJECT_ROOT / source_dir
    if not source_path.exists():
        print(f"  ERROR: Source directory not found: {source_path}")
        return None

    zip_path = Path(tempfile.gettempdir()) / f"{function_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_path):
            # Skip __pycache__, .git, node_modules
            dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'node_modules', '.pytest_cache')]
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_path)
                zf.write(file_path, arcname)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  Zip created: {zip_path} ({size_mb:.1f} MB)")

    # Lambda has a 50MB direct upload limit; 250MB unzipped limit
    if size_mb > 50:
        print(f"  WARNING: Zip exceeds 50MB direct upload limit. Will need S3 upload.")
        return None

    return zip_path


def deploy_function(function_name, zip_path, region, profile, dry_run=False):
    """Deploy a single Lambda function."""
    if dry_run:
        print(f"  DRY RUN: Would deploy {zip_path} to {function_name} in {region}")
        return True

    cmd = [
        "aws", "lambda", "update-function-code",
        "--function-name", function_name,
        "--zip-file", f"fileb://{zip_path}",
        "--region", region,
        "--profile", profile,
        "--output", "json"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        response = json.loads(result.stdout)
        print(f"  Deployed successfully. CodeSize: {response.get('CodeSize', 'N/A')} bytes")
        return True
    else:
        print(f"  FAILED: {result.stderr.strip()}")
        return False


def verify_function(function_name, region, profile):
    """Verify a Lambda function exists and is active."""
    cmd = [
        "aws", "lambda", "get-function",
        "--function-name", function_name,
        "--region", region,
        "--profile", profile,
        "--query", "Configuration.{State:State,Runtime:Runtime,CodeSize:CodeSize}",
        "--output", "json"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        info = json.loads(result.stdout)
        print(f"  Status: {info.get('State', 'Unknown')}, "
              f"Runtime: {info.get('Runtime', 'Unknown')}, "
              f"CodeSize: {info.get('CodeSize', 'Unknown')} bytes")
        return True
    else:
        print(f"  NOT FOUND in {region}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Deploy Lambda functions to any region")
    parser.add_argument("--region", required=True, help="Target AWS region")
    parser.add_argument("--profile", default="ekewaka", help="AWS CLI profile")
    parser.add_argument("--function", help="Deploy a single function (by name)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deployed")
    parser.add_argument("--verify-only", action="store_true", help="Only verify functions exist")
    args = parser.parse_args()

    inventory = load_inventory()

    if args.function:
        inventory = [f for f in inventory if f["name"] == args.function]
        if not inventory:
            print(f"Function '{args.function}' not found in inventory.")
            sys.exit(1)

    print(f"\nTarget region: {args.region}")
    print(f"Profile: {args.profile}")
    print(f"Functions: {len(inventory)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'VERIFY ONLY' if args.verify_only else 'DEPLOY'}")
    print("=" * 60)

    success = 0
    failed = 0

    for func in inventory:
        name = func["name"]
        print(f"\n[{name}]")

        if args.verify_only:
            if verify_function(name, args.region, args.profile):
                success += 1
            else:
                failed += 1
            continue

        # Create zip
        zip_path = create_zip(func["source_dir"], name)
        if not zip_path:
            failed += 1
            continue

        # Deploy
        if deploy_function(name, zip_path, args.region, args.profile, args.dry_run):
            success += 1
        else:
            failed += 1

        # Clean up temp zip
        if zip_path and zip_path.exists():
            zip_path.unlink()

    print("\n" + "=" * 60)
    print(f"Results: {success} succeeded, {failed} failed, {len(inventory)} total")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Step 3: Organize Lambda Source Code

If your Lambda source code isn't already in a consistent structure, organize it:

```
Downloader/
├── lambdas/                    # All Lambda source code
│   ├── admin-api/
│   │   └── index.py
│   ├── articles-api/
│   │   └── index.py
│   ├── auth-api/
│   │   └── index.py
│   ├── comments-handler/
│   │   └── lambda_function.py
│   ├── email-sender/
│   │   └── index.py
│   ├── testimony-auth/         # Node.js
│   │   ├── auth.js
│   │   ├── package.json
│   │   └── node_modules/
│   └── ...
```

**Important:** Some functions use `index.lambda_handler` and others use `lambda_function.lambda_handler`. The handler path must match the file structure in the zip.

### Handler-to-File Mapping

| Handler | Expected File |
|---------|--------------|
| `index.lambda_handler` | `index.py` at zip root |
| `lambda_function.lambda_handler` | `lambda_function.py` at zip root |
| `auth.handler` | `auth.js` at zip root (Node.js) |
| `testimony.handler` | `testimony.js` at zip root (Node.js) |
| `admin.handler` | `admin.js` at zip root (Node.js) |
| `email-sharing.handler` | `email-sharing.js` at zip root (Node.js) |
| `email-ses.handler` | `email-ses.js` at zip root (Node.js) |

---

## Step 4: Lambda Layers Deployment

Lambda layers also need to be deployed to the new region. Layers contain binary dependencies (ffmpeg, yt-dlp) that are platform-specific.

### Current Layers

| Layer | Contents | Size |
|-------|----------|------|
| `yt-dlp-layer-v2` | yt-dlp binary | Large |
| `ffmpeg-layer` | FFmpeg binaries | Large |
| `requests-layer` | Python requests library | Small |

### Layer Deployment Script

Layers are trickier because Terraform manages them via `lifecycle { ignore_changes }` similar to Lambda code. You need the original layer zip files.

```python
# deploy-layers.py (simplified)
import subprocess
import sys

LAYERS = [
    {
        "name": "yt-dlp-layer-v2",
        "zip_path": "layers/yt-dlp-layer-v2.zip",
        "runtimes": "python3.11"
    },
    {
        "name": "ffmpeg-layer",
        "zip_path": "layers/ffmpeg-layer.zip",
        "runtimes": "python3.11"
    },
    {
        "name": "requests-layer",
        "zip_path": "layers/requests-layer.zip",
        "runtimes": "python3.9 python3.10 python3.11 python3.12"
    }
]

def deploy_layer(layer, region, profile):
    cmd = [
        "aws", "lambda", "publish-layer-version",
        "--layer-name", layer["name"],
        "--zip-file", f"fileb://{layer['zip_path']}",
        "--compatible-runtimes", *layer["runtimes"].split(),
        "--region", region,
        "--profile", profile
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  {layer['name']}: Deployed successfully")
    else:
        print(f"  {layer['name']}: FAILED - {result.stderr}")

if __name__ == "__main__":
    region = sys.argv[1] if len(sys.argv) > 1 else "us-east-1"
    profile = sys.argv[2] if len(sys.argv) > 2 else "ekewaka"
    for layer in LAYERS:
        deploy_layer(layer, region, profile)
```

**Important:** Save your layer zip files! If you don't have them, you can download the current versions:

```bash
# Get the layer version download URL
aws lambda get-layer-version --layer-name ffmpeg-layer --version-number 1 \
  --profile ekewaka --region us-east-1 \
  --query "Content.Location" --output text
```

This returns a presigned S3 URL you can download the zip from.

---

## Step 5: Alternative — Terraform-Managed Lambda Code

Instead of external deployment scripts, you can have Terraform manage the code directly. This is more complex but fully declarative.

### How It Works

```hcl
# Create zip from source
data "archive_file" "articles_api" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambdas/articles-api"
  output_path = "${path.module}/../../.build/articles-api.zip"
}

module "lambda_articles_api" {
  source = "../../modules/lambda"

  function_name    = "articles-api"
  filename         = data.archive_file.articles_api.output_path
  source_code_hash = data.archive_file.articles_api.output_base64sha256
  ...
}
```

### Pros:
- `terraform apply` deploys both infrastructure AND code
- Code changes tracked in plan output
- No separate deployment step

### Cons:
- Every `terraform plan` checks all 48 zip files
- Slower plan/apply cycles
- Need to remove `lifecycle { ignore_changes = [filename, source_code_hash] }` from Lambda module
- Node.js functions need `node_modules` bundled (adds complexity)

### Recommendation

For the migration, use the **deployment script approach** (Steps 2-4). It's simpler and doesn't require changing the Lambda module. You can migrate to Terraform-managed code later as a separate improvement.

---

## Testing

### Test 1: Verify Script Against Current Region

```bash
# Verify all functions exist in us-east-1
python deploy-lambdas.py --region us-east-1 --profile ekewaka --verify-only
```

Expected: All 48 functions show as found with Active state.

### Test 2: Dry Run

```bash
# See what would be deployed without actually deploying
python deploy-lambdas.py --region us-east-1 --profile ekewaka --dry-run
```

Expected: Shows zip creation and "Would deploy" messages for all functions.

### Test 3: Deploy Single Function

```bash
# Deploy just one function to verify the pipeline works
python deploy-lambdas.py --region us-east-1 --profile ekewaka --function articles-api
```

Then test: `curl https://api.christianconservativestoday.com/articles`

### Test 4: Layer Download Verification

```bash
# Verify you can download existing layer zips
aws lambda get-layer-version --layer-name requests-layer --version-number 1 \
  --profile ekewaka --region us-east-1 \
  --query "Content.{Location:Location,CodeSize:CodeSize}" --output json
```

Download and save the zip for migration use.

---

## Checklist

- [ ] Lambda source code inventory created (`lambda-inventory.json`)
- [ ] All 48 functions mapped to source directories
- [ ] Deployment script created and tested (`deploy-lambdas.py`)
- [ ] Layer zip files saved locally (`layers/` directory)
- [ ] Layer deployment script created (`deploy-layers.py`)
- [ ] `--verify-only` passes against us-east-1
- [ ] `--dry-run` completes for all functions
- [ ] Single function deploy + test succeeds
- [ ] Handler-to-file mapping verified for all functions
- [ ] Git commit: "Phase 3: Lambda code deployment pipeline"
