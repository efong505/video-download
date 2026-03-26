variable "dashboard_name" {
  description = "Name of the CloudWatch dashboard"
  type        = string
}

variable "region" {
  description = "AWS region for dashboard metrics"
  type        = string
  # No Default must be passed explicitly
  # default     = "us-east-1"
}

variable "api_gateway_id" {
  description = "API Gateway ID to monitor"
  type        = string
}

variable "lambda_functions" {
  description = "List of Lambda function names to monitor"
  type        = list(string)
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "alarm_names" {
  description = "List of CloudWatch alarm names to display"
  type        = list(string)
  default     = []
}

variable "sqs_queue_names" {
  description = "List of SQS queue names to monitor"
  type        = list(string)
  default     = []
}

variable "dynamodb_table_names" {
  description = "List of DynamoDB table names to monitor"
  type        = list(string)
  default     = []
}

variable "cloudfront_distribution_id" {
  description = "CloudFront distribution ID to monitor"
  type        = string
  default     = ""
}
