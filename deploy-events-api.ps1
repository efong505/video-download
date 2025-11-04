cd events_api
Compress-Archive -Path * -DestinationPath ..\events_api.zip -Force
cd ..
aws lambda update-function-code --function-name events_api --zip-file fileb://events_api.zip
Write-Host "Events API deployed successfully!"
