resource "aws_cloudfront_distribution" "main" {
  enabled             = var.enabled
  is_ipv6_enabled     = true
  comment             = var.comment
  default_root_object = var.default_root_object
  price_class         = var.price_class
  aliases             = var.aliases

  origin {
    domain_name              = var.bucket_regional_domain_name
    origin_id                = "${var.bucket_name}.s3.${var.aws_region}.amazonaws.com-mgidi2pjodn"
    origin_access_control_id = var.origin_access_control_id
  }

  # Email tracking API origin (conditional)
  dynamic "origin" {
    for_each = var.tracking_api_domain != null ? [1] : []
    content {
      domain_name = var.tracking_api_domain
      origin_id   = "tracking-api-gateway"
      origin_path = var.tracking_api_stage

      custom_origin_config {
        http_port                = 80
        https_port               = 443
        origin_protocol_policy   = "https-only"
        origin_ssl_protocols     = ["TLSv1.2"]
        origin_read_timeout      = 30
        origin_keepalive_timeout = 5
      }
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "${var.bucket_name}.s3.${var.aws_region}.amazonaws.com-mgidi2pjodn"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true

    # Use AWS managed CachingOptimized policy
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  # Email open tracking behavior
  dynamic "ordered_cache_behavior" {
    for_each = var.tracking_api_domain != null ? [1] : []
    content {
      path_pattern           = "track/open/*"
      target_origin_id       = "tracking-api-gateway"
      allowed_methods        = ["GET", "HEAD"]
      cached_methods         = ["GET", "HEAD"]
      compress               = false
      viewer_protocol_policy = "redirect-to-https"

      # Use AWS managed CachingDisabled policy (tracking needs real-time)
      cache_policy_id = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
      
      # Use AWS managed AllViewer policy (pass all headers/query strings)
      origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac"
    }
  }

  # Email click tracking behavior
  dynamic "ordered_cache_behavior" {
    for_each = var.tracking_api_domain != null ? [1] : []
    content {
      path_pattern           = "track/click/*"
      target_origin_id       = "tracking-api-gateway"
      allowed_methods        = ["GET", "HEAD"]
      cached_methods         = ["GET", "HEAD"]
      compress               = false
      viewer_protocol_policy = "redirect-to-https"

      # Use AWS managed CachingDisabled policy
      cache_policy_id = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
      
      # Use AWS managed AllViewer policy
      origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac"
    }
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
