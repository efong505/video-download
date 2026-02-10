# API Gateway Lambda Integration Module
# Creates resource, method, integration, and permissions

variable "api_id" {
  type        = string
  description = "API Gateway REST API ID"
}

variable "root_resource_id" {
  type        = string
  description = "API Gateway root resource ID"
}

variable "path_part" {
  type        = string
  description = "Path segment for this resource (e.g., 'articles')"
}

variable "http_method" {
  type        = string
  description = "HTTP method (GET, POST, PUT, DELETE, ANY)"
}

variable "lambda_function_name" {
  type        = string
  description = "Name of the Lambda function to integrate"
}

variable "lambda_function_arn" {
  type        = string
  description = "ARN of the Lambda function to integrate"
}

variable "authorization" {
  type        = string
  description = "Authorization type (NONE, AWS_IAM, CUSTOM, COGNITO_USER_POOLS)"
  default     = "NONE"
}

variable "enable_cors" {
  type        = bool
  description = "Enable CORS for this endpoint"
  default     = true
}

# Create resource
resource "aws_api_gateway_resource" "this" {
  rest_api_id = var.api_id
  parent_id   = var.root_resource_id
  path_part   = var.path_part
}

# Create method
resource "aws_api_gateway_method" "this" {
  rest_api_id   = var.api_id
  resource_id   = aws_api_gateway_resource.this.id
  http_method   = var.http_method
  authorization = var.authorization
}

# Create Lambda integration
resource "aws_api_gateway_integration" "this" {
  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.this.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}

# Grant API Gateway permission to invoke Lambda
resource "aws_lambda_permission" "this" {
  statement_id  = "AllowAPIGatewayInvoke-${var.path_part}-${var.http_method}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:us-east-1:371751795928:${var.api_id}/*/*"
}

# CORS OPTIONS method (if enabled)
resource "aws_api_gateway_method" "options" {
  count = var.enable_cors ? 1 : 0

  rest_api_id   = var.api_id
  resource_id   = aws_api_gateway_resource.this.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "options" {
  count = var.enable_cors ? 1 : 0

  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options[0].http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "options" {
  count = var.enable_cors ? 1 : 0

  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options[0].http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "options" {
  count = var.enable_cors ? 1 : 0

  rest_api_id = var.api_id
  resource_id = aws_api_gateway_resource.this.id
  http_method = aws_api_gateway_method.options[0].http_method
  status_code = aws_api_gateway_method_response.options[0].status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,PUT,DELETE,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

# Outputs
output "resource_id" {
  value       = aws_api_gateway_resource.this.id
  description = "The resource ID"
}

output "resource_path" {
  value       = aws_api_gateway_resource.this.path
  description = "The full path of the resource"
}
