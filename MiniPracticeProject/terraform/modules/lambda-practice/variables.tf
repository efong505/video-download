variable "function_name" {
  description = "Name of the function"
  type = string
}

variable "runtime" {
  description = "Lambda runtime"
  type = string
  default = "python3.12"
}

variable "handler" {
  description = "Lambda handler"
  type = string
  default = "index.lambda_handler"
}

variable "memory_size" {
  description = "Memory allocation in MB"
  type = number
  default = 128
}

variable "timeout" {
  description = "Timeout in seconds"
  type = number
  default = 30
}

variable "role_arn" {
  description = "IAM role ARN for lambda execution"
  type = string
}

variable "environment" {
  description = "Environment tag"
  type = string
  default = "practice"
}