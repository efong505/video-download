import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
articles_table = dynamodb.Table('articles')

response = articles_table.scan()
articles = response.get('Items', [])

for article in articles:
    featured_image = article.get('featured_image', '')
    if 'd3oo5w3ywcz1uh.cloudfront.net' in featured_image:
        article_id = article['article_id']
        new_url = featured_image.replace('d3oo5w3ywcz1uh.cloudfront.net', 'd271vky579caz9.cloudfront.net')
        
        articles_table.update_item(
            Key={'article_id': article_id},
            UpdateExpression='SET featured_image = :img',
            ExpressionAttributeValues={':img': new_url}
        )
        print(f"Updated: {article.get('title')}")

print("Done!")
