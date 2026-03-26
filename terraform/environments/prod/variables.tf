variable "aws_region" {
  description = "AWS region to deploy all resources"
  type = string
  default = "us-east-1"
}

variable "account_id" {
  description = "AWS account Id"
  type = string
  default = "371751795928"
}

variable "environment" {
    description = "Environment name (prod, staging, dev)"
    type = string
    default = "production"
}

variable "project_name" {
    description = "Project name used in tags and resource naming"
    type = string
    default = "ChristianConservativePlatform"
}

variable "aws_profile" {
    description = "AWS CLI profile to use"
    type = string
    default = "ekewaka"
}