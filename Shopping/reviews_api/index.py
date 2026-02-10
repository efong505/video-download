import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
reviews_table = dynamodb.Table('Reviews')
products_table = dynamodb.Table('Products')

def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}
        action = params.get('action')
        
        if action == 'create':
            return create_review(event)
        elif action == 'list':
            return list_reviews(params)
        elif action == 'vote':
            return vote_review(event)
        else:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Invalid action'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def create_review(event):
    try:
        body = json.loads(event.get('body', '{}'))
        
        review_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        review = {
            'review_id': review_id,
            'product_id': body['product_id'],
            'user_id': body.get('user_id', 'guest'),
            'rating': body['rating'],
            'title': body['title'],
            'review_text': body['review_text'],
            'helpful_votes': 0,
            'unhelpful_votes': 0,
            'verified_purchase': body.get('verified_purchase', False),
            'status': 'approved',
            'created_at': timestamp
        }
        
        reviews_table.put_item(Item=review)
        
        # Update product rating
        update_product_rating(body['product_id'])
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'review_id': review_id, 'status': 'created'})
        }
    except Exception as e:
        print('Error in create_review:', str(e))
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def list_reviews(params):
    try:
        product_id = params.get('product_id')
        
        response = reviews_table.query(
            IndexName='product_id-created_at-index',
            KeyConditionExpression='product_id = :pid',
            ExpressionAttributeValues={':pid': product_id, ':approved': 'approved'},
            FilterExpression='#status = :approved',
            ExpressionAttributeNames={'#status': 'status'}
        )
        
        reviews = decimal_to_float(response.get('Items', []))
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'reviews': reviews, 'count': len(reviews)})
        }
    except Exception as e:
        print('Error in list_reviews:', str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e), 'reviews': [], 'count': 0})
        }

def vote_review(event):
    body = json.loads(event.get('body', '{}'))
    review_id = body['review_id']
    vote_type = body['vote_type']
    
    if vote_type == 'helpful':
        reviews_table.update_item(
            Key={'review_id': review_id},
            UpdateExpression='SET helpful_votes = helpful_votes + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
    else:
        reviews_table.update_item(
            Key={'review_id': review_id},
            UpdateExpression='SET unhelpful_votes = unhelpful_votes + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'status': 'voted'})
    }

def update_product_rating(product_id):
    response = reviews_table.query(
        IndexName='product_id-created_at-index',
        KeyConditionExpression='product_id = :pid',
        ExpressionAttributeValues={':pid': product_id, ':approved': 'approved'},
        FilterExpression='#status = :approved',
        ExpressionAttributeNames={'#status': 'status'}
    )
    
    reviews = response.get('Items', [])
    if reviews:
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
        products_table.update_item(
            Key={'product_id': product_id},
            UpdateExpression='SET average_rating = :rating, review_count = :count',
            ExpressionAttributeValues={
                ':rating': Decimal(str(round(avg_rating, 1))),
                ':count': len(reviews)
            }
        )
