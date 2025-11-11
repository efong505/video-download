# Rate Limiting Deployment Instructions

## Step 1: Create DynamoDB Table

Run in PowerShell:
```powershell
aws dynamodb create-table `
    --table-name rate-limits `
    --attribute-definitions AttributeName=rate_key,AttributeType=S `
    --key-schema AttributeName=rate_key,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST
```

## Step 2: Deploy Router Lambda

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\router
Compress-Archive -Path index.py -DestinationPath router-rl.zip -Force
aws lambda update-function-code --function-name video-download-router --zip-file fileb://router-rl.zip
Remove-Item router-rl.zip
```

## Step 3: Deploy Articles API Lambda

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\articles_api
Compress-Archive -Path index.py -DestinationPath articles-rl.zip -Force
aws lambda update-function-code --function-name articles-api --zip-file fileb://articles-rl.zip
Remove-Item articles-rl.zip
```

## Verify Deployment

```powershell
aws dynamodb describe-table --table-name rate-limits --query "Table.TableStatus"
aws lambda get-function --function-name video-download-router --query "Configuration.LastModified"
aws lambda get-function --function-name articles-api --query "Configuration.LastModified"
```

## Rate Limits Active

- Anonymous: 20/hour
- Free: 100/hour
- Paid: 1000/hour
- Admin: 10000/hour
