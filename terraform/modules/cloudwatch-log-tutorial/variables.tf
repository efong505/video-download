variable "log_group_name" {
    description = "The name of the CloudWatch Log Group to monitor"
    type        = string
    # No default = required
}

variable "retention_days" {
    description = "Number of days to retain log events in the specified log group"
    type        = number
    default     = 7 # Default to 7 days
}