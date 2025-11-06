#!/bin/bash
# Week 1 Deployment Script - SQS Queues
# Run this script to deploy all SQS queues for Christian Conservatives Today

set -e

REGION="us-east-1"
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --region)
            REGION="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "========================================"
echo "Week 1: SQS Queue Deployment"
echo "========================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN MODE - No changes will be made"
    echo ""
fi

# Step 1: Create Dead Letter Queues
echo "[1/5] Creating Dead Letter Queues..."

DLQ_NAMES=("video-processing-dlq" "thumbnail-generation-dlq" "email-dlq" "analytics-dlq")
declare -A DLQ_ARNS

for dlq_name in "${DLQ_NAMES[@]}"; do
    echo "  Creating $dlq_name..."
    
    if [ "$DRY_RUN" = false ]; then
        aws sqs create-queue \
            --queue-name "$dlq_name" \
            --region "$REGION" \
            --attributes '{"MessageRetentionPeriod":"1209600","VisibilityTimeout":"900"}' > /dev/null
        
        dlq_url=$(aws sqs get-queue-url --queue-name "$dlq_name" --region "$REGION" --query 'QueueUrl' --output text)
        dlq_arn=$(aws sqs get-queue-attributes --queue-url "$dlq_url" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)
        DLQ_ARNS[$dlq_name]=$dlq_arn
        
        echo "  ✅ Created: $dlq_arn"
    else
        echo "  [DRY RUN] Would create $dlq_name"
    fi
done

echo ""

# Step 2: Create Main Queues
echo "[2/5] Creating Main Queues..."

if [ "$DRY_RUN" = false ]; then
    # Video processing queue
    echo "  Creating video-processing-queue..."
    aws sqs create-queue \
        --queue-name video-processing-queue \
        --region "$REGION" \
        --attributes "{\"MessageRetentionPeriod\":\"345600\",\"VisibilityTimeout\":\"900\",\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARNS[video-processing-dlq]}\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"}" > /dev/null
    
    VIDEO_QUEUE_URL=$(aws sqs get-queue-url --queue-name video-processing-queue --region "$REGION" --query 'QueueUrl' --output text)
    echo "  ✅ Created: $VIDEO_QUEUE_URL"
    
    # Thumbnail generation queue
    echo "  Creating thumbnail-generation-queue..."
    aws sqs create-queue \
        --queue-name thumbnail-generation-queue \
        --region "$REGION" \
        --attributes "{\"MessageRetentionPeriod\":\"86400\",\"VisibilityTimeout\":\"300\",\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARNS[thumbnail-generation-dlq]}\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"}" > /dev/null
    
    THUMBNAIL_QUEUE_URL=$(aws sqs get-queue-url --queue-name thumbnail-generation-queue --region "$REGION" --query 'QueueUrl' --output text)
    echo "  ✅ Created: $THUMBNAIL_QUEUE_URL"
    
    # Email queue
    echo "  Creating email-queue..."
    aws sqs create-queue \
        --queue-name email-queue \
        --region "$REGION" \
        --attributes "{\"MessageRetentionPeriod\":\"172800\",\"VisibilityTimeout\":\"60\",\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARNS[email-dlq]}\\\",\\\"maxReceiveCount\\\":\\\"5\\\"}\"}" > /dev/null
    
    EMAIL_QUEUE_URL=$(aws sqs get-queue-url --queue-name email-queue --region "$REGION" --query 'QueueUrl' --output text)
    echo "  ✅ Created: $EMAIL_QUEUE_URL"
    
    # Analytics queue
    echo "  Creating analytics-queue..."
    aws sqs create-queue \
        --queue-name analytics-queue \
        --region "$REGION" \
        --attributes "{\"MessageRetentionPeriod\":\"86400\",\"VisibilityTimeout\":\"30\",\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARNS[analytics-dlq]}\\\",\\\"maxReceiveCount\\\":\\\"2\\\"}\"}" > /dev/null
    
    ANALYTICS_QUEUE_URL=$(aws sqs get-queue-url --queue-name analytics-queue --region "$REGION" --query 'QueueUrl' --output text)
    echo "  ✅ Created: $ANALYTICS_QUEUE_URL"
else
    echo "  [DRY RUN] Would create main queues"
fi

echo ""

# Step 3: Update IAM Permissions
echo "[3/5] Updating IAM Permissions..."

if [ "$DRY_RUN" = false ]; then
    cat > sqs-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl"
            ],
            "Resource": [
                "arn:aws:sqs:$REGION:*:video-processing-queue",
                "arn:aws:sqs:$REGION:*:thumbnail-generation-queue",
                "arn:aws:sqs:$REGION:*:email-queue",
                "arn:aws:sqs:$REGION:*:analytics-queue"
            ]
        }
    ]
}
EOF
    
    echo "  Policy document created: sqs-policy.json"
    echo "  ⚠️  Manual step required: Attach this policy to your Lambda execution role"
else
    echo "  [DRY RUN] Would create IAM policy"
fi

echo ""

# Step 4: Display Queue URLs
echo "[4/5] Queue URLs (save these for Lambda environment variables):"

if [ "$DRY_RUN" = false ]; then
    echo "  VIDEO_QUEUE_URL = $VIDEO_QUEUE_URL"
    echo "  THUMBNAIL_QUEUE_URL = $THUMBNAIL_QUEUE_URL"
    echo "  EMAIL_QUEUE_URL = $EMAIL_QUEUE_URL"
    echo "  ANALYTICS_QUEUE_URL = $ANALYTICS_QUEUE_URL"
else
    echo "  [DRY RUN] Queue URLs would be displayed here"
fi

echo ""

# Step 5: Next Steps
echo "[5/5] Next Steps:"
echo "  1. Attach sqs-policy.json to Lambda execution role in IAM console"
echo "  2. Update Lambda environment variables with queue URLs above"
echo "  3. Update Lambda code to send messages to SQS (see 01-SQS-IMPLEMENTATION.md)"
echo "  4. Configure Lambda triggers for queue processing"
echo "  5. Test with: ./scripts/test-sqs.sh"
echo ""

echo "========================================"
echo "✅ Week 1 Deployment Complete!"
echo "========================================"
