# Book Delivery System Setup

## 1. Create DynamoDB Table
```bash
aws dynamodb create-table \
    --table-name book_purchases \
    --attribute-definitions AttributeName=transaction_id,AttributeType=S \
    --key-schema AttributeName=transaction_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

## 2. Upload PDF to S3
```bash
aws s3 cp the-necessary-evil-full.pdf s3://my-video-downloads-bucket/books/
```

## 3. Create Lambda Function
```bash
aws lambda create-function \
    --function-name book-delivery-api \
    --runtime python3.12 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
    --handler index.lambda_handler \
    --zip-file fileb://book_delivery_api/function.zip \
    --timeout 30 \
    --memory-size 256 \
    --region us-east-1
```

## 4. Create API Gateway Endpoint
1. Go to API Gateway console
2. Create new REST API
3. Create resource: `/book-delivery`
4. Create POST method → Lambda proxy integration → book-delivery-api
5. Enable CORS
6. Deploy to stage (e.g., `prod`)
7. Note the Invoke URL: `https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/book-delivery`

## 5. Configure PayPal IPN
1. Log into PayPal Business account
2. Go to Account Settings → Notifications → Instant payment notifications
3. Click "Update"
4. Set Notification URL: `https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/book-delivery?action=ipn`
5. Check "Receive IPN messages (Enabled)"
6. Save

## 6. Test Manual Link Generation
```bash
curl "https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/book-delivery?action=generate_link&email=test@example.com&txn_id=TEST123"
```

## How It Works

1. Customer clicks PayPal button on book.html
2. Customer completes payment
3. PayPal sends IPN to your Lambda function
4. Lambda:
   - Verifies payment with PayPal
   - Generates 7-day signed S3 URL
   - Stores purchase in DynamoDB
   - Emails download link to customer
   - Notifies you of sale
5. Customer receives email with download link
6. Customer downloads PDF (link expires in 7 days)

## Manual Delivery (if needed)
If automatic delivery fails, manually generate link:
```
https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/book-delivery?action=generate_link&email=CUSTOMER_EMAIL&txn_id=PAYPAL_TXN_ID
```

## Deployment
```powershell
.\deploy-book-delivery.ps1
```
