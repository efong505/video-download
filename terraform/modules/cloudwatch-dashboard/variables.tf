variable "dashboard_name" {
  description = "Name of the CloudWatch dashboard"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
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
