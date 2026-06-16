# Local backend for tutorial
# In production, you would use S3 backend with state locking

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# For production, use S3 backend:
# terraform {
#   backend "s3" {
#     bucket         = "my-terraform-state-bucket"
#     key            = "infra-copy/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-state-lock"
#   }
# }
