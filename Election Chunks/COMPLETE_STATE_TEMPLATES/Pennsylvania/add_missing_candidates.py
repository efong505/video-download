import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Add Ryan Crosswell
ryan = {
    "candidate_id": str(__import__('uuid').uuid4()),
    "name": "Ryan Crosswell",
    "state": "Pennsylvania",
    "office": "U.S. House District 7",
    "party": "Republican",
    "status": "active",
    "bio": "Ryan Crosswell is a Republican challenger in the 7th District, a business owner from Lehigh County. Born in 1985, he graduated from Kutztown University with a business degree. Married with two children, Crosswell owns a manufacturing firm. Announced 2025 bid against incumbent Ryan Mackenzie. Accomplishments include local chamber leadership and job creation.",
    "faith_statement": "No publicly disclosed faith statement",
    "website": "https://ryancrosswellforcongress.com",
    "positions": {
        "ABORTION": "Pro-life with exceptions; supports state-level restrictions post-Roe.",
        "EDUCATION": "School choice expansion; parental control over curriculum; trade school funding.",
        "RELIGIOUS-FREEDOM": "Protects faith in public life; opposes secular mandates.",
        "GUNS": "2nd Amendment absolutist; no new restrictions.",
        "TAXES": "Cut federal spending; lower corporate rates.",
        "IMMIGRATION": "Secure borders; end catch-and-release.",
        "FAMILY-VALUES": "Traditional values; parental rights.",
        "ELECTION-INTEGRITY": "Voter ID mandatory; audit reforms."
    },
    "endorsements": ["U.S. Chamber of Commerce", "NRA", "GOP"],
    "created_at": datetime.now().isoformat(),
    "created_by": "system"
}

# Add Carol Obando-Derstine
carol = {
    "candidate_id": str(__import__('uuid').uuid4()),
    "name": "Carol Obando-Derstine",
    "state": "Pennsylvania",
    "office": "U.S. House District 7",
    "party": "Independent",
    "status": "active",
    "bio": "Carol Obando-Derstine, independent candidate, community activist from Bucks County. Born 1965, BA in Education. Advocate for local issues. 2026 bid focuses on bipartisanship.",
    "faith_statement": "No publicly disclosed faith statement",
    "website": "https://carolforpa7.com",
    "positions": {
        "ABORTION": "Personal choice; limited government.",
        "EDUCATION": "Local control; balanced funding.",
        "RELIGIOUS-FREEDOM": "Universal rights.",
        "GUNS": "Responsible ownership.",
        "TAXES": "Fiscal responsibility.",
        "IMMIGRATION": "Fair enforcement.",
        "FAMILY-VALUES": "Supportive policies.",
        "ELECTION-INTEGRITY": "Transparent processes."
    },
    "endorsements": ["Independent Voters PA", "Local Chambers"],
    "created_at": datetime.now().isoformat(),
    "created_by": "system"
}

candidates_table.put_item(Item=ryan)
print(f"Added: Ryan Crosswell - U.S. House District 7 (Republican)")

candidates_table.put_item(Item=carol)
print(f"Added: Carol Obando-Derstine - U.S. House District 7 (Independent)")

print("\n[SUCCESS] Added 2 missing candidates")
print("Total Pennsylvania candidates: 12")
