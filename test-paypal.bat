@echo off
aws lambda invoke --function-name paypal-billing-api --cli-binary-format raw-in-base64-out --payload "{\"queryStringParameters\":{\"action\":\"test\"},\"httpMethod\":\"GET\"}" out.json
type out.json
