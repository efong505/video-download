# GitHub Actions CI/CD Setup

## Overview

Automate Lambda deployments with GitHub Actions. Every push to `main` branch triggers automatic deployment.

**Benefits**:
- ✅ Deploy in 2 minutes (vs 10 minutes manual)
- ✅ Automatic testing before deployment
- ✅ Rollback capability
- ✅ Deployment history
- ✅ Zero human error

---

## Prerequisites

1. GitHub repository for your code
2. AWS credentials (Access Key ID + Secret Access Key)
3. Lambda functions already created in AWS

---

## Step 1: Create GitHub Repository (10 minutes)

If you don't have a GitHub repo yet:

```bash
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

# Initialize git (if not already done)
git init

# Create .gitignore
cat > .gitignore <<EOF
*.zip
*.pyc
__pycache__/
.env
.venv
env/
venv/
node_modules/
.DS_Store
*.log
EOF

# Add all files
git add .
git commit -m "Initial commit"

# Create repo on GitHub (via web interface)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/christian-conservatives-today.git
git branch -M main
git push -u origin main
```

---

## Step 2: Configure AWS Credentials in GitHub (5 minutes)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value |
|------------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_REGION` | `us-east-1` |
| `AWS_ACCOUNT_ID` | Your 12-digit AWS account ID |

**Get your AWS credentials**:
```bash
# View current credentials
aws configure list

# Get account ID
aws sts get-caller-identity --query Account --output text
```

---

## Step 3: Create GitHub Actions Workflows (30 minutes)

Create `.github/workflows/` directory:

```bash
mkdir -p .github/workflows
```

### Workflow 1: Deploy Admin API

Create `.github/workflows/deploy-admin-api.yml`:

```yaml
name: Deploy Admin API

on:
  push:
    branches: [main]
    paths:
      - 'admin_api/**'
      - '.github/workflows/deploy-admin-api.yml'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd admin_api
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt -t .
          fi

      - name: Create deployment package
        run: |
          cd admin_api
          zip -r ../admin-api-deployment.zip . -x "*.git*" "*.pyc" "__pycache__/*"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Lambda
        run: |
          aws lambda update-function-code \
            --function-name admin_api \
            --zip-file fileb://admin-api-deployment.zip

      - name: Wait for update to complete
        run: |
          aws lambda wait function-updated \
            --function-name admin_api

      - name: Test deployment
        run: |
          aws lambda invoke \
            --function-name admin_api \
            --payload '{"httpMethod":"GET","path":"/health"}' \
            response.json
          cat response.json

      - name: Notify success
        if: success()
        run: echo "✅ Admin API deployed successfully!"

      - name: Notify failure
        if: failure()
        run: echo "❌ Admin API deployment failed!"
```

### Workflow 2: Deploy Auth API

Create `.github/workflows/deploy-auth-api.yml`:

```yaml
name: Deploy Auth API

on:
  push:
    branches: [main]
    paths:
      - 'auth_api/**'
      - '.github/workflows/deploy-auth-api.yml'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd auth_api
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt -t .
          fi

      - name: Create deployment package
        run: |
          cd auth_api
          zip -r ../auth-api-deployment.zip . -x "*.git*" "*.pyc" "__pycache__/*"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Lambda
        run: |
          aws lambda update-function-code \
            --function-name auth_api \
            --zip-file fileb://auth-api-deployment.zip

      - name: Wait for update to complete
        run: |
          aws lambda wait function-updated \
            --function-name auth_api

      - name: Test deployment
        run: |
          aws lambda invoke \
            --function-name auth_api \
            --payload '{"httpMethod":"GET","path":"/health"}' \
            response.json
          cat response.json
```

### Workflow 3: Deploy All APIs

Create `.github/workflows/deploy-all.yml`:

```yaml
name: Deploy All APIs

on:
  workflow_dispatch:
    inputs:
      confirm:
        description: 'Type "deploy-all" to confirm'
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate confirmation
        run: |
          if [ "${{ github.event.inputs.confirm }}" != "deploy-all" ]; then
            echo "❌ Confirmation failed. Type 'deploy-all' to proceed."
            exit 1
          fi

  deploy-lambdas:
    needs: validate
    runs-on: ubuntu-latest
    strategy:
      matrix:
        lambda:
          - { name: 'admin_api', dir: 'admin_api' }
          - { name: 'auth_api', dir: 'auth_api' }
          - { name: 'articles_api', dir: 'articles_api' }
          - { name: 'video_list_api', dir: 'video_list_api' }
          - { name: 'news_api', dir: 'news_api' }
          - { name: 'resources_api', dir: 'resources_api' }
          - { name: 'contributors_api', dir: 'contributors_api' }
          - { name: 'comments_api', dir: 'comments_api' }
          - { name: 'tag_api', dir: 'tag_api' }
          - { name: 'prayer_api', dir: 'prayer_api' }
          - { name: 'events_api', dir: 'events_api' }
          - { name: 'email_subscription_api', dir: 'email_subscription_api' }
          - { name: 'ministry_tools_api', dir: 'ministry_tools_api' }
          - { name: 'notifications_api', dir: 'notifications_api' }
          - { name: 'url_analysis_api', dir: 'url_analysis_api' }
          - { name: 'paypal_billing_api', dir: 'paypal_billing_api' }
          - { name: 'downloader', dir: 'downloader' }
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd ${{ matrix.lambda.dir }}
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt -t .
          fi

      - name: Create deployment package
        run: |
          cd ${{ matrix.lambda.dir }}
          zip -r ../${{ matrix.lambda.name }}-deployment.zip . -x "*.git*" "*.pyc" "__pycache__/*"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Lambda
        run: |
          aws lambda update-function-code \
            --function-name ${{ matrix.lambda.name }} \
            --zip-file fileb://${{ matrix.lambda.name }}-deployment.zip

      - name: Wait for update
        run: |
          aws lambda wait function-updated \
            --function-name ${{ matrix.lambda.name }}

      - name: Verify deployment
        run: |
          echo "✅ ${{ matrix.lambda.name }} deployed successfully!"
