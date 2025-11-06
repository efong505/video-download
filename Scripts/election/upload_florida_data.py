import boto3
import csv
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
summaries_table = dynamodb.Table('state-summaries')

def upload_races():
    with open('Election Data and Files/CSV files/florida_races.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            race_id = str(uuid.uuid4())
            races_table.put_item(Item={
                'race_id': race_id,
                'state': row['state'],
                'office': row['office'],
                'election_date': row['election_date'],
                'race_type': row['race_type'],
                'description': row['description'],
                'created_at': datetime.utcnow().isoformat()
            })
            count += 1
            print(f"Uploaded: {row['state']} - {row['office']}")
        print(f"\nTotal races uploaded: {count}")

def upload_summary():
    with open('Election Data and Files/Voter Guides_Summaries/florida_summary_guide.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    summaries_table.put_item(Item={
        'state': 'Florida',
        'title': 'Florida 2024-2026 Elections - Complete Christian Conservatives Today Guide',
        'election_year': '2024-2026',
        'content': content,
        'last_updated': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'updated_by': 'admin'
    })
    print("Florida summary guide uploaded successfully!")

if __name__ == '__main__':
    print("Uploading Florida election data...\n")
    upload_races()
    print("\nUploading Florida summary guide...\n")
    upload_summary()
    print("\n✅ Florida data upload complete!")
