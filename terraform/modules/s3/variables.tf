variable "bucket_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "versioning_enabled" {
  description = "Enable versioning for the bucket"
  type = bool
  default = true
}

variable "sse_algorithm" {
  description = "Server-side encryption algorithm (AES256 or aws:kms)"
  type = string
  default = "AES256"
}