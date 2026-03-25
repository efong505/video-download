# Week 9: End-to-End Test
$base = "https://ydq9xzya5d.execute-api.us-east-1.amazonaws.com/prod"
Write-Host "`n=== END-TO-END TEST ===" -ForegroundColor Cyan

# Step 1: Browse products
Write-Host "`n[1/5] Browsing products..." -ForegroundColor Yellow
$products = (Invoke-WebRequest -Uri "$base/products?action=list&limit=3" -UseBasicParsing).Content | ConvertFrom-Json
$product = $products.products[0]
Write-Host "  Found: $($product.name) - `$$($product.price)" -ForegroundColor Green

# Step 2: Track the view
Write-Host "`n[2/5] Tracking product view..." -ForegroundColor Yellow
$viewBody = @{product_id=$product.product_id; product_name=$product.name; product_price=[double]$product.price; product_category=$product.category; session_id="e2e-test"} | ConvertTo-Json
$view = (Invoke-WebRequest -Uri "$base/tracking?action=track-view" -Method POST -ContentType "application/json" -Body $viewBody -UseBasicParsing).Content | ConvertFrom-Json
Write-Host "  View tracked: $($view.view_id)" -ForegroundColor Green

# Step 3: Track add to cart
Write-Host "`n[3/5] Adding to cart (tracking)..." -ForegroundColor Yellow
$cartBody = @{product_id=$product.product_id; session_id="e2e-test"} | ConvertTo-Json
$cart = (Invoke-WebRequest -Uri "$base/tracking?action=track-cart-add" -Method POST -ContentType "application/json" -Body $cartBody -UseBasicParsing).Content | ConvertFrom-Json
Write-Host "  Cart add tracked: updated=$($cart.updated)" -ForegroundColor Green

# Step 4: Place order
Write-Host "`n[4/5] Placing order..." -ForegroundColor Yellow
$price = [double]$product.price
$tax = [Math]::Round($price * 0.08, 2)
$total = $price + $tax
$orderBody = @{
    user_id = "e2e-test-user"
    user_email = "e2e-test@example.com"
    items = @(@{product_id=$product.product_id; name=$product.name; price=$price; quantity=1})
    subtotal = $price
    tax = $tax
    total = $total
    shipping_address = "123 Test St"
} | ConvertTo-Json -Depth 3
$order = (Invoke-WebRequest -Uri "$base/orders?action=create" -Method POST -ContentType "application/json" -Body $orderBody -UseBasicParsing).Content | ConvertFrom-Json
Write-Host "  Order created: $($order.order_id)" -ForegroundColor Green

# Step 5: Verify order exists
Write-Host "`n[5/5] Verifying order..." -ForegroundColor Yellow
$orders = (Invoke-WebRequest -Uri "$base/orders?action=list&user_id=e2e-test-user" -UseBasicParsing).Content | ConvertFrom-Json
$found = $orders.orders | Where-Object { $_.order_id -eq $order.order_id }
if ($found) {
    Write-Host "  Order verified! Status: $($found.order_status)" -ForegroundColor Green
} else {
    Write-Host "  Order NOT found!" -ForegroundColor Red
}

# Step 6: Check recommendations work after view
Write-Host "`n[Bonus] Checking recommendations..." -ForegroundColor Yellow
$recs = (Invoke-WebRequest -Uri "$base/tracking?action=recommendations&session_id=e2e-test" -UseBasicParsing).Content | ConvertFrom-Json
Write-Host "  Recommendations: $($recs.recommendations.Count) products (source: $($recs.source))" -ForegroundColor Green

Write-Host "`n=== END-TO-END TEST COMPLETE ===" -ForegroundColor Green
