output "domain_name" {
  description = "Custom domain name"
  value       = aws_api_gateway_domain_name.this.domain_name
}

output "regional_domain_name" {
  description = "Regional domain name for the API Gateway"
  value       = aws_api_gateway_domain_name.this.regional_domain_name
}

output "regional_zone_id" {
  description = "Regional zone ID for the API Gateway"
  value       = aws_api_gateway_domain_name.this.regional_zone_id
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name (if using edge-optimized)"
  value       = aws_api_gateway_domain_name.this.cloudfront_domain_name
}
