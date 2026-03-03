output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = module.s3_practice.bucket_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb_practice.table_name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = module.lambda_practice.function_name
}

output "cloudwatch_log_group" {
  description = "Name of the Cloudwatch log group"
  value       = module.cloudwatch_practice.log_group_name
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic"
  value       = module.sns_practice.topic_arn
}