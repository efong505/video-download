# ============================================
# Shopping System Infrastructure
# ============================================

# Order Processing Queue
module "sqs_order_processing" {
  source = "../../modules/sqs-queue-with-dlq"
  
  queue_name = "order-processing-queue"
  visibility_timeout = 300 # 5 minutes
  max_receive_count = 3
}

# Payment Processing Queue
module "sqs_payment_processing" {
  source = "../../modules/sqs-queue-with-dlq"
  
  queue_name = "payment-processing-queue"
  visibility_timeout = 180 # 3 minutes
  max_receive_count = 3
}

# Email Notifications Queue
module "sqs_email_notifications" {
  source = "../../modules/sqs-queue-with-dlq"
  
  queue_name = "email-notification-queue"
  visibility_timeout = 60 # 1 minute
  max_receive_count = 3
}

# Inventory Update Queue
module "sqs_inventory_update" {
  source = "../../modules/sqs-queue-with-dlq"
  
  queue_name = "inventory-update-queue"
  visibility_timeout = 120 # 2 minutes
  max_receive_count = 3
}

# Shopping DynamoDB Tables (using existing dynamodb module)
module "dynamodb_shopping_products" {
  source = "../../modules/dynamodb"
  
  table_name   = "Products"
  hash_key     = "product_id"
  billing_mode = "PAY_PER_REQUEST"
  
  attributes = [
    { name = "product_id", type = "S" },
    { name = "category", type = "S" },
    { name = "created_at", type = "S" },
    { name = "status", type = "S" },
    { name = "sales_count", type = "N" },
    { name = "featured", type = "S" }
  ]
  
  global_secondary_indexes = [
    {
      name            = "category-created_at-index"
      hash_key        = "category"
      range_key       = "created_at"
      projection_type = "ALL"
    },
    {
      name            = "status-sales_count-index"
      hash_key        = "status"
      range_key       = "sales_count"
      projection_type = "ALL"
    },
    {
      name            = "featured-created_at-index"
      hash_key        = "featured"
      range_key       = "created_at"
      projection_type = "ALL"
    }
  ]
}

module "dynamodb_shopping_orders" {
  source = "../../modules/dynamodb"

  table_name = "Orders"
  hash_key   = "order_id"
  range_key = "user_id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "order_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "order_date", type = "S" },
    { name = "order_status", type = "S" },
    { name = "payment_status", type = "S" }
  ]
   global_secondary_indexes = [
    {
      name            = "user_id-order_date-index"
      hash_key        = "user_id"
      range_key       = "order_date"
      projection_type = "ALL"
    },
    {
      name            = "order_status-order_date-index"
      hash_key        = "order_status"
      range_key       = "order_date"
      projection_type = "ALL"
    },
    {
      name            = "payment_status-order_date-index"
      hash_key        = "payment_status"
      range_key       = "order_date"
      projection_type = "ALL"
    }
  ]
}

module "dynamodb_shopping_cart" {
  source = "../../modules/dynamodb"
  
  table_name    = "Cart"
  hash_key      = "user_id"
  billing_mode  = "PAY_PER_REQUEST"
  ttl_enabled   = true
  ttl_attribute = "expires_at"
  
  attributes = [
    { name = "user_id", type = "S" }
  ]
}

module "dynamodb_shopping_reviews" {
  source = "../../modules/dynamodb"
  
  table_name   = "Reviews"
  hash_key     = "review_id"
  range_key    = "product_id"
  billing_mode = "PAY_PER_REQUEST"
  
  attributes = [
    { name = "review_id", type = "S" },
    { name = "product_id", type = "S" },
    { name = "user_id", type = "S" },
    { name = "created_at", type = "S" }
  ]
  
  global_secondary_indexes = [
    {
      name            = "product_id-created_at-index"
      hash_key        = "product_id"
      range_key       = "created_at"
      projection_type = "ALL"
    },
    {
      name            = "user_id-created_at-index"
      hash_key        = "user_id"
      range_key       = "created_at"
      projection_type = "ALL"
    }
  ]
}

# ============================================
# Shopping Lambda Functions
# ============================================

module "lambda_products_api" {
  source = "../../modules/lambda"
  
  function_name = "products-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 512
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/testimony-lambda-role"
}

module "lambda_orders_api" {
  source = "../../modules/lambda"
  
  function_name = "orders-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
}

module "lambda_reviews_api" {
  source = "../../modules/lambda"
  
  function_name = "reviews-api"
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = "arn:aws:iam::371751795928:role/lambda-execution-role"
}

# ============================================
# Shopping API Gateway (Separate from Unified API)
# ============================================

resource "aws_api_gateway_rest_api" "shopping_api" {
  name        = "shopping-api"
  description = "Shopping system API endpoints"
  
  endpoint_configuration {
    types = ["EDGE"]
  }

  lifecycle {
    # Don't manage the actual resources/methods/integrations
    # They were created manually and are working
    ignore_changes = [body, policy]
  }
}

output "shopping_api_id" {
  value       = aws_api_gateway_rest_api.shopping_api.id
  description = "Shopping API Gateway ID"
}

output "shopping_api_endpoint" {
  value       = aws_api_gateway_rest_api.shopping_api.execution_arn
  description = "Shopping API Gateway execution ARN"
}

# Outputs
output "shopping_queue_urls" {
  value = {
    order_processing    = module.sqs_order_processing.queue_url
    payment_processing  = module.sqs_payment_processing.queue_url
    email_notification  = module.sqs_email_notifications.queue_url
    inventory_update    = module.sqs_inventory_update.queue_url
  }
  description = "Shopping system SQS queue URLs"
}

output "shopping_dynamodb_tables" {
  description = "Shopping DynamoDB table names"
  value = {
    products = module.dynamodb_shopping_products.table_name
    orders   = module.dynamodb_shopping_orders.table_name
    cart     = module.dynamodb_shopping_cart.table_name
    reviews  = module.dynamodb_shopping_reviews.table_name
  }
}

