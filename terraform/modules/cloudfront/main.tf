resource "aws_cloudfront_distribution" "main" {
  enabled             = var.enabled
  is_ipv6_enabled     = true
  comment             = var.comment
  default_root_object = var.default_root_object
  price_class         = var.price_class
  aliases             = var.aliases

  origin {
    domain_name              = var.bucket_regional_domain_name
    origin_id                = "${var.bucket_name}.s3.us-east-1.amazonaws.com-mgidi2pjodn"
    origin_access_control_id = var.origin_access_control_id
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "${var.bucket_name}.s3.us-east-1.amazonaws.com-mgidi2pjodn"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    # Use AWS managed CachingOptimized policy
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = var.acm_certificate_arn == null
    acm_certificate_arn            = var.acm_certificate_arn
    ssl_support_method             = var.acm_certificate_arn != null ? "sni-only" : null
    minimum_protocol_version       = var.acm_certificate_arn != null ? "TLSv1.2_2021" : null
  }

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [
      # Ignore changes to cache behaviors if managed elsewhere
      default_cache_behavior[0].forwarded_values,
    ]
  }

  tags = {
    Name = "${var.bucket_name}-distribution"
  }
}
