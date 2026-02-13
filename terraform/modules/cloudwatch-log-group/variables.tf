variable "log_group_name" {
  description = "Name of the CloudWatch Log Group"
  type        = string
}

variable "retention_days" {
  description = "Log retention in days (7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653)"
  type        = number
}

variable "tags" {
  description = "Tags to apply to the log group"
  type        = map(string)
  default     = {}
}
