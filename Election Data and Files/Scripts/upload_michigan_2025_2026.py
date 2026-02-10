import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

races = [
    {
        "race_id": "MI-SEN-2026",
        "state": "Michigan",
        "race_type": "Senate",
        "office": "U.S. Senator",
        "district": "Statewide",
        "election_date": "2026-11-03",
        "incumbent": "Debbie Stabenow (D) - RETIRING",
        "status": "Open Seat - TOP PICKUP OPPORTUNITY",
        "importance": "CRITICAL - Senate control, open seat, swing state",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-GOV-2026",
        "state": "Michigan",
        "race_type": "Statewide",
        "office": "Governor",
        "district": "Statewide",
        "election_date": "2026-11-03",
        "incumbent": "Gretchen Whitmer (D) - TERM LIMITED",
        "status": "Open Seat - Major Opportunity",
        "importance": "CRITICAL - State control, open seat",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-AG-2026",
        "state": "Michigan",
        "race_type": "Statewide",
        "office": "Attorney General",
        "district": "Statewide",
        "election_date": "2026-11-03",
        "incumbent": "Dana Nessel (D)",
        "status": "Competitive",
        "importance": "High - Election integrity, religious liberty",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-SOS-2026",
        "state": "Michigan",
        "race_type": "Statewide",
        "office": "Secretary of State",
        "district": "Statewide",
        "election_date": "2026-11-03",
        "incumbent": "Jocelyn Benson (D)",
        "status": "Competitive",
        "importance": "High - Election integrity",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-01-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "1",
        "election_date": "2026-11-03",
        "incumbent": "Jack Bergman (R)",
        "status": "Safe Republican",
        "importance": "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-02-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "2",
        "election_date": "2026-11-03",
        "incumbent": "John Moolenaar (R)",
        "status": "Safe Republican",
        "importance": "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-03-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "3",
        "election_date": "2026-11-03",
        "incumbent": "Hillary Scholten (D)",
        "status": "Competitive - Pickup Opportunity",
        "importance": "High - Flip opportunity",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-04-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "4",
        "election_date": "2026-11-03",
        "incumbent": "Bill Huizenga (R)",
        "status": "Safe Republican",
        "importance": "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-05-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "5",
        "election_date": "2026-11-03",
        "incumbent": "Tim Walberg (R)",
        "status": "Safe Republican",
        "importance": "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-06-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "6",
        "election_date": "2026-11-03",
        "incumbent": "Debbie Dingell (D)",
        "status": "Safe Democrat",
        "importance": "Monitor",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-07-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "7",
        "election_date": "2026-11-03",
        "incumbent": "Elissa Slotkin (D) - RUNNING FOR SENATE",
        "status": "Open Seat - TOP PICKUP OPPORTUNITY",
        "importance": "CRITICAL - Flip opportunity",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-08-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "8",
        "election_date": "2026-11-03",
        "incumbent": "Dan Kildee (D) - RETIRING",
        "status": "Open Seat - Pickup Opportunity",
        "importance": "High - Flip opportunity",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-09-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "9",
        "election_date": "2026-11-03",
        "incumbent": "Lisa McClain (R)",
        "status": "Safe Republican",
        "importance": "Hold",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-10-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "10",
        "election_date": "2026-11-03",
        "incumbent": "John James (R)",
        "status": "Competitive - Must Hold",
        "importance": "High - Defend seat",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-11-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "11",
        "election_date": "2026-11-03",
        "incumbent": "Haley Stevens (D)",
        "status": "Competitive - Pickup Opportunity",
        "importance": "High - Flip opportunity",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-12-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "12",
        "election_date": "2026-11-03",
        "incumbent": "Rashida Tlaib (D)",
        "status": "Safe Democrat",
        "importance": "Monitor",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "race_id": "MI-13-2026",
        "state": "Michigan",
        "race_type": "House",
        "office": "U.S. Representative",
        "district": "13",
        "election_date": "2026-11-03",
        "incumbent": "Shri Thanedar (D)",
        "status": "Safe Democrat",
        "importance": "Monitor",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

candidates = [
    {
        "candidate_id": "elissa-slotkin-mi-sen-2026",
        "name": "Elissa Slotkin",
        "race_id": "MI-SEN-2026",
        "state": "Michigan",
        "party": "Democrat",
        "incumbent": False,
        "office_sought": "U.S. Senator",
        "background": "U.S. Representative MI-7, former CIA analyst, national security background",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice, supports teachers unions",
            "religious_freedom": "Weak record on religious liberty",
            "guns": "Gun control advocate, F-rating from NRA",
            "immigration": "Supports pathway to citizenship, weak border",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["EMILY's List", "Planned Parenthood", "Progressive groups"],
        "website": "elissaslotkin.com",
        "christian_conservative_rating": "FAILS - Liberal voting record",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "candidate_id": "mike-rogers-mi-sen-2026",
        "name": "Mike Rogers",
        "race_id": "MI-SEN-2026",
        "state": "Michigan",
        "party": "Republican",
        "incumbent": False,
        "office_sought": "U.S. Senator",
        "background": "Former U.S. Representative, House Intelligence Committee Chairman, FBI agent, proven conservative leader",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment defender",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["Michigan Right to Life (expected)", "NRA (expected)", "Michigan GOP"],
        "website": "mikerogers.com",
        "christian_conservative_rating": "STRONG - Proven conservative record",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "candidate_id": "tudor-dixon-mi-gov-2026",
        "name": "Tudor Dixon",
        "race_id": "MI-GOV-2026",
        "state": "Michigan",
        "party": "Republican",
        "incumbent": False,
        "office_sought": "Governor",
        "background": "2022 GOP nominee, businesswoman, conservative media host, strong Christian conservative",
        "positions": {
            "abortion": "100% pro-life, no exceptions",
            "education": "School choice champion, parental rights warrior",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment absolutist",
            "immigration": "Secure border, oppose sanctuary cities",
            "economy": "Lower taxes, cut regulations"
        },
        "endorsements": ["Michigan Right to Life", "NRA", "President Trump (2022)", "Conservative groups"],
        "website": "tudordixon.com",
        "christian_conservative_rating": "EXCELLENT - Strong biblical values",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    {
        "candidate_id": "tom-barrett-mi-07-2026",
        "name": "Tom Barrett",
        "race_id": "MI-07-2026",
        "state": "Michigan",
        "party": "Republican",
        "incumbent": False,
        "office_sought": "U.S. Representative",
        "background": "Michigan State Senator, Army veteran, Iraq War combat veteran, conservative leader",
        "positions": {
            "abortion": "Pro-life - protect unborn life",
            "education": "School choice, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, support manufacturing"
        },
        "endorsements": ["Michigan GOP", "Veterans groups", "Conservative organizations"],
        "website": "barrettformichigan.com",
        "christian_conservative_rating": "STRONG - Conservative record",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
]

print("Uploading Michigan races...")
for race in races:
    races_table.put_item(Item=race)
    print(f"+ {race['race_id']}")

print(f"\nSuccessfully uploaded {len(races)} Michigan races")

print("\nUploading Michigan candidates...")
for candidate in candidates:
    candidates_table.put_item(Item=candidate)
    print(f"+ {candidate['name']} - {candidate['party']}")

print(f"\nSuccessfully uploaded {len(candidates)} Michigan candidates")
print("\nMichigan 2025-2026 races and candidates uploaded successfully!")
