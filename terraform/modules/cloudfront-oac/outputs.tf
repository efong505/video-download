output "id" {
  description = "Origin Access Control ID"
  value       = aws_cloudfront_origin_access_control.main.id
}

output "etag" {
  description = "Origin Access Control ETag"
  value       = aws_cloudfront_origin_access_control.main.etag
}
