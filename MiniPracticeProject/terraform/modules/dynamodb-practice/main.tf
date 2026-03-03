resource "aws_dynamodb_table" "this" {
  name = var.table_name
  billing_mode = "PAY_PER_REQUEST" # On-demand (no cost when empty)
  hash_key = var.hash_key

  attribute {
    name = var.hash_key
    type = "S" # String type
  }

  tags = {
    Name = var.table_name
    Environment = var.environment
    ManagedBy = "Terraform"
  }
}