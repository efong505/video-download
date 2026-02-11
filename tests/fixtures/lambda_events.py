"""
Reusable test fixtures for Lambda functions
"""
import json


def create_api_gateway_event(
    http_method="GET",
    path="/",
    body=None,
    headers=None,
    query_params=None,
    path_params=None
):
    """
    Create a mock API Gateway event
    
    Args:
        http_method: HTTP method (GET, POST, etc.)
        path: Request path
        body: Request body (will be JSON encoded)
        headers: Request headers dict
        query_params: Query string parameters dict
        path_params: Path parameters dict
    
    Returns:
        dict: Mock API Gateway event
    """
    event = {
        "httpMethod": http_method,
        "path": path,
        "headers": headers or {"Content-Type": "application/json"},
        "queryStringParameters": query_params,
        "pathParameters": path_params,
        "body": json.dumps(body) if body else None,
        "isBase64Encoded": False,
        "requestContext": {
            "requestId": "test-request-id",
            "identity": {
                "sourceIp": "127.0.0.1"
            }
        }
    }
    return event


def create_s3_event(bucket_name, object_key, event_name="ObjectCreated:Put"):
    """
    Create a mock S3 event
    
    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        event_name: S3 event name
    
    Returns:
        dict: Mock S3 event
    """
    return {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "eventName": event_name,
                "s3": {
                    "bucket": {
                        "name": bucket_name,
                        "arn": f"arn:aws:s3:::{bucket_name}"
                    },
                    "object": {
                        "key": object_key,
                        "size": 1024
                    }
                }
            }
        ]
    }


def create_dynamodb_stream_event(table_name, event_name="INSERT", keys=None, new_image=None):
    """
    Create a mock DynamoDB Stream event
    
    Args:
        table_name: DynamoDB table name
        event_name: Event name (INSERT, MODIFY, REMOVE)
        keys: Record keys dict
        new_image: New image dict
    
    Returns:
        dict: Mock DynamoDB Stream event
    """
    return {
        "Records": [
            {
                "eventID": "test-event-id",
                "eventName": event_name,
                "eventSource": "aws:dynamodb",
                "dynamodb": {
                    "Keys": keys or {"id": {"S": "test-id"}},
                    "NewImage": new_image or {"id": {"S": "test-id"}, "data": {"S": "test-data"}},
                    "StreamViewType": "NEW_AND_OLD_IMAGES"
                }
            }
        ]
    }


def create_lambda_context(
    function_name="test-function",
    memory_limit_mb=512,
    timeout_seconds=30
):
    """
    Create a mock Lambda context object
    
    Args:
        function_name: Lambda function name
        memory_limit_mb: Memory limit in MB
        timeout_seconds: Timeout in seconds
    
    Returns:
        Mock Lambda context object
    """
    from unittest.mock import Mock
    
    context = Mock()
    context.function_name = function_name
    context.memory_limit_in_mb = memory_limit_mb
    context.invoked_function_arn = f"arn:aws:lambda:us-east-1:123456789012:function:{function_name}"
    context.aws_request_id = "test-request-id"
    context.log_group_name = f"/aws/lambda/{function_name}"
    context.log_stream_name = "test-log-stream"
    context.get_remaining_time_in_millis = lambda: timeout_seconds * 1000
    
    return context


# Common test data
VALID_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdC11c2VyIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIn0.test"

SAMPLE_USER = {
    "user_id": "test-user-123",
    "email": "test@example.com",
    "role": "user",
    "subscription_status": "active"
}

SAMPLE_ARTICLE = {
    "article_id": "test-article-123",
    "title": "Test Article",
    "content": "Test content",
    "author": "Test Author",
    "created_at": "2026-02-10T12:00:00Z"
}

SAMPLE_VIDEO = {
    "video_id": "test-video-123",
    "title": "Test Video",
    "url": "https://example.com/video.mp4",
    "thumbnail": "https://example.com/thumb.jpg",
    "duration": 300
}
