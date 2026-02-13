variable "layer_name" {
  type = string
}

variable "description" {
  type    = string
  default = ""
}

variable "compatible_runtimes" {
  type = list(string)
}

variable "filename" {
  type    = string
  default = "placeholder.zip"
}
