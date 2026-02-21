# Add this to main.tf after the other Lambda functions

# PayPal IPN Handler Lambda
module "lambda_paypal_ipn_handler" {
  source = "../../modules/lambda"

  function_name = "paypal-ipn-handler"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 256
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
  publish       = true
  create_alias  = true
  alias_name    = "live"

  environment_variables = {}
}

# PayPal IPN endpoint
module "api_paypal_ipn" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "paypal-ipn"
  http_method          = "POST"
  lambda_function_name = module.lambda_paypal_ipn_handler.function_name
  lambda_function_arn  = module.lambda_paypal_ipn_handler.function_arn
  enable_cors          = false  # PayPal doesn't need CORS
}
