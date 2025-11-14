# Deploy Shopping frontend to S3
$bucket = "my-video-downloads-bucket"
$shoppingPath = "Shopping"

Write-Host "Deploying Shopping frontend to S3..." -ForegroundColor Cyan

# Upload HTML files
aws s3 cp ../shop.html s3://$bucket/$shoppingPath/shop.html --content-type "text/html"
aws s3 cp ../cart.html s3://$bucket/$shoppingPath/cart.html --content-type "text/html"
aws s3 cp ../test-products.html s3://$bucket/$shoppingPath/test-products.html --content-type "text/html"
aws s3 cp ../test-cart.html s3://$bucket/$shoppingPath/test-cart.html --content-type "text/html"

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "Access at: https://techcross-videos.s3.amazonaws.com/$shoppingPath/shop.html" -ForegroundColor Yellow
