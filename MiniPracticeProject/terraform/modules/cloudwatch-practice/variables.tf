variable "log_group_name" {
  description = "Name of the Cloudwatch log group"
  type = string
}

variable "retention_days" {
  description = "Log retention in days"
  type = number
  default = 7
}

variable "environment" {
  description = "Environment tag"
  type = string
  default = "practice"
}