variable "table_name" {
  description = "Name of the DynamoDB table"
  type = string
}

variable "hash_key" {
  description = "Hash key (partition key) for the table"
  type = string
}

variable "environment" {
  description = "Environment tag"
  type = string
  default = "practice"
}