# Delete duplicate articles, keeping the ones with views

$articlesToDelete = @(
    "209df79e-3a4d-4586-a58c-23c4c88588f4",
    "86e23703-7d4c-4129-b900-51ab4cbad666",
    "3efc0bc6-7968-43b3-ba11-e6da4b2dc50f",
    "4b29f1f6-43e7-45fb-b661-caabca7cc5c0",
    "cf7cd893-01eb-44eb-922b-8fc3026efea3"
)

Write-Host "Deleting $($articlesToDelete.Count) duplicate articles..."

foreach ($articleId in $articlesToDelete) {
    Write-Host "Deleting article: $articleId"
    
    $key = "{`"article_id`": {`"S`": `"$articleId`"}}"
    
    aws dynamodb delete-item --table-name articles --key $key --profile ekewaka --region us-east-1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Success" -ForegroundColor Green
    } else {
        Write-Host "  Failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done! Deleted $($articlesToDelete.Count) duplicate articles."
