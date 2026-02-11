variable "bucket_name" {
  description = "S3 bucket name for origin"
  type        = string
}

variable "bucket_regional_domain_name" {
  description = "S3 bucket regional domain name"
  type        = string
}

variable "origin_access_control_id" {
  description = "Origin Access Control ID"
  type        = string
}

variable "aliases" {
  description = "Custom domain aliases"
  type        = list(string)
  default     = []
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN (must be in us-east-1)"
  type        = string
  default     = null
}

variable "price_class" {
  description = "CloudFront price class"
  type        = string
  default     = "PriceClass_100"
}

variable "enabled" {
  description = "Whether the distribution is enabled"
  type        = bool
  default     = true
}

variable "comment" {
  description = "Comment for the distribution"
  type        = string
  default     = ""
}

variable "default_root_object" {
  description = "Default root object"
  type        = string
  default     = "index.html"
}
