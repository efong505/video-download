import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

# DELAWARE - Only Senate race in 2026
de_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Delaware', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-09-15', 'incumbent': 'Chris Coons', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Safe Democrat'}
]

# NEW JERSEY - Only Senate race in 2026 (Governor was 2025)
nj_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'New Jersey', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-06-02', 'incumbent': 'Cory Booker', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Likely Democrat'}
]

# RHODE ISLAND - Senate and Governor races in 2026
ri_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Rhode Island', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-09-08', 'incumbent': 'Jack Reed', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Safe Democrat'},
    {'race_id': str(uuid.uuid4()), 'state': 'Rhode Island', 'office': 'Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-09-08', 'incumbent': 'Dan McKee', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Likely Democrat'}
]

print("Uploading Delaware races...")
for race in de_races:
    races_table.put_item(Item=race)
    print(f"  Added: {race['office']} - {race['incumbent']} ({race['incumbent_party']})")

print("\nUploading New Jersey races...")
for race in nj_races:
    races_table.put_item(Item=race)
    print(f"  Added: {race['office']} - {race['incumbent']} ({race['incumbent_party']})")

print("\nUploading Rhode Island races...")
for race in ri_races:
    races_table.put_item(Item=race)
    print(f"  Added: {race['office']} - {race['incumbent']} ({race['incumbent_party']})")

print("\n" + "="*60)
print("UPLOAD COMPLETE")
print("="*60)
print(f"Delaware: {len(de_races)} races")
print(f"New Jersey: {len(nj_races)} races")
print(f"Rhode Island: {len(ri_races)} races")
print(f"TOTAL: {len(de_races) + len(nj_races) + len(ri_races)} races")
print("\nNOTE: No candidates added - races are placeholders until candidates declare")
