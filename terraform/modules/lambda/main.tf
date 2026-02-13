variable "function_name" {
  type = string
}

variable "runtime" {
  type = string
}

variable "handler" {
  type = string
}

variable "memory_size" {
  type = number
}

variable "timeout" {
  type = number
}

variable "role_arn" {
  type = string
}

variable "environment_variables" {
  type    = map(string)
  default = {}
}

variable "layers" {
  type    = list(string)
  default = []
}

variable "publish" {
  description = "Whether to publish creation/change as new Lambda Function Version"
  type        = bool
  default     = false
}

variable "create_alias" {
  description = "Whether to create a Lambda alias"
  type        = bool
  default     = false
}

variable "alias_name" {
  description = "Name of the Lambda alias"
  type        = string
  default     = "live"
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.role_arn
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  filename      = "${path.module}/placeholder.zip"
  layers        = var.layers
  publish       = var.publish

  environment {
    variables = var.environment_variables
  }

  lifecycle {
    ignore_changes = [filename, source_code_hash, environment]
  }
}

resource "aws_lambda_alias" "this" {
  count            = var.create_alias ? 1 : 0
  name             = var.alias_name
  function_name    = aws_lambda_function.this.function_name
  function_version = aws_lambda_function.this.version

  lifecycle {
    ignore_changes = [function_version]
  }
}

output "function_name" {
  value = aws_lambda_function.this.function_name
}

output "function_arn" {
  value = aws_lambda_function.this.arn
}

output "version" {
  value = aws_lambda_function.this.version
}

output "qualified_arn" {
  value = aws_lambda_function.this.qualified_arn
}

output "alias_arn" {
  value = var.create_alias ? aws_lambda_alias.this[0].arn : null
}

output "alias_invoke_arn" {
  value = var.create_alias ? aws_lambda_alias.this[0].invoke_arn : null
}
