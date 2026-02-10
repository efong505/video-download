import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

# Delete the duplicate Mayor race and wrong House race
races_table.delete_item(Key={'race_id': '4029a7c5-32fa-4fe5-a037-e6e3502497b9'})
print("Deleted duplicate Mayor race")

# Add missing House districts (1-10, 12-13)
house_races = [
    {"race_id": "MI-01-2026", "district": "1", "status": "Safe Republican"},
    {"race_id": "MI-02-2026", "district": "2", "status": "Safe Republican"},
    {"race_id": "MI-03-2026", "district": "3", "status": "Competitive - Pickup Opportunity"},
    {"race_id": "MI-04-2026", "district": "4", "status": "Safe Republican"},
    {"race_id": "MI-05-2026", "district": "5", "status": "Safe Republican"},
    {"race_id": "MI-06-2026", "district": "6", "status": "Safe Democrat"},
    {"race_id": "MI-07-2026", "district": "7", "status": "Open Seat - TOP PICKUP OPPORTUNITY"},
    {"race_id": "MI-08-2026", "district": "8", "status": "Open Seat - Pickup Opportunity"},
    {"race_id": "MI-09-2026", "district": "9", "status": "Safe Republican"},
    {"race_id": "MI-10-2026", "district": "10", "status": "Competitive - Must Hold"},
    {"race_id": "MI-12-2026", "district": "12", "status": "Safe Democrat"},
    {"race_id": "MI-13-2026", "district": "13", "status": "Safe Democrat"}
]

for race in house_races:
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": race["district"],
        "election_date": "2026-11-03",
        "status": race["status"],
        "importance": "High - Flip opportunity" if "Pickup" in race["status"] else "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    print(f"+ MI-{race['district']}-2026")

print(f"\nMichigan House races restored: 12 districts")
print("Total Michigan races should now be: 17 (1 Senate + 4 Statewide + 12 House)")
