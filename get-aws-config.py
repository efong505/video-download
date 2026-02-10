#!/usr/bin/env python3
"""
AWS Configuration Helper
Loads configuration from aws-config.json to prevent hardcoded values
"""

import json
import os

CONFIG_FILE = 'aws-config.json'

def load_config():
    """Load AWS configuration from JSON file"""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def get_s3_bucket():
    """Get S3 bucket name"""
    config = load_config()
    return config['s3']['bucket']

def get_s3_config():
    """Get complete S3 configuration"""
    config = load_config()
    return config['s3']

def get_dynamodb_table(table_key):
    """Get DynamoDB table name by key"""
    config = load_config()
    return config['dynamodb']['tables'].get(table_key)

def get_lambda_config():
    """Get Lambda configuration"""
    config = load_config()
    return config['lambda']

# Example usage
if __name__ == '__main__':
    print("AWS Configuration:")
    print(f"S3 Bucket: {get_s3_bucket()}")
    print(f"Video Prefix: {get_s3_config()['video_prefix']}")
    print(f"Videos Table: {get_dynamodb_table('videos')}")
