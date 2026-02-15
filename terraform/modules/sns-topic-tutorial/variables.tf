variable "topic_name" {
  description = "The name of the SNS topic to create."
  type        = string
}

variable "email_subscriptions" {
    description = "List of email addresses to subscribe"
    type        = list(string)
    default     = []
}

variable "display_name" {
    description = "The display name for the SNS topic"
    type        = string
    default     = null
}