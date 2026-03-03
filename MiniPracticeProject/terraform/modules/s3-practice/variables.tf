variable "bucket_prefix" {
  description = "Prefix for s3 bucket name"
  type = string
}

variable "environment" {
  description = "Environment tag"
  type = string
  default = "practice"
}

