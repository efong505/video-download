variable "role_name" {
    description = "Name of the IAM role"
    type        = string
}

variable "assume_role_policy" {
    description = "The policy that grants an entity permission to assume the role"
    type        = string
}

variable "managed_policy_arns" {
    description = "List of ARNs of the managed policies to attach to the role"
    type        = list(string)
    default     = []
}

variable "tags" {
    description = "Tags to apply to the IAM role"
    type        = map(string)
    default     = {}
}