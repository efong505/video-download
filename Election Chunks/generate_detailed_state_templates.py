"""
Generate detailed state-specific templates with actual race breakdowns.

This replaces generic templates with specific race counts and examples
based on each state's actual congressional districts and elections.
"""

STATE_INFO = {
    "Alabama": {
        "districts": 7,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 105,
        "senate_districts": 35,
        "major_cities": ["Huntsville", "Birmingham", "Montgomery", "Mobile", "Tuscaloosa"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Alaska": {
        "districts": 1,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 40,
        "senate_districts": 20,
        "major_cities": ["Anchorage", "Fairbanks", "Juneau", "Wasilla", "Sitka"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Arizona": {
        "districts": 9,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 30,  # 30 districts, 2 seats each
        "senate_districts": 30,
        "major_cities": ["Phoenix", "Tucson", "Mesa", "Chandler", "Gilbert"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Arkansas": {
        "districts": 4,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 100,
        "senate_districts": 35,
        "major_cities": ["Little Rock", "Fayetteville", "Fort Smith", "Springdale", "Jonesboro"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "California": {
        "districts": 52,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 80,
        "senate_districts": 40,
        "major_cities": ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Colorado": {
        "districts": 8,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 65,
        "senate_districts": 35,
        "major_cities": ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Connecticut": {
        "districts": 5,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 151,
        "senate_districts": 36,
        "major_cities": ["Bridgeport", "Stamford", "New Haven", "Hartford", "Waterbury"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Delaware": {
        "districts": 1,
        "senate_year": 2026,
        "gov_year": None,
        "assembly_districts": 41,
        "senate_districts": 21,
        "major_cities": ["Wilmington", "Dover", "Newark", "Middletown", "Milford"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Florida": {
        "districts": 28,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 120,
        "senate_districts": 40,
        "major_cities": ["Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Georgia": {
        "districts": 14,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 180,
        "senate_districts": 56,
        "major_cities": ["Atlanta", "Columbus", "Augusta", "Macon", "Savannah"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Hawaii": {
        "districts": 2,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 51,
        "senate_districts": 25,
        "major_cities": ["Honolulu", "East Honolulu", "Pearl City", "Hilo", "Waipahu"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Idaho": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 35,  # 35 districts, 2 seats each
        "senate_districts": 35,
        "major_cities": ["Boise", "Meridian", "Nampa", "Caldwell", "Idaho Falls"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Illinois": {
        "districts": 17,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 118,
        "senate_districts": 59,
        "major_cities": ["Chicago", "Aurora", "Joliet", "Naperville", "Rockford"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Indiana": {
        "districts": 9,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 100,
        "senate_districts": 50,
        "major_cities": ["Indianapolis", "Fort Wayne", "Evansville", "Fishers", "South Bend"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Iowa": {
        "districts": 4,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 100,
        "senate_districts": 50,
        "major_cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Kansas": {
        "districts": 4,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 125,
        "senate_districts": 40,
        "major_cities": ["Wichita", "Overland Park", "Kansas City", "Olathe", "Topeka"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Kentucky": {
        "districts": 6,
        "senate_year": 2026,
        "gov_year": 2027,
        "assembly_districts": 100,
        "senate_districts": 38,
        "major_cities": ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Louisiana": {
        "districts": 6,
        "senate_year": 2026,
        "gov_year": 2027,
        "assembly_districts": 105,
        "senate_districts": 39,
        "major_cities": ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Maine": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 151,
        "senate_districts": 35,
        "major_cities": ["Portland", "Lewiston", "Bangor", "South Portland", "Auburn"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Maryland": {
        "districts": 8,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 141,
        "senate_districts": 47,
        "major_cities": ["Baltimore", "Frederick", "Gaithersburg", "Rockville", "Bowie"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Massachusetts": {
        "districts": 9,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 160,
        "senate_districts": 40,
        "major_cities": ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Michigan": {
        "districts": 13,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 110,
        "senate_districts": 38,
        "major_cities": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Minnesota": {
        "districts": 8,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 134,
        "senate_districts": 67,
        "major_cities": ["Minneapolis", "Saint Paul", "Rochester", "Duluth", "Bloomington"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Mississippi": {
        "districts": 4,
        "senate_year": 2026,
        "gov_year": 2027,
        "assembly_districts": 122,
        "senate_districts": 52,
        "major_cities": ["Jackson", "Gulfport", "Southaven", "Hattiesburg", "Biloxi"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Missouri": {
        "districts": 8,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 163,
        "senate_districts": 34,
        "major_cities": ["Kansas City", "Saint Louis", "Springfield", "Columbia", "Independence"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Montana": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": None,
        "assembly_districts": 100,
        "senate_districts": 50,
        "major_cities": ["Billings", "Missoula", "Great Falls", "Bozeman", "Butte"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Nebraska": {
        "districts": 3,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 0,  # Unicameral
        "senate_districts": 49,
        "major_cities": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Nevada": {
        "districts": 4,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 42,
        "senate_districts": 21,
        "major_cities": ["Las Vegas", "Henderson", "North Las Vegas", "Reno", "Sparks"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "New Hampshire": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 400,
        "senate_districts": 24,
        "major_cities": ["Manchester", "Nashua", "Concord", "Rochester", "Dover"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "New Jersey": {
        "districts": 12,
        "senate_year": 2026,
        "gov_year": 2025,
        "assembly_districts": 40,  # As per example
        "senate_districts": 40,
        "major_cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Trenton"],
        "school_board_seats": 22,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 9
    },
    "New Mexico": {
        "districts": 3,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 70,
        "senate_districts": 42,
        "major_cities": ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "New York": {
        "districts": 26,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 150,
        "senate_districts": 63,
        "major_cities": ["New York", "Buffalo", "Yonkers", "Rochester", "Syracuse"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "North Carolina": {
        "districts": 14,
        "senate_year": 2026,
        "gov_year": None,
        "assembly_districts": 120,
        "senate_districts": 50,
        "major_cities": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "North Dakota": {
        "districts": 1,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 94,
        "senate_districts": 47,
        "major_cities": ["Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Ohio": {
        "districts": 15,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 99,
        "senate_districts": 33,
        "major_cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Oklahoma": {
        "districts": 5,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 101,
        "senate_districts": 48,
        "major_cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Edmond"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Oregon": {
        "districts": 6,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 60,
        "senate_districts": 30,
        "major_cities": ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Pennsylvania": {
        "districts": 17,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 203,
        "senate_districts": 50,
        "major_cities": ["Philadelphia", "Pittsburgh", "Allentown", "Reading", "Erie"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Rhode Island": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 75,
        "senate_districts": 38,
        "major_cities": ["Providence", "Warwick", "Cranston", "Pawtucket", "East Providence"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "South Carolina": {
        "districts": 7,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 124,
        "senate_districts": 46,
        "major_cities": ["Charleston", "Columbia", "North Charleston", "Mount Pleasant", "Rock Hill"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "South Dakota": {
        "districts": 1,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 35,  # 35 districts, 2 seats each
        "senate_districts": 35,
        "major_cities": ["Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Tennessee": {
        "districts": 9,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 99,
        "senate_districts": 33,
        "major_cities": ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Texas": {
        "districts": 38,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 150,
        "senate_districts": 31,
        "major_cities": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Utah": {
        "districts": 4,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 75,
        "senate_districts": 29,
        "major_cities": ["Salt Lake City", "West Valley City", "West Jordan", "Provo", "St. George"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Vermont": {
        "districts": 1,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 150,
        "senate_districts": 30,
        "major_cities": ["Burlington", "South Burlington", "Rutland", "Essex Junction", "Barre"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Virginia": {
        "districts": 11,
        "senate_year": None,
        "gov_year": 2025,
        "assembly_districts": 100,
        "senate_districts": 40,
        "major_cities": ["Virginia Beach", "Chesapeake", "Norfolk", "Richmond", "Newport News"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Washington": {
        "districts": 10,
        "senate_year": None,
        "gov_year": None,
        "assembly_districts": 98,
        "senate_districts": 49,
        "major_cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "West Virginia": {
        "districts": 2,
        "senate_year": 2026,
        "gov_year": None,
        "assembly_districts": 100,
        "senate_districts": 34,
        "major_cities": ["Charleston", "Huntington", "Morgantown", "Parkersburg", "Wheeling"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Wisconsin": {
        "districts": 8,
        "senate_year": None,
        "gov_year": 2026,
        "assembly_districts": 99,
        "senate_districts": 33,
        "major_cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    },
    "Wyoming": {
        "districts": 1,
        "senate_year": 2026,
        "gov_year": 2026,
        "assembly_districts": 62,
        "senate_districts": 31,
        "major_cities": ["Cheyenne", "Casper", "Gillette", "Laramie", "Rock Springs"],
        "school_board_seats": 25,
        "city_council_seats": 35,
        "mayoral_races": 3,
        "county_races": 10
    }
}

import os

def generate_chunk1_detailed(state, info):
    """Generate CHUNK_1 with actual race breakdown"""
    
    districts = info['districts']
    senate_year = info['senate_year']
    gov_year = info['gov_year']
    assembly = info['assembly_districts']
    senate_districts = info['senate_districts']
    school_boards = info.get('school_board_seats', 15)
    city_councils = info.get('city_council_seats', 20)
    mayors = info.get('mayoral_races', 3)
    county = info.get('county_races', 10)
    
    # Calculate race counts
    federal_races = (1 if senate_year else 0) + districts
    state_races = 2 if gov_year in [2025, 2026, 2027] else 0
    legislature_races = assembly + senate_districts if gov_year in [2025, 2026, 2027] else 0
    municipal_races = school_boards + city_councils + mayors + county
    
    total_races = federal_races + state_races + legislature_races + municipal_races
    
    template = f"""# CHUNK 1: {state.upper()} RACES ARRAY ONLY

## TASK: Provide ONLY the races array for {state} 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY {total_races} races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, {state}.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal ({senate_year or 2026}) - {federal_races} races
"""
    
    if senate_year:
        template += f"1. U.S. Senate\n"
        template += f"2-{federal_races}. U.S. House Districts 1-{districts} (ALL {districts})\n\n"
    else:
        template += f"1-{federal_races}. U.S. House Districts 1-{districts} (ALL {districts})\n\n"
    
    if state_races > 0:
        template += f"""### State ({gov_year}) - {state_races} races
Governor, Lieutenant Governor

"""
    
    if legislature_races > 0:
        template += f"""### State Legislature ({gov_year}) - {legislature_races} races
- House/Assembly: {assembly} seats (Districts 1-{assembly})
- Senate: {senate_districts} seats (Districts 1-{senate_districts})

"""
    
    template += f"""### Municipal & County (2025-2026) - {municipal_races} races
- School Boards: {school_boards} seats across major cities
- City Councils: {city_councils} seats across major cities
- Mayoral Races: {mayors} races
- County Positions: {county} races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {{
        "state": "{state}",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "{senate_year or 2026}-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and {state}.gov..."
    }},
    # CONTINUE FOR ALL {total_races} RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: {total_races}
- Federal: {federal_races}
- State: {state_races}
- Legislature: {legislature_races}
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
"""
    
    return template

def get_state_size(districts):
    """Determine state size based on congressional districts"""
    if districts >= 20:
        return "Large", 25, 200
    elif districts >= 10:
        return "Medium", 15, 150
    else:
        return "Small", 5, 100

def generate_candidate_chunks(state, num_chunks, max_candidates):
    """Generate candidate chunk templates"""
    chunks = []
    candidates_per_chunk = max_candidates // num_chunks
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(num_chunks):
        letter = letters[i]
        chunk_num = i + 1
        
        template = f"""# CHUNK 2{letter.upper()}: {state.upper()} CANDIDATES (Part {chunk_num}/{num_chunks})

## TASK: Provide UP TO {candidates_per_chunk} candidates for {state}

**CRITICAL**: Only include candidates who have PUBLICLY DECLARED for 2025-2026 races.

**DO NOT:**
- ❌ Invent fake candidates
- ❌ Include candidates from previous elections unless they've declared for 2025-2026
- ❌ Duplicate candidates from other chunks

**DO:**
- ✅ Research actual declared candidates from Ballotpedia, campaign websites, news sources
- ✅ Include complete bio, positions, endorsements
- ✅ Include race_id linking to races from CHUNK_1
- ✅ Verify all information is accurate and sourced

## FORMAT:

```python
candidates = [
    {{
        "state": "{state}",
        "office": "U.S. Senate",
        "name": "Candidate Name",
        "party": "Republican",
        "bio": "Detailed bio...",
        "positions": {{
            "abortion": "Position...",
            "immigration": "Position...",
            "economy": "Position..."
        }},
        "endorsements": ["Organization 1", "Organization 2"],
        "website": "https://...",
        "faith_statement": "Statement..."
    }},
    # UP TO {candidates_per_chunk} candidates
]
```

**START OUTPUT NOW - CANDIDATES ARRAY ONLY**
"""
        chunks.append((f"CHUNK_2{letter.upper()}_CANDIDATES.md", template))
    
    return chunks

# Generate for all states
output_dir = "COMPLETE_STATE_TEMPLATES"
for state, info in STATE_INFO.items():
    state_dir = os.path.join(output_dir, state.replace(" ", "_"))
    os.makedirs(state_dir, exist_ok=True)
    
    # Generate CHUNK_1 (races)
    chunk1_content = generate_chunk1_detailed(state, info)
    with open(os.path.join(state_dir, "CHUNK_1_RACES.md"), 'w', encoding='utf-8') as f:
        f.write(chunk1_content)
    
    # Generate candidate chunks based on state size
    size_name, num_chunks, max_candidates = get_state_size(info['districts'])
    candidate_chunks = generate_candidate_chunks(state, num_chunks, max_candidates)
    
    for filename, content in candidate_chunks:
        with open(os.path.join(state_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Generated {state} ({size_name}): 1 race file + {num_chunks} candidate files")

print(f"\nGenerated detailed templates for all 50 states with state-size-based candidate chunks")
