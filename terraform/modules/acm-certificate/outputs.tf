output "certificate_arn" {
  value       = aws_acm_certificate_validation.this.certificate_arn
  description = "ARN of validated ACM certificate"
}

output "domain_name" {
  value       = aws_acm_certificate.this.domain_name
  description = "Domain name of certificate"
}
