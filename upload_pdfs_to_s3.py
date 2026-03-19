"""
Upload PDF guides to S3 for email attachments
Run: python upload_pdfs_to_s3.py
"""
import boto3
import os

# Use specific profile
session = boto3.Session(profile_name='ekewaka')
s3 = session.client('s3')
BUCKET = 'my-video-downloads-bucket'  # Your S3 bucket
PREFIX = 'book-pdfs/'  # Folder in S3

pdfs = [
    'christian-ai-survival-guide.pdf',
    'church-discussion-guide.pdf',
    'ai-parent-guide.pdf',
    'book-teaser.pdf'
]

print("Uploading PDFs to S3...")

for pdf in pdfs:
    local_path = pdf
    s3_key = f"{PREFIX}{pdf}"
    
    if not os.path.exists(local_path):
        print(f"ERROR: {local_path} not found")
        continue
    
    print(f"Uploading {pdf}...")
    s3.upload_file(
        local_path,
        BUCKET,
        s3_key,
        ExtraArgs={
            'ContentType': 'application/pdf',
            'ContentDisposition': f'attachment; filename="{pdf}"'
        }
    )
    print(f"  > Uploaded to s3://{BUCKET}/{s3_key}")

print("\nAll PDFs uploaded successfully!")
print(f"\nS3 URLs:")
for pdf in pdfs:
    print(f"  https://{BUCKET}/{PREFIX}{pdf}")
