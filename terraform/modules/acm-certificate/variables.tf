variable "domain_name" {
  type        = string
  description = "Domain name for ACM certificate"
}

variable "hosted_zone_id" {
  type        = string
  description = "Route53 hosted zone ID for DNS validation"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags to apply to certificate"
}
