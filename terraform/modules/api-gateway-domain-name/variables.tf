variable "domain_name" {
  description = "Custom domain name for API Gateway"
  type        = string
}

variable "certificate_arn" {
  description = "ARN of ACM certificate for the domain"
  type        = string
}

variable "api_id" {
  description = "API Gateway REST API ID"
  type        = string
}

variable "stage_name" {
  description = "API Gateway stage name to map"
  type        = string
}

variable "base_path" {
  description = "Base path for the mapping (empty string for root)"
  type        = string
  default     = ""
}

variable "hosted_zone_id" {
  description = "Route53 hosted zone ID for DNS record"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
