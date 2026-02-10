# Example: Add this to your main.tf to create the unified API

# Create unified API Gateway
module "unified_api" {
  source = "../../modules/api-gateway"
  
  api_name        = "ministry-platform-api"
  api_description = "Unified API for Christian Conservative Platform"
  stage_name      = "prod"
}

# Example: Connect auth endpoint
module "api_auth" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id              = module.unified_api.api_id
  root_resource_id    = module.unified_api.root_resource_id
  path_part           = "auth"
  http_method         = "ANY"
  lambda_function_name = module.lambda_auth_api.function_name
  lambda_function_arn  = module.lambda_auth_api.function_arn
  enable_cors         = true
}

# Example: Connect articles endpoint
module "api_articles" {
  source = "../../modules/api-gateway-lambda-integration"
  
  api_id              = module.unified_api.api_id
  root_resource_id    = module.unified_api.root_resource_id
  path_part           = "articles"
  http_method         = "ANY"
  lambda_function_name = module.lambda_articles_api.function_name
  lambda_function_arn  = module.lambda_articles_api.function_arn
  enable_cors         = true
}

# Add more endpoints following the same pattern...
