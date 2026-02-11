variable "bucket_name" {
  type = string
}

variable "environment" {
  type = string
}

resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["https://christianconservativestoday.com"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_policy" "main" {
  bucket = aws_s3_bucket.main.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipal"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.main.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::371751795928:distribution/E3N00R2D2NE9C5"
          }
        }
      },
      {
        Sid       = "AllowCrossAccountAccess"
        Effect    = "Allow"
        Principal = {
          AWS = [
            "arn:aws:iam::628478946937:root",
            "arn:aws:iam::846247542066:root"
          ]
        }
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetBucketLocation",
          "s3:GetBucketVersioning",
          "s3:ListBucketVersions",
          "s3:GetBucketPublicAccessBlock",
          "s3:GetBucketCORS"
        ]
        Resource = [
          aws_s3_bucket.main.arn,
          "${aws_s3_bucket.main.arn}/*"
        ]
      }
    ]
  })
}

output "bucket_id" {
  value = aws_s3_bucket.main.id
}

output "bucket_arn" {
  value = aws_s3_bucket.main.arn
}

output "bucket_regional_domain_name" {
  description = "S3 bucket regional domain name"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}
