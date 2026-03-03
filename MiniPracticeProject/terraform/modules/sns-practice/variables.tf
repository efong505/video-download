variable "topic_name" {
  description = "Name of the SNS topic"
  type = string
}

variable "environment" {
  description = "Environment tag"
  type = string
  default = "practice"
}