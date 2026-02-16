variable "queue_name" {
  description = "Name of the SQS queue"
  type = string
}

variable "visibility_timeout" {
  description = "Visibility timeout in seconds"
  type = number
  default = 30
}

variable "message_retention" {
  description = "Message retention period in seconds"
  type = number
  default = 345600 # 4 days
}

variable "max_receive_count" {
  description = "Maximum number before sending to DLQ"
  type = number
  default = 3
}