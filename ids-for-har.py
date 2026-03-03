import json
from datetime import datetime

def get_request_ids(har_file_path):
    with open(har_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data['log']['entries']:
        timestamp = entry['startedDateTime']
        for header in entry['response'].get('headers', []):
            name = header['name'].lower()
            if name == 'x-amzn-requestid' or name == 'cf-ray':
                print(f"{timestamp} - {header['value']}")

get_request_ids('harfile.har')