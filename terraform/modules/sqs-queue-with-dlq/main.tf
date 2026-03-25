# Dead Letter Queue
resource "aws_sqs_queue" "dlq" {
  name                       = var.dlq_name != "" ? var.dlq_name : "${var.queue_name}-dlq"
  message_retention_seconds  = var.dlq_message_retention > 0 ? var.dlq_message_retention : var.message_retention
  visibility_timeout_seconds = var.dlq_visibility_timeout > 0 ? var.dlq_visibility_timeout : 30

  lifecycle {
    ignore_changes = [max_message_size]
  }
}

# Main Queue
resource "aws_sqs_queue" "main" {
  name                       = var.queue_name
  visibility_timeout_seconds = var.visibility_timeout
  message_retention_seconds  = var.message_retention

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  lifecycle {
    ignore_changes = [max_message_size]
  }
}