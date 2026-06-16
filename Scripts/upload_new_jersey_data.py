import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# New Jersey Races
races = [
    # FEDERAL RACES - 2026
    {
        "state": "New Jersey",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Critical Senate race - Cory Booker (D) seeking re-election"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "South Jersey district - Donald Norcross (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive South Jersey district - Jeff Van Drew (R) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Jersey swing district - Herb Conaway (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Jersey district - Chris Smith (R) long-time incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Northern NJ competitive district - Josh Gottheimer (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Jersey district - Frank Pallone (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive suburban district - Tom Kean Jr. (R) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban district covering parts of Essex and Hudson counties - Rob Menendez (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban district - Bill Pascrell Jr. (D) or successor"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 10",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban district including Newark - LaMonica McIver (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 11",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Suburban district - Mikie Sherrill (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 12",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Jersey district - Bonnie Watson Coleman (D) incumbent"
    },
    
    # STATE LEGISLATURE - 2025
    {
        "state": "New Jersey",
        "office": "State Senate District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "South Jersey district - all 40 Senate seats up in 2025"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Atlantic County district"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Cumberland, Gloucester, Salem counties"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 8",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Burlington and Camden counties"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 11",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Monmouth County competitive district"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 16",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Hunterdon, Mercer, Middlesex, Somerset counties"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 21",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Union County district"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 24",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Morris, Sussex, Warren counties"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 25",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Morris County"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 26",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Morris, Passaic, Sussex counties"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 30",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Monmouth County"
    },
    {
        "state": "New Jersey",
        "office": "State Senate District 38",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Bergen County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - South Jersey"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Atlantic County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Cumberland, Gloucester, Salem"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 8",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Burlington and Camden"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 11",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Monmouth County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 16",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Central Jersey"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 21",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Union County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 24",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Morris, Sussex, Warren"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 25",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Morris County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 26",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Morris, Passaic, Sussex"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 30",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Monmouth County"
    },
    {
        "state": "New Jersey",
        "office": "State Assembly District 38",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Two seats - Bergen County"
    },
    
    # SCHOOL BOARD RACES - 2025 (CRITICAL)
    {
        "state": "New Jersey",
        "office": "Newark Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Critical race for parental rights in NJ's largest school district"
    },
    {
        "state": "New Jersey",
        "office": "Newark Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Newark school board control - curriculum and policy decisions"
    },
    {
        "state": "New Jersey",
        "office": "Newark Board of Education At-Large Seat 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Newark school board seat - education policy direction"
    },
    {
        "state": "New Jersey",
        "office": "Jersey City Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Jersey City schools - parental rights and curriculum control"
    },
    {
        "state": "New Jersey",
        "office": "Jersey City Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Jersey City school board - education policy"
    },
    {
        "state": "New Jersey",
        "office": "Jersey City Board of Education At-Large Seat 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Jersey City school board control"
    },
    {
        "state": "New Jersey",
        "office": "Paterson Board of Education District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Paterson schools - critical for education reform"
    },
    {
        "state": "New Jersey",
        "office": "Paterson Board of Education District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Paterson school board seat"
    },
    {
        "state": "New Jersey",
        "office": "Paterson Board of Education District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Paterson school board - parental rights focus"
    },
    {
        "state": "New Jersey",
        "office": "Elizabeth Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Elizabeth schools - curriculum and policy control"
    },
    {
        "state": "New Jersey",
        "office": "Elizabeth Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Elizabeth school board seat"
    },
    {
        "state": "New Jersey",
        "office": "Edison Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Edison schools - suburban district with parental engagement"
    },
    {
        "state": "New Jersey",
        "office": "Edison Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Edison school board - education policy"
    },
    {
        "state": "New Jersey",
        "office": "Woodbridge Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Woodbridge schools - parental rights and curriculum"
    },
    {
        "state": "New Jersey",
        "office": "Woodbridge Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Woodbridge school board control"
    },
    {
        "state": "New Jersey",
        "office": "Camden Board of Education District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Camden schools - education reform critical"
    },
    {
        "state": "New Jersey",
        "office": "Camden Board of Education District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Camden school board seat"
    },
    {
        "state": "New Jersey",
        "office": "Trenton Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "State capital schools - education policy direction"
    },
    {
        "state": "New Jersey",
        "office": "Trenton Board of Education At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Trenton school board control"
    },
    {
        "state": "New Jersey",
        "office": "Clifton Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Clifton schools - parental rights focus"
    },
    {
        "state": "New Jersey",
        "office": "Passaic Board of Education District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Passaic schools - curriculum control"
    },
    {
        "state": "New Jersey",
        "office": "Union City Board of Education At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Union City schools - education policy"
    },
    
    # MUNICIPAL RACES - 2025
    {
        "state": "New Jersey",
        "office": "Newark Mayor",
        "election_date": "2025-05-13",
        "race_type": "general",
        "description": "NJ's largest city - Ras Baraka seeking re-election"
    },
    {
        "state": "New Jersey",
        "office": "Jersey City Mayor",
        "election_date": "2025-05-13",
        "race_type": "general",
        "description": "Major city mayoral race - Steven Fulop term-limited"
    },
    {
        "state": "New Jersey",
        "office": "Paterson Mayor",
        "election_date": "2025-05-13",
        "race_type": "general",
        "description": "Third largest city in NJ"
    },
    {
        "state": "New Jersey",
        "office": "Elizabeth Mayor",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Major Union County city"
    },
    {
        "state": "New Jersey",
        "office": "Trenton Mayor",
        "election_date": "2025-05-13",
        "race_type": "general",
        "description": "State capital mayoral race"
    },
    {
        "state": "New Jersey",
        "office": "Camden Mayor",
        "election_date": "2025-05-13",
        "race_type": "general",
        "description": "South Jersey major city"
    },
    
    # COUNTY RACES - 2025
    {
        "state": "New Jersey",
        "office": "Bergen County Executive",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "NJ's most populous county - James Tedesco (D) incumbent"
    },
    {
        "state": "New Jersey",
        "office": "Essex County Executive",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Major urban county including Newark"
    },
    {
        "state": "New Jersey",
        "office": "Hudson County Executive",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Urban county including Jersey City"
    },
    {
        "state": "New Jersey",
        "office": "Middlesex County Freeholder District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Central Jersey county board"
    },
    {
        "state": "New Jersey",
        "office": "Monmouth County Freeholder At-Large",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Competitive suburban county"
    },
    {
        "state": "New Jersey",
        "office": "Morris County Freeholder At-Large",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Republican-leaning suburban county"
    },
    {
        "state": "New Jersey",
        "office": "Ocean County Freeholder At-Large",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Conservative Shore county"
    },
    {
        "state": "New Jersey",
        "office": "Passaic County Freeholder District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Northern NJ county board"
    },
    {
        "state": "New Jersey",
        "office": "Union County Freeholder At-Large",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Central NJ county board"
    },
    {
        "state": "New Jersey",
        "office": "Atlantic County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Law enforcement leadership - Shore county"
    },
    {
        "state": "New Jersey",
        "office": "Burlington County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Law enforcement leadership"
    },
    {
        "state": "New Jersey",
        "office": "Camden County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "South Jersey law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Cape May County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Shore county law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Cumberland County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "South Jersey law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Gloucester County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "South Jersey law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Hunterdon County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Rural county law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Mercer County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "State capital county law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Salem County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "South Jersey law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Somerset County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Central Jersey law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Sussex County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Rural northern county law enforcement"
    },
    {
        "state": "New Jersey",
        "office": "Warren County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Rural western county law enforcement"
    },
]

# New Jersey Candidates
candidates = [
    # U.S. SENATE
    {
        "state": "New Jersey",
        "office": "U.S. Senate",
        "name": "Cory Booker",
        "party": "Democrat",
        "incumbent": True,
        "bio": "Incumbent Senator since 2013, former Newark Mayor",
        "positions": "Progressive Democrat, supports abortion rights, LGBTQ+ agenda, gun control",
        "faith_statement": "Baptist background, progressive social positions conflict with traditional Christian values",
        "website": "https://www.corybooker.com",
        "endorsements": "Democratic establishment, progressive groups",
        "priority": "high"
    },
    {
        "state": "New Jersey",
        "office": "U.S. Senate",
        "name": "Republican Challenger TBD",
        "party": "Republican",
        "incumbent": False,
        "bio": "Republican primary to determine nominee",
        "positions": "Conservative alternative needed for NJ",
        "faith_statement": "To be determined based on primary winner",
        "website": "",
        "endorsements": "TBD",
        "priority": "high"
    },
    
    # U.S. HOUSE DISTRICT 2
    {
        "state": "New Jersey",
        "office": "U.S. House District 2",
        "name": "Jeff Van Drew",
        "party": "Republican",
        "incumbent": True,
        "bio": "Former Democrat who switched parties in 2019, dentist, strong Trump supporter",
        "positions": "Pro-life, supports religious liberty, opposes radical gender ideology, strong on border security",
        "faith_statement": "Catholic, traditional values, defender of faith and family",
        "website": "https://www.vandrew.house.gov",
        "endorsements": "Republican Party, pro-life groups, conservative organizations",
        "priority": "high"
    },
    
    # U.S. HOUSE DISTRICT 4
    {
        "state": "New Jersey",
        "office": "U.S. House District 4",
        "name": "Chris Smith",
        "party": "Republican",
        "incumbent": True,
        "bio": "Serving since 1981, leading pro-life advocate in Congress, human rights champion",
        "positions": "Strongly pro-life, religious liberty defender, fights human trafficking, traditional marriage supporter",
        "faith_statement": "Catholic, deeply committed to sanctity of life, faith-driven public service",
        "website": "https://www.chrissmith.house.gov",
        "endorsements": "National Right to Life, pro-life organizations, Catholic groups",
        "priority": "high"
    },
    
    # U.S. HOUSE DISTRICT 7
    {
        "state": "New Jersey",
        "office": "U.S. House District 7",
        "name": "Tom Kean Jr.",
        "party": "Republican",
        "incumbent": True,
        "bio": "Son of former Governor, former State Senate Minority Leader, elected 2022",
        "positions": "Moderate Republican, pro-business, supports some conservative social positions",
        "faith_statement": "Christian background, more moderate on social issues",
        "website": "https://www.kean.house.gov",
        "endorsements": "Republican Party, business groups",
        "priority": "medium"
    },
    
    # NEWARK MAYOR
    {
        "state": "New Jersey",
        "office": "Newark Mayor",
        "name": "Ras Baraka",
        "party": "Democrat",
        "incumbent": True,
        "bio": "Incumbent mayor since 2014, former principal and city councilman",
        "positions": "Progressive Democrat, supports abortion rights, LGBTQ+ agenda",
        "faith_statement": "Limited public faith statements, progressive social positions",
        "website": "https://www.rasbaraka.com",
        "endorsements": "Democratic establishment, progressive groups",
        "priority": "medium"
    },
    
    # JERSEY CITY MAYOR
    {
        "state": "New Jersey",
        "office": "Jersey City Mayor",
        "name": "Steven Fulop",
        "party": "Democrat",
        "incumbent": True,
        "bio": "Current mayor term-limited, multiple candidates expected",
        "positions": "Progressive Democrat, supports abortion rights and LGBTQ+ policies",
        "faith_statement": "Jewish background, progressive social positions",
        "website": "",
        "endorsements": "Democratic establishment",
        "priority": "medium"
    },
    
    # SCHOOL BOARD CANDIDATES (Sample - more to be added)
    {
        "state": "New Jersey",
        "office": "Newark Board of Education At-Large Seat 1",
        "name": "Candidate TBD",
        "party": "Nonpartisan",
        "incumbent": False,
        "bio": "School board elections are nonpartisan - research local candidates",
        "positions": "Focus on parental rights, curriculum transparency, academic excellence",
        "faith_statement": "Research individual candidates' values and positions",
        "website": "",
        "endorsements": "TBD",
        "priority": "high"
    },
    {
        "state": "New Jersey",
        "office": "Jersey City Board of Education At-Large Seat 1",
        "name": "Candidate TBD",
        "party": "Nonpartisan",
        "incumbent": False,
        "bio": "School board elections are nonpartisan - research local candidates",
        "positions": "Focus on parental rights, curriculum transparency, academic excellence",
        "faith_statement": "Research individual candidates' values and positions",
        "website": "",
        "endorsements": "TBD",
        "priority": "high"
    },
    {
        "state": "New Jersey",
        "office": "Edison Board of Education At-Large Seat 1",
        "name": "Candidate TBD",
        "party": "Nonpartisan",
        "incumbent": False,
        "bio": "School board elections are nonpartisan - research local candidates",
        "positions": "Focus on parental rights, curriculum transparency, academic excellence",
        "faith_statement": "Research individual candidates' values and positions",
        "website": "",
        "endorsements": "TBD",
        "priority": "high"
    },
    
    # BERGEN COUNTY EXECUTIVE
    {
        "state": "New Jersey",
        "office": "Bergen County Executive",
        "name": "James Tedesco",
        "party": "Democrat",
        "incumbent": True,
        "bio": "County Executive since 2015, former Paramus Mayor",
        "positions": "Moderate Democrat, focuses on county services and infrastructure",
        "faith_statement": "Catholic background, limited public faith statements",
        "website": "",
        "endorsements": "Democratic Party",
        "priority": "medium"
    },
]

# New Jersey Summary
summary = {
    "state": "New Jersey",
    "title": "New Jersey 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# New Jersey 2025-2026 Elections: Christian Conservative Voter Guide

## Executive Summary

New Jersey faces critical elections in both 2025 and 2026 that will shape the state's direction on life, family, religious liberty, and education. While New Jersey leans heavily Democratic, Christian conservatives have opportunities to make their voices heard, especially in school board races, local elections, and competitive legislative districts.

**Key Dates:**
- May 13, 2025: Municipal elections (Newark, Jersey City, Paterson, Trenton, Camden)
- November 4, 2025: General election (State Legislature, school boards, county offices)
- November 3, 2026: Federal midterm elections (U.S. Senate, all 12 House seats)

**Priority Races for Christian Conservatives:**
1. School board elections across all major cities (2025)
2. U.S. Senate race - Cory Booker vs. Republican challenger (2026)
3. U.S. House Districts 2, 4, 7 - defending pro-life champions (2026)
4. State Legislature - all 40 Senate seats and 80 Assembly seats (2025)
5. County sheriff races - law enforcement leadership (2025)

## Why New Jersey Matters

New Jersey is the most densely populated state in America with 9.3 million residents. Despite its blue-state reputation, New Jersey has:
- Strong Catholic and evangelical communities
- Growing Hispanic evangelical population
- Orthodox Jewish communities aligned on life and family issues
- Suburban parents concerned about education and parental rights
- Pro-life pregnancy centers serving thousands

**The Stakes:**
- Abortion: NJ has some of the most extreme abortion laws in America (up to birth)
- Education: Gender ideology and critical race theory in schools
- Religious Liberty: Threats to faith-based adoption agencies and healthcare workers
- Parental Rights: School boards hiding information from parents
- Life Issues: Assisted suicide legalized, euthanasia expansion proposed

## 2026 Federal Races

### U.S. Senate: Cory Booker (D) vs. Republican Challenger

**The Race:**
Senator Cory Booker seeks his third full term. First elected in 2013 special election, Booker is a progressive Democrat with national ambitions. While NJ hasn't elected a Republican senator since 1972, recent trends show opportunities.

**Cory Booker's Record:**
- **Abortion:** 100% NARAL rating, voted against Born-Alive Abortion Survivors Protection Act
- **Religious Liberty:** Opposed religious exemptions, hostile to faith-based organizations
- **Marriage/Family:** Supports redefinition of marriage, LGBTQ+ agenda in schools
- **Parental Rights:** Opposes parental notification, supports gender ideology for minors
- **Life Issues:** Supports taxpayer-funded abortion, opposed Hyde Amendment
- **Judicial Nominees:** Voted for radical pro-abortion judges

**Faith Perspective:**
Booker claims Baptist background but his voting record consistently opposes biblical values on life, marriage, and religious freedom. He has been hostile to Christian judicial nominees, questioning their faith commitments.

**Republican Opportunity:**
The right Republican candidate could make this competitive by focusing on:
- Parental rights and education
- Rising cost of living and taxes
- Crime and public safety
- Suburban swing voters
- Hispanic evangelical outreach

**Christian Conservative Action:**
- Pray for a strong Republican nominee who shares our values
- Register voters in churches and faith communities
- Educate voters on Booker's extreme record
- Mobilize in competitive counties: Monmouth, Ocean, Morris, Somerset

### U.S. House of Representatives - All 12 Districts

New Jersey's congressional delegation is currently 9 Democrats and 3 Republicans. Christian conservatives must defend our champions and target competitive seats.

#### DISTRICT 2 - Jeff Van Drew (R) - MUST DEFEND

**The District:** South Jersey - Atlantic, Cape May, Cumberland, Salem counties, parts of Gloucester and Ocean

**Incumbent:** Jeff Van Drew switched from Democrat to Republican in 2019 over impeachment. He's been a reliable conservative vote.

**Van Drew's Record:**
- **Pro-Life Champion:** 100% National Right to Life rating
- **Religious Liberty:** Defender of faith-based organizations
- **Parental Rights:** Opposes gender ideology in schools
- **Border Security:** Strong supporter of border enforcement
- **Traditional Values:** Supports traditional marriage and family

**Why This Matters:**
Van Drew is one of only 3 Republicans in NJ's delegation. Losing this seat would be devastating. Democrats will target heavily.

**Christian Conservative Action:**
- Volunteer for Van Drew campaign
- Pray for his re-election
- Door-to-door outreach in churches
- Voter registration drives

#### DISTRICT 4 - Chris Smith (R) - PRO-LIFE HERO

**The District:** Central Jersey - Monmouth and Ocean counties

**Incumbent:** Chris Smith has served since 1981 and is Congress's leading pro-life advocate.

**Smith's Record:**
- **Pro-Life Legend:** Author of numerous pro-life bills, fought human trafficking
- **International Religious Freedom:** Champion for persecuted Christians worldwide
- **Sanctity of Life:** Opposed abortion, euthanasia, embryonic stem cell research
- **Human Dignity:** Led efforts against sex trafficking and modern slavery

**Why This Matters:**
Chris Smith is a national treasure for the pro-life movement. His leadership has saved countless lives. We cannot afford to lose him.

**Christian Conservative Action:**
- Support Smith's re-election
- Thank him for his faithful service
- Share his pro-life record with younger voters
- Ensure strong turnout in Monmouth and Ocean counties

#### DISTRICT 7 - Tom Kean Jr. (R) - COMPETITIVE

**The District:** Suburban - parts of Essex, Morris, Somerset, Union, Warren counties

**Incumbent:** Tom Kean Jr. won in 2022, flipping this seat from Democrat control.

**Kean's Record:**
- More moderate Republican
- Pro-business, fiscal conservative
- Mixed record on social issues
- Son of popular former Governor

**Why This Matters:**
This is NJ's most competitive district. Democrats will pour millions into recapturing it. Kean needs conservative base support.

**Christian Conservative Action:**
- Hold Kean accountable on life and family issues
- Ensure he doesn't compromise on parental rights
- Support if he stands firm on values
- High turnout essential in this swing district

#### DISTRICTS TO TARGET

**District 3 (Central Jersey):** Herb Conaway (D) won in 2024. Moderate district, winnable with right candidate.

**District 5 (Northern NJ):** Josh Gottheimer (D) is moderate but supports abortion. Competitive with strong Republican.

**District 11 (Suburban):** Mikie Sherrill (D) flipped this seat in 2018. Suburban moms concerned about education could flip it back.

## 2025 State Legislative Races - ALL SEATS UP

### Why State Legislature Matters

New Jersey's State Legislature has enormous power over:
- Abortion policy (already extreme, could get worse)
- Education curriculum and parental rights
- Religious liberty protections
- Healthcare conscience rights
- Tax and spending policies

**Current Control:** Democrats dominate both chambers
- State Senate: 25 Democrats, 15 Republicans (out of 40 seats)
- General Assembly: 52 Democrats, 28 Republicans (out of 80 seats)

**2025 Opportunity:**
ALL 40 Senate seats and ALL 80 Assembly seats are up for election. This is our chance to gain ground.

### Target Districts for Christian Conservatives

#### Competitive Senate Districts:

**District 11 (Monmouth County):**
Suburban swing district. Focus on parental rights and education.

**District 16 (Central Jersey):**
Hunterdon, Mercer, Middlesex, Somerset counties. Suburban parents concerned about schools.

**District 24 (Morris, Sussex, Warren):**
Rural and suburban mix. Strong conservative base, need turnout.

**District 30 (Monmouth County):**
Competitive Shore district. Life and family issues resonate.

#### Assembly Districts to Watch:

Every Senate district elects 2 Assembly members. Focus on districts 8, 11, 16, 24, 25, 26, 30, 38 where we can flip seats or defend Republicans.

### Key Issues for Legislative Races:

1. **Parental Rights:** Parents' right to know about their children's education and medical decisions
2. **Education:** Stop gender ideology and critical race theory in schools
3. **Abortion:** Oppose any expansion of already extreme abortion laws
4. **Religious Liberty:** Protect faith-based organizations and healthcare workers
5. **Taxes:** NJ has highest property taxes in America - need relief

## 2025 School Board Elections - CRITICAL PRIORITY

### Why School Boards Matter Most

School boards control:
- Curriculum content (gender ideology, critical race theory, sex education)
- Library book selections
- Bathroom and locker room policies
- Parental notification policies
- Budget and tax levies

**New Jersey Context:**
NJ school boards have been battlegrounds over:
- Transgender policies hiding information from parents
- Sexually explicit materials in school libraries
- Critical race theory in curriculum
- Sex education starting in kindergarten

### Major School Board Races (November 4, 2025)

#### Newark Board of Education
**Why It Matters:** NJ's largest school district (38,000 students)
**Seats Up:** Multiple at-large seats
**Issues:** Academic performance, parental rights, curriculum transparency
**Action:** Research candidates, attend forums, vote for parental rights champions

#### Jersey City Board of Education  
**Why It Matters:** Second largest district (30,000 students)
**Seats Up:** Multiple at-large seats
**Issues:** Gender policies, curriculum, budget accountability
**Action:** Organize parents, vet candidates, mobilize churches

#### Edison Board of Education
**Why It Matters:** Large suburban district, active parent community
**Seats Up:** At-large seats
**Issues:** Academic excellence, parental involvement, curriculum
**Action:** Strong parental rights candidates can win here

#### Paterson Board of Education
**Why It Matters:** Third largest district, education reform critical
**Seats Up:** District seats
**Issues:** Academic performance, parental engagement, transparency
**Action:** Support reform candidates, mobilize faith communities

#### Other Critical Districts:
- Elizabeth Board of Education
- Woodbridge Board of Education
- Camden Board of Education
- Trenton Board of Education
- Clifton Board of Education
- Passaic Board of Education
- Union City Board of Education

### School Board Strategy for Christian Conservatives:

1. **Research Candidates Early:** Attend candidate forums, ask about parental rights
2. **Ask Key Questions:**
   - Will you ensure parents are notified about curriculum content?
   - Do you support parental opt-out for controversial materials?
   - Will you oppose gender ideology in elementary schools?
   - Do you support transparency in library book selections?
3. **Mobilize Churches:** School board elections have low turnout - organized faith communities can swing races
4. **Vote in November 2025:** Don't skip these races - they're on the general election ballot

## 2025 Municipal Elections

### Major Mayoral Races (May 13, 2025)

#### Newark Mayor
**Incumbent:** Ras Baraka (D)
**Outlook:** Heavily Democratic city, but faith communities can influence
**Issues:** Crime, education, economic development
**Action:** Engage African American churches, focus on life and family values

#### Jersey City Mayor
**Incumbent:** Steven Fulop (D) - term limited
**Outlook:** Open seat, multiple Democrats running
**Issues:** Development, taxes, education
**Action:** Research candidates, support most conservative option

#### Paterson Mayor
**Issues:** Education, crime, economic opportunity
**Action:** Engage Hispanic evangelical churches - growing influence

#### Trenton Mayor (State Capital)
**Issues:** Crime, education, city services
**Action:** Faith community mobilization essential

#### Camden Mayor
**Issues:** Education reform, public safety, economic development
**Action:** Support candidates committed to school choice and parental rights

### Why Municipal Elections Matter:

Mayors and city councils control:
- Police department policies and funding
- Local education policy support
- Zoning for churches and pregnancy centers
- LGBTQ+ ordinances and policies
- Budget priorities

## 2025 County Elections

### County Executives and Freeholders

New Jersey's 21 counties have significant power over:
- Law enforcement (Sheriff departments)
- Social services
- Health departments
- Parks and recreation
- Property taxes

**Key County Races:**

#### Bergen County (Most Populous)
**County Executive:** James Tedesco (D) seeking re-election
**Outlook:** Competitive suburban county
**Action:** Focus on taxes, public safety, parental rights

#### Essex County (Includes Newark)
**County Executive:** Joseph DiVincenzo Jr. (D)
**Action:** Engage urban faith communities

#### Hudson County (Includes Jersey City)
**Action:** Support conservative alternatives in Democratic primary

#### Monmouth County (Competitive)
**Freeholder races:** Republicans can win here
**Action:** High priority for conservative turnout

#### Morris County (Republican-leaning)
**Action:** Defend Republican control, ensure conservative candidates

#### Ocean County (Most Conservative)
**Action:** Maintain Republican control, support pro-life champions

### Sheriff Races - Law Enforcement Leadership

All 21 counties elect Sheriffs in 2025. Sheriffs control:
- County jail operations
- Court security
- Warrant service
- Some law enforcement functions

**Priority Sheriff Races:**
- Atlantic County Sheriff
- Burlington County Sheriff
- Camden County Sheriff
- Monmouth County Sheriff
- Ocean County Sheriff

**Why Sheriffs Matter:**
- Public safety leadership
- Cooperation with ICE on immigration
- Protection of Second Amendment rights
- Support for faith-based prison ministries

## Key Issues for New Jersey Christian Conservatives

### 1. ABORTION - The Most Extreme Laws in America

**Current Status:**
- Abortion legal through all 9 months for any reason
- No parental notification for minors
- Taxpayer funding of abortion
- "Reproductive Freedom Act" enshrines abortion in state law
- No informed consent requirements
- No waiting periods

**What's at Stake:**
Democrats want to expand abortion even further:
- Abortion tourism from other states
- More taxpayer funding
- Forcing pro-life healthcare workers to participate
- Shutting down pregnancy resource centers

**Christian Conservative Response:**
- Support pro-life candidates at every level
- Volunteer at pregnancy resource centers
- Educate about fetal development and abortion reality
- Pray outside abortion facilities
- Support adoption and foster care
- Vote for legislators who will limit abortion

**Pro-Life Resources in NJ:**
- Several Pregnancy Resource Centers statewide
- Catholic Charities adoption services
- Maternity homes for women in crisis
- Post-abortion healing ministries

### 2. PARENTAL RIGHTS - Schools Hiding Information

**The Crisis:**
New Jersey school districts have policies allowing:
- Social gender transition without parental knowledge
- Use of opposite-sex names/pronouns hidden from parents
- Access to opposite-sex bathrooms and locker rooms
- Counseling about gender identity without parental consent

**Recent Battles:**
- Marlboro Township parents sued over transgender policy
- Hanover Township parents fought curriculum secrecy
- Multiple districts adopted policies hiding information from parents

**What's at Stake in 2025:**
School board elections will determine whether parents have rights or schools have total control over children.

**Christian Conservative Action:**
- Run for school board or support parental rights candidates
- Attend school board meetings
- Request curriculum transparency
- Opt children out of controversial content
- Consider Christian school or homeschool options
- Vote in November 2025 school board elections

### 3. RELIGIOUS LIBERTY - Under Attack

**Current Threats:**
- Faith-based adoption agencies forced to place children with same-sex couples
- Christian healthcare workers forced to participate in procedures violating conscience
- Churches threatened over biblical teaching on marriage and sexuality
- Religious schools pressured on hiring and admissions
- Pregnancy centers targeted with regulations

**Recent Cases:**
- Catholic Charities stopped doing adoptions rather than violate beliefs
- Christian schools challenged over employment policies
- Pregnancy centers face hostile regulations

**What's at Stake:**
- Will churches be free to preach biblical truth?
- Can Christian schools maintain biblical standards?
- Will healthcare workers be forced to violate conscience?
- Can faith-based charities operate according to beliefs?

**Christian Conservative Action:**
- Support religious liberty legal defense organizations
- Contact legislators about conscience protections
- Attend public hearings on religious liberty issues
- Vote for candidates committed to First Amendment
- Support Alliance Defending Freedom and similar groups

### 4. EDUCATION - Curriculum Battles

**The Issues:**
- **Gender Ideology:** Taught starting in elementary school
- **Critical Race Theory:** Dividing children by race
- **Sex Education:** Graphic content, starting too young
- **Library Books:** Sexually explicit materials
- **Parental Exclusion:** Parents kept in the dark

**New Jersey Specific:**
- State mandates LGBTQ+ curriculum in all grades
- "Inclusive" curriculum requirements
- Comprehensive sex education requirements
- Limited parental opt-out rights

**Christian Conservative Response:**
- Win school board elections
- Request curriculum review
- Exercise opt-out rights where available
- Attend school board meetings
- Document concerning materials
- Consider alternatives (Christian school, homeschool)
- Support school choice legislation

### 5. LIFE ISSUES BEYOND ABORTION

**Assisted Suicide:**
- Legalized in NJ in 2019
- Expansion efforts ongoing
- Threatens vulnerable elderly and disabled
- Pressure on those with expensive medical conditions

**Euthanasia:**
- Proposals to expand assisted suicide
- Threats to hospice care
- Devaluing of human life

**Embryonic Research:**
- Taxpayer funding of embryo-destructive research
- Cloning concerns
- IVF regulation issues

**Christian Conservative Action:**
- Support palliative care and hospice
- Oppose assisted suicide expansion
- Protect vulnerable populations
- Advocate for life-affirming healthcare
- Support disability rights organizations

## Church Mobilization Strategy

### How Churches Can Make a Difference

**1. Voter Registration Drives**
- Register members to vote (nonpartisan)
- Provide voter registration forms
- Encourage civic participation
- Deadline: 21 days before election

**2. Voter Education**
- Distribute nonpartisan voter guides
- Host candidate forums (invite all candidates)
- Educate on biblical principles for voting
- Provide information on ballot measures

**3. Prayer and Fasting**
- Pray for elections and candidates
- Fast for God's will in elections
- Pray for wisdom for voters
- Spiritual warfare against evil agendas

**4. Volunteer Mobilization**
- Encourage members to volunteer for campaigns
- Organize phone banks
- Door-to-door canvassing
- Poll watching on election day

**5. Get Out the Vote**
- Remind members to vote
- Provide rides to polls
- Absentee ballot assistance
- Early voting information

### Legal Guidelines for Churches

**What Churches CAN Do:**
- Register voters (nonpartisan)
- Distribute nonpartisan voter guides
- Educate on issues from biblical perspective
- Host candidate forums (all candidates invited)
- Encourage voting and civic participation
- Pastor can endorse as individual (not from pulpit)

**What Churches CANNOT Do:**
- Endorse candidates as a church
- Contribute to campaigns
- Distribute partisan materials
- Campaign for candidates using church resources

**Resources:**
- Alliance Defending Freedom Church Alliance
- Family Research Council Voter Guide
- iVoterGuide.com for candidate positions

## Critical Dates and Deadlines

### 2025 Elections

**Municipal Elections (May 13, 2025):**
- Voter Registration Deadline: April 22, 2025
- Early Voting: May 3-11, 2025
- Election Day: May 13, 2025

**General Election (November 4, 2025):**
- Voter Registration Deadline: October 14, 2025
- Early Voting: October 25 - November 2, 2025
- Election Day: November 4, 2025
- **On Ballot:** State Legislature (all seats), School Boards, County offices, Municipal offices

### 2026 Elections

**Primary Election (June 2, 2026):**
- Voter Registration Deadline: May 12, 2026
- Early Voting: May 23-31, 2026
- Primary Day: June 2, 2026

**General Election (November 3, 2026):**
- Voter Registration Deadline: October 13, 2026
- Early Voting: October 24 - November 1, 2026
- Election Day: November 3, 2026
- **On Ballot:** U.S. Senate, U.S. House (all 12 districts)

## How to Vote in New Jersey

### Voter Registration
- Online: nj.gov/state/elections/voter-registration.shtml
- By mail: Download form, mail to county clerk
- In person: County clerk or MVC office
- Deadline: 21 days before election

### Voting Options
1. **Early Voting:** 9 days before election at designated locations
2. **Election Day:** Vote at assigned polling place
3. **Mail-In Ballot:** Request online or by mail, return by 8 PM election day
4. **Provisional Ballot:** If registration issue, cast provisional ballot

### What to Bring
- No ID required if registered
- First-time voters may need ID
- Sample ballot helpful but not required

## Prayer Points for New Jersey

### Pray For:

**1. Spiritual Awakening**
- Revival in churches across New Jersey
- Salvation of political leaders
- Holy Spirit conviction on life and family issues
- Churches to engage in civic arena

**2. Elections**
- Godly candidates to run for office
- Wisdom for voters
- Exposure of corruption and evil agendas
- Protection from voter fraud
- Clear victories for righteousness

**3. Specific Issues**
- End to abortion in New Jersey
- Protection of children from gender ideology
- Parental rights restored
- Religious liberty preserved
- Biblical marriage defended

**4. Leaders**
- Salvation of Governor Phil Murphy
- Conversion of Senator Cory Booker
- Wisdom for pro-life legislators
- Courage for Christian elected officials
- Protection for those standing for truth

**5. Churches**
- Boldness to speak truth
- Unity across denominational lines
- Mobilization of believers to vote
- Wisdom in political engagement
- Protection from government overreach

### Scripture for New Jersey Elections

**2 Chronicles 7:14** - "If my people, which are called by my name, shall humble themselves, and pray, and seek my face, and turn from their wicked ways; then will I hear from heaven, and will forgive their sin, and will heal their land."

**Proverbs 29:2** - "When the righteous are in authority, the people rejoice: but when the wicked beareth rule, the people mourn."

**1 Timothy 2:1-2** - "I exhort therefore, that, first of all, supplications, prayers, intercessions, and giving of thanks, be made for all men; For kings, and for all that are in authority; that we may lead a quiet and peaceable life in all godliness and honesty."

## Action Steps for Christian Conservatives

### Immediate Actions (Now - Spring 2025)

1. **Register to Vote** - Ensure you and family members are registered
2. **Research Candidates** - Start learning about municipal and school board candidates
3. **Pray** - Begin praying for elections and candidates
4. **Connect** - Join local conservative/pro-life groups
5. **Volunteer** - Sign up to help with campaigns

### Spring 2025 (Municipal Elections)

1. **Vote May 13** - Newark, Jersey City, Paterson, Trenton, Camden mayors
2. **Research Candidates** - Know their positions on life and family
3. **Mobilize Church** - Encourage members to vote
4. **Volunteer** - Help with campaigns if possible

### Fall 2025 (General Election)

1. **Vote November 4** - State Legislature, School Boards, County offices
2. **School Board Priority** - Research and vote for parental rights candidates
3. **State Legislature** - Support pro-life, pro-family candidates
4. **Sheriff Races** - Vote for law-and-order candidates
5. **Mobilize** - Get out the vote in your church and community

### 2026 (Federal Elections)

1. **Primary June 2** - Vote for strongest conservative in Republican primary
2. **General November 3** - Vote for U.S. Senate and House
3. **Defend Champions** - Support Chris Smith and Jeff Van Drew
4. **Target Booker** - Work to defeat Cory Booker
5. **Flip Seats** - Help Republicans win competitive House districts

## Resources for New Jersey Christian Conservatives

### Voter Information
- NJ Division of Elections: nj.gov/state/elections
- Sample Ballots: nj.gov/state/elections/vote-by-mail.shtml
- Polling Place Locator: voter.svrs.nj.gov/polling-place-search

### Voter Guides
- iVoterGuide.com - Candidate positions on key issues
- Family Research Council Voter Guide
- Christian Coalition Voter Guide
- Local pro-life organization guides

### Pro-Life Organizations
- NJ Right to Life: njrtl.org
- Pregnancy resource centers statewide
- Catholic Charities
- Lutherans for Life

### Religious Liberty
- Alliance Defending Freedom: adflegal.org
- First Liberty Institute: firstliberty.org
- Becket Fund for Religious Liberty: becketlaw.org

### Parental Rights
- Moms for Liberty NJ chapters
- Parents Defending Education
- Family Policy Alliance

### Political Engagement
- NJ Family Policy Council
- American Family Association
- Concerned Women for America NJ

### News and Information
- Christian Post
- The Federalist
- Daily Wire
- PJ Media
- LifeNews.com

## Conclusion: New Jersey Can Change

New Jersey may be a blue state, but Christian conservatives can make a significant impact:

**We Can Win:**
- School board races (low turnout = opportunity)
- Local elections (organized faith communities swing races)
- Competitive legislative districts (suburban parents concerned about education)
- Sheriff races (law and order message resonates)

**We Must Engage:**
- 2025 is critical for school boards and state legislature
- 2026 is opportunity to defeat Cory Booker and flip House seats
- Every election matters for life, family, and religious liberty

**We Need You:**
- Register and vote
- Research candidates
- Volunteer for campaigns
- Mobilize your church
- Pray for elections
- Run for office (especially school board)

**The Stakes Are High:**
- Children's education and safety
- Parental rights
- Religious liberty
- Sanctity of life
- Biblical marriage and family
- Future of New Jersey

**God is Sovereign:**
Remember that God is in control. Our job is to be faithful, to vote according to biblical principles, to pray, and to trust God with the results.

"Blessed is the nation whose God is the LORD" - Psalm 33:12

## Contact Information

**New Jersey Division of Elections**
Phone: 609-292-3760
Website: nj.gov/state/elections

**County Clerk Offices**
Find your county clerk for voter registration and election information at nj.gov/counties

**Report Election Issues**
NJ Election Law Enforcement Commission: 609-292-8700

---

*This guide is provided for educational purposes to help Christian conservatives make informed voting decisions based on biblical principles. It is not an endorsement by any church or religious organization.*

**Last Updated:** January 2025
**Next Update:** After 2025 municipal elections

*"When the righteous are in authority, the people rejoice: but when the wicked beareth rule, the people mourn." - Proverbs 29:2*
""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing New Jersey races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} New Jersey races...")
race_ids = {}
for race in races:
    office = race['office']
    if office in existing_race_map:
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {office}")
    else:
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {office}")
    race_ids[office] = race_id
print(f"\n[SUCCESS] Processed {len(races)} races")

print(f"\nChecking for existing New Jersey candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} New Jersey candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    if key in existing_candidate_map:
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {name} - {office}")
    else:
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {name} - {office}")
print(f"\n[SUCCESS] Processed {len(candidates)} candidates")

print("\nProcessing New Jersey summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'New Jersey'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] New Jersey data upload complete!")
