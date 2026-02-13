variable "topic_name" {
  description   = "The name of the SNS topic to create."
  type          = string
}

variable "email_addresses" {
  description   = "The email addresses to subscribe to the SNS topic."
  type          = list(string)
  default       = []
}

variable "tags" {
    description = "Tas to apply to the topic."
    type        = map(string)
    default     = {}
}