import boto3
from decimal import Decimal
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Products')

products = [
    {
        'product_id': str(uuid.uuid4()),
        'name': 'Christian Conservative T-Shirt',
        'description': 'Premium quality t-shirt with faith-based design',
        'price': Decimal('24.99'),
        'category': 'apparel',
        'stock': 100,
        'featured': '1',
        'image_url': 'https://via.placeholder.com/300x300?text=T-Shirt',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'product_id': str(uuid.uuid4()),
        'name': 'Prayer Journal',
        'description': 'Beautiful leather-bound prayer journal',
        'price': Decimal('19.99'),
        'category': 'books',
        'stock': 50,
        'featured': '1',
        'image_url': 'https://via.placeholder.com/300x300?text=Journal',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'product_id': str(uuid.uuid4()),
        'name': 'Faith & Freedom Mug',
        'description': 'Ceramic mug with inspirational message',
        'price': Decimal('14.99'),
        'category': 'accessories',
        'stock': 75,
        'featured': '0',
        'image_url': 'https://via.placeholder.com/300x300?text=Mug',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'product_id': str(uuid.uuid4()),
        'name': 'Voter Guide 2025',
        'description': 'Comprehensive Christian voter guide',
        'price': Decimal('9.99'),
        'category': 'books',
        'stock': 200,
        'featured': '1',
        'image_url': 'https://via.placeholder.com/300x300?text=Guide',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'product_id': str(uuid.uuid4()),
        'name': 'Patriot Cap',
        'description': 'Embroidered cap with American flag',
        'price': Decimal('18.99'),
        'category': 'apparel',
        'stock': 60,
        'featured': '0',
        'image_url': 'https://via.placeholder.com/300x300?text=Cap',
        'created_at': datetime.utcnow().isoformat()
    }
]

print("Adding sample products...")
for product in products:
    table.put_item(Item=product)
    print(f"Added: {product['name']} - ${product['price']}")

print(f"\nSuccessfully added {len(products)} products!")
