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

variable "dlq_name" {
  description = "Override DLQ name. Defaults to {queue_name}-dlq if empty."
  type    = string
  default = ""
}

variable "dlq_message_retention" {
  description = "DLQ message retention in seconds. Defaults to main queue retention if 0."
  type    = number
  default = 0
}

variable "dlq_visibility_timeout" {
  description = "DLQ visibility timeout in seconds. Defaults to 30 if 0."
  type    = number
  default = 0
}