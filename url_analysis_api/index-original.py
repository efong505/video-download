import json
import boto3
import os
from html.parser import HTMLParser
import re
import requests

# AWS Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Environment variable to enable/disable AI
USE_AI_SUMMARY = os.environ.get('USE_AI_SUMMARY', 'false').lower() == 'true'

class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.title = None
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            property_name = attrs_dict.get('property', '').lower()
            content = attrs_dict.get('content', '')
            
            if name == 'description':
                self.meta_tags['description'] = content
            elif property_name == 'og:title':
                self.meta_tags['og_title'] = content
            elif property_name == 'og:description':
                self.meta_tags['og_description'] = content
            elif property_name == 'og:image':
                self.meta_tags['og_image'] = content
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        context_type = body.get('context', 'resource')  # 'resource' or 'article'
        
        if not url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL required'})
            }
        
        # Analyze URL with context
        result = analyze_url(url, context_type)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def analyze_url(url, context_type='resource'):
    """Extract meta tags and optionally generate AI summary"""
    
    # Fetch webpage
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}
    
    # Extract meta tags
    parser = MetaTagParser()
    parser.feed(html)
    
    # Get text content for AI summary
    text_content = extract_text_content(html)
    
    # Build result
    result = {
        'url': url,
        'title': parser.meta_tags.get('og_title') or parser.title or 'Untitled',
        'description': parser.meta_tags.get('og_description') or parser.meta_tags.get('description') or '',
        'image': parser.meta_tags.get('og_image') or '',
        'ai_enabled': USE_AI_SUMMARY,
        'context': context_type
    }
    
    # Generate AI summary if enabled
    if USE_AI_SUMMARY and text_content:
        try:
            ai_summary = generate_ai_summary(text_content, result['title'], context_type)
            result['ai_summary'] = ai_summary
        except Exception as e:
            result['ai_error'] = str(e)
    
    return result

def extract_text_content(html):
    """Extract main text content from HTML"""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit to first 3000 characters for AI processing
    return text[:3000]

def generate_ai_summary(content, title, context_type='resource'):
    """Generate summary using AWS Bedrock Claude"""
    
    # Different prompts based on context
    if context_type == 'article':
        prompt = f"""Summarize this article in 2-3 sentences from a Christian conservative perspective. Focus on key facts and biblical relevance if applicable.

Title: {title}

Content: {content}

Summary:"""
    else:  # resource context
        prompt = f"""Summarize this page in 2-3 sentences. If there is a Christian reference to this page, highlight how it is beneficial from a Christian conservative perspective focusing on key facts and biblical relevance if applicable.

Title: {title}

Content: {content}

Summary:"""
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response['body'].read())
    summary = response_body['content'][0]['text'].strip()
    
    return summary
