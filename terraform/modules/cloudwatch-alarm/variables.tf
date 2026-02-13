variable "alarm_name" {
    type = string
}

variable "comparison_operator" {
    type = string
}

variable "evaluation_periods" {
  type = string
}

variable "metric_name" {
  type = string
}

variable "namespace" {
  type = string
}

variable "period" {
  type = string
}

variable "statistic" {
  type = string
}

variable "threshold" {
  type = number
}

variable "alarm_description" {
  type = string
}

variable "treat_missing_data" {
  type = string
  default = "notBreaching"
}

variable "alarm_actions" {
  type = list(string)
}

variable "dimensions" {
  type = map(string)
}

variable "tags" {
  type = map(string)
}