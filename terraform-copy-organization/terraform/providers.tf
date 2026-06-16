# Terraform version and required providers
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Production account provider (default)
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Infrastructure-Copy-Tutorial"
      ManagedBy   = "Terraform"
      Environment = "Production"
    }
  }
}

# Child account provider (using assume role)
provider "aws" {
  alias  = "child"
  region = var.aws_region

  assume_role {
    role_arn     = var.child_account_role_arn
    session_name = "terraform-copy-tutorial"
    external_id  = var.external_id
  }

  default_tags {
    tags = {
      Project     = "Infrastructure-Copy-Tutorial"
      ManagedBy   = "Terraform"
      Environment = "Child-Account"
      CopiedFrom  = "Production"
    }
  }
}