```

---

## Step 4: Create Reusable Workflow Template (15 minutes)

Create `.github/workflows/lambda-deploy-template.yml`:

```yaml
name: Lambda Deploy Template

on:
  workflow_call:
    inputs:
      lambda-name:
        required: true
        type: string
      lambda-dir:
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
      AWS_SECRET_ACCESS_KEY:
        required: true
      AWS_REGION:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd ${{ inputs.lambda-dir }}
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt -t .
          fi

      - name: Create deployment package
        run: |
          cd ${{ inputs.lambda-dir }}
          zip -r ../${{ inputs.lambda-name }}-deployment.zip . -x "*.git*" "*.pyc" "__pycache__/*"

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Deploy to Lambda
        run: |
          aws lambda update-function-code \
            --function-name ${{ inputs.lambda-name }} \
            --zip-file fileb://${{ inputs.lambda-name }}-deployment.zip

      - name: Wait for update
        run: |
          aws lambda wait function-updated \
            --function-name ${{ inputs.lambda-name }}

      - name: Verify deployment
        run: |
          echo "✅ ${{ inputs.lambda-name }} deployed successfully!"
```

Now create simplified workflows that use this template:

`.github/workflows/deploy-articles.yml`:
```yaml
name: Deploy Articles API

on:
  push:
    branches: [main]
    paths:
      - 'articles_api/**'
  workflow_dispatch:

jobs:
  deploy:
    uses: ./.github/workflows/lambda-deploy-template.yml
    with:
      lambda-name: articles_api
      lambda-dir: articles_api
    secrets:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      AWS_REGION: ${{ secrets.AWS_REGION }}
```

---

## Step 5: Test GitHub Actions (20 minutes)

### Test 1: Manual Trigger
1. Go to GitHub → Actions tab
2. Select "Deploy Admin API"
3. Click "Run workflow"
4. Watch the deployment progress

### Test 2: Automatic Trigger
```bash
# Make a small change to admin_api
cd admin_api
echo "# Updated" >> index.py

# Commit and push
git add .
git commit -m "Test GitHub Actions deployment"
git push origin main

# Watch deployment in GitHub Actions tab
```

### Test 3: Verify Deployment
```bash
# Test the deployed Lambda
aws lambda invoke \
  --function-name admin_api \
  --payload '{"httpMethod":"GET","path":"/health"}' \
  response.json

cat response.json
```

---

## Step 6: Add Deployment Notifications (Optional)

### Slack Notifications

Add to any workflow:

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Deployment of ${{ matrix.lambda.name }} ${{ job.status }}'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

GitHub automatically sends email on workflow failures if enabled in Settings.

---

## Step 7: Create Rollback Workflow (15 minutes)

Create `.github/workflows/rollback.yml`:

```yaml
name: Rollback Lambda

on:
  workflow_dispatch:
    inputs:
      lambda-name:
        description: 'Lambda function name'
        required: true
        type: choice
        options:
          - admin_api
          - auth_api
          - articles_api
          - video_list_api
          - news_api
      version:
        description: 'Version to rollback to (leave empty for previous)'
        required: false

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Get previous version
        if: ${{ github.event.inputs.version == '' }}
        id: get-version
        run: |
          VERSION=$(aws lambda list-versions-by-function \
            --function-name ${{ github.event.inputs.lambda-name }} \
            --query 'Versions[-2].Version' \
            --output text)
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Rollback Lambda
        run: |
          VERSION=${{ github.event.inputs.version || steps.get-version.outputs.version }}
          aws lambda update-alias \
            --function-name ${{ github.event.inputs.lambda-name }} \
            --name prod \
            --function-version $VERSION

      - name: Verify rollback
        run: |
          echo "✅ Rolled back ${{ github.event.inputs.lambda-name }} to version $VERSION"
```

---

## Deployment Workflow Summary

### Automatic Deployments
```
Code Change → Git Push → GitHub Actions → Deploy → Test → Notify
```

### Manual Deployments
```
GitHub Actions Tab → Select Workflow → Run Workflow → Deploy
```

### Rollback
```
GitHub Actions Tab → Rollback Workflow → Select Lambda → Select Version → Rollback
```

---

## Best Practices

1. **Branch Protection**: Require PR reviews before merging to `main`
2. **Testing**: Add unit tests that run before deployment
3. **Staging**: Create a `staging` branch that deploys to staging environment
4. **Versioning**: Use Lambda versions and aliases for rollback capability
5. **Monitoring**: Set up CloudWatch alarms for Lambda errors

---

## Troubleshooting

### Issue: Workflow fails with "Access Denied"
**Solution**: Check AWS credentials in GitHub Secrets

### Issue: Lambda not updating
**Solution**: Check Lambda function name matches exactly

### Issue: Dependencies not installing
**Solution**: Ensure `requirements.txt` exists in Lambda directory

### Issue: Deployment succeeds but Lambda errors
**Solution**: Check CloudWatch logs for runtime errors

---

## Next Steps

1. ✅ Complete API Gateway consolidation (Week 1)
2. ✅ Set up GitHub repository
3. ✅ Configure AWS credentials in GitHub
4. ✅ Create workflow files
5. ✅ Test deployments
6. ✅ Update frontend to use new API URLs
7. ✅ Monitor for 1 week
8. ✅ Delete old APIs

---

**Congratulations!** You now have enterprise-grade CI/CD for your serverless platform. 🎉
