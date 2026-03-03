resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role = var.role_arn
  handler = var.handler
  runtime = var.runtime
  memory_size = var.memory_size
  timeout = var.timeout
  filename = "${path.module}/placeholder.zip"

  tags = {
    Name = var.function_name
    Environment = var.environment
    ManagedBy = "Terraform"
  }

  lifecycle {
    # Don't update when code changes (managed separately)
    ignore_changes = [ filename, source_code_hash ]
  }
}