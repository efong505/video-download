# API Gateway REST API Module
# Creates a unified REST API with Lambda integrations

variable "api_name" {
  type        = string
  description = "Name of the API Gateway"
}

variable "api_description" {
  type        = string
  description = "Description of the API Gateway"
  default     = ""
}

variable "stage_name" {
  type        = string
  description = "Deployment stage name"
  default     = "prod"
}

# Create REST API
resource "aws_api_gateway_rest_api" "this" {
  name        = var.api_name
  description = var.api_description

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# Create deployment
resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.this.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create stage
resource "aws_api_gateway_stage" "this" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = var.stage_name
}

# Enable CORS for the API
resource "aws_api_gateway_gateway_response" "cors" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  response_type = "DEFAULT_4XX"

  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"  = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Headers" = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Methods" = "'*'"
  }
}

# Outputs
output "api_id" {
  value       = aws_api_gateway_rest_api.this.id
  description = "The ID of the API Gateway"
}

output "api_arn" {
  value       = aws_api_gateway_rest_api.this.arn
  description = "The ARN of the API Gateway"
}

output "root_resource_id" {
  value       = aws_api_gateway_rest_api.this.root_resource_id
  description = "The resource ID of the REST API's root"
}

output "invoke_url" {
  value       = aws_api_gateway_stage.this.invoke_url
  description = "The URL to invoke the API"
}

output "stage_arn" {
  value       = aws_api_gateway_stage.this.arn
  description = "The ARN of the stage"
}
