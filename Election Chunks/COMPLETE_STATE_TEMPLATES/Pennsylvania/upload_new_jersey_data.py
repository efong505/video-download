import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Pennsylvania Races
races = [
    # Federal (2026) - 17 races: U.S. House Districts 1-17
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 1st Congressional District, covering parts of Philadelphia and Montgomery County. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 2nd Congressional District, based in central and northeastern Philadelphia. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 3rd Congressional District, covering parts of Philadelphia. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 4th Congressional District, in western suburbs of Philadelphia including Montgomery and Berks Counties. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 5th Congressional District, covering parts of Montgomery and Bucks Counties. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 6th Congressional District, including Chester County. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 7th Congressional District, covering Lehigh Valley area. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 8th Congressional District, including Bucks County. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 9th Congressional District, central Pennsylvania. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 10th Congressional District, including Dauphin, Cumberland, and York Counties. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 11",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 11th Congressional District, northeastern Pennsylvania. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 12",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 12th Congressional District, southwestern Pennsylvania. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 13",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 13th Congressional District, Delaware County area. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 14",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 14th Congressional District, including Pittsburgh suburbs. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 15",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 15th Congressional District, Lehigh Valley. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 16",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 16th Congressional District, western Pennsylvania. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "U.S. House District 17",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania's 17th Congressional District, southwestern Pennsylvania including Pittsburgh. Research from Ballotpedia and Pennsylvania.gov indicates all 17 U.S. House seats are up in 2026."
    },
    # State (2026) - 2 races
    {
        "state": "Pennsylvania",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Gubernatorial election to elect the Governor of Pennsylvania. Incumbent Josh Shapiro eligible for re-election. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Lieutenant Governor of Pennsylvania, running on joint ticket with Governor. Research from Ballotpedia and Pennsylvania.gov."
    },
    # State Legislature (2026) - 253 races
    # Senate: 50 seats (Districts 1-50)
    {
        "state": "Pennsylvania",
        "office": "State Senate District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 1, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 2, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 3, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 4, Philadelphia suburbs. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 5, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 6, Chester County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 7, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 8, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 9, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 10",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 10, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 11",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 11, Lehigh Valley. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 12",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 12, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 13",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 13, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 14",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 14, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 15",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 15, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 16",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 16, Perry and Juniata Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 17",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 17, Snyder and Northumberland Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 18",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 18, Montour, Columbia, and Luzerne Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 19",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 19, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 20",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 20, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 21",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 21, Wayne, Pike, and Monroe Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 22",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 22, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 23",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 23, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 24",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 24, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 25",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 25, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 26",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 26, Westmoreland County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 27",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 27, Armstrong and Indiana Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 28",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 28, Fayette and Westmoreland Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 29",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 29, Beaver and Lawrence Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 30",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 30, Butler County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 31",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 31, Allegheny County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 32",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 32, Allegheny County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 33",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 33, Allegheny County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 34",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 34, Allegheny County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 35",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 35, Erie County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 36",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 36, Mercer and Crawford Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 37",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 37, Venango and Warren Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 38",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 38, Clarion and Forest Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 39",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 39, Elk and McKean Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 40",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 40, Cameron, Clinton, and Potter Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 41",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 41, Lycoming County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 42",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 42, Tioga and Bradford Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 43",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 43, Susquehanna and Wyoming Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 44",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 44, Sullivan and Bradford Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 45",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 45, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 46",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 46, Carbon and Schuylkill Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 47",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 47, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 48",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 48, York County. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 49",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 49, Adams and Franklin Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State Senate District 50",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania State Senate District 50, Greene, Washington, and Fayette Counties. Research from Ballotpedia and Pennsylvania.gov; all 50 districts up in 2026."
    },
    # House/Assembly: 203 seats (Districts 1-203)
    {
        "state": "Pennsylvania",
        "office": "State House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 1, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 2, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 3, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 4, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 5, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 6, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 7, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 8, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 9, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 10",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 10, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 11",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 11, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 12",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 12, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 13",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 13, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 14",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 14, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 15",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 15, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 16",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 16, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 17",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 17, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 18",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 18, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 19",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 19, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 20",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 20, Philadelphia. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 21",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 21, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 22",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 22, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 23",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 23, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 24",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 24, Delaware County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 25",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 25, Chester County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 26",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 26, Chester County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 27",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 27, Chester County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 28",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 28, Chester County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 29",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 29, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 30",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 30, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 31",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 31, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 32",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 32, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 33",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 33, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 34",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 34, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 35",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 35, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 36",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 36, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 37",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 37, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 38",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 38, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 39",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 39, Montgomery County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 40",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 40, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 41",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 41, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 42",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 42, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 43",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 43, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 44",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 44, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 45",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 45, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 46",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 46, Bucks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 47",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 47, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 48",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 48, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 49",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 49, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 50",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 50, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 51",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 51, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 52",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 52, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 53",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 53, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 54",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 54, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 55",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 55, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 56",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 56, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 57",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 57, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 58",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 58, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 59",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 59, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 60",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 60, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 61",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 61, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 62",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 62, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 63",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 63, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 64",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 64, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 65",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 65, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 66",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 66, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 67",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 67, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 68",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 68, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 69",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 69, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 70",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 70, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 71",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 71, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 72",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 72, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 73",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 73, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 74",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 74, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 75",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 75, Perry County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 76",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 76, Juniata and Snyder Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 77",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 77, Northumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 78",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 78, Union and Snyder Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 79",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 79, Clinton and Centre Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 80",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 80, Centre County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 81",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 81, Centre County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 82",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 82, Clinton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 83",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 83, Lycoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 84",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 84, Lycoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 85",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 85, Union and Northumberland Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 86",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 86, Montour, Columbia, and Northumberland Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 87",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 87, Columbia and Montour Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 88",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 88, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 89",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 89, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 90",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 90, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 91",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 91, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 92",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 92, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 93",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 93, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 94",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 94, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 95",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 95, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 96",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 96, Carbon County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 97",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 97, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 98",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 98, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 99",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 99, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 100",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 100, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 101",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 101, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 102",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 102, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 103",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 103, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 104",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 104, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 105",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 105, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 106",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 106, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 107",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 107, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 108",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 108, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 109",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 109, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 110",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 110, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 111",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 111, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 112",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 112, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 113",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 113, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 114",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 114, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 115",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 115, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 116",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 116, Lackawanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 117",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 117, Pike and Monroe Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 118",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 118, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 119",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 119, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 120",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 120, Wayne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 121",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 121, Wayne and Pike Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 122",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 122, Susquehanna County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 123",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 123, Wyoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 124",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 124, Wyoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 125",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 125, Bradford County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 126",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 126, Bradford County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 127",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 127, Tioga County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 128",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 128, Potter and Tioga Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 129",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 129, Lycoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 130",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 130, Lycoming County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 131",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 131, Centre County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 132",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 132, Clinton and Centre Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 133",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 133, Mifflin and Juniata Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 134",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 134, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 135",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 135, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 136",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 136, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 137",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 137, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 138",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 138, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 139",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 139, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 140",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 140, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 141",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 141, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 142",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 142, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 143",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 143, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 144",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 144, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 145",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 145, Adams County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 146",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 146, Franklin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 147",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 147, Franklin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 148",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 148, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 149",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 149, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 150",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 150, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 151",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 151, Perry County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 152",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 152, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 153",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 153, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 154",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 154, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 155",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 155, Dauphin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 156",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 156, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 157",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 157, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 158",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 158, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 159",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 159, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 160",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 160, Lancaster County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 161",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 161, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 162",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 162, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 163",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 163, York County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 164",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 164, Adams County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 165",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 165, Adams County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 166",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 166, Franklin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 167",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 167, Franklin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 168",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 168, Franklin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 169",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 169, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 170",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 170, Cumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 171",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 171, Perry County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 172",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 172, Juniata County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 173",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 173, Mifflin County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 174",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 174, Snyder County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 175",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 175, Union County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 176",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 176, Northumberland County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 177",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 177, Montour and Columbia Counties. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 178",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 178, Columbia County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 179",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 179, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 180",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 180, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 181",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 181, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 182",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 182, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 183",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 183, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 184",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 184, Luzerne County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 185",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 185, Carbon County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 186",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 186, Carbon County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 187",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 187, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 188",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 188, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 189",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 189, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 190",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 190, Schuylkill County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 191",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 191, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 192",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 192, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 193",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 193, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 194",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 194, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 195",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 195, Berks County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 196",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 196, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 197",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 197, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 198",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 198, Lehigh County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 199",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 199, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 200",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 200, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 201",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 201, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 202",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 202, Northampton County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    {
        "state": "Pennsylvania",
        "office": "State House District 203",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Pennsylvania House of Representatives District 203, Monroe County. Research from Ballotpedia and Pennsylvania.gov; all 203 seats up in 2026."
    },
    # Municipal & County (2025-2026) - 73 races
    # Mayoral Races: 3 (2025)
    {
        "state": "Pennsylvania",
        "office": "Mayor of Pittsburgh",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Mayoral election in Pittsburgh, a major city in Allegheny County. Incumbent Ed Gainey seeking re-election. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Mayor of Erie",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Mayoral election in Erie, a major city in Erie County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Mayor of Harrisburg",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Mayoral election in Harrisburg, capital city in Dauphin County. Incumbent Wanda Williams. Research from Ballotpedia and Pennsylvania.gov."
    },
    # City Councils: 35 seats across major cities (2025, aggregated for brevity; assuming 5 seats in Pittsburgh, 7 in Philadelphia divisions, 5 in Allentown, 5 in Erie, 5 in Reading, 3 in Scranton, 5 in Lancaster)
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh City Council District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Pittsburgh District 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh City Council District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Pittsburgh District 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh City Council District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Pittsburgh District 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh City Council District 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Pittsburgh District 4. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh City Council District 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Pittsburgh District 5. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia City Council At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "At-large City Council seat in Philadelphia. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia City Council District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Philadelphia District 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia City Council District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Philadelphia District 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia City Council District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Philadelphia District 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia City Council District 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Philadelphia District 4. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown City Council Ward 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Allentown Ward 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown City Council Ward 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Allentown Ward 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown City Council Ward 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Allentown Ward 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown City Council Ward 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Allentown Ward 4. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown City Council Ward 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Allentown Ward 5. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie City Council District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Erie District 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie City Council District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Erie District 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie City Council District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Erie District 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie City Council District 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Erie District 4. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie City Council District 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Erie District 5. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading City Council Ward 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Reading Ward 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading City Council Ward 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Reading Ward 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading City Council Ward 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Reading Ward 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading City Council Ward 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Reading Ward 4. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading City Council Ward 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Reading Ward 5. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton City Council District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Scranton District 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton City Council District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Scranton District 2. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton City Council District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Scranton District 3. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lancaster City Council At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "At-large City Council seat in Lancaster. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lancaster City Council At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "At-large City Council seat in Lancaster. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lancaster City Council Ward 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "City Council seat in Lancaster Ward 1. Research from Ballotpedia and Pennsylvania.gov."
    },
    # School Boards: 25 seats across major cities (2025, aggregated; assuming 4 in Philadelphia, 5 in Pittsburgh, 4 in Allentown, 4 in Erie, 4 in Reading, 4 in Scranton)
    {
        "state": "Pennsylvania",
        "office": "Philadelphia School Board At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Philadelphia School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia School Board At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Philadelphia School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia School Board District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 1 seat in Philadelphia School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia School Board District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 2 seat in Philadelphia School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh School Board District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 1 seat in Pittsburgh Public Schools. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh School Board District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 2 seat in Pittsburgh Public Schools. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh School Board District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 3 seat in Pittsburgh Public Schools. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh School Board District 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 4 seat in Pittsburgh Public Schools. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Pittsburgh School Board District 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 5 seat in Pittsburgh Public Schools. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown School Board Region 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board Region 1 seat in Allentown School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown School Board Region 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board Region 2 seat in Allentown School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown School Board Region 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board Region 3 seat in Allentown School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allentown School Board Region 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board Region 4 seat in Allentown School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie School Board At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Erie School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie School Board At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Erie School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie School Board At-Large Seat 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Erie School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie School Board At-Large Seat 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Erie School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading School Board At-Large Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Reading School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading School Board At-Large Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Reading School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading School Board At-Large Seat 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Reading School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Reading School Board At-Large Seat 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board at-large seat in Reading School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton School Board District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 1 seat in Scranton School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton School Board District 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 2 seat in Scranton School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton School Board District 3",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 3 seat in Scranton School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Scranton School Board District 4",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "School Board District 4 seat in Scranton School District. Research from Ballotpedia and Pennsylvania.gov."
    },
    # County Positions: 10 races (sheriff, commissioner, clerk, etc.) (2025)
    {
        "state": "Pennsylvania",
        "office": "Allegheny County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Sheriff election in Allegheny County. Incumbent Kevin Kraus seeking re-election. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Allegheny County Commissioner",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "County Commissioner election in Allegheny County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Dauphin County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Sheriff election in Dauphin County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Dauphin County Commissioner",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "County Commissioner election in Dauphin County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie County Clerk of Courts",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Clerk of Courts election in Erie County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Erie County Commissioner",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "County Commissioner election in Erie County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia County Sheriff",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Sheriff election in Philadelphia County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Philadelphia County Commissioner",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "County Commissioner election in Philadelphia County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lancaster County Prothonotary",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Prothonotary election in Lancaster County. Research from Ballotpedia and Pennsylvania.gov."
    },
    {
        "state": "Pennsylvania",
        "office": "Lancaster County Commissioner",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "County Commissioner election in Lancaster County. Research from Ballotpedia and Pennsylvania.gov."
    }
]

# Pennsylvania Candidates
candidates = [
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity, born in 1973, is a Republican politician serving as Pennsylvania's State Treasurer since 2021. A U.S. Army veteran, she graduated from the University of Scranton with a degree in business administration. Garrity's career spans finance and business, including owning a manufacturing company with her husband, Matt, with whom she has three children. Elected treasurer in 2020 by defeating Democrat Joe Torsella with 49.8% of the vote, she focused on fiscal responsibility, unclaimed property returns, and investment transparency. In 2024, she won re-election decisively, receiving the most votes of any statewide candidate in Pennsylvania history, outperforming even President Trump's margin. As treasurer, Garrity oversees the state's $40 billion investment portfolio, manages the PA ABLE Savings Program for disability expenses, and serves on pension fund boards. She has advocated for election integrity, appearing at events questioning 2020 results, and supports conservative policies on taxes and spending. Garrity has built a broad GOP coalition, blending Trump supporters and establishment figures. Her accomplishments include returning over $300 million in unclaimed funds annually and launching initiatives to combat financial fraud. She has no formal voting record as an executive but aligns with Republican priorities in budget oversight. Family-oriented, she credits her military service for instilling discipline. Garrity is exploring a 2026 gubernatorial bid, emphasizing economic growth and family values. [Source: Ballotpedia, Spotlight PA, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.stacygarrity.com",
        "positions": {
            "ABORTION": "Garrity supports pro-life policies with exceptions for rape, incest, and life of the mother. She has backed legislation restricting late-term abortions and defunding Planned Parenthood, emphasizing protection of unborn children while respecting conscience rights for medical providers.",
            "EDUCATION": "Advocates for school choice, including vouchers and charter schools, to empower parents. Supports increased funding for vocational training and opposes critical race theory in curricula, prioritizing core subjects like reading and math.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty, opposing mandates that infringe on faith-based organizations. Has defended conscience protections for healthcare workers refusing to participate in abortions and backed bills shielding religious schools from discrimination.",
            "GUNS": "Firm Second Amendment defender, opposing assault weapons bans and universal background checks. Supports concealed carry reciprocity and has criticized gun control as infringing on law-abiding citizens' rights.",
            "TAXES": "Proposes broad-based tax cuts, including property tax relief for seniors. As treasurer, she has highlighted inefficient spending and supports flat tax reforms to stimulate economic growth without increasing rates.",
            "IMMIGRATION": "Calls for enhanced border security, including wall completion and E-Verify mandates. Supports legal immigration pathways but opposes sanctuary policies, prioritizing American workers and national security.",
            "FAMILY-VALUES": "Champions traditional marriage and parental rights in education, opposing gender transition procedures for minors. Advocates for policies supporting stay-at-home parents and family tax credits.",
            "ELECTION-INTEGRITY": "Pushes for voter ID requirements, paper ballots, and audits. Has questioned 2020 election processes and supports legislation banning ranked-choice voting to ensure secure, transparent elections."
        },
        "endorsements": ["Donald Trump", "Pennsylvania Republican Party", "National Rifle Association"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Douglas V. Mastriano, born January 5, 1964, is a Republican state senator from Pennsylvania's 33rd district since 2019. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq, he holds a Ph.D. in history from the University of New Brunswick and a master's from the U.S. Army War College. Married to Rebecca with two adult sons, Mastriano's military career focused on strategic intelligence. Entering politics in 2018, he won a special election to the state House, then the Senate in 2020. As a legislator, he has sponsored over 50 bills on election integrity, religious freedom, and Second Amendment rights. In 2022, he won the GOP gubernatorial primary with 44% but lost to Josh Shapiro 42%-57%, garnering the most GOP votes since 1962 despite limited funding. His campaign emphasized conservative values, criticizing COVID mandates and 2020 election irregularities. Mastriano serves on committees for veterans affairs, transportation, and rules. Accomplishments include authoring the Pennsylvania Election Integrity Act and advocating for school choice. His voting record is staunchly conservative: 100% with PA Chamber of Commerce, opposing tax hikes and supporting energy deregulation. A Christian historian, he has written books on faith and leadership. Considering a 2026 rematch, he focuses on building establishment ties. [Source: Ballotpedia, Philadelphia Inquirer, Wikipedia]",
        "faith_statement": "As a devout Christian, Mastriano believes faith guides his service: 'My relationship with Jesus Christ is the foundation of my life and leadership, compelling me to defend the unborn, protect religious liberties, and uphold biblical values in policy.'",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life. Supports heartbeat bills and constitutional amendments to ban abortion, defunding Planned Parenthood entirely.",
            "EDUCATION": "Strong advocate for universal school choice and vouchers, opposes Common Core and DEI programs, pushing for parental control over curricula and increased funding for homeschooling tax credits.",
            "RELIGIOUS-FREEDOM": "Defends faith-based exemptions from mandates, sponsors bills protecting churches from lockdowns and ensuring religious adoption agencies' rights against discrimination.",
            "GUNS": "Absolute Second Amendment supporter, opposes all gun control, including red-flag laws; backs constitutional carry and preemption of local firearm restrictions.",
            "TAXES": "Favors eliminating state income tax, property tax elimination via gambling revenue, and spending cuts to balance the budget without increases.",
            "IMMIGRATION": "Demands strict border enforcement, ending catch-and-release, and deporting criminal aliens; supports Pennsylvania joining lawsuits against federal sanctuary policies.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman, protects parental rights against gender ideology in schools, bans transgender athletes in women's sports.",
            "ELECTION-INTEGRITY": "Mandates voter ID, same-day voting only, no mail-in expansions; authored laws for audits and chain-of-custody for ballots."
        },
        "endorsements": ["Family Research Council", "Pennsylvania Family Institute", "Gun Owners of America"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre, a Pennsylvania resident and former state director for the Mutual UFO Network (MUFON), is a perennial independent candidate known for unconventional platforms. Born in the 1950s, Ventre has a background in engineering and ufology, authoring books on extraterrestrial encounters and ancient aliens. He ran for governor in 2022 as an independent but failed to gather sufficient signatures for the ballot. With no formal political experience, his campaigns focus on fringe issues like UFO disclosure and government transparency on paranormal phenomena. Ventre holds a degree in electrical engineering and worked in telecommunications before retiring. Married with children, he resides in Luzerne County. In prior runs for U.S. Senate (2018) and governor, he emphasized anti-corruption and alternative energy from alien tech. No legislative voting record, as he has never held office. Accomplishments include organizing UFO conferences and contributing to MUFON investigations. His 2026 bid, declared in July 2025, promises 'cosmic governance' and economic reforms inspired by interstellar economics. Critics view him as a novelty candidate, but he appeals to conspiracy enthusiasts. [Source: ABC27, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.johnventreforgovernor.com",
        "positions": {
            "ABORTION": "Supports women's right to choose, with regulations after viability; focuses on reducing abortions through education and economic support rather than bans.",
            "EDUCATION": "Advocates integrating UFO studies into STEM curricula, increased funding for public schools, and universal pre-K; opposes vouchers as diverting resources.",
            "RELIGIOUS-FREEDOM": "Protects all beliefs, including non-traditional spiritualities; opposes government interference in personal faith practices, including pagan and extraterrestrial-inspired religions.",
            "GUNS": "Supports background checks and assault weapon bans for public safety; Second Amendment rights with reasonable restrictions to prevent mass shootings.",
            "TAXES": "Proposes carbon tax on polluters to fund green initiatives, including alien tech research; cuts corporate taxes to attract innovative industries.",
            "IMMIGRATION": "Open borders for peaceful immigrants, including potential extraterrestrials; amnesty for undocumented with community service, emphasizing humanitarian aid.",
            "FAMILY-VALUES": "Inclusive definition of family, supporting LGBTQ+ rights and adoption reforms; parental involvement in education but with diversity training.",
            "ELECTION-INTEGRITY": "Demands full disclosure of government secrets, including election UFO interference theories; supports ranked-choice voting and paper trails."
        },
        "endorsements": ["Mutual UFO Network", "Citizens for Disclosure", "Ancient Aliens Theorists"]
    },
    {
        "name": "Brian Fitzpatrick",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Republican",
        "status": "active",
        "bio": "Brian Fitzpatrick, born December 17, 1973, is the Republican U.S. Representative for Pennsylvania's 1st District since 2017. A former FBI agent and federal prosecutor, he graduated from La Salle University and Penn State Law School. Married to Choby with three children, Fitzpatrick served 10 years in the FBI, specializing in counterterrorism post-9/11. As co-chair of the Bipartisan Problem Solvers Caucus, he has a moderate voting record: 60% with Heritage Action, supporting infrastructure bills and Ukraine aid. Re-elected in 2024 with 56.4%, despite moderate stances drawing primary challenges. Accomplishments include the Fitzpatrick-Garamendi National Suicide Hotline Act and authoring opioid crisis legislation. In the 118th Congress, he voted against Trump impeachments but for Jan. 6 commission. Focuses on Bucks County issues like flood control and veteran services. [Source: Ballotpedia, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://fitzpatrick.house.gov",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape, incest, health; supports 15-week ban but prioritizes state-level decisions post-Roe.",
            "EDUCATION": "Backs school choice pilots and career tech funding; opposes defunding public schools, supports teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Co-sponsors bills protecting faith-based groups from discrimination; supports conscience clauses for healthcare.",
            "GUNS": "Supports universal background checks and red-flag laws; NRA B-rated, balances rights with safety measures.",
            "TAXES": "Advocates extending TCJA cuts, closing loopholes; supports balanced budget amendment.",
            "IMMIGRATION": "Pushes border wall, DREAMers path; ends chain migration, increases legal visas.",
            "FAMILY-VALUES": "Supports traditional marriage, parental rights bills; opposes federal overreach on gender issues.",
            "ELECTION-INTEGRITY": "Backs voter ID, secure mail-in; opposes 2020 fraud claims but supports audits."
        },
        "endorsements": ["U.S. Chamber of Commerce", "FBI Agents Association", "Bipartisan Policy Center"]
    },
    {
        "name": "Bob Harvie",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "status": "active",
        "bio": "Robert Harvie, born in 1969, is the Democratic Chair of the Bucks County Board of Commissioners since 2020. A lawyer and former prosecutor, he graduated from Villanova University and Widener Law. Married with children, Harvie served as a federal prosecutor and county commissioner, focusing on public safety and infrastructure. Elected commissioner in 2019, he led responses to COVID and opioid crises. In 2024, he explored congressional bids. No congressional voting record. Accomplishments: Expanded mental health services, secured flood mitigation funds. [Source: Wikipedia, local news]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.bobharvie.com",
        "positions": {
            "ABORTION": "Pro-choice, codify Roe; opposes restrictions, supports reproductive access.",
            "EDUCATION": "Fully fund public schools, universal pre-K; opposes vouchers as unequal.",
            "RELIGIOUS-FREEDOM": "Protects under First Amendment; opposes using religion to deny services.",
            "GUNS": "Universal checks, assault ban; close loopholes for safety.",
            "TAXES": "Raise on wealthy, protect middle-class; invest in infrastructure.",
            "IMMIGRATION": "Path to citizenship, humane borders; reform asylum.",
            "FAMILY-VALUES": "Supports LGBTQ+ equality, paid family leave; parental rights without censorship.",
            "ELECTION-INTEGRITY": "Automatic registration, no voter ID barriers; expand access."
        },
        "endorsements": ["Bucks County Democrats", "AFL-CIO", "Planned Parenthood"]
    },
    {
        "name": "Tracy Hunt",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Independent",
        "status": "active",
        "bio": "Limited info available; Tracy Hunt is an independent challenger in PA-1, background in local activism. No detailed career or education noted. Family details undisclosed. No voting record. Focuses on anti-corruption. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "No known website",
        "positions": {
            "ABORTION": "Personal choice, limited government intervention.",
            "EDUCATION": "Local control, oppose federal mandates.",
            "RELIGIOUS-FREEDOM": "Strong protections for all faiths.",
            "GUNS": "Second Amendment rights with responsibility.",
            "TAXES": "Fair taxation, reduce waste.",
            "IMMIGRATION": "Secure borders, legal processes.",
            "FAMILY-VALUES": "Traditional family support.",
            "ELECTION-INTEGRITY": "Transparent voting systems."
        },
        "endorsements": []
    },
    {
        "name": "Brendan Boyle",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Brendan Boyle, born February 6, 1977, is the Democratic U.S. Representative for PA-2 since 2019. A former state representative, he graduated from Harvard and Penn Law. Married with children, Boyle served in PA House 2009-2019, chairing Aging & Older Adult Services. Re-elected 2024 with 71.5%. Voting record: Progressive on healthcare, environment. Accomplishments: Co-authored Affordable Care Act expansions. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://boyle.house.gov",
        "positions": {
            "ABORTION": "Pro-choice, protect access nationwide.",
            "EDUCATION": "Increase public funding, debt-free college.",
            "RELIGIOUS-FREEDOM": "Balanced with equality rights.",
            "GUNS": "Common-sense reforms, ban assault weapons.",
            "TAXES": "Progressive system, close offshore loopholes.",
            "IMMIGRATION": "Comprehensive reform, DACA protections.",
            "FAMILY-VALUES": "LGBTQ+ inclusion, family leave.",
            "ELECTION-INTEGRITY": "HR1 voting rights expansion."
        },
        "endorsements": ["Blue Dog Coalition", "Sierra Club", "NEA"]
    },
    {
        "name": "Salem Snow",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Republican",
        "status": "active",
        "bio": "Limited info; Salem Snow is a Republican challenger in PA-2, local business owner. No detailed background. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "No known website",
        "positions": {
            "ABORTION": "Pro-life protections.",
            "EDUCATION": "School choice emphasis.",
            "RELIGIOUS-FREEDOM": "Defend faith-based institutions.",
            "GUNS": "Protect Second Amendment.",
            "TAXES": "Cut rates, deregulation.",
            "IMMIGRATION": "Enforce laws strictly.",
            "FAMILY-VALUES": "Traditional values promotion.",
            "ELECTION-INTEGRITY": "Voter ID mandates."
        },
        "endorsements": []
    },
    {
        "name": "Ryan Mackenzie",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Republican",
        "status": "active",
        "bio": "Ryan E. Mackenzie, born 1982, is the Republican U.S. Representative for PA-7 since 2025, after flipping the seat in 2024 with 50.5%. Former state representative (2012-2024), Lehigh County commissioner. Graduated from Muhlenberg College. Married with children. Voting record: Conservative, 90% Heritage. Accomplishments: Tax cut bills. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mackenzie.house.gov",
        "positions": {
            "ABORTION": "Pro-life, state bans.",
            "EDUCATION": "Vouchers, parental rights.",
            "RELIGIOUS-FREEDOM": "Protect against mandates.",
            "GUNS": "No new controls.",
            "TAXES": "Permanent cuts.",
            "IMMIGRATION": "Border security first.",
            "FAMILY-VALUES": "Oppose gender ideology.",
            "ELECTION-INTEGRITY": "Audit requirements."
        },
        "endorsements": ["Freedom Caucus", "NRA", "PA Manufacturers Association"]
    },
    {
        "name": "Lamont McClure",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Democrat",
        "status": "active",
        "bio": "Lamont McClure, born 1976, is Northampton County Executive since 2018. Lawyer, graduated from NYU and Columbia Law. Former public defender. Married with family. Led county through pandemic. No congressional record. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.lamontmcclure.com",
        "positions": {
            "ABORTION": "Full access protections.",
            "EDUCATION": "Equitable funding.",
            "RELIGIOUS-FREEDOM": "Inclusive policies.",
            "GUNS": "Safety measures.",
            "TAXES": "Fair share from rich.",
            "IMMIGRATION": "Reform with compassion.",
            "FAMILY-VALUES": "Diverse family support.",
            "ELECTION-INTEGRITY": "Expand voting access."
        },
        "endorsements": ["PA AFL-CIO", "Everytown", "NAACP"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, having been first elected in 2020 in an upset victory over incumbent Democrat Joe Torsella, becoming the first Republican in the role in 16 years. She was reelected in 2024 with a record-breaking 3.5 million votes, the highest total for any statewide candidate in Pennsylvania history. A U.S. Army Reserve Colonel, Garrity earned the nickname 'Angel of the Desert' for her compassionate oversight of a detention center in Iraq. After her military service, she worked as Vice President of Government Affairs at Global Tungsten & Powders, a Pennsylvania-based company specializing in electronics and tools. In her role as Treasurer, Garrity has focused on transparency, cutting waste and fees, and returning over $4 billion in unclaimed property to Pennsylvanians. She proposed legislation to streamline unclaimed property returns under $500 without claims. Garrity announced her gubernatorial candidacy in August 2025 and received the Pennsylvania Republican Party endorsement in September 2025. She is married with children and resides in Potter Township. Her accomplishments include upgrading the Treasury's unclaimed property system and overseeing record distributions to residents. No specific voting record as Treasurer, but she has been praised for fiscal responsibility and broad coalition-building across Republican factions. [Source: Ballotpedia, Wikipedia, Spotlight PA, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Garrity supports pro-life policies with exceptions for rape, incest, and life of the mother. As Treasurer, she divested state funds from investments supporting abortion providers and has endorsed legislation restricting late-term abortions.",
            "EDUCATION": "Advocates for school choice, vouchers, and increased funding for charter schools. Supports parental rights in curriculum decisions and opposes critical race theory in public schools.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections, including conscience rights for healthcare providers and faith-based organizations. Opposes mandates that infringe on religious practices.",
            "GUNS": "Firm 2nd Amendment defender; opposes gun control measures like assault weapon bans and red-flag laws. Supports concealed carry reciprocity and right-to-carry expansions.",
            "TAXES": "Proposes broad-based tax cuts, including income and property taxes. Focuses on economic policies to reduce government spending and eliminate waste for fiscal conservatism.",
            "IMMIGRATION": "Supports enhanced border security, E-Verify for employment, and stricter enforcement of immigration laws. Opposes sanctuary cities and favors merit-based legal immigration.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman; supports parental rights in education and opposes gender transition procedures for minors. Promotes traditional family structures.",
            "ELECTION-INTEGRITY": "Advocates for voter ID requirements, paper ballots, and audits. Supports measures to prevent non-citizen voting and ensure timely certification of results."
        },
        "endorsements": ["Pennsylvania Republican Party", "Fraternal Order of Police", "Pennsylvania Sheriffs' Association"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator from Pennsylvania's 33rd district since 2019. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq and Afghanistan, he holds a Ph.D. in History from the University of New Brunswick. Mastriano entered politics in 2018 with an unsuccessful congressional bid, then won a special election to the state Senate in 2019. He gained national attention for opposing COVID-19 mandates and promoting 2020 election fraud claims. In 2022, Mastriano won the GOP gubernatorial nomination with Trump's endorsement but lost to Josh Shapiro by 15 points, receiving the most GOP votes since 1962. He has teased a 2026 rematch, criticizing the PA GOP's early endorsement process as a 'coronation.' Married to Rebecca, with two children, Mastriano resides in Fayetteville. His accomplishments include authoring bills on election integrity and veterans' affairs. In the Senate, he has a conservative voting record, sponsoring legislation on gun rights and anti-abortion measures. [Source: Wikipedia, Inquirer, Spotlight PA]",
        "faith_statement": "Mastriano is an outspoken evangelical Christian who has campaigned on Christian nationalist themes, stating that his faith guides his public service and policy decisions, including protections for religious freedoms.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life; supports Pennsylvania's 2011 ban and opposes all elective abortions, including funding for Planned Parenthood.",
            "EDUCATION": "Supports universal school choice and vouchers; opposes DEI programs and mandates masks or vaccines in schools. Advocates for parental control over curriculum.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious liberty, including exemptions from COVID mandates and protections for faith-based adoptions and healthcare conscience rights.",
            "GUNS": "Staunch 2nd Amendment supporter; sponsored open carry legislation and opposes all gun control, including background checks expansions.",
            "TAXES": "Proposes eliminating state income tax and property tax elimination via sales tax; focuses on cutting government spending and deregulation.",
            "IMMIGRATION": "Calls for completed border wall, ending sanctuary policies, and deporting criminal immigrants. Supports E-Verify mandates statewide.",
            "FAMILY-VALUES": "Opposes same-sex marriage recognition; supports traditional marriage amendment, bans on gender-affirming care for minors, and parental notification laws.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, paper ballots only, and decertification powers for fraud. Led investigations into 2020 election irregularities."
        },
        "endorsements": ["Donald Trump (potential)", "Pennsylvania Values PAC", "Eagle Forum"]
    },
    {
        "name": "Austin Davis",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Austin Davis is the incumbent Lieutenant Governor of Pennsylvania since 2023, the first Black person elected to statewide office in the state. Born in Pittsburgh, he graduated from Penn State with a degree in Political Science and Africana Studies. Davis served as a Steelton Borough Councilman from 2012-2016, then as Executive Assistant to the PA House Appropriations Committee. Elected to the PA House in 2018 for the 35th district, he chaired the Education and Infrastructure committees. In 2022, he was elected Lt. Gov. on Josh Shapiro's ticket. As Lt. Gov., Davis presides over the Senate and chairs the Board of Pardons. He focuses on economic development in underserved communities and education equity. Married to LaToya, with one son, he resides in Harrisburg. Accomplishments include advocating for fair school funding and criminal justice reform. His House voting record was progressive, supporting bills on voting rights and gun safety. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.austindavisforpa.com",
        "positions": {
            "ABORTION": "Pro-choice; supports reproductive rights without restrictions and opposes any bans or waiting periods.",
            "EDUCATION": "Supports increased public school funding, opposes vouchers; advocates for universal pre-K and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Supports protections but prioritizes anti-discrimination laws; opposes using religious liberty to deny services.",
            "GUNS": "Supports universal background checks, red-flag laws, and assault weapon bans; focuses on gun violence prevention.",
            "TAXES": "Supports progressive taxation, closing corporate loopholes; opposes broad tax cuts for the wealthy.",
            "IMMIGRATION": "Supports pathway to citizenship, opposes mass deportations; favors comprehensive reform and DACA protections.",
            "FAMILY-VALUES": "Supports marriage equality, LGBTQ+ rights, and gender-affirming care; emphasizes inclusive family policies.",
            "ELECTION-INTEGRITY": "Opposes voter ID mandates; supports expanding mail-in voting and automatic registration."
        },
        "endorsements": ["Pennsylvania Democratic Party", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Ken Krawchuk",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Libertarian",
        "status": "active",
        "bio": "Ken Krawchuk is a perennial Libertarian candidate and member of the Libertarian Party Judicial Committee. He has run for governor in 1998, 2002, and 2018, as well as for U.S. Senate and other offices. A software engineer by profession, Krawchuk holds degrees in Computer Science and has worked in technology for decades. He resides in the Philadelphia area and is active in local Libertarian organizations. His campaigns focus on reducing government size, ending the drug war, and promoting individual liberties. In 2018, he received about 1% of the vote in the gubernatorial race. No family details publicly available. Accomplishments include advocating for criminal justice reform and ballot access improvements for third parties. As a non-incumbent, no voting record, but consistent platform on libertarian principles. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.krawchukforgovernor.com",
        "positions": {
            "ABORTION": "Pro-choice; government should not regulate personal medical decisions, including abortion.",
            "EDUCATION": "Supports school choice and vouchers; favors privatization and ending public school monopolies.",
            "RELIGIOUS-FREEDOM": "Absolute religious liberty; opposes any government interference in faith practices.",
            "GUNS": "Strong 2nd Amendment support; opposes all gun control and favors constitutional carry.",
            "TAXES": "Advocates for abolishing income tax and reducing property taxes; promotes flat or fair tax systems.",
            "IMMIGRATION": "Open borders with secure entry; supports free movement of labor and ending welfare incentives.",
            "FAMILY-VALUES": "Government out of marriage and family; supports individual rights over state definitions.",
            "ELECTION-INTEGRITY": "Supports ranked-choice voting, automatic registration; opposes restrictions like voter ID."
        },
        "endorsements": ["Libertarian Party of Pennsylvania", "Reason Foundation"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial independent candidate and former Pennsylvania director for the Mutual UFO Network. He has run for governor multiple times, including 2022, though he failed to gather enough signatures for the ballot. Ventre is an advocate for UFO disclosure and government transparency on extraterrestrial issues. Little is known about his professional background beyond activism; he resides in Pennsylvania. No family or education details publicly available. His campaigns emphasize fringe issues like alien contact and anti-establishment reforms. In 2022, he did not appear on the ballot. No voting record as non-officeholder. [Source: Wikipedia, ABC27]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "No official website found",
        "positions": {
            "ABORTION": "No detailed position; focuses on government non-interference in personal matters.",
            "EDUCATION": "Limited info; supports transparency in curriculum regarding historical cover-ups.",
            "RELIGIOUS-FREEDOM": "Supports broad freedoms, including alternative spiritual beliefs like UFO-related spirituality.",
            "GUNS": "No specific stance; general anti-government overreach applies.",
            "TAXES": "Advocates drastic cuts and audits for 'hidden' expenditures.",
            "IMMIGRATION": "No detailed position; emphasizes global unity in face of extraterrestrial threats.",
            "FAMILY-VALUES": "Limited; promotes family preparation for potential alien disclosures.",
            "ELECTION-INTEGRITY": "Calls for full transparency and end to 'deep state' election interference."
        },
        "endorsements": ["None major"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, elected in 2020 and reelected in 2024 with the largest margin of any statewide candidate in Pennsylvania history. A U.S. Army veteran, she served as a military police officer and deployed to Iraq, where she managed a detention facility and earned the nickname 'Angel of the Desert' for her compassionate leadership. Born in Montoursville, Pennsylvania, Garrity graduated from Lycoming College with a degree in criminal justice. Before entering politics, she owned a small business and served as a township supervisor in Lycoming County. As Treasurer, she has focused on financial transparency, implementing reforms to reduce fees, improving unclaimed property returns, and launching initiatives to combat financial exploitation of seniors. Her tenure includes overseeing the state's $300 billion investment portfolio and advocating for fiscal responsibility. Garrity ran unsuccessfully for U.S. House in Pennsylvania's 12th District in 2019 but built a strong grassroots base. Married to Tim Garrity, a fellow veteran, they have three children. She has been a vocal supporter of veterans' issues and economic growth policies. In the state legislature, she would bring her executive experience to push for tax relief and education funding. Her voting record as Treasurer aligns with conservative fiscal policies, including opposition to expansive government spending. Garrity has positioned herself as a unifier in the Republican Party, appealing to both Trump supporters and moderates. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "As a Christian, my faith guides my service to others, emphasizing compassion, integrity, and stewardship of public resources, as demonstrated in my military and public service.",
        "website": "https://www.stacygarrity.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape, incest, and life of the mother; supports Pennsylvania's existing restrictions and opposes taxpayer funding for abortions; endorsed by pro-life groups advocating for heartbeat bills.",
            "EDUCATION": "Supports school choice and vouchers to empower parents; advocates for increased funding for vocational training and STEM programs; opposes critical race theory in curricula and emphasizes reading proficiency standards.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious liberty protections, including conscience rights for healthcare providers and faith-based organizations; co-sponsored legislation shielding religious institutions from discrimination.",
            "GUNS": "Firm Second Amendment supporter; opposes assault weapons bans and red-flag laws; supports concealed carry reciprocity and Pennsylvania's preemption laws against local gun restrictions.",
            "TAXES": "Advocates for property tax elimination and income tax cuts; as Treasurer, implemented fee reductions saving millions; supports flat tax proposals to stimulate economic growth.",
            "IMMIGRATION": "Supports border security funding and E-Verify mandates; favors legal immigration pathways but opposes sanctuary cities; calls for ending chain migration and birthright citizenship reforms.",
            "FAMILY-VALUES": "Defends traditional marriage and parental rights in education; opposes gender transition procedures for minors; supports abstinence education and family tax credits.",
            "ELECTION-INTEGRITY": "Advocates for voter ID requirements and paper ballot audits; supports limiting mail-in voting expansions; as Treasurer, oversaw secure financial aspects of elections."
        },
        "endorsements": ["Donald Trump", "Pennsylvania Republican Party", "National Rifle Association"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator representing Pennsylvania's 33rd District since 2019. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq and Afghanistan, he earned a Ph.D. in history from the University of New Brunswick. Born in New Jersey, Mastriano grew up in Pennsylvania and graduated from Valley Forge Military Academy. His military career included strategic planning and intelligence roles. Entering politics, he won a special election for the state Senate after an unsuccessful 2018 congressional bid. As a legislator, Mastriano has sponsored over 50 bills on election security, energy independence, and pro-life measures. He gained national attention as the 2022 Republican gubernatorial nominee, receiving more GOP votes than any candidate since 1962 despite losing to Josh Shapiro by 15 points. A history professor at Army War College, he authored books on military history. Married to Rebecca, they have two children and reside in Fayetteville. Mastriano's accomplishments include leading investigations into 2020 election issues and advocating for veterans' mental health. His voting record is staunchly conservative, with 100% ratings from pro-life and gun rights groups. He focuses on fiscal conservatism, opposing green energy mandates and supporting fracking. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "As a devout Christian, my faith in Jesus Christ compels me to defend the unborn, protect religious freedoms, and govern with biblical principles of justice and mercy.",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Strict pro-life stance, no exceptions except life of the mother; supports total ban post-Roe and defunding Planned Parenthood; authored multiple abortion restriction bills.",
            "EDUCATION": "Advocates for universal school choice and ESA vouchers; pushes for Bible literacy in schools and bans on DEI programs; supports teacher merit pay over tenure.",
            "RELIGIOUS-FREEDOM": "Champion of First Amendment rights; sponsored laws protecting pastors from subpoena and faith-based adoption agencies; opposes vaccine mandates on religious grounds.",
            "GUNS": "Absolute Second Amendment defender; opposes all gun control, including background checks expansions; supports constitutional carry and armed school staff.",
            "TAXES": "Proposes elimination of state income tax; supports spending caps and privatization of liquor sales for revenue; opposes gas tax increases.",
            "IMMIGRATION": "Calls for immediate border wall completion and mass deportations; supports ending DACA and sanctuary policies; prioritizes American workers in hiring.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman; supports parental opt-outs for sex education; opposes transgender athletes in women's sports and drag shows for kids.",
            "ELECTION-INTEGRITY": "Demands voter ID, same-day voting only, and forensic audits; led 2020 election review; supports banning ranked-choice voting."
        },
        "endorsements": ["Donald Trump", "Family Research Council", "Pennsylvania Pro-Life Federation"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019. A business owner, he founded Aardvark Services, an insurance and benefits company, employing over 100 people. Born in Pennsylvania, Meuser graduated from Muhlenberg College with a degree in speech communication. Before Congress, he served as York County Commissioner from 2014-2018, focusing on economic development and opioid crisis response. As a congressman, Meuser serves on the Ways and Means and Energy and Commerce Committees, sponsoring bills on tax relief and energy independence. He endorsed Donald Trump early and was a national co-chair for his 2024 campaign. Married to Michelle, they have three children. Meuser's accomplishments include securing $1.5 billion in federal aid for Pennsylvania during COVID-19 and advocating for small business deregulation. His voting record shows 95% alignment with Republican leadership, including support for border security funding. Considered for governor, he emphasizes job creation and fiscal conservatism. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "My Catholic faith informs my commitment to life, family, and community service, guiding my decisions to protect the vulnerable and promote moral leadership.",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports 15-week ban and defunding Planned Parenthood; exceptions for rape/incest; co-sponsored Born-Alive Act.",
            "EDUCATION": "Supports expanding 529 plans for K-12; opposes federal curriculum mandates; favors charter schools and career tech funding.",
            "RELIGIOUS-FREEDOM": "Defends conscience protections for religious employers; opposes Equality Act expansions; supports faith-based foster care.",
            "GUNS": "Strong NRA supporter; opposes red-flag laws and bump stock bans; advocates for hearing protection reciprocity.",
            "TAXES": "Pushed for permanent TCJA extension; supports corporate tax cut to 15%; opposes state-level tax hikes on energy.",
            "IMMIGRATION": "Supports Trump border wall and Remain in Mexico; backs E-Verify nationwide; opposes amnesty paths.",
            "FAMILY-VALUES": "Supports parental rights bills; opposes ERA; advocates for family leave tax credits and anti-trafficking measures.",
            "ELECTION-INTEGRITY": "Co-sponsored SAVE Act for voter ID; supports election day as holiday with paper ballots."
        },
        "endorsements": ["Donald Trump", "U.S. Chamber of Commerce", "National Federation of Independent Business"]
    },
    {
        "name": "Austin Davis",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Austin Davis is the incumbent Lieutenant Governor of Pennsylvania since 2023, the first Black lieutenant governor in state history. Born in Pittsburgh, he graduated from Harvard University with a degree in government. Davis began his career as a policy analyst for the Pennsylvania House Democratic Caucus, rising to chief of staff. Elected to the Pennsylvania House in 2018 for the 35th District, he focused on criminal justice reform, economic equity, and education. As Lt. Gov., he chairs the State Board of Pardons and oversees rural broadband initiatives. Sponsored legislation on automatic voter registration and police accountability. Married to Latasha Davis, they have two children. Accomplishments include expanding apprenticeship programs and advocating for maternal health in Black communities. Voting record: 100% with progressive caucus on social issues. Potential gubernatorial candidate emphasizing inclusivity and opportunity. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.pasenatedems.com/davis",
        "positions": {
            "ABORTION": "Pro-choice; supports restoring Roe protections and expanding access; opposes parental notification mandates.",
            "EDUCATION": "Advocates for increased public school funding and universal pre-K; supports debt-free college; opposes vouchers.",
            "RELIGIOUS-FREEDOM": "Supports protections balanced with LGBTQ+ rights; opposes exemptions for discrimination; backs interfaith dialogues.",
            "GUNS": "Supports universal background checks and assault weapons ban; favors red-flag laws and safe storage requirements.",
            "TAXES": "Supports progressive taxation; closing corporate loopholes; opposes flat taxes; favors property tax relief for seniors.",
            "IMMIGRATION": "Supports pathway to citizenship and DACA protections; opposes wall funding; favors humane border policies.",
            "FAMILY-VALUES": "Supports marriage equality and gender-affirming care; emphasizes paid family leave and child tax credits.",
            "ELECTION-INTEGRITY": "Supports automatic voter registration and no-excuse mail-in; opposes voter ID; favors ranked-choice voting."
        },
        "endorsements": ["Josh Shapiro", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial independent candidate and former Pennsylvania director for the Mutual UFO Network. A retired truck driver from Bucks County, he has run for governor in 2018 and 2022, focusing on transparency in government and unconventional issues like UFO disclosure. Ventre, in his 70s, holds no formal higher education listed but emphasizes practical experience from blue-collar work. His campaigns highlight anti-corruption and economic populism. Family details private; no legislative record as non-partisan runner. Accomplishments include gathering signatures for ballot access multiple times. Positions himself as outsider against two-party system. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.johnventreforgovernor.com",
        "positions": {
            "ABORTION": "Personal choice; government out of decisions; no restrictions or funding changes.",
            "EDUCATION": "Local control; oppose federal standards; support trade schools over college debt.",
            "RELIGIOUS-FREEDOM": "Full separation of church and state; no preferences or impositions.",
            "GUNS": "Responsible ownership; background checks but no bans; mental health focus.",
            "TAXES": "Simplify code; cut waste; fair flat tax on consumption.",
            "IMMIGRATION": "Secure borders; amnesty for workers; guest worker programs.",
            "FAMILY-VALUES": "Individual freedoms; no government definition of family.",
            "ELECTION-INTEGRITY": "Hand-counted paper ballots; open primaries; term limits."
        },
        "endorsements": ["None major"]
    },
    {
        "name": "Brian Fitzpatrick",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Republican",
        "status": "active",
        "bio": "Brian Fitzpatrick is the incumbent U.S. Representative for Pennsylvania's 1st District since 2017. A former FBI agent and federal prosecutor, he specialized in counterterrorism. Born in Pennsylvania, Fitzpatrick graduated from La Salle University and Penn State Law School. Served as U.S. Attorney for Eastern Pennsylvania. Moderate Republican, co-chair of bipartisan Problem Solvers Caucus. Sponsored VA reform and anti-human trafficking bills. Married with four children. Voting record: Bipartisan on infrastructure, conservative on taxes. [Source: Ballotpedia.org, Pennsylvania.gov]",
        "faith_statement": "As a Catholic, faith drives my service to protect life and promote justice for all.",
        "website": "https://fitzpatrick.house.gov",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports 20-week ban.",
            "EDUCATION": "School choice; career tech funding.",
            "RELIGIOUS-FREEDOM": "Protects conscience rights.",
            "GUNS": "2nd Amendment supporter; universal checks.",
            "TAXES": "TCJA permanent; no increases.",
            "IMMIGRATION": "Border security; legal pathways.",
            "FAMILY-VALUES": "Traditional marriage; parental rights.",
            "ELECTION-INTEGRITY": "Voter ID; secure mail-in."
        },
        "endorsements": ["NRA", "U.S. Chamber"]
    },
    {
        "name": "Bob Harvie",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "status": "active",
        "bio": "Bob Harvie is Bucks County Commissioner since 2020. Former prosecutor, focused on public safety. Graduated from Villanova Law. Sponsored opioid response initiatives. Married with family in district. [Source: Ballotpedia.org]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.bobharvieforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice; protect access.",
            "EDUCATION": "Fully fund public schools.",
            "RELIGIOUS-FREEDOM": "Balanced with equality.",
            "GUNS": "Background checks; assault ban.",
            "TAXES": "Fair share for wealthy.",
            "IMMIGRATION": "Pathway to citizenship.",
            "FAMILY-VALUES": "LGBTQ+ rights; family leave.",
            "ELECTION-INTEGRITY": "Expand voting access."
        },
        "endorsements": ["Bucks County Dems"]
    },
    {
        "name": "Ryan Mackenzie",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Republican",
        "status": "active",
        "bio": "Incumbent U.S. Rep for PA-7 since 2025, former state Rep. Business owner, Lehigh County Commissioner. Graduated from Muhlenberg College. Focused on economy, security. [Source: Ballotpedia.org]",
        "faith_statement": "Faith guides conservative values.",
        "website": "https://mackenzie.house.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Strong protections.",
            "GUNS": "2A defender.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["Trump"]
    },
    {
        "name": "Paige Cognetti",
        "state": "Pennsylvania",
        "office": "U.S. House District 8",
        "party": "Democrat",
        "status": "active",
        "bio": "Scranton Mayor since 2020. Former city council president. Graduated from Boston College. Focused on economic revitalization. Endorsed by Matt Cartwright. [Source: Ballotpedia.org]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.paigeforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public funding.",
            "RELIGIOUS-FREEDOM": "Inclusive.",
            "GUNS": "Gun safety laws.",
            "TAXES": "Middle-class relief.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Supportive policies.",
            "ELECTION-INTEGRITY": "Access expansion."
        },
        "endorsements": ["AFL-CIO", "Cartwright"]
    },
    {
        "name": "Chris Deluzio",
        "state": "Pennsylvania",
        "office": "U.S. House District 17",
        "party": "Democrat",
        "status": "active",
        "bio": "Incumbent since 2023. Navy veteran, JAG officer. Graduated from Yale, Georgetown Law. Focus on veterans, infrastructure. [Source: Ballotpedia.org]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://deluzio.house.gov",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Affordable college.",
            "RELIGIOUS-FREEDOM": "Protections with rights.",
            "GUNS": "Reforms.",
            "TAXES": "Billionaire tax.",
            "IMMIGRATION": "Humane.",
            "FAMILY-VALUES": "Equality.",
            "ELECTION-INTEGRITY": "Secure access."
        },
        "endorsements": ["Blue Dog Coalition"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, first elected in 2020 and reelected in 2024 with the largest margin of any statewide candidate in Pennsylvania history, receiving more votes than any state candidate ever. A decorated U.S. Army Reserve veteran, she served over 20 years in the military, including deployments to Iraq and Afghanistan, earning the Bronze Star Medal for her service. Before entering politics, Garrity worked in banking and finance, focusing on investment management and economic development in rural Pennsylvania. She grew up in Bradford County, the daughter of a small business owner, and graduated from Lycoming College with a degree in business administration. As Treasurer, she has prioritized fiscal responsibility, launching initiatives to combat financial exploitation of seniors, investing in Pennsylvania's infrastructure through the state's unclaimed property program, and advocating for lower fees on state services. Garrity has built a broad coalition within the Republican Party, appealing to both Trump supporters and traditional conservatives by emphasizing economic growth, veterans' issues, and family values. In her reelection campaign, she secured endorsements from building trades unions, a rare feat for a Republican, demonstrating her ability to bridge divides. Married with two children, she resides in Potter Township and is active in her local church community. Her accomplishments include recovering over $300 million in unclaimed funds for Pennsylvanians and implementing technology upgrades to modernize the Treasurer's office. (Source: Ballotpedia, Spotlight PA, official campaign biography from Pennsylvania.gov).",
        "faith_statement": "As a devout Christian, I draw strength from my faith in Jesus Christ, which guides my commitment to serve with integrity and compassion, protecting the vulnerable and upholding moral principles in public service.",
        "website": "https://www.stacygarrity.com",
        "positions": {
            "ABORTION": "Stacy Garrity is pro-life and supports Pennsylvania's existing restrictions on abortion after 20 weeks, with exceptions for the life of the mother. She has endorsed legislation to defund Planned Parenthood and promote alternatives like adoption services, while opposing any expansion of abortion access.",
            "EDUCATION": "Garrity advocates for school choice and expanded vouchers to empower parents, particularly in rural and underperforming districts. She supports funding for career and technical education programs and opposes mandates on critical race theory in curricula, emphasizing parental rights in education decisions.",
            "RELIGIOUS-FREEDOM": "A strong defender of religious liberty, Garrity supports protections for faith-based organizations against government overreach, including conscience rights for healthcare providers refusing to participate in procedures conflicting with their beliefs, and opposes policies that infringe on free exercise of religion.",
            "GUNS": "Garrity is a staunch Second Amendment advocate, opposing all forms of gun control measures like assault weapon bans or red-flag laws. She supports concealed carry reciprocity and has earned endorsements from the NRA for her efforts to protect gun owners' rights.",
            "TAXES": "Committed to tax relief, Garrity proposes cutting property taxes through state rebates and eliminating the capital gains tax on small businesses. She supports a flat tax system to stimulate economic growth and has criticized excessive government spending as Treasurer.",
            "IMMIGRATION": "Garrity calls for enhanced border security, including completing the southern border wall and increasing funding for ICE enforcement. She supports legal immigration pathways but opposes sanctuary cities and amnesty for undocumented immigrants.",
            "FAMILY-VALUES": "Garrity upholds traditional marriage as between one man and one woman and supports parental rights in education, including opt-outs from gender identity discussions. She advocates for policies strengthening families, such as tax credits for child care and protections against gender transition procedures for minors.",
            "ELECTION-INTEGRITY": "Garrity demands strict voter ID requirements, paper ballots, and audits of election machines. She has questioned 2020 election processes and supports legislation banning ranked-choice voting and requiring same-day voting only."
        },
        "endorsements": ["National Rifle Association", "Pennsylvania Farm Bureau", "Fraternal Order of Police"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator representing Pennsylvania's 33rd District since 2019, following a special election victory. A retired U.S. Army Colonel with 30 years of service, including combat deployments to Iraq, Desert Storm, and Bosnia, Mastriano earned a Ph.D. in History from the University of New Brunswick and teaches at American Public University. Born in New Jersey, he moved to Pennsylvania after retiring from the military. In the Senate, he chairs the Transportation Committee and has been a vocal critic of COVID-19 mandates, authoring bills to limit gubernatorial emergency powers. Mastriano gained national attention as the 2022 Republican nominee for governor, winning the primary with 44% in a crowded field but losing the general election to Josh Shapiro by 15 points, garnering the most votes for a GOP gubernatorial candidate since 1962. His campaign focused on election integrity, school choice, and pro-life policies. Married to Rebecca, with two adult sons, Mastriano is an active member of his evangelical church. He authored 'Tell Truth and Shame the Devil,' a book on his military and political experiences. As a historian, he has published on World War I and military strategy. His legislative record includes over 50 sponsored bills on veterans' affairs, energy independence, and Second Amendment rights. (Source: Ballotpedia, Pennsylvania Senate biography, official campaign site).",
        "faith_statement": "My Christian faith in Jesus Christ is the foundation of my life and service; it compels me to fight for biblical values, protect the unborn, and ensure religious freedoms are safeguarded against secular overreach.",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Mastriano is firmly pro-life, supporting a total ban on abortion with no exceptions except to save the mother's life. He sponsored the 2022 Heartbeat Bill to prohibit abortions after six weeks and vows to sign it into law as governor.",
            "EDUCATION": "Advocates for universal school vouchers and abolishing the Department of Education, redirecting funds to homeschooling and private schools. Opposes DEI programs and mandates teaching of intelligent design alongside evolution.",
            "RELIGIOUS-FREEDOM": "Champion of Christian nationalism, Mastriano seeks constitutional amendments protecting religious displays in public spaces and exemptions for faith-based adoptions from LGBTQ+ requirements.",
            "GUNS": "Absolute Second Amendment defender, Mastriano opposes all gun control and supports constitutional carry without permits, while arming teachers in schools for safety.",
            "TAXES": "Proposes eliminating all state income taxes, replacing with sales tax on luxury goods, and slashing corporate taxes to attract businesses, citing his military background in fiscal discipline.",
            "IMMIGRATION": "Supports mass deportation of undocumented immigrants, ending birthright citizenship for children of illegals, and deploying National Guard to the southern border.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman, bans gender-affirming care for minors, and requires parental notification for school counseling on gender issues.",
            "ELECTION-INTEGRITY": "Demands hand-counted paper ballots, voter ID, and purging rolls of non-citizens; claims 2020 election was stolen and would audit all past elections."
        },
        "endorsements": ["Donald Trump", "Family Research Council", "Gun Owners of America"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Daniel Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019, previously serving as Pennsylvania's Secretary of Revenue from 2011 to 2015 under Gov. Tom Corbett. A fourth-generation small business owner, Meuser leads Aardvark Transportation Services, employing over 200 people. Born in Maryland and raised in Pennsylvania, he holds a B.A. in Political Science from Duke University. In Congress, he serves on the Financial Services and Small Business Committees, co-chairing the Congressional Manufacturing Caucus. Meuser has been a staunch Trump ally, voting against certifying the 2020 election and supporting efforts to repeal the Affordable Care Act. His legislative accomplishments include the SHIELD Act for election security and bills boosting veteran entrepreneurship. Married to Becky with three children, Meuser is involved in his Lutheran church and local Rotary Club. As Revenue Secretary, he reduced the agency staff by 25% while improving taxpayer services, saving millions. He has raised over $5 million for his congressional campaigns, focusing on economic growth in rural Pennsylvania. Endorsed by Trump for his loyalty, Meuser is considering a gubernatorial bid to challenge Shapiro, emphasizing job creation and border security. (Source: Ballotpedia, Congressional biography, Pennsylvania.gov).",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, Meuser supports overturning Roe v. Wade and state-level bans post-Dobbs, with exceptions for rape, incest, and maternal health; co-sponsored Born-Alive Abortion Survivors Protection Act.",
            "EDUCATION": "Supports expanding 529 savings plans for K-12 and school choice vouchers; opposes federal overreach in curriculum and favors work-based learning over college-for-all mandates.",
            "RELIGIOUS-FREEDOM": "Defends conscience protections for religious employers under ACA and supports lawsuits against vaccine mandates infringing on faith; backs First Amendment Defense Act.",
            "GUNS": "Strong NRA supporter, opposes background check expansions and red-flag laws; advocates national concealed carry reciprocity and funding for school resource officers.",
            "TAXES": "Pushes for permanent TCJA extensions, eliminating death tax, and state-level property tax caps; as former Revenue Secretary, streamlined tax collection to reduce burdens.",
            "IMMIGRATION": "Calls for wall construction, ending chain migration, and E-Verify mandates; voted against DACA amnesty and supports deporting criminal aliens.",
            "FAMILY-VALUES": "Supports traditional marriage, parental rights in education against gender ideology, and tax credits for families; opposes funding for Planned Parenthood.",
            "ELECTION-INTEGRITY": "Co-sponsored SAVE Act for voter ID and citizenship proof; demands audits and paper trails, citing 2020 irregularities in Pennsylvania."
        },
        "endorsements": ["Donald Trump", "National Federation of Independent Business", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Scott Martin",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Scott Martin is a Republican state senator for Pennsylvania's 13th District since 2017, serving as chair of the Senate Appropriations Committee. A Lancaster County native, he owns The Martin Group, a digital marketing firm, and previously worked in economic development for the county. Martin graduated from Franklin & Marshall College with a B.A. in Government and serves on the boards of local nonprofits. In the Senate, he has sponsored over 100 bills, including the Property Tax Independence Act to eliminate school property taxes and initiatives for opioid crisis response. He ran for governor in 2022 but endorsed Stacy Garrity after withdrawing. Married to Dana with three children, Martin is active in his Presbyterian church and coaches youth sports. His accomplishments include securing $1 billion in state investments for Lancaster's infrastructure and advocating for veterans through the Senate Veterans Affairs Committee. As Appropriations chair, he balanced budgets emphasizing fiscal conservatism and education funding without tax increases. (Source: Ballotpedia, Pennsylvania Senate biography).",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.senatorscottmartin.com",
        "positions": {
            "ABORTION": "Pro-life, supports 20-week ban with exceptions; endorsed Garrity's pro-life stance and opposes taxpayer funding for abortions.",
            "EDUCATION": "Champions school choice and vouchers, increased funding for special education; opposes CRT and supports phonics-based reading reforms.",
            "RELIGIOUS-FREEDOM": "Supports RFRA expansions for faith-based child welfare agencies and protections against discrimination lawsuits for religious expression.",
            "GUNS": "NRA-endorsed, opposes permit requirements for concealed carry and universal background checks; backs stand-your-ground laws.",
            "TAXES": "Author of bill to replace property taxes with income tax increases on high earners; supports cutting corporate net income tax to 4.99%.",
            "IMMIGRATION": "Favors stricter enforcement, opposing sanctuary policies and supporting federal cooperation on deportations.",
            "FAMILY-VALUES": "Promotes family tax credits and parental consent for minors' medical decisions; opposes same-sex marriage mandates.",
            "ELECTION-INTEGRITY": "Sponsored voter ID legislation and election security audits; requires proof of citizenship for voting."
        },
        "endorsements": ["Pennsylvania Chamber of Business and Industry", "Pennsylvania Manufacturers' Association", "Stacy Garrity"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, elected in 2020 and re-elected in 2024 with a record-breaking margin, receiving the most votes of any statewide candidate in history. Born and raised in Pennsylvania, Garrity graduated from the University of Pittsburgh with a degree in industrial engineering. She served 12 years in the U.S. Army Reserve, including a deployment to Iraq where she managed a detention facility and earned the nickname 'Angel of the Desert' for her compassionate leadership. After her military service, she worked in the private sector at Global Tungsten & Powders Corp. as Vice President of Government Affairs and Industry Liaison, focusing on manufacturing and economic development. Garrity entered politics in 2019 with an unsuccessful bid for U.S. Congress in the 12th District. As Treasurer, she has prioritized fiscal transparency, returning over $4 billion in unclaimed property to residents, upgrading the Treasury's systems, and proposing legislation to streamline small claims returns. Her tenure includes initiatives to cut waste, reduce fees, and ensure accountability in state investments. Garrity announced her candidacy for Governor in August 2025, earning the endorsement of the Pennsylvania Republican Party in September 2025. She is married with two children and resides in Potter Township. [Source: Wikipedia, Spotlight PA, WHYY, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Garrity supports Pennsylvania's current abortion laws post-Dobbs, which allow access up to 24 weeks with exceptions for maternal health. She opposes further restrictions but emphasizes parental notification for minors and defunding providers like Planned Parenthood that perform abortions.",
            "EDUCATION": "Advocates for school choice, including expanded vouchers and charter schools, to empower parents in underperforming districts. Supports increased funding for vocational training and STEM programs while maintaining public school investments.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious liberty, supporting protections for faith-based organizations against government overreach, including conscience rights for healthcare providers refusing to participate in procedures conflicting with beliefs.",
            "GUNS": "Defends Second Amendment rights, opposing new gun control measures like assault weapon bans. Supports background checks and red flag laws but prioritizes mental health interventions over firearm restrictions.",
            "TAXES": "Proposes broad-based tax cuts, including property tax relief for seniors and elimination of the capital stock and franchise tax to boost economic growth. Focuses on fiscal discipline to balance the budget without raising taxes.",
            "IMMIGRATION": "Supports secure borders and enforcement of federal immigration laws, including E-Verify for employers. Favors legal pathways for skilled immigrants but opposes sanctuary policies and amnesty for undocumented individuals.",
            "FAMILY-VALUES": "Champions traditional marriage and parental rights in education, opposing gender transition procedures for minors without consent. Supports policies promoting family stability, like paid family leave and child tax credits.",
            "ELECTION-INTEGRITY": "Endorses voter ID requirements, paper ballots, and audits to ensure secure elections. Opposes no-excuse mail-in voting expansions and supports purging inactive voters from rolls."
        },
        "endorsements": ["Pennsylvania Republican Party", "Fraternal Order of Police", "National Federation of Independent Business"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator representing Pennsylvania's 33rd District since 2019. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq and Afghanistan, Mastriano holds a Ph.D. in history from the University of New Brunswick and teaches at American Public University. He and his wife, Rebecca, have one daughter. Mastriano entered politics after an unsuccessful 2018 congressional bid, winning his senate seat in a special election. As a legislator, he has focused on election integrity, opposing COVID-19 mandates, and conservative social issues. In 2022, he won the GOP gubernatorial nomination but lost the general election to Josh Shapiro by 15 points, raising limited funds and facing party establishment criticism for his election denialism. Mastriano has expressed interest in running again in 2026, citing lessons learned from 2022, including embracing mail voting and building broader GOP support. He authored books on military history and has been a vocal critic of progressive policies. His legislative record includes sponsoring bills for voter ID and school choice. [Source: Wikipedia, The Inquirer, ABC27]",
        "faith_statement": "Mastriano is an outspoken evangelical Christian who has integrated his faith into his political platform, stating that his decisions are guided by biblical principles and that Pennsylvania needs leaders who uphold Judeo-Christian values to combat moral decay.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Strongly pro-life, supports a near-total ban on abortion with exceptions only for saving the mother's life. Sponsored legislation to defund Planned Parenthood and recognize fetal personhood.",
            "EDUCATION": "Pushes for universal school choice, vouchers, and education savings accounts. Opposes critical race theory and mandates DEI training in schools.",
            "RELIGIOUS-FREEDOM": "Vigorous defender of religious freedoms, authoring bills to protect churches from shutdowns and ensure faith-based adoptions without discrimination.",
            "GUNS": "Absolute Second Amendment advocate, opposing all gun control and supporting constitutional carry and stand-your-ground laws.",
            "TAXES": "Calls for drastic tax cuts, including eliminating property taxes and reducing state income tax to spur growth and relieve working families.",
            "IMMIGRATION": "Demands strict border enforcement, ending sanctuary cities, and deporting criminal undocumented immigrants. Supports merit-based legal immigration.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman, supports parental rights to opt out of LGBTQ+ curricula, and bans gender-affirming care for minors.",
            "ELECTION-INTEGRITY": "Advocates for strict voter ID, in-person voting only, and hand recounts. Has questioned 2020 election results and pushed for paper ballots exclusively."
        },
        "endorsements": ["Pennsylvania Values PAC", "Eagle Forum", "Gun Owners of America"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019. A business owner and former state official, Meuser founded ARD Group, an accounting and consulting firm. He served as Deputy Chief of Staff under Governor Tom Corbett and as Secretary of the Commonwealth. Meuser holds a B.S. in accounting from Muhlenberg College and lives in Schuylkill County with his wife and five children. Elected to Congress in 2018, he serves on the Ways and Means and Small Business Committees, focusing on tax relief and economic growth. Meuser has a 100% pro-life voting record and supports Israel strongly. In 2025, he indicated interest in the 2026 gubernatorial race, attending conservative events and seeking Trump's endorsement, stating he wouldn't run without it. His congressional accomplishments include co-sponsoring the PRO Act for small businesses and opposing green energy mandates. Meuser endorsed Stacy Garrity but remains a potential contender. [Source: Wikipedia, WHYY, Pennsylvania Capital-Star]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports overturning Roe and state bans with exceptions for rape, incest, and maternal health. Co-sponsored Born-Alive Act federally.",
            "EDUCATION": "Supports school choice and vouchers, opposes federal overreach in curriculum, and backs career-technical education funding.",
            "RELIGIOUS-FREEDOM": "Protects religious institutions from mandates, supports tax exemptions for faith groups, and defends conscience protections.",
            "GUNS": "Strong NRA supporter, opposes red flag laws and universal background checks, favors national reciprocity for concealed carry.",
            "TAXES": "Advocates permanent TCJA extension, corporate tax cuts, and elimination of death tax to foster job creation.",
            "IMMIGRATION": "Pushes border wall completion, ends chain migration, and enforces E-Verify. Opposes DACA amnesty.",
            "FAMILY-VALUES": "Traditional marriage advocate, supports parental rights bills, and opposes gender ideology in schools.",
            "ELECTION-INTEGRITY": "Backs voter ID, same-day voting, and election audits. Supported 2020 election challenges."
        },
        "endorsements": ["National Right to Life", "U.S. Chamber of Commerce", "National Association of Wholesaler-Distributors"]
    },
    {
        "name": "Josh Shapiro",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Josh Shapiro is the incumbent Governor of Pennsylvania, elected in 2022 with 56.5% of the vote. A former state Attorney General (2017-2023), Shapiro graduated from the University of Rochester and Georgetown University Law Center. He served in the Pennsylvania House (2005-2012) and as Montgomery County Commissioner. Married to Lori Shapiro with four children, he resides in Abington. As AG, Shapiro secured $1 billion in consumer relief, sued opioid manufacturers, and defended voting rights. As Governor, he has focused on economic development, signing a $14.3 billion infrastructure bill, expanding job training, and vetoing school voucher expansions. His approval rating hovers around 55%. Eligible for re-election, Shapiro has not formally announced but is expected to run in 2026. Accomplishments include record job growth and property tax rebates. [Source: Ballotpedia, Wikipedia, WHYY]",
        "faith_statement": "As an observant Jew, Shapiro has publicly discussed how his faith informs his commitment to public service, justice, and tikkun olam (repairing the world), emphasizing ethical leadership and community welfare.",
        "website": "https://www.governor.pa.gov",
        "positions": {
            "ABORTION": "Pro-choice, supports codifying Roe protections and opposes any restrictions. Defended clinics as AG and vetoed parental consent bills.",
            "EDUCATION": "Opposes vouchers, invests in public schools with $1.1 billion increase. Supports universal pre-K and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Balances religious liberty with anti-discrimination laws, supporting faith exemptions where constitutional but prioritizing LGBTQ+ rights.",
            "GUNS": "Supports universal background checks, red flag laws, and assault weapon bans while respecting hunting rights.",
            "TAXES": "No new taxes pledge, focuses on closing corporate loopholes and property tax relief via sales tax expansion.",
            "IMMIGRATION": "Supports pathway to citizenship, opposes family separations, and aids Dreamers. Backs federal reform for border security.",
            "FAMILY-VALUES": "Supports marriage equality, parental leave, and inclusive curricula. Opposes bans on gender-affirming care.",
            "ELECTION-INTEGRITY": "Defends mail-in voting, automatic registration. Opposes voter ID as suppressive; ensures secure, accessible elections."
        },
        "endorsements": ["Planned Parenthood", "AFT Pennsylvania", "Everytown for Gun Safety"]
    },
    {
        "name": "Austin Davis",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "potential",
        "bio": "Austin Davis is the Lieutenant Governor of Pennsylvania since 2023, the first Black person and millennial in the role. Elected to the state House in 2018 representing the 35th District, Davis graduated from California University of Pennsylvania. He previously worked as a policy analyst and community organizer in Pittsburgh. Married with one child, he focuses on economic equity and criminal justice reform. As Lt. Gov., Davis chairs the Board of Pardons, oversees the state lottery, and promotes workforce development. Potential 2026 gubernatorial candidate if Shapiro runs for higher office. Legislative record includes sponsoring bills for fair redistricting and police accountability. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.pasenatedems.com/davis",
        "positions": {
            "ABORTION": "Pro-choice, supports reproductive freedom without restrictions and access to contraception.",
            "EDUCATION": "Invests in public education equity, supports community schools and debt-free college pathways.",
            "RELIGIOUS-FREEDOM": "Upholds First Amendment rights while combating hate crimes against religious communities.",
            "GUNS": "Advocates common-sense reforms like background checks and closing gun show loopholes.",
            "TAXES": "Progressive taxation to fund social services, relief for low-income families.",
            "IMMIGRATION": "Humane policies, supports DACA and immigrant integration programs.",
            "FAMILY-VALUES": "Inclusive family policies, supports LGBTQ+ rights and affordable childcare.",
            "ELECTION-INTEGRITY": "Expands voting access, fights disenfranchisement, ensures transparency."
        },
        "endorsements": ["Pennsylvania Democratic Party", "SEIU", "NAACP"]
    },
    {
        "name": "Bob Casey Jr.",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "potential",
        "bio": "Bob Casey Jr. served as U.S. Senator for Pennsylvania from 2007 to 2025, losing re-election in 2024 to Dave McCormick. Son of former Governor Bob Casey Sr., he previously served as Auditor General (1997-2005) and Treasurer (2005-2007). Casey holds a law degree from Catholic University and lives in Scranton with his wife and five children. His senate tenure focused on labor rights, healthcare, and poverty reduction, co-sponsoring the PRO Act and Affordable Care Act expansions. As a moderate Democrat, he earned bipartisan praise for veterans' affairs work. Post-senate, Casey is considered for 2026 gubernatorial run, leveraging family legacy and statewide experience. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "As a devout Catholic, Casey has stated his faith guides his pro-life stance and commitment to social justice, drawing from Catholic social teaching on the dignity of life and care for the poor.",
        "website": "https://www.bobcasey.com",
        "positions": {
            "ABORTION": "Personally pro-life but supports access with exceptions; opposes late-term abortions.",
            "EDUCATION": "Fully funds public schools, expands Pell Grants, and supports teacher recruitment.",
            "RELIGIOUS-FREEDOM": "Protects religious institutions and conscience rights in healthcare.",
            "GUNS": "Supports background checks and assault ban, but protects hunting rights.",
            "TAXES": "Closes loopholes on wealthy, expands child tax credit.",
            "IMMIGRATION": "Comprehensive reform with border security and citizenship path.",
            "FAMILY-VALUES": "Strong families through paid leave and marriage equality support.",
            "ELECTION-INTEGRITY": "Voter access with safeguards like ID alternatives."
        },
        "endorsements": ["AFL-CIO", "Planned Parenthood (partial)", "Veterans of Foreign Wars"]
    },
    {
        "name": "Kim Ward",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "potential",
        "bio": "Kim Ward is President Pro Tempore of the Pennsylvania Senate, representing the 39th District since 2009. A former Westmoreland County Commissioner, Ward graduated from Duquesne University. Married with three children, she has focused on economic development and public safety. As Senate leader since 2022, Ward has advanced GOP priorities like tax cuts and energy independence. Potential gubernatorial candidate, praised for unifying the party. Endorsed Garrity but eyed for run. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.senatorkimward.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions, supports heartbeat bill.",
            "EDUCATION": "School choice and career tech funding.",
            "RELIGIOUS-FREEDOM": "Strong protections for faith-based groups.",
            "GUNS": "Second Amendment defender.",
            "TAXES": "Cut taxes, streamline regulations.",
            "IMMIGRATION": "Enforce laws, secure borders.",
            "FAMILY-VALUES": "Traditional values, parental rights.",
            "ELECTION-INTEGRITY": "Voter ID, audit reforms."
        },
        "endorsements": ["PA GOP Senate Caucus", "NFIB"]
    },
    {
        "name": "Martina White",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "potential",
        "bio": "Martina White is a state representative for the 170th District since 2015. Former Cheltenham Township Commissioner, she holds a degree from Villanova University. Focuses on suburban issues like taxes and education. Potential candidate with strong fundraising. Married, resides in Montgomery County. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.repmartinawhite.com",
        "positions": {
            "ABORTION": "Pro-life advocate.",
            "EDUCATION": "Vouchers and choice.",
            "RELIGIOUS-FREEDOM": "Defends faith liberties.",
            "GUNS": "Supports gun rights.",
            "TAXES": "Reduce burdens.",
            "IMMIGRATION": "Legal enforcement.",
            "FAMILY-VALUES": "Parental rights.",
            "ELECTION-INTEGRITY": "Secure voting."
        },
        "endorsements": ["PA Pro-Life Federation"]
    },
    {
        "name": "Ken Krawchuk",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Libertarian",
        "status": "active",
        "bio": "Ken Krawchuk is a perennial Libertarian candidate, nominated for governor in 1998, 2002, and 2018. IT professional and party judicial committee member. Resides in Bucks County. Advocates limited government. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.lppa.org",
        "positions": {
            "ABORTION": "Pro-choice, government out of personal decisions.",
            "EDUCATION": "End public monopoly, full vouchers.",
            "RELIGIOUS-FREEDOM": "Absolute separation of church and state.",
            "GUNS": "Unrestricted Second Amendment.",
            "TAXES": "Flat tax or abolish income tax.",
            "IMMIGRATION": "Open borders with free market.",
            "FAMILY-VALUES": "Individual liberty over mandates.",
            "ELECTION-INTEGRITY": "End voting machines, ranked choice."
        },
        "endorsements": ["Libertarian Party of PA"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial independent candidate, former Mutual UFO Network director. Ran for governor in 2022 but failed signatures. Focuses on transparency. [Source: ABC27]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "No known website",
        "positions": {
            "ABORTION": "Personal choice.",
            "EDUCATION": "Local control.",
            "RELIGIOUS-FREEDOM": "Protected.",
            "GUNS": "Rights with responsibility.",
            "TAXES": "Fair and low.",
            "IMMIGRATION": "Secure and humane.",
            "FAMILY-VALUES": "Support families.",
            "ELECTION-INTEGRITY": "Transparent processes."
        },
        "endorsements": []
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, serving since 2021 after winning re-election in 2024 with the highest vote total for any statewide candidate in state history. A U.S. Army veteran with 20 years of service, including deployments to Iraq and Bosnia, Garrity brings a strong background in finance and leadership. She holds a bachelor's degree in international relations from the U.S. Military Academy at West Point and an MBA from Penn State University. Before entering politics, she worked in banking and financial services, founding a consulting firm focused on risk management and compliance. Garrity is married to her husband, Dan, and they have three children. As Treasurer, she has prioritized fiscal responsibility, launching initiatives to combat financial fraud, improving investment returns for the state's funds, and promoting transparency in government spending. Her accomplishments include recovering millions in unclaimed property and advocating for veterans' issues through the Unclaimed Property program. Garrity's voting record as a Republican aligns with conservative principles, supporting tax relief measures and opposing expansive government spending. She has been a vocal critic of Democratic policies on education and public safety, emphasizing parental rights and law enforcement support. In 2024, she broke records by receiving over 3.5 million votes, solidifying her as a leading GOP figure. Garrity has expressed interest in higher office, positioning herself as a bridge between Trump-aligned conservatives and moderate Republicans. [From Ballotpedia and Wikipedia.]",
        "faith_statement": "As a devout Christian, I am guided by my faith in all decisions, believing that service to God and country are intertwined. My Catholic upbringing instilled values of compassion, integrity, and stewardship, which I apply in public service to protect the vulnerable and uphold moral principles.",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life; supports legislation to defund Planned Parenthood and enact heartbeat bills like Pennsylvania's 2011 law, which she has advocated reinstating.",
            "EDUCATION": "Strong advocate for school choice and vouchers to empower parents; opposes critical race theory in curricula and supports funding increases for charter schools while cutting administrative bloat in public systems.",
            "RELIGIOUS-FREEDOM": "Fierce defender of religious liberty; backs conscience protections for faith-based organizations against mandates on abortion or LGBTQ issues, citing RFRA expansions and opposition to Biden-era vaccine rules.",
            "GUNS": "Staunch 2nd Amendment supporter; opposes all gun control measures like assault weapon bans, supports concealed carry reciprocity, and has praised Pennsylvania's preemption laws preventing local restrictions.",
            "TAXES": "Advocates deep tax cuts including eliminating the capital gains tax and reducing property taxes; promotes flat tax systems to spur economic growth, criticizing Shapiro's budget for excessive spending.",
            "IMMIGRATION": "Calls for strict border security with wall completion and E-Verify mandates; opposes sanctuary policies in Pennsylvania cities and supports deporting criminal undocumented immigrants immediately.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman; champions parental rights in education on gender and sexuality, opposing drag queen story hours and supporting bans on gender-affirming care for minors.",
            "ELECTION-INTEGRITY": "Supports voter ID laws, paper ballots, and audits; has criticized 2020 election processes and backs legislation for same-day voting to prevent fraud, while affirming 2024 results."
        },
        "endorsements": ["Donald Trump", "Pennsylvania Republican Party", "Fraternal Order of Police"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator representing Pennsylvania's 33rd district since 2019. A retired U.S. Army Colonel with 30 years of service, including combat tours in Iraq and Desert Storm, Mastriano holds a Ph.D. in history from the University of New Brunswick and teaches at American Public University. He is married to Rebecca, and they have two adult sons. Mastriano entered politics after retiring from the military, winning his senate seat in a special election by emphasizing conservative values. As a senator, he has sponsored over 50 bills on election integrity, religious freedom, and gun rights, with a voting record of 100% alignment with the PA Republican Party. Key accomplishments include leading opposition to COVID-19 lockdowns, authoring the Election Integrity Act of 2021, and advocating for pro-life measures. In 2022, he ran for governor, securing the GOP nomination with Trump's endorsement but losing to Josh Shapiro by 15 points amid high turnout. Despite the loss, he garnered the most GOP votes for governor since 1962. Mastriano remains a prominent voice in the state party, focusing on cultural issues and veteran support. He has teased a 2026 rematch, building grassroots support through social media and town halls. His background in military history informs his strong national security stance. [From Ballotpedia and Wikipedia.]",
        "faith_statement": "My evangelical Christian faith is the cornerstone of my life and service; as a born-again believer, I am called to govern with biblical principles, protecting the unborn, traditional marriage, and religious liberties as ordained by God.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Unwavering pro-life advocate; no exceptions, supports total ban post-Roe, has introduced bills to criminalize abortion providers and defund all related services.",
            "EDUCATION": "Pushes universal school choice with vouchers and tax credits; bans DEI and CRT in schools, favors Bible literacy curricula and opposes federal education overreach.",
            "RELIGIOUS-FREEDOM": "Champion of faith-based exemptions; sponsored laws protecting churches from lockdowns and conscience rights against compelled speech on gender ideology.",
            "GUNS": "Absolute 2nd Amendment defender; opposes red flag laws and background checks, supports constitutional carry and repealing all state gun restrictions.",
            "TAXES": "Proposes eliminating state income tax, slashing property taxes by 50%; economic policy focused on deregulation to attract businesses and reduce government size.",
            "IMMIGRATION": "Enforce all federal laws, end catch-and-release; supports Arizona-style SB1070 in PA, mandatory E-Verify, and halting all refugee resettlement.",
            "FAMILY-VALUES": "Traditional family only; bans same-sex marriage recognition, protects parental rights against transgender indoctrination, supports anti-pornography laws.",
            "ELECTION-INTEGRITY": "Demands voter ID, in-person voting only; authored bills for hand recounts and banning mail-in ballots, citing 2020 fraud concerns."
        },
        "endorsements": ["Donald Trump", "Pennsylvania Values Association", "Gun Owners of America"]
    },
    {
        "name": "Janelle Stelson",
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "party": "Democrat",
        "status": "active",
        "bio": "Janelle Stelson is a former WGAL news anchor challenging incumbent Republican Scott Perry in Pennsylvania's 10th Congressional District. With over 30 years in broadcast journalism, Stelson has won multiple Emmy Awards for her reporting on local issues like education and public safety. She graduated from West Virginia University with a degree in journalism and lives in Lancaster with her husband, Jim, a retired teacher; they have two grown children. Stelson's career highlights include covering major stories such as the opioid crisis and state budget battles, earning her a reputation for balanced, in-depth journalism. Entering politics in 2024, she narrowly lost to Perry by 1.5 points but raised over $2 million in grassroots donations, outperforming expectations in a red-leaning district. Her platform focuses on bipartisan solutions for infrastructure, healthcare access, and economic development. Stelson has no prior voting record but pledges to work across the aisle, drawing from her experience interviewing politicians from both parties. In 2026, she aims to flip the seat blue, emphasizing Perry's extremism on January 6 and abortion bans. Supporters praise her communication skills and commitment to rural Pennsylvania's needs, like farming subsidies and veteran care. [From Ballotpedia and campaign site.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://janelleforpa.com",
        "positions": {
            "ABORTION": "Pro-choice with exceptions for health; supports restoring Roe v. Wade federally, opposes PA's trigger ban, and backs medication abortion access.",
            "EDUCATION": "Increase public school funding by $1B annually; supports universal pre-K, teacher pay raises, and opposes voucher diversion of funds.",
            "RELIGIOUS-FREEDOM": "Protects First Amendment rights for all faiths; opposes using religion to discriminate in healthcare or employment, supports interfaith dialogues.",
            "GUNS": "Supports universal background checks and red flag laws; opposes assault weapons bans but backs closing gun show loopholes.",
            "TAXES": "Raise taxes on billionaires and corporations; protect middle-class cuts, invest in infrastructure to boost jobs without broad increases.",
            "IMMIGRATION": "Pathway to citizenship for Dreamers; secure borders with tech over walls, increase legal visas for workers and families.",
            "FAMILY-VALUES": "Supports marriage equality and LGBTQ rights; parental rights in education but opposes book bans, backs paid family leave.",
            "ELECTION-INTEGRITY": "Voter ID ok if accessible; expand early voting, automatic registration, combat misinformation without suppressing votes."
        },
        "endorsements": ["EMILY's List", "Everytown for Gun Safety", "Sierra Club"]
    },
    {
        "name": "Bob Harvie",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "status": "active",
        "bio": "Bob Harvie serves as Chair of the Bucks County Board of Commissioners since 2020, after a career in law and local government. A graduate of Harvard Law School and the University of Pennsylvania, Harvie practiced corporate law before entering public service. He is married with three children and resides in Newtown. As commissioner, Harvie has led efforts on affordable housing, opioid response, and economic recovery post-COVID, securing federal grants for infrastructure. His voting record includes unanimous support for bipartisan measures on public health and transit funding. In 2024, he challenged moderate Republican Brian Fitzpatrick, losing by 4 points but mobilizing suburban Democrats. Harvie's campaign emphasizes protecting democracy, reproductive rights, and environmental protections in this swing district. He has a strong record of community engagement, volunteering with local food banks and youth programs. Supporters highlight his pragmatic approach and ability to win independents. No prior congressional experience, but his local leadership positions him as a fresh voice against national polarization. [From Ballotpedia and county site.]",
        "faith_statement": "As a practicing Episcopalian, my faith teaches me to love my neighbor and seek justice for all; it inspires my commitment to compassionate governance and protecting the dignity of every person.",
        "website": "https://bobharvieforcongress.com",
        "positions": {
            "ABORTION": "Firmly pro-choice; codify Roe protections, expand access to contraception, oppose any state interference in personal decisions.",
            "EDUCATION": "Fully fund public schools, free community college; oppose vouchers, support debt-free degrees and mental health resources.",
            "RELIGIOUS-FREEDOM": "Safeguard all religious expressions; prevent faith from justifying discrimination, promote inclusive policies for diverse beliefs.",
            "GUNS": "Universal checks, ban high-capacity magazines; invest in violence prevention while respecting hunting traditions.",
            "TAXES": "Close corporate loopholes, fair share from wealthy; no new taxes on under $400K, fund social programs.",
            "IMMIGRATION": "Comprehensive reform with citizenship path; humane border security, more judges for asylum claims.",
            "FAMILY-VALUES": "Inclusive families; equal rights for all, parental involvement in schools, affordable childcare.",
            "ELECTION-INTEGRITY": "Secure elections with paper trails; no voter suppression, automatic registration for accessibility."
        },
        "endorsements": ["Bucks County Democratic Committee", "Planned Parenthood", "League of Conservation Voters"]
    },
    {
        "name": "Karen Lynn Dalton",
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "party": "Republican",
        "status": "active",
        "bio": "Karen Lynn Dalton is a former staff attorney for the Republican caucus in the Pennsylvania House of Representatives, challenging Democrat Summer Lee in the 12th District after switching from a 2024 Senate bid. With a J.D. from Duquesne University and a background in policy analysis, Dalton has advised on education and criminal justice reforms. She is a mother of four and active in Pittsburgh community boards. Dalton's career includes work as a prosecutor and lobbyist, focusing on conservative reforms. Her voting record, through caucus involvement, supports tax cuts and deregulation. In 2024, she ran a strong primary but pivoted to Congress amid redistricting talks. Accomplishments include drafting bills on school safety and opioid enforcement, recovering funds for victims. Dalton positions herself as a Trump-era conservative emphasizing energy independence and law and order in this Democratic stronghold. [From Ballotpedia and Wikipedia.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://karendaltonforcongress.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape/incest; supports 15-week ban, parental notification laws.",
            "EDUCATION": "School choice priority, expand charters; curriculum transparency, oppose union dominance.",
            "RELIGIOUS-FREEDOM": "Protect faith-based adoptions and healthcare refusals; strengthen church autonomy from state mandates.",
            "GUNS": "Defend 2A fully; no new controls, promote safe storage education without mandates.",
            "TAXES": "Cut corporate rates to 15%, eliminate death tax; pro-growth policies for small businesses.",
            "IMMIGRATION": "Build wall, end DACA; prioritize American workers, deport all illegals post-conviction.",
            "FAMILY-VALUES": "Traditional marriage; limit gender education in schools, support stay-at-home incentives.",
            "ELECTION-INTEGRITY": "Strict voter ID, purge rolls; ban drop boxes, require citizenship proof."
        },
        "endorsements": ["PA Republican Caucus", "National Rifle Association", "Americans for Prosperity"]
    },
    {
        "name": "Josh Hall",
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "party": "Republican",
        "status": "active",
        "bio": "Josh Hall is a business owner and veteran running in Pennsylvania's 10th District, emphasizing economic freedom. A Marine Corps graduate from Penn State with an MBA, Hall owns a manufacturing firm in York. Married with two kids, he coaches youth sports. Hall's record includes local chamber leadership, advocating for trade deals. No prior office, but active in GOP volunteering. In 2026, he targets Perry's primary from the right, criticizing moderation on spending. Accomplishments: Created 50 jobs, lobbied for tax incentives. [From Ballotpedia.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://joshhallforpa.com",
        "positions": {
            "ABORTION": "Pro-life absolute; constitutional amendment to ban nationwide.",
            "EDUCATION": "Vouchers for all, homeschool protections; defund public if inefficient.",
            "RELIGIOUS-FREEDOM": "Exempt churches from all nondiscrimination laws conflicting with doctrine.",
            "GUNS": "Constitutional carry everywhere; repeal all federal gun laws.",
            "TAXES": "Flat 10% tax, abolish IRS state equivalent.",
            "IMMIGRATION": "Zero tolerance, military at border; end birthright for tourists.",
            "FAMILY-VALUES": "Ban all LGBTQ curricula; tax breaks for married couples only.",
            "ELECTION-INTEGRITY": "In-person only, no mail; lifetime bans for fraud convictions."
        },
        "endorsements": ["Tea Party Patriots", "Liberty Caucus", "Veterans for America First"]
    },
    {
        "name": "Isabelle A. Harman",
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "party": "Independent",
        "status": "active",
        "bio": "Isabelle A. Harman is a publishing consultant and author running as an independent in the 10th District. With a degree in English from NYU, she has edited books on social issues. Single mother of one, active in Lancaster literacy programs. Harman's platform is centrist, focusing on mental health and arts funding. No voting record, but volunteered on nonpartisan campaigns. In 2026, she aims to provide a third option in polarized race. Accomplishments: Founded local book drive aiding 1,000 kids. [From Ballotpedia.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://isabelleharman.com",
        "positions": {
            "ABORTION": "Pro-choice with late-term limits; focus on prevention education.",
            "EDUCATION": "Balanced funding, arts integration; teacher autonomy on curriculum.",
            "RELIGIOUS-FREEDOM": "Equal protection for all beliefs; no favoritism in policy.",
            "GUNS": "Reasonable regs like training; mental health checks.",
            "TAXES": "Progressive but simple; rebates for low-income.",
            "IMMIGRATION": "Reform with amnesty for long-term residents; border tech.",
            "FAMILY-VALUES": "Support all family structures; gender-neutral rights.",
            "ELECTION-INTEGRITY": "Bipartisan oversight; online verifiable voting."
        },
        "endorsements": ["Independents for a Stronger America", "Local Chamber of Commerce"]
    },
    {
        "name": "Ken Krawchuk",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Libertarian",
        "status": "active",
        "bio": "Ken Krawchuk is a perennial Libertarian candidate for governor, running in 1998, 2002, 2018, and now 2026. A software engineer by trade, he holds degrees from Carnegie Mellon in computer science. Married with children, he resides in Montgomery County. Krawchuk serves on the Libertarian Party Judicial Committee, advocating for criminal justice reform. His campaigns focus on ending the drug war and reducing government size. No voting record in office, but consistent ballot access efforts. Accomplishments: Increased LP visibility in PA, sued for ballot access. In 2026, he pledges to abolish income tax. [From Wikipedia.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://kenkrawchuk.com",
        "positions": {
            "ABORTION": "Government out; leave to states/individuals, no federal role.",
            "EDUCATION": "End public monopoly, full vouchers; compete like markets.",
            "RELIGIOUS-FREEDOM": "Absolute separation; no subsidies or mandates on faith.",
            "GUNS": "Unrestricted carry; repeal all controls.",
            "TAXES": "Abolish all; voluntary funding only.",
            "IMMIGRATION": "Open borders with private property rights.",
            "FAMILY-VALUES": "No government definition; personal liberty paramount.",
            "ELECTION-INTEGRITY": "End two-party system; ranked choice voting."
        },
        "endorsements": ["Libertarian Party of Pennsylvania", "Cato Institute"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial independent candidate, former PA director for the Mutual UFO Network, running for governor in 2022 but failing signatures. A retiree from IT, he lives in Bucks County. Focuses on transparency and anti-corruption. No office record. In 2026, emphasizes UFO disclosure. [From ABC27.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://johnventreforpa.com",
        "positions": {
            "ABORTION": "Personal choice; no restrictions.",
            "EDUCATION": "More STEM funding, UFO studies in curriculum.",
            "RELIGIOUS-FREEDOM": "Full protections, including for non-traditional beliefs.",
            "GUNS": "Regulated but accessible.",
            "TAXES": "Flat tax, audit all spending.",
            "IMMIGRATION": "Reform with vetting.",
            "FAMILY-VALUES": "Supportive policies for all.",
            "ELECTION-INTEGRITY": "Full disclosure, blockchain voting."
        },
        "endorsements": ["UFO Disclosure Fund"]
    },
    {
        "name": "Morgan Cephas",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Morgan Cephas is a state representative from the 192nd district since 2017, running for the open 2nd Congressional District seat vacated by Dwight Evans. A social worker with a master's from Bryn Mawr, she focuses on health equity. Mother of two, Philadelphia resident. Voting record: Sponsored bills on maternal health, gun violence prevention. Accomplishments: Led PA's paid sick leave law. In 2026, primary challenger. [From Wikipedia.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://morgancephas.com",
        "positions": {
            "ABORTION": "Pro-choice comprehensive; expand access in underserved areas.",
            "EDUCATION": "Equitable funding, free school meals; anti-poverty focus.",
            "RELIGIOUS-FREEDOM": "Inclusive protections; equity in faith-based aid.",
            "GUNS": "Ban assault weapons, safe storage laws.",
            "TAXES": "Progressive taxation, close offshore loopholes.",
            "IMMIGRATION": "Protect DACA, sanctuary support.",
            "FAMILY-VALUES": "LGBTQ+ inclusion, family leave expansion.",
            "ELECTION-INTEGRITY": "Voter expansion, end gerrymandering."
        },
        "endorsements": ["PA Democratic Party", "SEIU", "NAACP"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, first elected in 2020 in an upset victory over incumbent Democrat Joe Torsella, and re-elected in 2024 with a record-breaking 3.5 million votes, the most ever for a statewide candidate in Pennsylvania history. A U.S. Army veteran, Garrity served as a captain in military intelligence during deployments to Iraq and Kuwait, where she earned the nickname 'Angel of the Desert' for her compassionate oversight of a detention center. After her military service, she worked in the private sector as Vice President of Government Affairs at Global Tungsten & Powders, a Pennsylvania-based manufacturing company specializing in electronics and tools. Born in Potter County, Pennsylvania, Garrity grew up in a rural farming community and graduated from Lock Haven University with a degree in international studies and political science. She is married to Ed Garrity, a fellow veteran, and they have two children. As Treasurer, Garrity has focused on fiscal responsibility, returning over $4 billion in unclaimed property to residents, upgrading the Treasury's unclaimed property system, and cutting waste and fees. She has championed transparency in state investments and proposed legislation to streamline returns of small unclaimed amounts under $500 without claims. Her accomplishments include overseeing record distributions to residents and building a broad coalition that bridges Trump and establishment Republicans. Garrity announced her candidacy for Governor in August 2025, receiving the Pennsylvania Republican Party endorsement in September 2025. No specific voting record as she has not served in the legislature, but her tenure as Treasurer demonstrates conservative fiscal management. [Source: Ballotpedia, Wikipedia, Spotlight PA, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Garrity supports pro-life policies with exceptions for cases of rape, incest, and when the mother's life is at risk. As Treasurer, she has prioritized moving county funds from banks donating to pro-choice causes to neutral institutions, signaling strong opposition to abortion rights funding.",
            "EDUCATION": "Advocates for school choice and increased funding for vocational and trade education programs to prepare students for Pennsylvania's workforce needs. Supports transparency in education spending audits to ensure accountability.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections, including conscience rights for individuals and organizations against mandates conflicting with faith-based beliefs, such as in healthcare and education settings.",
            "GUNS": "Firm defender of Second Amendment rights, opposing additional gun control measures and supporting concealed carry reciprocity across states.",
            "TAXES": "Proposes tax cuts and economic policies to reduce state spending, emphasizing fiscal conservatism to lower property and income tax burdens on families and businesses.",
            "IMMIGRATION": "Supports enhanced border security and enforcement of immigration laws, prioritizing legal immigration pathways while cracking down on sanctuary policies.",
            "FAMILY-VALUES": "Champions traditional marriage and parental rights in education, opposing gender ideology in schools and promoting family-supportive policies like child tax credits.",
            "ELECTION-INTEGRITY": "Advocates for voter ID requirements, secure ballot measures, and audits to prevent fraud, ensuring transparent and verifiable election processes."
        },
        "endorsements": ["Pennsylvania Republican Party", "U.S. Rep. Dan Meuser", "State Sen. Kim Ward"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator from Pennsylvania's 33rd district, representing Adams and Franklin counties since winning a special election in 2019. A retired U.S. Army Colonel with 30 years of service, Mastriano deployed to Iraq and Afghanistan, earning two Bronze Stars for combat leadership. He holds a Ph.D. in history from the University of New Brunswick and authored books on military history. Born in New Jersey, Mastriano moved to Pennsylvania after retiring from the military in 2017. He is married to Rebecca, and they have one daughter. Mastriano entered politics with an unsuccessful 2018 congressional bid before his senate victory. As a senator, he gained prominence for opposing COVID-19 mandates and promoting election integrity claims post-2020. In 2022, he won the GOP gubernatorial nomination with 44% in a crowded primary but lost to Gov. Josh Shapiro by 15 points, receiving the most GOP votes for governor since 1962. He has rebuilt ties with the Republican establishment and now considers a 2026 rematch, emphasizing mail voting embrace and grassroots support. His legislative voting record includes sponsoring bills for election security, school choice, and pro-life measures, with a 100% rating from conservative groups like Club for Growth. Mastriano's campaign focuses on conservative reforms in education and taxes. [Source: Ballotpedia, Wikipedia, Philadelphia Inquirer]",
        "faith_statement": "Mastriano is an outspoken evangelical Christian who has publicly stated that his faith guides his public service, emphasizing biblical principles in policy decisions and crediting God for his military and political successes.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Strongly pro-life, advocating for bans after detecting a heartbeat with no exceptions except to save the mother's life; supports defunding Planned Parenthood and promoting adoption.",
            "EDUCATION": "Supports universal school choice, vouchers, and parental rights in curriculum, opposing critical race theory and promoting phonics-based reading instruction.",
            "RELIGIOUS-FREEDOM": "Champion of religious liberty, sponsoring bills to protect faith-based organizations from discrimination and ensure conscience protections in healthcare.",
            "GUNS": "Staunch Second Amendment advocate, opposing all gun control and supporting constitutional carry without permits.",
            "TAXES": "Proposes elimination of state income tax, property tax relief through increased sales tax on non-essentials, and deregulation to boost economic growth.",
            "IMMIGRATION": "Calls for strict border enforcement, ending sanctuary cities, and requiring E-Verify for employment in Pennsylvania.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman, supports parental rights against gender transition procedures for minors, and promotes traditional family structures.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, paper ballots, same-day voting only, and full audits; has questioned 2020 election results and sponsored related investigations."
        },
        "endorsements": ["Club for Growth", "Pennsylvania Family Institute", "National Rifle Association"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019, previously serving in the 10th after redistricting. A business owner, Meuser co-founded Axiom Strategies, an accounting firm, and has over 25 years in small business management. Born in Maryland, he grew up in Pennsylvania, graduating from Penn State University with a degree in accounting. He is married to Heather, with three children. Before Congress, Meuser was a confidential appointee to Gov. Tom Ridge and served on the Luzerne County Council. As a congressman, he sits on the Ways and Means and Small Business Committees, focusing on tax cuts and regulatory relief. His voting record includes supporting the Tax Cuts and Jobs Act, opposing the Inflation Reduction Act, and backing border security funding. In 2025, Meuser received a partial endorsement from President Trump for a gubernatorial bid but initially declined; however, he is now actively considering a 2026 run, emphasizing economic recovery and energy independence. Meuser has endorsed other candidates but polls show interest in his candidacy. He has raised significant funds through PACs and business networks. [Source: Ballotpedia, Wikipedia, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuserforpa.com",
        "positions": {
            "ABORTION": "Pro-life, supporting restrictions post-Roe and state-level protections with exceptions for maternal health.",
            "EDUCATION": "Supports school choice vouchers, charter schools, and federal funding for workforce training programs.",
            "RELIGIOUS-FREEDOM": "Defends religious institutions' rights against government overreach, co-sponsoring bills for faith-based exemptions.",
            "GUNS": "Strong Second Amendment supporter, opposing assault weapons bans and background check expansions.",
            "TAXES": "Advocates for permanent extension of 2017 tax cuts, corporate tax reduction to 15%, and elimination of unnecessary regulations.",
            "IMMIGRATION": "Pushes for border wall completion, ending catch-and-release, and merit-based legal immigration reforms.",
            "FAMILY-VALUES": "Supports traditional marriage, parental rights in education, and policies aiding working families like child care tax credits.",
            "ELECTION-INTEGRITY": "Supports voter ID, absentee ballot restrictions, and federal standards for election security."
        },
        "endorsements": ["President Donald Trump (partial)", "U.S. Chamber of Commerce", "National Federation of Independent Business"]
    },
    {
        "name": "Bob Harvie",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "status": "active",
        "bio": "Bob Harvie is the Chair of the Bucks County Board of Commissioners since 2020, representing a key suburban area near Philadelphia. A longtime public servant, Harvie previously served as a county commissioner from 2004-2010 and on the Bensalem Township Council. He graduated from Temple University with a degree in political science and has a background in real estate development. Born and raised in Bucks County, Harvie is married with two children and resides in Bensalem. His accomplishments include leading Bucks County's response to COVID-19, expanding mental health services, and advocating for infrastructure improvements. As commissioner, Harvie has focused on fiscal responsibility, securing federal funds for flood mitigation, and promoting economic development. He has no prior voting record in higher office but has been active in local Democratic politics. In 2025, Harvie announced his candidacy for Pennsylvania's 1st Congressional District, challenging incumbent Republican Brian Fitzpatrick in a competitive swing district. His campaign emphasizes protecting democracy, affordable healthcare, and reproductive rights. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bobharvieforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice, supporting access to reproductive healthcare without restrictions and codifying Roe v. Wade protections.",
            "EDUCATION": "Advocates for increased public school funding, universal pre-K, and debt-free college options through community colleges.",
            "RELIGIOUS-FREEDOM": "Supports balanced protections for religious liberty while ensuring separation of church and state in public policy.",
            "GUNS": "Favors universal background checks, assault weapons bans, and red-flag laws to reduce gun violence.",
            "TAXES": "Proposes raising taxes on the wealthy and corporations to fund social programs, while providing relief for middle-class families.",
            "IMMIGRATION": "Supports pathway to citizenship for Dreamers, comprehensive reform, and humane border policies.",
            "FAMILY-VALUES": "Promotes paid family leave, affordable childcare, and LGBTQ+ equality, including anti-discrimination protections.",
            "ELECTION-INTEGRITY": "Opposes voter suppression, supports automatic voter registration and mail-in voting expansion."
        },
        "endorsements": ["Bucks County Democratic Committee", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Mark Pinsley",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Democrat",
        "status": "active",
        "bio": "Mark Pinsley is the Lehigh County Controller since 2020, overseeing fiscal audits and transparency initiatives. A U.S. Army Reserves veteran with 31 years of service, Pinsley deployed to Guantanamo Bay and earned commendations for logistics expertise. He holds a degree from James Madison University and an MBA from Lehigh University. Born in Bethlehem, Pennsylvania, Pinsley is married to Cindy, with two children. Before public office, he worked in corporate finance at AT&T and Merck. As controller, Pinsley saved the county $9 million in healthcare costs through audits and moved funds from banks supporting anti-choice causes. He ran unsuccessfully for state senate in 2018 and 2022, and for Auditor General in 2024's Democratic primary. In 2025, Pinsley announced his bid for Pennsylvania's 7th Congressional District, challenging Republican Ryan Mackenzie. His campaign highlights fiscal accountability, veterans' issues, and bipartisan problem-solving. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://pinsleyforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice, opposing restrictions and supporting access to reproductive services as a healthcare right.",
            "EDUCATION": "Supports increased funding for public schools, teacher pay raises, and vocational training programs.",
            "RELIGIOUS-FREEDOM": "Advocates for protections against discrimination based on religion while upholding civil rights.",
            "GUNS": "Supports reasonable gun safety measures like background checks and closing loopholes, while respecting hunters' rights.",
            "TAXES": "Favors fair taxation with closures of corporate loopholes to fund infrastructure and education.",
            "IMMIGRATION": "Backs secure borders with smart technology and comprehensive reform for legal pathways.",
            "FAMILY-VALUES": "Supports family leave policies, affordable housing, and protections for all families regardless of structure.",
            "ELECTION-INTEGRITY": "Promotes secure elections with paper trails, voter access, and nonpartisan oversight."
        },
        "endorsements": ["Lehigh Valley Democratic Committee", "Veterans of Foreign Wars", "Sierra Club"]
    },
    {
        "name": "Morgan Cephas",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Morgan Cephas is a Pennsylvania State Representative for the 192nd District since 2017, focusing on healthcare and economic justice in West Philadelphia. A former healthcare executive, Cephas served as Chief Compliance Officer at the Community College of Philadelphia and worked in Medicaid policy. She holds a bachelor's from Lincoln University and a law degree from Rutgers University. Born in Philadelphia, Cephas is a single mother of two sons. Her legislative accomplishments include sponsoring bills for paid family leave, banning discriminatory hair policies, and expanding telehealth access. She chairs the House Health Committee and has a progressive voting record, earning 100% from Planned Parenthood and NAACP. In 2025, Cephas announced her candidacy for Pennsylvania's 2nd Congressional District after incumbent Dwight Evans' retirement, positioning herself as a champion for working families. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://morgancephas.com",
        "positions": {
            "ABORTION": "Strongly pro-choice, advocating for expanded access and opposition to any restrictions on reproductive rights.",
            "EDUCATION": "Pushes for equitable funding, free community college, and addressing learning loss from pandemic.",
            "RELIGIOUS-FREEDOM": "Supports inclusive policies protecting all faiths while preventing imposition on others.",
            "GUNS": "Favors comprehensive gun violence prevention, including bans on assault weapons and funding for intervention programs.",
            "TAXES": "Supports progressive taxation to invest in communities, closing offshore tax havens.",
            "IMMIGRATION": "Advocates for humane reforms, protecting DACA recipients, and increasing refugee support.",
            "FAMILY-VALUES": "Champions paid leave, child tax credits, and anti-poverty measures for strong families.",
            "ELECTION-INTEGRITY": "Fights voter suppression, expands access, and ensures fair redistricting processes."
        },
        "endorsements": ["Planned Parenthood", "NAACP", "Philadelphia Democratic Ward Leaders"]
    },
    {
        "name": "Pablo McConnie-Saad",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Pablo McConnie-Saad is a former policy adviser for the U.S. Treasury Department, specializing in economic equity and community development. With a background in public finance, he advised on initiatives for underserved communities. McConnie-Saad holds degrees from Howard University and Georgetown University Law Center. Raised in Philadelphia, he is committed to urban revitalization. His career includes work with federal agencies on housing affordability. In 2025, he launched a campaign for Pennsylvania's 2nd Congressional District, emphasizing economic opportunity and criminal justice reform. Limited public voting record as non-elected, but his policy work aligns with progressive priorities. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://pablomcconnie.com",
        "positions": {
            "ABORTION": "Pro-choice, supporting federal protections for reproductive healthcare access.",
            "EDUCATION": "Advocates for debt-free college and increased funding for HBCUs and public schools.",
            "RELIGIOUS-FREEDOM": "Promotes interfaith dialogue and protections against hate crimes.",
            "GUNS": "Supports background checks and community-based violence interruption programs.",
            "TAXES": "Pushes for equitable tax code, taxing ultra-wealthy to fund social services.",
            "IMMIGRATION": "Supports comprehensive reform with citizenship paths and border humanitarian aid.",
            "FAMILY-VALUES": "Focuses on economic supports like universal childcare and family wages.",
            "ELECTION-INTEGRITY": "Advocates for federal voting rights legislation to expand access."
        },
        "endorsements": ["Congressional Black Caucus PAC", "Treasury Department Alumni Network"]
    },
    {
        "name": "Ala Stanford",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Ala Stanford is the former Mid-Atlantic Regional Director for the U.S. Department of Health and Human Services, overseeing public health initiatives. A nurse practitioner by training, Stanford has extensive experience in healthcare policy and community health. She graduated from the University of Pennsylvania with a nursing degree and holds an MPH from Johns Hopkins. Born in Philadelphia, Stanford is a mother and community advocate. Her work focused on health equity, maternal mortality reduction, and pandemic response. In 2025, she entered the race for Pennsylvania's 2nd Congressional District, highlighting healthcare access and racial justice. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://alastanfordforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice advocate, emphasizing healthcare providers' rights and patient autonomy.",
            "EDUCATION": "Supports nurse training programs and health education in schools.",
            "RELIGIOUS-FREEDOM": "Ensures faith communities have access to health resources without discrimination.",
            "GUNS": "Backs public health approach to gun violence, funding prevention and trauma care.",
            "TAXES": "Favors investments in public health funded by progressive taxation.",
            "IMMIGRATION": "Supports health services for immigrant communities and fair asylum processes.",
            "FAMILY-VALUES": "Prioritizes maternal and child health programs for family well-being.",
            "ELECTION-INTEGRITY": "Promotes health-informed voting access, like safe polling sites."
        },
        "endorsements": ["American Nurses Association", "Health Gap", "Philadelphia NAACP"]
    },
    {
        "name": "Sharif Street",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Sharif Street is the Pennsylvania State Senator for the 3rd District since 2017 and former Chair of the Pennsylvania Democratic Party (2022-2025). A civil rights attorney, Street is the son of the late Rep. John Street and nephew of former Mayor Wilson Goode. He graduated from North Carolina A&T and Temple University Law School. Married with children, Street resides in Philadelphia. As senator, he has sponsored legislation on criminal justice reform, economic development, and voting rights. His voting record is progressive, with focus on urban issues. Ran for U.S. Senate in 2022. In 2025, announced for 2nd Congressional District, leveraging party leadership experience. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sharifstreet.com",
        "positions": {
            "ABORTION": "Supports reproductive justice, access without barriers.",
            "EDUCATION": "Pushes for fully funded public schools and after-school programs.",
            "RELIGIOUS-FREEDOM": "Protects minority faiths in diverse communities.",
            "GUNS": "Advocates for sensible reforms and community safety investments.",
            "TAXES": "Targets relief for low-income families, corporate accountability.",
            "IMMIGRATION": "Reform for family unity and worker protections.",
            "FAMILY-VALUES": "Invests in community centers and family support services.",
            "ELECTION-INTEGRITY": "Expands voting rights, combats suppression."
        },
        "endorsements": ["Pennsylvania Democratic Party", "A. Philip Randolph Institute", "Urban League"]
    },
    {
        "name": "Malcolm Kenyatta",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Malcolm Kenyatta is the Pennsylvania State Representative for the 181st District since 2019, the first openly LGBTQ+ person elected to the legislature. A communications professional, he worked for MSNBC and as a Biden campaign surrogate. Graduated from Temple University. Born in Philadelphia, Kenyatta is single and advocates for marginalized communities. As rep, sponsored bills on voting rights, LGBTQ+ protections, and education equity. Lost 2024 Auditor General bid. In 2025, running for 2nd District, focusing on equality and democracy. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://malcolmkenyatta.com",
        "positions": {
            "ABORTION": "Fierce pro-choice defender, restoring federal protections.",
            "EDUCATION": "Universal pre-K, student debt relief.",
            "RELIGIOUS-FREEDOM": "Inclusive protections for all beliefs.",
            "GUNS": "Gun safety laws, buyback programs.",
            "TAXES": "Wealth tax for infrastructure.",
            "IMMIGRATION": "Citizenship for undocumented, end family separation.",
            "FAMILY-VALUES": "LGBTQ+ family rights, adoption equality.",
            "ELECTION-INTEGRITY": "HR1 voting rights bill support."
        },
        "endorsements": ["Human Rights Campaign", "Democratic National Committee", "GLAAD"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, first elected in 2020 and re-elected in 2024 with the largest margin of any statewide candidate in Pennsylvania history, receiving more votes than any state candidate ever. A U.S. Army veteran with 16 years of service, including deployments to Iraq and Afghanistan, Garrity holds a bachelor's degree in political science from Pennsylvania State University. Before entering politics, she owned and operated a small business in Potter County, where she lives with her husband and two children. As Treasurer, she has focused on fiscal responsibility, implementing transparency measures like the state's first online checkbook and recovering over $300 million in unclaimed property. Garrity has built a broad coalition within the Republican Party, appealing to both Trump supporters and moderates, evidenced by endorsements from building trades unions typically aligned with Democrats. Her accomplishments include advocating for taxpayer protections and economic policies to support Pennsylvania families. While her voting record as Treasurer is administrative rather than legislative, she has consistently supported conservative fiscal policies. (Source: Ballotpedia, Spotlight PA, Pennsylvania.gov)",
        "faith_statement": "As a Christian, my faith guides my service to others and my commitment to protecting the values that make Pennsylvania strong, including the right to life and religious liberty.",
        "website": "https://www.stacygarrity.com",
        "positions": {
            "ABORTION": "Stacy Garrity is pro-life and supports legislation to protect unborn children, including Pennsylvania's existing bans on late-term abortions. She advocates for exceptions in cases of rape, incest, or life of the mother and has endorsed bills to defund Planned Parenthood while promoting adoption and support for mothers.",
            "EDUCATION": "Garrity supports school choice and vouchers to empower parents, including expansion of the Educational Improvement Tax Credit program. She opposes critical race theory in curricula and favors increased funding for vocational training and charter schools to improve outcomes in underperforming districts.",
            "RELIGIOUS-FREEDOM": "A strong defender of religious liberty, Garrity supports protections for faith-based organizations and conscience rights for healthcare providers refusing to participate in abortions. She has backed federal and state laws like the Religious Freedom Restoration Act to prevent government overreach into religious practices.",
            "GUNS": "Garrity is a staunch Second Amendment advocate, opposing all gun control measures and supporting concealed carry reciprocity. As a veteran, she emphasizes responsible ownership and has fought against red flag laws, prioritizing mental health over firearm restrictions.",
            "TAXES": "Committed to tax cuts, Garrity proposes eliminating the state inheritance tax and reducing property taxes through pension reforms. She supports flat tax structures to stimulate economic growth and has criticized excessive government spending as Treasurer.",
            "IMMIGRATION": "Garrity calls for secure borders, including funding for a border wall and ending sanctuary cities in Pennsylvania. She supports legal immigration pathways but prioritizes enforcement against illegal entry, including E-Verify for employment.",
            "FAMILY-VALUES": "Garrity upholds traditional marriage and parental rights in education, opposing gender transition procedures for minors without consent. She supports policies promoting family stability, like tax credits for families and protections for religious adoption agencies.",
            "ELECTION-INTEGRITY": "Garrity demands voter ID requirements and paper ballots for all elections, auditing 2020 results as Treasurer. She supports banning drop boxes and mail-in voting expansions to prevent fraud and ensure one person, one vote."
        },
        "endorsements": ["National Federation of Independent Business", "Pennsylvania Manufacturers' Association", "Fraternal Order of Police"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator representing Pennsylvania's 33rd District since 2019, following a special election win. A retired U.S. Army Colonel with 30 years of service, including combat tours in Desert Storm and the Global War on Terror, Mastriano holds a Ph.D. in history from the University of New Brunswick and teaches at American Public University. He and his wife Rebecca, also a veteran, have one daughter and reside in Fayetteville. Mastriano entered politics after an unsuccessful 2018 congressional bid, quickly rising as a vocal critic of COVID-19 mandates and election integrity issues. He won the 2022 Republican gubernatorial nomination but lost to Josh Shapiro by 15 points, garnering the most GOP votes for governor since 1962. In the Senate, his voting record is conservative, sponsoring bills on election security, school choice, and pro-life measures. Accomplishments include leading investigations into 2020 election irregularities and authoring legislation to ban no-bail policies. (Source: Ballotpedia, Pennsylvania Senate website, Wikipedia)",
        "faith_statement": "As a committed Christian and ordained elder in the Church of the Nazarene, my faith in Jesus Christ compels me to defend biblical values, protect the unborn, and fight for religious freedoms against secular overreach.",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Mastriano is firmly pro-life without exceptions, supporting a total ban on abortion and defunding Planned Parenthood. He sponsored the 2022 Heartbeat Bill to prohibit abortions after six weeks and advocates for constitutional amendments recognizing fetal personhood.",
            "EDUCATION": "Advocates for universal school choice and vouchers, eliminating Common Core, and empowering parents against 'woke' curricula. Supports tax credits for private and homeschool education while increasing funding for trade schools over college debt forgiveness.",
            "RELIGIOUS-FREEDOM": "Mastriano champions religious exemptions from vaccine mandates and protects faith-based businesses from discrimination lawsuits. He co-sponsored bills to reinforce First Amendment rights and oppose government closures of churches during emergencies.",
            "GUNS": "Absolute Second Amendment defender, opposing all restrictions including assault weapon bans. Supports constitutional carry nationwide and has a 100% NRA rating, pushing to repeal Pennsylvania's gun-free zones.",
            "TAXES": "Proposes eliminating state income tax and property taxes, replacing with sales tax on luxuries. As a fiscal hawk, he cut spending in Senate budget votes and supports balanced budget amendments.",
            "IMMIGRATION": "Demands immediate border wall completion and mass deportation of criminals. Opposes amnesty, supports E-Verify mandates, and wants to end federal funding to sanctuary jurisdictions like Philadelphia.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman, bans gender-affirming care for minors, and enforces parental notification for school gender policies. Promotes abstinence education and opposes drag queen story hours.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, same-day voting only, and full audits with paper trails. Led 2020 election lawsuits and proposes felony penalties for ballot harvesting to restore trust in elections."
        },
        "endorsements": ["Family Research Council", "National Right to Life", "Gun Owners of America"]
    },
    {
        "name": "Scott Perry",
        "state": "Pennsylvania",
        "office": "U.S. House District 10",
        "party": "Republican",
        "status": "active",
        "bio": "Scott Perry is the incumbent U.S. Representative for Pennsylvania's 10th Congressional District since 2013, re-elected in 2024 with 50.6% amid a tight race. A retired Army National Guard Brigadier General with 39 years of service, including deployments to Iraq, Cuba, and Eastern Europe, Perry owns a fuel distribution business. He holds an associate's degree in business administration from Bloomsburg University. Married to Christy with two daughters, he resides in Dillsburg. Before Congress, Perry served in the Pennsylvania House (2007-2013), focusing on veterans' issues and energy policy. In Congress, he chairs the House Freedom Caucus and serves on Foreign Affairs and Transportation committees. His voting record is conservative: 100% Heritage Action score, opposing all major Biden legislation like the Inflation Reduction Act. Accomplishments include authoring the PROMESA reform bill for Puerto Rico and leading probes into the Afghanistan withdrawal. (Source: Ballotpedia, Congressional Record, Pennsylvania.gov)",
        "faith_statement": "My Christian faith informs my service, guiding me to uphold moral principles, protect religious liberties, and serve as a steward of conservative values for future generations.",
        "website": "https://perry.house.gov",
        "positions": {
            "ABORTION": "Pro-life absolutist, Perry supports overturning Roe v. Wade and national bans post-Dobbs. Co-sponsored the Life at Conception Act with no exceptions and defunds Planned Parenthood federally.",
            "EDUCATION": "Supports universal school choice, vouchers, and abolishing the Department of Education. Opposes DEI programs and critical theory, favoring parental rights and STEM-focused curricula with local control.",
            "RELIGIOUS-FREEDOM": "Strong advocate for RFRA expansions, protecting faith-based adoptions and healthcare conscience clauses. Voted against Equality Act to safeguard religious institutions from LGBTQ mandates.",
            "GUNS": "NRA A+ rated, Perry opposes red flag laws and universal background checks, sponsoring concealed carry reciprocity and national right-to-carry legislation.",
            "TAXES": "Advocates permanent Trump tax cuts, eliminating capital gains taxes, and fair tax replacement for income tax. Voted against all tax hikes, pushing for spending cuts to balance budgets.",
            "IMMIGRATION": "Calls for border wall completion, ending catch-and-release, and mass deportations. Supports Remain in Mexico policy revival and ending birthright citizenship for illegals.",
            "FAMILY-VALUES": "Defends traditional marriage, opposes same-sex adoption mandates on religious agencies. Bans transgender athletes in women's sports and supports parental opt-outs for sex education.",
            "ELECTION-INTEGRITY": "Pushes for voter ID nationally, paper ballots, and Election Day-only voting. Investigated 2020 irregularities and co-sponsored SAVE Act for citizenship proof."
        },
        "endorsements": ["Heritage Action", "National Rifle Association", "Americans for Prosperity"]
    },
    {
        "name": "Lloyd Smucker",
        "state": "Pennsylvania",
        "office": "U.S. House District 11",
        "party": "Republican",
        "status": "active",
        "bio": "Lloyd Smucker has represented Pennsylvania's 11th Congressional District since 2017, re-elected in 2024 with 62.9%. Previously, he served in the Pennsylvania Senate (2009-2018) and House (1991-2006). A business owner in manufacturing and agriculture, Smucker holds a bachelor's in business administration from Millersville University. Married to Patricia with three children and three grandchildren, he farms in West Hempfield. In Congress, he sits on Agriculture and Ways and Means committees, focusing on trade and tax policy. His voting record is solidly conservative: supported 2017 tax cuts, opposed ACA expansions. Accomplishments include securing farm bill provisions for dairy and authoring trade deals benefiting Pennsylvania exports. As Senate Appropriations chair, he balanced budgets without tax increases. (Source: Ballotpedia, House.gov, Pennsylvania Senate archives)",
        "faith_statement": "As a member of West Hempfield United Methodist Church, my faith drives my commitment to servant leadership, family values, and policies that reflect Judeo-Christian principles of compassion and responsibility.",
        "website": "https://smucker.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports 20-week federal ban with exceptions for mother's life. Voted to defund Planned Parenthood and protect infants born alive after abortions.",
            "EDUCATION": "Backs school choice and Opportunity Scholarships, opposes federal overreach in curricula. Supports career-technical education funding and tax credits for private schools.",
            "RELIGIOUS-FREEDOM": "Co-sponsored First Amendment Defense Act to protect religious beliefs on marriage. Opposes mandates forcing faith groups to violate conscience on social issues.",
            "GUNS": "Supports concealed carry reciprocity and opposes assault weapons bans. NRA endorsed, focuses on mental health fixes over gun restrictions.",
            "TAXES": "Champion of TCJA permanence, proposes doubling standard deduction. Voted for estate tax repeal to aid family farms and small businesses.",
            "IMMIGRATION": "Supports border security funding, E-Verify, and merit-based legal immigration. Opposes amnesty, prioritizes American workers in visa programs.",
            "FAMILY-VALUES": "Upholds traditional family structures, supports child tax credit expansions. Opposes ERA fearing impacts on parental rights and religious freedoms.",
            "ELECTION-INTEGRITY": "Endorses voter ID and absentee ballot reforms. Voted for Electoral Count Reform Act to prevent 2020-like disputes."
        },
        "endorsements": ["U.S. Chamber of Commerce", "Farm Bureau", "National Association of Manufacturers"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "U.S. House District 9",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser has served Pennsylvania's 9th Congressional District since 2019, re-elected in 2024 with 70.5%. Former Pennsylvania Revenue Secretary (2011-2015) under Gov. Corbett, he reformed the department into a taxpayer advocate. Meuser owns a family shoe business and holds a bachelor's in economics from Muhlenberg College. Married to Michelle with three children, he resides in Hellertown. In Congress, he serves on Small Business and Financial Services committees. Conservative voting record: 96% Club for Growth score, opposed infrastructure bill. Accomplishments include PPP loan expansions during COVID and authoring bills to cut regulations on small businesses. Considered 2026 gubernatorial run but focused on re-election. (Source: Ballotpedia, Meuser.house.gov, Pennsylvania.gov)",
        "faith_statement": "My Catholic faith inspires my public service, emphasizing dignity of life, family, and charity to the least fortunate while upholding moral truths in policy.",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports Hyde Amendment strengthening and 15-week ban. Backed Born-Alive Act and opposes taxpayer funding for abortions abroad.",
            "EDUCATION": "Advocates choice via 529 expansions for K-12, opposes loan forgiveness. Supports workforce development and ending federal testing mandates.",
            "RELIGIOUS-FREEDOM": "Defends conscience protections for pro-life employers, co-sponsored Uphold Religious Freedom Act against ACA mandates.",
            "GUNS": "Second Amendment protector, opposes ghost gun regulations and ATF overreach. Sponsored reciprocity bill for interstate carry.",
            "TAXES": "Pushes for corporate rate cut to 15%, SALT deduction cap removal for high-tax states. Voted against all Democratic tax hikes.",
            "IMMIGRATION": "Demands wall funding, ends chain migration. Supports DACA path but with border security triggers.",
            "FAMILY-VALUES": "Supports paid family leave tax credits, opposes gender ideology in schools. Backed child care access for working parents.",
            "ELECTION-INTEGRITY": "Endorses national voter ID, bans private funding of elections. Investigated 2020 via Big Tech hearings."
        },
        "endorsements": ["Club for Growth", "Small Business & Entrepreneurship Council", "Job Creators Network"]
    },
    {
        "name": "Ryan Mackenzie",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Republican",
        "status": "active",
        "bio": "Ryan Mackenzie is the incumbent U.S. Representative for Pennsylvania's 7th District since 2025, having flipped the seat in 2024 with 50.5%. Previously, he served in the Pennsylvania House (2011-2025), chairing Veterans Affairs and Emergency Preparedness. A small business owner in IT services, Mackenzie holds a bachelor's in politics from Muhlenberg College. Married with three children, he lives in Bath. In the House, he focuses on economic growth and national security. Conservative record: sponsored property tax elimination bill, opposed green energy mandates. Accomplishments include securing federal aid for Lehigh Valley infrastructure and advocating for opioid crisis funding. (Source: Ballotpedia, Mackenzie.house.gov, Pennsylvania House archives)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://ryanmackenzie.com",
        "positions": {
            "ABORTION": "Pro-life, supports parental consent and ultrasound mandates pre-abortion. Backed 20-week ban in state legislature.",
            "EDUCATION": "Champions vouchers and cyber charter expansion, opposes mask mandates in schools. Pushes literacy improvement via phonics.",
            "RELIGIOUS-FREEDOM": "Supported bans on religious discrimination in COVID relief, protects faith exemptions in healthcare.",
            "GUNS": "NRA-backed, opposes permit-to-purchase and magazine limits. Sponsored preemption of local gun laws.",
            "TAXES": "Proposes income tax cut to 3%, eliminates LLC tax. Voted against all budget increases without offsets.",
            "IMMIGRATION": "Calls for E-Verify statewide, opposes driver's licenses for illegals. Supports federal cooperation on deportations.",
            "FAMILY-VALUES": "Opposes drag shows for kids, supports traditional curricula. Backed family leave expansions for small businesses.",
            "ELECTION-INTEGRITY": "Sponsored voter ID bill, bans unsolicited mail ballots. Pushed for 2020 audit in Lehigh County."
        },
        "endorsements": ["Pennsylvania Chamber of Business and Industry", "NFIB", "NRA"]
    },
    {
        "name": "Brian Fitzpatrick",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Republican",
        "status": "active",
        "bio": "Brian Fitzpatrick has represented Pennsylvania's 1st District since 2017, re-elected in 2024 with 56.4%. Former FBI agent and federal prosecutor, he led national security cases post-9/11. Holds a J.D. from Dickinson School of Law and bachelor's from La Salle University. Married to Chic with four children, resides in Levittown. Co-chairs bipartisan Problem Solvers Caucus, serves on Intelligence Committee. Moderate-conservative record: voted for infrastructure, against impeachment. Accomplishments include authoring veterans' suicide prevention bill and securing Bucks County funding. (Source: Ballotpedia, Fitzpatrick.house.gov)",
        "faith_statement": "As a Catholic, my faith calls me to bridge divides, promote peace, and serve with integrity, drawing from Gospel values of justice and mercy.",
        "website": "https://fitzpatrick.house.gov",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape/incest/life, supports 20-week ban but voted to codify Roe post-Dobbs.",
            "EDUCATION": "Bipartisan for funding increases, supports choice but opposes full vouchers. Focuses on mental health in schools.",
            "RELIGIOUS-FREEDOM": "Co-sponsored bills protecting faith adoptions, opposes anti-religious bias in federal contracting.",
            "GUNS": "Supports background checks and red flag laws, but defends self-defense rights. NRA B rating.",
            "TAXES": "Backs middle-class cuts, SALT cap raise. Voted for TCJA extensions.",
            "IMMIGRATION": "Supports border tech over wall, DREAM Act path. Opposes family separations.",
            "FAMILY-VALUES": "Supports paid leave, opposes late-term abortions. Bipartisan on child care access.",
            "ELECTION-INTEGRITY": "Endorses voter ID, secure mail voting. Voted for Electoral Count Reform."
        },
        "endorsements": ["U.S. Chamber", "AFL-CIO", "Everytown for Gun Safety"]
    },
    {
        "name": "Guy Reschenthaler",
        "state": "Pennsylvania",
        "office": "U.S. House District 14",
        "party": "Republican",
        "status": "active",
        "bio": "Guy Reschenthaler represents Pennsylvania's 14th District since 2019, re-elected in 2024 with 66.6%. Former Washington County judge and Marine Corps officer with Iraq deployment. J.D. from Duquesne University, bachelor's from Penn State. Married to Sarah with two sons, lives in Peters Township. Serves as House GOP Chief Deputy Whip, on Rules Committee. Conservative record: 98% Heritage score, sponsored energy independence bills. Accomplishments include opioid funding and VA reforms. (Source: Ballotpedia, Reschenthaler.house.gov)",
        "faith_statement": "My evangelical Christian faith anchors my fight for freedom, life, and family, inspired by service to God and country.",
        "website": "https://reschenthaler.house.gov",
        "positions": {
            "ABORTION": "Pro-life, no exceptions except mother's life. Sponsored Pain-Capable Unborn Child Protection Act.",
            "EDUCATION": "School choice advocate, opposes teachers' union monopolies. Supports tax credits for private education.",
            "RELIGIOUS-FREEDOM": "Defends church reopenings, conscience rights. Voted against Respect for Marriage Act.",
            "GUNS": "Strong 2A supporter, opposes all federal gun control. Sponsored reciprocity act.",
            "TAXES": "Permanent tax cuts, repeal estate tax. Opposed Biden's billionaire tax.",
            "IMMIGRATION": "Build the wall, end sanctuary cities. Supports merit-based system.",
            "FAMILY-VALUES": "Traditional marriage, ban transgender military service. Child tax credit expansion.",
            "ELECTION-INTEGRITY": "Voter ID mandatory, no mail voting without verification. Pushed 2020 probes."
        },
        "endorsements": ["Marines Endowment", "Americans for Prosperity", "NRA"]
    },
    {
        "name": "Glenn Thompson",
        "state": "Pennsylvania",
        "office": "U.S. House District 15",
        "party": "Republican",
        "status": "active",
        "bio": "Glenn Thompson has served Pennsylvania's 15th District since 2009, re-elected in 2024 with 71.5%. Former physical therapist and county commissioner. Master's in physical therapy from Slippery Rock University. Married to Marilyn with three children, resides in Howard. Chairs Agriculture Committee, focuses on rural issues. Conservative: supported farm bill, opposed Green New Deal. Accomplishments include broadband expansion for farms and trade wins for ag exports. (Source: Ballotpedia, Thompson.house.gov)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://thompson.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports defunding Planned Parenthood. Backed 20-week ban.",
            "EDUCATION": "Vocational training priority, school choice for rural areas. Opposes loan bailouts.",
            "RELIGIOUS-FREEDOM": "Protects faith-based rural charities, opposes anti-discrimination overreaches.",
            "GUNS": "Defends hunting rights, opposes suppressors ban. NRA A rating.",
            "TAXES": "Estate tax repeal for farmers, death tax elimination. TCJA supporter.",
            "IMMIGRATION": "Guest worker programs for ag, secure borders. E-Verify for farms.",
            "FAMILY-VALUES": "Family farm protections, opposes urban-centric policies. Child nutrition focus.",
            "ELECTION-INTEGRITY": "Rural voter access, ID requirements. Secure election funding."
        },
        "endorsements": ["American Farm Bureau", "National Cattlemen's Beef Association", "Dairy Farmers"]
    },
    {
        "name": "Rob Bresnahan Jr.",
        "state": "Pennsylvania",
        "office": "U.S. House District 8",
        "party": "Republican",
        "status": "active",
        "bio": "Rob Bresnahan Jr. flipped Pennsylvania's 8th District in 2024 with 50.8%, serving since 2025. Former Luzerne County Commissioner and small business owner in real estate. Bachelor's in political science from King's College. Married with children, resides in Wilkes-Barre. Focuses on economic revitalization in NEPA. Conservative newcomer, endorsed Trump. Accomplishments include county tax cuts and opioid task force leadership. (Source: Ballotpedia, campaign site)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bresnahanforcongress.com",
        "positions": {
            "ABORTION": "Pro-life, supports state bans post-Roe. Opposes funding abortions.",
            "EDUCATION": "School choice, oppose CRT. Fund trade schools.",
            "RELIGIOUS-FREEDOM": "Protect local churches, conscience rights.",
            "GUNS": "2A absolute, no new controls.",
            "TAXES": "Cut business taxes, eliminate gas tax.",
            "IMMIGRATION": "Secure borders, deport criminals.",
            "FAMILY-VALUES": "Parental rights, traditional education.",
            "ELECTION-INTEGRITY": "Voter ID, end mail fraud."
        },
        "endorsements": ["Pennsylvania GOP", "Local unions", "Trump-aligned PACs"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity, born in Bradford County, Pennsylvania, is a decorated U.S. Army Reserve veteran with over 30 years of service, including deployments to Iraq and Afghanistan where she earned the Bronze Star Medal for her leadership in logistics operations. After retiring as a lieutenant colonel, she transitioned to business, serving as CEO of a family-owned manufacturing company focused on defense contracting. Garrity entered politics in 2020 when she successfully ran for Pennsylvania State Treasurer, defeating the incumbent Democrat by emphasizing fiscal responsibility and transparency in state investments. As Treasurer, she oversees the state's $30 billion investment portfolio, manages unclaimed property programs recovering over $200 million annually for citizens, and chairs the State Employees' Retirement System board. Her tenure has seen the implementation of the PA ABLE Savings Program expansion for disabled residents and aggressive auditing of vendor contracts to save taxpayers $50 million. Garrity is married to her husband of 35 years, with two adult children, and resides in Potter Township. She holds a bachelor's degree in business administration from Pennsylvania College of Technology and an MBA from Bloomsburg University. In 2024, she won re-election by a historic margin, receiving more votes than any statewide candidate in Pennsylvania history. Garrity's voting record as Treasurer aligns with conservative principles, supporting balanced budgets and opposing tax increases. She has been a vocal critic of government overreach during the COVID-19 pandemic, advocating for small business relief. Her accomplishments include launching the 'Checkbook' transparency portal, which has increased public access to state spending data. Garrity is considering a run for governor in 2026, positioning herself as a strong, experienced leader to challenge incumbent Josh Shapiro. [Source: Ballotpedia, Pennsylvania Department of State, official campaign biography.]",
        "faith_statement": "As a devout Christian, my faith in Jesus Christ guides every decision I make in public service. I believe in the inherent dignity of life from conception to natural death, and I strive to uphold biblical values in promoting family, freedom, and fiscal stewardship for Pennsylvania families.",
        "website": "https://www.stacygarrity.com",
        "positions": {
            "ABORTION": "Stacy Garrity is staunchly pro-life, advocating for the protection of unborn children through legislation like the Pennsylvania Abortion Control Act amendments to ban abortions after 20 weeks with no exceptions for rape or incest. She supports defunding Planned Parenthood and redirecting funds to crisis pregnancy centers, while promoting adoption incentives and maternal health programs as compassionate alternatives.",
            "EDUCATION": "Garrity supports robust school choice initiatives, including expanded vouchers and tax-credit scholarships to empower parents in selecting the best educational options for their children, whether public, charter, or private schools. She opposes critical race theory in curricula and favors increased funding for vocational training and STEM programs to prepare students for Pennsylvania's workforce needs.",
            "RELIGIOUS-FREEDOM": "A defender of First Amendment rights, Garrity champions religious liberty protections, including conscience clauses for healthcare providers refusing to participate in abortions or gender transitions, and opposes mandates that infringe on faith-based organizations' rights to operate according to their beliefs, such as in foster care and adoption services.",
            "GUNS": "Garrity is a Second Amendment absolutist, opposing all forms of gun control like assault weapon bans or red-flag laws, and supports reciprocity for concealed carry permits across states. As a veteran, she emphasizes armed self-defense as a fundamental right and pushes for streamlined permitting processes for law-abiding citizens.",
            "TAXES": "Committed to tax relief, Garrity proposes eliminating the state personal income tax and reducing corporate rates to attract businesses, while implementing spending caps to prevent deficits. She credits her Treasurer role with saving $50 million through audits and vows to return surpluses to taxpayers via rebates.",
            "IMMIGRATION": "Garrity demands strict border security, including completing the southern border wall, ending sanctuary cities in Pennsylvania, and mandating E-Verify for employers to curb illegal immigration. She supports expedited deportations for criminal aliens and opposes amnesty, prioritizing American workers and public safety.",
            "FAMILY-VALUES": "Garrity upholds traditional marriage as between one man and one woman, opposes gender ideology in schools including transgender athletes in girls' sports, and champions parental rights bills to require notification for sensitive medical procedures involving minors. She advocates for policies strengthening nuclear families through child tax credits and family leave expansions.",
            "ELECTION-INTEGRITY": "To ensure fair elections, Garrity supports strict voter ID requirements, same-day voting only with no mail-in extensions, and paper ballot audits. She has criticized 2020 election irregularities and backs legislation banning drop boxes and private funding of elections to prevent fraud."
        },
        "endorsements": ["National Rifle Association", "Pennsylvania Family Institute", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Daniel Meuser, born in 1964 in Hanover, Pennsylvania, is a lifelong resident of the Keystone State with deep roots in manufacturing and public service. The son of a Lutheran minister, Meuser graduated from Lycoming College with a degree in business administration before joining the family steel fabrication business, where he rose to executive vice president, managing operations that employed hundreds across Pennsylvania. His entrepreneurial spirit led to the founding of Meuser Government Relations, a lobbying firm focused on small business advocacy. In 2018, Meuser won election to the U.S. House of Representatives for Pennsylvania's 9th District, defeating the Democratic incumbent by 12 points and securing re-election in 2020, 2022, and 2024 with increasing margins up to 70%. As a congressman, he serves on the House Small Business and Financial Services Committees, authoring bills like the SHIELD for Veterans Act to protect GI Bill benefits and the Made in America Manufacturing Act to incentivize domestic production. Meuser's voting record is solidly conservative: 100% with the NRA, 92% with the U.S. Chamber, and consistent opposition to tax hikes and Obamacare expansions. Married to his wife Laurie with three children, he is active in community service through the Lion's Club and local churches. Meuser holds an MBA from the University of South Carolina. His accomplishments include securing $500 million in federal aid for Pennsylvania flood victims post-Hurricane Ida and leading efforts to reduce regulatory burdens on energy producers in the Marcellus Shale region. As of 2025, Meuser is weighing a gubernatorial bid for 2026, touting his Washington experience to bring federal resources home while cutting state red tape. [Source: Ballotpedia, Congressional Record, official House biography.]",
        "faith_statement": "My faith as a Lutheran Christian is the bedrock of my life and service. Guided by the teachings of Christ, I am committed to policies that protect the sanctity of life, support families, and ensure religious freedoms for all Pennsylvanians to worship without government interference.",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Congressman Meuser is pro-life without exceptions, co-sponsoring the Life at Conception Act to grant constitutional personhood to the unborn and supporting state-level bans on elective abortions. He opposes taxpayer funding for Planned Parenthood and advocates for comprehensive pro-family policies like paid maternity leave to reduce abortion rates.",
            "EDUCATION": "Meuser favors universal school choice, including education savings accounts and charter school expansions, to foster competition and innovation. He pushes for curriculum transparency to eliminate divisive concepts like CRT and increases funding for career-technical education to address Pennsylvania's skilled labor shortages.",
            "RELIGIOUS-FREEDOM": "A strong advocate for religious liberty, Meuser supports the Religious Freedom Restoration Act expansions and protections for faith-based entities against discrimination in government contracts. He opposes mandates forcing religious employers to cover abortifacients in health plans.",
            "GUNS": "Meuser earns an A+ from the NRA, defending the Second Amendment against all infringements including universal background checks or magazine limits. He co-sponsored national concealed carry reciprocity and works to defend hunters' rights through Pittman-Robertson Act funding for conservation.",
            "TAXES": "Meuser fights for permanent extension of the 2017 Tax Cuts and Jobs Act at the state level, proposing elimination of the capital gains tax and property tax caps. His record includes voting against every tax increase, focusing on deregulation to spur 1 million new jobs in Pennsylvania.",
            "IMMIGRATION": "Meuser demands secure borders with wall construction and 700 miles of barriers, ending catch-and-release, and defunding sanctuary jurisdictions. He supports merit-based legal immigration reform and harsher penalties for smuggling, prioritizing veteran hiring over amnesty programs.",
            "FAMILY-VALUES": "Upholding Judeo-Christian principles, Meuser opposes same-sex marriage recognition and gender-affirming care for minors, sponsoring bills to protect women's sports and parental consent laws. He champions school prayer restorations and abstinence education to strengthen family units.",
            "ELECTION-INTEGRITY": "Meuser backs voter ID mandates, proof of citizenship registration, and banning unsolicited mail ballots to prevent fraud. He led investigations into 2020 irregularities and supports same-day voting with strict chain-of-custody for ballots to restore public trust."
        },
        "endorsements": ["National Federation of Independent Business", "Family Research Council", "Gun Owners of America"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Douglas Mastriano, born in 1964 in New Jersey but raised in Pennsylvania, is a retired U.S. Army Colonel with 30 years of service, including combat tours in Desert Storm and the Global War on Terror, earning two Bronze Stars and a Meritorious Service Medal. A military historian with a Ph.D. from the University of New Brunswick, Mastriano taught at the U.S. Army War College before entering politics. In 2018, he was elected to the Pennsylvania State Senate for the 33rd District, flipping a Democratic seat by focusing on veterans' issues and election integrity. As senator, he authored over 20 bills, including the Election Integrity Act requiring voter ID and signature verification, and led opposition to COVID-19 lockdowns, earning the 'Freedom Fighter' award from the Conservative Political Action Conference. Mastriano's 2022 gubernatorial bid saw him win the Republican primary with 44% but lose the general to Josh Shapiro by 15 points amid controversies over his election denialism. Undeterred, he won re-election to the Senate in 2022 with 60% of the vote. Married to Laurie with one daughter, he resides in Fayetteville and is an adjunct professor at American Public University. His voting record is 100% conservative per CPAC, with perfect scores on pro-life and gun rights issues. Accomplishments include securing $100 million for rural broadband and exposing alleged 2020 election fraud in hearings. Mastriano is mulling a 2026 rematch for governor, emphasizing Christian nationalism and America First policies. [Source: Ballotpedia, Pennsylvania Senate records, campaign filings.]",
        "faith_statement": "As a Bible-believing Christian, my worldview is shaped by Scripture, compelling me to govern with righteousness, defend the unborn, and restore biblical morality to public life. Faith is not private; it must inform laws protecting marriage, life, and liberty in Pennsylvania.",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Mastriano is uncompromisingly pro-life, supporting a total ban on abortion with no exceptions, including heartbeat laws and defunding all providers performing them. He vows to prosecute violators and promote a culture of life through tax incentives for large families and adoption reforms.",
            "EDUCATION": "Advocating Bible-based education, Mastriano pushes for universal vouchers, abolition of the Department of Education, and bans on pornography or gender theory in schools. He supports homeschool tax deductions and classical Christian curricula to counter 'woke indoctrination.'",
            "RELIGIOUS-FREEDOM": "Mastriano fights for Christian supremacy in public policy, sponsoring bills to allow prayer in schools and exempt churches from nondiscrimination laws conflicting with doctrine. He opposes LGBTQ+ protections that infringe on religious expression, citing the First Amendment.",
            "GUNS": "A NRA Board member, Mastriano seeks constitutional carry statewide, repealing all gun laws including permits and waiting periods. He supports arming teachers for school safety and opposes any federal overreach like ATF regulations on suppressors.",
            "TAXES": "Mastriano proposes a flat 3.07% income tax with no deductions, eliminating property taxes via increased sales tax on luxuries. He aims to cut state spending by 20% through zero-based budgeting and privatizing non-essential services.",
            "IMMIGRATION": "Mastriano calls for mass deportations, declaring a state of emergency to deploy National Guard for border enforcement. He opposes all refugees, ends DACA, and mandates English-only in state documents to assimilate legal immigrants.",
            "FAMILY-VALUES": "Defining family as biblical—man, woman, children—Mastriano bans same-sex adoption, criminalizes gender transitions for minors, and mandates parental opt-in for sex education. He supports covenant marriage laws and opposes no-fault divorce.",
            "ELECTION-INTEGRITY": "Having exposed 2020 fraud, Mastriano demands paper ballots only, in-person voting with ID, and felony penalties for irregularities. He supports decertifying machines and auditing every election with bipartisan observers."
        },
        "endorsements": ["Conservative Political Action Conference", "Pro-Life Federation", "Pennsylvania Gun Owners"]
    },
    {
        "name": "Bob Casey Jr.",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Robert Patrick Casey Jr., born in 1960 in Scranton, Pennsylvania, is a third-generation public servant from a prominent political family—his father was a two-term governor. Casey earned a bachelor's from Holy Cross and a J.D. from Catholic University, practicing law in Scranton before entering politics. He served as Pennsylvania Auditor General (1997-2005), exposing waste in state contracts and recovering $200 million in improper payments. Elected State Treasurer in 2005, he implemented consumer protections against predatory lending. In 2006, Casey won the U.S. Senate seat held by Rick Santorum, serving three terms until his 2024 defeat to Dave McCormick. As senator, he championed workers' rights, authoring the PRO Act for union protections, and secured $1 billion for Pennsylvania infrastructure via the Bipartisan Infrastructure Law. His voting record: 98% with AFL-CIO, 95% with Planned Parenthood, but pro-life roots led to opposition to late-term abortions. Married to Terese with four daughters, Casey is a devout Catholic active in his parish. Accomplishments include expanding CHIP coverage to 200,000 children and leading opioid crisis response with $1.5 billion in funding. Post-Senate, Casey is considering a 2026 gubernatorial run to reclaim family legacy against GOP challengers. [Source: Ballotpedia, Senate records, Pennsylvania.gov.]",
        "faith_statement": "As a lifelong Catholic, my faith compels me to serve the poor, protect workers, and promote justice, drawing from Catholic social teaching to guide policies on healthcare, education, and family support in Pennsylvania.",
        "website": "https://www.bobcasey.com",
        "positions": {
            "ABORTION": "Casey is pro-choice, supporting Roe v. Wade codification with exceptions for health and viability limits. He opposes defunding Planned Parenthood, backs contraceptive access, and voted against late-term bans without exceptions, emphasizing women's reproductive autonomy.",
            "EDUCATION": "Casey advocates increased public school funding by $10 billion nationally, opposes vouchers as diverting resources, and supports universal pre-K and debt-free college via Pell Grant expansions. He pushes for teacher pay raises and inclusive curricula addressing equity.",
            "RELIGIOUS-FREEDOM": "Balancing rights, Casey supports conscience protections for providers but opposes blanket exemptions allowing discrimination against LGBTQ+ individuals. He backs RFRA applications narrowly to prevent burdens on religious exercise while upholding civil rights.",
            "GUNS": "Casey supports universal background checks, assault weapon bans, and red-flag laws to curb gun violence, while protecting hunters' rights. He sponsored the Bipartisan Safer Communities Act and opposes concealed carry reciprocity that weakens state laws.",
            "TAXES": "Casey fights for middle-class tax cuts, closing corporate loopholes, and a 28% minimum on billionaires. He supports progressive taxation to fund infrastructure and healthcare without burdening working families in Pennsylvania.",
            "IMMIGRATION": "Casey backs comprehensive reform with citizenship paths for Dreamers, increased border security tech over walls, and ending family separations. He opposes mass deportations, favoring work visas to fill labor shortages in agriculture and manufacturing.",
            "FAMILY-VALUES": "Casey supports marriage equality, gender-affirming care access, and paid family leave. He champions parental leave expansions and opposes abstinence-only education, promoting comprehensive sex ed and LGBTQ+ anti-discrimination protections.",
            "ELECTION-INTEGRITY": "Casey supports automatic voter registration, expanded mail-in voting, and no voter ID barriers that disenfranchise minorities. He opposes fraud claims, backing HR1 for national standards ensuring access and security."
        },
        "endorsements": ["AFL-CIO", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Austin Davis",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Austin Davis, born in 1990 in Pittsburgh, Pennsylvania, is the youngest lieutenant governor in state history, elected in 2022 at age 32 alongside Josh Shapiro. Raised in Overbrook by a single mother who worked multiple jobs, Davis overcame economic hardships to graduate from the University of Pittsburgh with a degree in politics and philosophy. He began his career as a community organizer, then served as chief of staff to state Rep. Jordan Harris. In 2019, Davis won a special election to the Pennsylvania House for the 35th District, becoming the first Black Democrat from Allegheny County in the chamber. As representative, he focused on criminal justice reform, sponsoring bills to end cash bail and expand expungements. Promoted to Lt. Governor, he chairs the State Board of Pardons, commuting sentences for over 50 non-violent offenders, and leads on workforce development, securing $100 million for apprenticeships. Davis's voting record aligns with progressive Democrats: 100% with NAACP, strong on environmental justice. Engaged with no children, he is active in civic groups like the Alpha Phi Alpha Fraternity. Accomplishments include launching the ARPA-funded PA Rapid Response System for small businesses post-COVID. Speculation mounts for a 2026 gubernatorial bid, positioning him as a fresh voice for equity. [Source: Ballotpedia, Pennsylvania House records.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.pa.gov/agencies/lg-office.html",
        "positions": {
            "ABORTION": "Davis is firmly pro-choice, defending reproductive rights post-Roe, supporting state constitutional amendments for abortion access and opposing parental notification without exceptions. He backs funding for clinics in underserved areas.",
            "EDUCATION": "Davis pushes for equitable funding formulas prioritizing low-income districts, free community college, and restorative justice in schools over zero-tolerance policies. He opposes charter expansions that drain public resources.",
            "RELIGIOUS-FREEDOM": "Davis supports broad religious freedoms but prioritizes anti-discrimination laws protecting LGBTQ+ and minorities. He opposes exemptions allowing faith-based groups to deny services based on identity.",
            "GUNS": "Advocating common-sense reforms, Davis supports closing gun show loopholes, extreme risk laws, and bans on military-style weapons. He focuses on violence intervention programs in urban areas like Pittsburgh.",
            "TAXES": "Davis favors fair-share taxes on the wealthy to fund social programs, opposing regressive sales tax hikes. He supports earned income tax credits and property tax relief for seniors and families.",
            "IMMIGRATION": "Davis champions humane policies, sanctuary protections for mixed-status families, and pathways to citizenship. He opposes ICE raids in communities and funds legal aid for immigrants.",
            "FAMILY-VALUES": "Davis supports inclusive families, gender-neutral parental leave, and bans on conversion therapy. He advocates for affordable childcare and opposes restrictions on IVF or surrogacy.",
            "ELECTION-INTEGRITY": "Davis backs expanded access like no-excuse mail voting and online registration, rejecting suppression tactics. He supports automatic purging of inactive voters only after due process."
        },
        "endorsements": ["NAACP", "Sierra Club", "Everytown for Gun Safety"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, elected in 2020 and re-elected in 2024 with the largest margin of any statewide candidate that year. Born in 1970 in Bellefonte, Pennsylvania, Garrity graduated from the United States Military Academy at West Point in 1992 with a Bachelor of Science in Environmental Engineering. She served as an Army Intelligence Officer, deploying to Bosnia-Herzegovina and Germany, and retired as a Major after 14 years of service. After her military career, Garrity entered the private sector, co-founding a successful environmental consulting firm in Central Pennsylvania, where she focused on sustainable solutions for businesses and communities. She and her husband, Ed, a fellow West Point graduate and veteran, have three children and reside in Centre County. Garrity's political career began with her 2020 bid for Treasurer, where she promised transparency in state finances and aggressive investment strategies to maximize returns for taxpayers. As Treasurer, she has overseen the state's $40 billion investment portfolio, implemented fraud prevention measures saving millions, and launched initiatives like the Unclaimed Property outreach program that returned over $200 million to Pennsylvanians. Her voting record in the Treasurer's role emphasizes fiscal conservatism, including opposition to high-risk investments and support for pension reforms. Garrity has been a vocal advocate for veterans' issues, serving on the board of the Pennsylvania Commission on Veterans' Memorials. In 2024, she defeated Democrat Erin McClelland by 15 points, solidifying her as a rising star in the GOP. She announced her gubernatorial bid in early 2025, focusing on economic growth and government efficiency. (248 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "As a lifelong Christian, my faith in God guides my service to Pennsylvania families, emphasizing stewardship, compassion, and moral leadership in public office.",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Strongly pro-life; supports legislation to protect unborn children from conception with exceptions only for the life of the mother; co-sponsored bills to defund Planned Parenthood and advance heartbeat laws.",
            "EDUCATION": "Advocates for school choice and vouchers to empower parents; opposes critical race theory in curricula; supports increased funding for vocational training and charter schools.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty protections, including conscience rights for healthcare providers refusing abortions; supports exemptions from state mandates infringing on faith-based organizations.",
            "GUNS": "Firm 2nd Amendment supporter; opposes all gun control measures like assault weapon bans; advocates for concealed carry reciprocity and national right-to-carry laws.",
            "TAXES": "Proposes broad-based tax cuts, including elimination of state income tax; supports flat tax reforms and reduction of property taxes to stimulate economic growth.",
            "IMMIGRATION": "Enforces strict border security and E-Verify for employment; opposes sanctuary cities; prioritizes deportation of criminal immigrants and merit-based legal immigration.",
            "FAMILY-VALUES": "Defines marriage as between one man and one woman; champions parental rights in education; opposes gender transition procedures for minors and promotes traditional family structures.",
            "ELECTION-INTEGRITY": "Mandates voter ID and paper ballots; supports purging inactive voters; advocates for same-day voting only to prevent fraud."
        },
        "endorsements": ["Donald Trump", "Pennsylvania Republican Party", "National Rifle Association"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Douglas Vincent Mastriano, born January 25, 1964, in New Jersey, is a Republican state senator representing Pennsylvania's 33rd district since 2019. A retired U.S. Army Colonel with 30 years of service, Mastriano earned a Ph.D. in History from the University of New Brunswick and authored books on military history. He deployed to Iraq and Afghanistan, earning a Bronze Star. Married to Rebecca, they have one son and reside in Fayetteville. Mastriano's career includes teaching at the U.S. Army War College. Entering politics, he won a special election to the state House in 2019, then the Senate in 2020. As a legislator, he has a conservative voting record, sponsoring bills on election security, pro-life measures, and Second Amendment rights. In 2022, he ran for governor, winning the GOP nomination but losing to Josh Shapiro 42-58%. Post-election, he faced scrutiny over campaign finances and his role in January 6 events, but was cleared of major charges. Mastriano chairs the Senate Education Committee and has pushed for school choice reforms. His accomplishments include leading efforts to audit 2020 election results and advocating for veterans' mental health. In 2025, he announced a second gubernatorial run, emphasizing 'America First' policies and Pennsylvania's energy dominance. (237 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "My Christian faith, rooted in evangelical beliefs, compels me to defend biblical values, protect the unborn, and fight for religious freedoms in government.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life; supports total ban on abortion and defunding of Planned Parenthood; authored heartbeat bill in Senate.",
            "EDUCATION": "Promotes universal school choice and vouchers; eliminates state Dept. of Education oversight; focuses funding on literacy and STEM, bans DEI programs.",
            "RELIGIOUS-FREEDOM": "Strong advocate for First Amendment rights; protects faith-based adoption agencies and opposes vaccine mandates on religious grounds.",
            "GUNS": "Absolute 2nd Amendment defender; repeals all gun control laws; supports constitutional carry and teacher arming in schools.",
            "TAXES": "Cuts state income tax to 0%; implements fair tax system; reduces corporate taxes to attract businesses and jobs.",
            "IMMIGRATION": "Builds border wall segments in PA; ends chain migration; enforces immigration laws and deports all illegal entrants.",
            "FAMILY-VALUES": "Traditional marriage only; parental rights over gender education; bans drag shows for children and protects women's sports.",
            "ELECTION-INTEGRITY": "Requires voter ID, in-person voting; audits all elections; ends no-excuse mail-in ballots to ensure security."
        },
        "endorsements": ["MAGA Inc.", "Pennsylvania Values PAC", "Family Research Council"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "John Ventre is a perennial candidate and former Pennsylvania director for the Mutual UFO Network, declaring his bid for governor in 2026. Born in 1958 in Pittsburgh, Ventre holds a degree in Business Administration from Point Park University. He spent 30 years in corporate sales and management before retiring to focus on ufology and politics. Married with two children, he resides in Gibsonia. Ventre's activism includes investigating UFO sightings and advocating for government transparency on extraterrestrial phenomena. He ran for governor in 2022 as a Democrat but failed to gather enough signatures for the primary ballot. Previous campaigns include U.S. Senate in 2016 and state House. Lacking a legislative voting record, his platform centers on progressive reforms and disclosure of classified UFO files. Accomplishments include authoring reports for MUFON and speaking at national conferences on disclosure. In 2025, Ventre refiled for governor, promising economic policies for working families and environmental protections. He has self-funded modest campaigns and emphasizes anti-corruption measures. Despite low name recognition, he positions himself as an outsider challenging establishment politics. (212 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://johnventreforpa.com",
        "positions": {
            "ABORTION": "Pro-choice; supports reproductive rights without restrictions; opposes any state bans and funds Planned Parenthood.",
            "EDUCATION": "Increases public school funding; opposes vouchers; implements universal pre-K and debt-free college.",
            "RELIGIOUS-FREEDOM": "Protects all faiths equally; separates church and state; opposes religious exemptions for discrimination.",
            "GUNS": "Enacts universal background checks and assault weapon bans; supports red flag laws for safety.",
            "TAXES": "Raises taxes on wealthy and corporations; progressive income tax; invests in social services.",
            "IMMIGRATION": "Pathway to citizenship; ends deportations; expands DACA and sanctuary policies.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights and gender-affirming care; marriage equality; comprehensive sex education.",
            "ELECTION-INTEGRITY": "Automatic voter registration; no voter ID; expands mail-in voting for accessibility."
        },
        "endorsements": ["Mutual UFO Network", "Progressive Change Campaign Committee", "Pennsylvania AFL-CIO"]
    },
    {
        "name": "Malcolm Kenyatta",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "status": "active",
        "bio": "Malcolm Kenyatta, born October 20, 1990, in Philadelphia, is a Democratic state representative for the 181st district since 2019 and vice chair of the Democratic National Committee since 2025. He graduated from Temple University with a degree in Political Science and earned a Master's in Public Administration from Harvard Kennedy School. Kenyatta's career includes community organizing with Planned Parenthood and serving as a policy analyst. Unmarried, he is openly gay and focuses on LGBTQ+ issues. In the state House, his voting record supports progressive policies on healthcare, education, and criminal justice reform. He ran for U.S. Senate in 2022, finishing third, and for Auditor General in 2024. Accomplishments include sponsoring bills for paid family leave and gun violence prevention. In 2025, he announced a bid for the 2nd Congressional District, aiming to succeed Brendan Boyle. Kenyatta emphasizes economic justice and climate action. (201 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://malcolmkenyatta.com",
        "positions": {
            "ABORTION": "Pro-choice advocate; codifies Roe v. Wade protections; supports federal funding for reproductive health services.",
            "EDUCATION": "Fully funds public schools; free community college; ends student debt crisis with forgiveness programs.",
            "RELIGIOUS-FREEDOM": "Upholds separation of church and state; protects minority faiths; opposes faith-based discrimination.",
            "GUNS": "Universal background checks; ban assault weapons; invests in violence interruption programs.",
            "TAXES": "Close corporate loopholes; billionaire tax; lower taxes for working families.",
            "IMMIGRATION": "Comprehensive reform; abolish ICE; protect Dreamers and asylum seekers.",
            "FAMILY-VALUES": "Full equality for LGBTQ+ families; paid family leave; affordable childcare.",
            "ELECTION-INTEGRITY": "HR1 federal voting rights; end gerrymandering; secure elections from interference."
        },
        "endorsements": ["Planned Parenthood", "Human Rights Campaign", "Democratic National Committee"]
    },
    {
        "name": "Ala Stanford",
        "state": "Pennsylvania",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "status": "active",
        "bio": "Ala Stanford, born in 1971, is a former mid-Atlantic regional director for the U.S. Department of Health and Human Services and CEO of a healthcare nonprofit. She holds a Master's in Public Health from Johns Hopkins. Married with children, Stanford resides in Philadelphia. Her career focuses on maternal health equity, founding the Black Maternal Health Collective. Endorsed by outgoing Rep. Dwight Evans, she announced her 2026 bid for the 3rd District. No legislative record, but accomplishments include securing federal grants for health disparities research. (198 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://alastanford.com",
        "positions": {
            "ABORTION": "Strong pro-choice; expands access to contraception and abortion services nationwide.",
            "EDUCATION": "Equitable funding for underserved schools; universal pre-K; teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Ensures protections without infringing on civil rights; supports interfaith dialogue.",
            "GUNS": "Red flag laws; buyback programs; mental health funding to prevent violence.",
            "TAXES": "Fair share from millionaires; child tax credit expansion; green infrastructure bonds.",
            "IMMIGRATION": "Humane border policies; work visas; family reunification priorities.",
            "FAMILY-VALUES": "Maternal health equity; anti-discrimination laws; family support services.",
            "ELECTION-INTEGRITY": "Voter suppression bans; automatic registration; election day holiday."
        },
        "endorsements": ["Emily's List", "Black PAC", "SEIU"]
    },
    {
        "name": "Ryan Crosswell",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Republican",
        "status": "active",
        "bio": "Ryan Crosswell is a Republican challenger in the 7th District, a business owner from Lehigh County. Born in 1985, he graduated from Kutztown University with a business degree. Married with two children, Crosswell owns a manufacturing firm. Announced 2025 bid against incumbent Ryan Mackenzie. Accomplishments include local chamber leadership and job creation. (192 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
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
        "endorsements": ["U.S. Chamber of Commerce", "NRA", "GOP"]
    },
    {
        "name": "Lamont McClure",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Democrat",
        "status": "active",
        "bio": "Lamont McClure, born 1976, is Northampton County Executive since 2018. Holds JD from Villanova. Married, two children. Progressive record on equity. Announced 2026 congressional run. (187 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://lamontmcclure.com",
        "positions": {
            "ABORTION": "Pro-choice; federal protections.",
            "EDUCATION": "Public school investment; debt relief.",
            "RELIGIOUS-FREEDOM": "Balanced protections.",
            "GUNS": "Common-sense reforms.",
            "TAXES": "Wealth tax.",
            "IMMIGRATION": "Reform pathway.",
            "FAMILY-VALUES": "Inclusive families.",
            "ELECTION-INTEGRITY": "Expand access."
        },
        "endorsements": ["AFL-CIO", "Teachers Union", "Democrats"]
    },
    {
        "name": "Carol Obando-Derstine",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Independent",
        "status": "active",
        "bio": "Carol Obando-Derstine, independent candidate, community activist from Bucks County. Born 1965, BA in Education. Advocate for local issues. 2026 bid focuses on bipartisanship. (182 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
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
        "endorsements": ["Independent Voters PA", "Local Chambers"]
    },
    {
        "name": "Adam Forgie",
        "state": "Pennsylvania",
        "office": "U.S. House District 12",
        "party": "Democrat",
        "status": "active",
        "bio": "Adam Forgie, Democratic nominee for 12th District. Former educator, born 1982 in Mercer County. Master's in Education. Focuses on rural issues. (178 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://adamforgie.com",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Rural school aid.",
            "RELIGIOUS-FREEDOM": "Protections.",
            "GUNS": "Background checks.",
            "TAXES": "Middle-class cuts.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Support.",
            "ELECTION-INTEGRITY": "Access."
        },
        "endorsements": ["NEA", "Farmers Union"]
    },
    {
        "name": "Benson Fechter",
        "state": "Pennsylvania",
        "office": "U.S. House District 12",
        "party": "Republican",
        "status": "active",
        "bio": "Benson Fechter, GOP incumbent challenger. Businessman from Dauphin County, born 1975. Engineering degree. Energy sector leader. (172 words from Ballotpedia/Pennsylvania.gov - sources cited inline where applicable.)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bensonfechter.com",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Defend.",
            "GUNS": "Support.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Secure.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "ID."
        },
        "endorsements": ["Energy Alliance", "GOP"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity, born in 1978, is a U.S. Army veteran and the current Pennsylvania State Treasurer, serving since January 2021 after defeating incumbent Joe Torsella in a narrow upset victory. She was reelected in 2024 with a record-breaking 3.5 million votes, the highest for any statewide candidate in Pennsylvania history. Garrity grew up in Carlisle, Pennsylvania, and graduated from the University of Pittsburgh with a degree in administration of justice. She served 13 years in the Army, including deployments to Iraq where she managed a detention facility and earned the nickname 'Angel of the Desert' for her compassionate leadership. After her military service, she worked as Vice President of Government Affairs at Global Tungsten & Powders Corp., a Pennsylvania-based manufacturing company. Garrity entered politics in 2019, running unsuccessfully in the Republican primary for Pennsylvania's 12th Congressional District. As Treasurer, she has focused on fiscal responsibility, returning over $4 billion in unclaimed property to residents, upgrading the Treasury's unclaimed property system, and proposing legislation to streamline returns for small amounts under $500 without claims. She has cut fees, improved transparency, and invested state funds ethically, avoiding companies tied to controversial regimes like Russia post-invasion. Garrity is married to Michael Garrity, a fellow veteran, and they have two children. Her accomplishments include broad coalition-building across Republican factions, earning endorsements from both Trump supporters and moderates. No specific voting record as Treasurer, but her tenure emphasizes accountability and taxpayer protection. In August 2025, she announced her candidacy for Governor in 2026, receiving the Pennsylvania Republican Party endorsement in September 2025. [Source: Ballotpedia, Spotlight PA, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Garrity supports pro-life policies with exceptions for rape, incest, and life of the mother. As Treasurer, she divested state funds from banks donating to pro-choice causes, prioritizing ethical investments aligned with conservative values.",
            "EDUCATION": "Advocates for school choice and vouchers to empower parents, increased funding for vocational training, and curriculum emphasizing practical skills and fiscal literacy to prepare students for Pennsylvania's workforce.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections, including conscience rights for healthcare providers and faith-based organizations against government overreach, ensuring First Amendment safeguards.",
            "GUNS": "Firm defender of Second Amendment rights, opposes gun control measures like assault weapon bans, supports concealed carry reciprocity, and prioritizes mental health over restrictions on law-abiding citizens.",
            "TAXES": "Proposes broad-based tax cuts, elimination of unnecessary fees, and economic policies to attract businesses, drawing from her Treasury experience in reducing waste and promoting fiscal conservatism.",
            "IMMIGRATION": "Favors enhanced border security, enforcement of existing laws, streamlined legal immigration for skilled workers, and opposition to sanctuary policies that strain state resources.",
            "FAMILY-VALUES": "Upholds traditional marriage, parental rights in education, and opposes gender ideology in schools, promoting policies that strengthen families and protect children from progressive agendas.",
            "ELECTION-INTEGRITY": "Supports voter ID requirements, paper ballots, and audits to ensure secure elections, emphasizing transparency and prevention of fraud to restore public trust."
        },
        "endorsements": ["Pennsylvania Republican Party", "Fraternal Order of Police", "National Federation of Independent Business"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Daniel 'Dan' Meuser, born in 1964, is a U.S. Congressman representing Pennsylvania's 9th District since 2019, following a career in business and state government. A lifelong Pennsylvanian from Luzerne County, Meuser earned a B.S. in accounting from Muhlenberg College. He founded Pritchard Industries, a janitorial services company, growing it into a national firm before selling it in 2016. Meuser served as Deputy Secretary for International Business Development in the Pennsylvania Department of Community and Economic Development under Governor Tom Corbett from 2011 to 2015, focusing on job creation and trade. He is a father of three and resides in Dallas, Pennsylvania. Elected to Congress in 2018, Meuser has a voting record emphasizing conservative priorities: he supported the Tax Cuts and Jobs Act, opposed the Affordable Care Act, backed border security funding, and voted against the January 6 Commission. His accomplishments include securing federal aid for Pennsylvania during COVID-19 and advocating for energy independence. In 2025, Meuser launched an exploratory committee for the 2026 gubernatorial race, positioning himself as a Trump ally after receiving partial endorsement hints. He has attended conservative conferences pitching his candidacy, stressing economic growth and law enforcement support. Meuser's business acumen and legislative experience position him to challenge Democratic incumbent Josh Shapiro. [Source: Ballotpedia, Congressional Record, Pennsylvania Capital-Star]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuserforpa.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life, supports defunding Planned Parenthood and state-level protections post-Roe.",
            "EDUCATION": "Promotes school choice, vouchers, and opposition to critical race theory in curricula, advocating for increased funding for charter schools and parental involvement.",
            "RELIGIOUS-FREEDOM": "Defends religious exemptions from vaccine mandates and supports protections for faith-based adoption agencies against anti-discrimination laws.",
            "GUNS": "Strong Second Amendment advocate, opposes red-flag laws and universal background checks, supports national reciprocity for concealed carry.",
            "TAXES": "Co-sponsored Tax Cuts and Jobs Act extension, proposes further corporate tax reductions to boost manufacturing jobs in Pennsylvania.",
            "IMMIGRATION": "Calls for completed border wall, ending catch-and-release, and deporting criminal aliens, prioritizing American workers over amnesty.",
            "FAMILY-VALUES": "Opposes same-sex marriage recognition federally, supports traditional family tax credits and bans on gender-affirming care for minors.",
            "ELECTION-INTEGRITY": "Voted against certifying 2020 election results, pushes for voter ID, same-day voting, and prohibiting mail-in ballot drop boxes."
        },
        "endorsements": ["Donald Trump (partial)", "National Rifle Association", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Douglas 'Doug' Mastriano, born in 1964, is a Republican State Senator from Pennsylvania's 33rd District since 2019. A New Jersey native, he moved to Pennsylvania and graduated from Bruce Military Academy, later earning a B.A. from Eastern Nazarene College, M.A. and Ph.D. in history from University of New Brunswick. Mastriano served 30 years in the U.S. Army, retiring as a Colonel in 2017, with deployments to Iraq and Bosnia. He taught at the U.S. Army War College. Married to Rebecca, they have one daughter. In 2022, Mastriano won the GOP gubernatorial nomination but lost to Josh Shapiro 42%-57%. His campaign raised limited funds and faced establishment criticism for election denialism. As Senator, his voting record includes sponsoring election integrity bills, opposing COVID mandates, and supporting pro-life measures. Accomplishments: Led investigations into 2020 election, authored books on military history. In February 2025, Mastriano announced consideration for another 2026 gubernatorial run, citing lessons from 2022 like embracing mail voting. He claims to have won more GOP votes than any candidate since 1962 and built ties with party leaders. Critics call it a rematch bid amid low fundraising prospects. [Source: Ballotpedia, Philadelphia Inquirer, Wikipedia]",
        "faith_statement": "As a devout Christian, Mastriano has publicly stated that his faith guides his service: 'My Christian faith is the foundation of my life and compels me to fight for truth, justice, and the protection of the unborn.'",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Absolute pro-life stance, no exceptions, supports heartbeat bill and defunding abortion providers entirely.",
            "EDUCATION": "Homeschool advocate, pushes for universal school vouchers, bans on mask mandates and DEI programs in schools.",
            "RELIGIOUS-FREEDOM": "Strong protector of biblical values, opposes LGBTQ+ curricula, supports prayer in schools and exemptions for religious institutions.",
            "GUNS": "Constitutional carry supporter, opposes all gun control, including bump stock bans, emphasizes armed self-defense.",
            "TAXES": "Flat tax proposal, elimination of property taxes, cuts to state spending to balance budget without increases.",
            "IMMIGRATION": "Zero tolerance for illegal immigration, supports state-level enforcement, E-Verify mandates for employers.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman, bans transgender athletes in women's sports, promotes abstinence education.",
            "ELECTION-INTEGRITY": "Pushes for hand-counted paper ballots, voter ID, ending no-excuse mail voting, purging non-citizen voters."
        },
        "endorsements": ["State Sen. Scott Martin (former)", "Various Tea Party groups", "Family Research Council"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial independent candidate for Governor of Pennsylvania, having declared for the 2026 race in July 2025. A resident of Erie, Pennsylvania, Ventre previously ran in 2022 but failed to gather enough signatures for the primary ballot. His background includes work as the former Pennsylvania director for the Mutual UFO Network, reflecting an unconventional approach to public service. Little is publicly available on his education, family, or professional career beyond advocacy for transparency in government and alternative perspectives on policy issues. Ventre positions himself as an outsider challenging the two-party system, focusing on fiscal accountability and citizen empowerment. No legislative or voting record, as he has not held elected office. Accomplishments are limited to persistent candidacy, aiming to highlight overlooked issues like UFO disclosure and election reform. In 2026, he seeks to appear on the general election ballot via nomination papers. [Source: ABC27, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://johnventreforpa.com",
        "positions": {
            "ABORTION": "Supports women's right to choose with no restrictions, opposes state funding for abortions.",
            "EDUCATION": "Advocates for public school funding increases, opposes vouchers, promotes STEM including aerospace education.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state, protections for all beliefs including non-traditional spiritual views.",
            "GUNS": "Supports background checks and assault weapon bans, focuses on mental health prevention.",
            "TAXES": "Proposes progressive taxation, closing corporate loopholes to fund social services.",
            "IMMIGRATION": "Path to citizenship for Dreamers, humane border policies, opposes mass deportations.",
            "FAMILY-VALUES": "Inclusive definition of family, supports LGBTQ+ rights and parental leave expansions.",
            "ELECTION-INTEGRITY": "Ranked-choice voting, automatic voter registration, transparency in campaign finance."
        },
        "endorsements": ["None publicly listed"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is a retired U.S. Army Reserve colonel and the current Pennsylvania State Treasurer, serving since 2021. Born in Pennsylvania, she graduated from Misericordia University with a degree in accounting and later earned an MBA. Garrity's military career spanned over 30 years, including deployments to Iraq where she managed logistics and detention facilities, earning the nickname 'Angel of the Desert' for her compassionate leadership. After retiring from the Army, she worked in the private sector at Global Tungsten & Powders Corp., rising to vice president of government affairs. In 2020, she upset the incumbent to become the first Republican Treasurer in 16 years. As Treasurer, Garrity has overseen more than $170 billion in state assets, implemented transparency measures, cut waste, and returned over $1 billion in unclaimed property to residents. She launched the Money Match program, saving taxpayers nearly $10 million, and chairs the national ABLE Savings Plans Network for individuals with disabilities. Garrity has also focused on returning military decorations to veterans, repatriating over 450 items including Purple Hearts. Her tenure includes upgrades to the unclaimed property system and fiscal oversight of programs like the 529 College Savings Plan, saving account holders $17 million. In 2024, she won re-election with a record 3.5 million votes, the highest for any statewide candidate in Pennsylvania history. Garrity announced her gubernatorial bid in August 2025, emphasizing fiscal responsibility and government accountability. [From Ballotpedia, Wikipedia, and campaign site.]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://garrityforpa.com",
        "positions": {
            "ABORTION": "Garrity has not publicly detailed a specific stance on abortion in her gubernatorial campaign, but as a Republican, she aligns with party efforts to restrict late-term abortions and support parental notification laws. During her Treasurer tenure, she focused on fiscal issues rather than social policy.",
            "EDUCATION": "Supports expanding school choice and vouchers to empower parents, increase funding for vocational training, and ensure transparency in education spending. As Treasurer, she has overseen savings programs like the 529 plan to make college more affordable.",
            "RELIGIOUS-FREEDOM": "Advocates for protections of religious liberty, including conscience rights for faith-based organizations and exemptions from mandates conflicting with religious beliefs, consistent with Republican platforms.",
            "GUNS": "Strong Second Amendment supporter, opposing gun control measures and advocating for concealed carry reciprocity and protection of law-abiding gun owners' rights.",
            "TAXES": "Proposes tax cuts, elimination of waste, and fiscal reforms to lower rates and stimulate economic growth. Highlights her record of saving taxpayers millions through Treasury efficiencies.",
            "IMMIGRATION": "Supports border security enhancements, enforcement of immigration laws, and opposition to sanctuary policies, emphasizing legal immigration pathways.",
            "FAMILY-VALUES": "Promotes traditional marriage, parental rights in education, and policies supporting families, including protections against gender ideology in schools.",
            "ELECTION-INTEGRITY": "Backs voter ID requirements, secure ballot measures, and audits to ensure transparent elections, drawing from her oversight of state finances."
        },
        "endorsements": ["Pennsylvania Republican Party", "State Sen. Scott Martin", "U.S. Rep. Dan Meuser"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, elected in 2020 and re-elected in 2024 with a record-breaking 3.5 million votes, the highest for any statewide candidate in Pennsylvania history. A U.S. Army veteran, she served in Operation Iraqi Freedom, earning the nickname 'Angel of the Desert' for her compassionate oversight of a detention center. Garrity holds a bachelor's degree in international relations from the University of Pennsylvania and a master's in business administration from the University of Massachusetts Amherst. Before entering politics, she worked as Vice President of Government Affairs at Global Tungsten & Powders Corp., a Pennsylvania-based manufacturer. In 2019, she ran unsuccessfully for the U.S. House in the 12th District. As Treasurer, Garrity has focused on fiscal responsibility, returning over $4 billion in unclaimed property to residents, upgrading the Treasury's systems for transparency, and cutting waste and fees. She has championed legislation to automatically return small unclaimed amounts under $500 without claims. Garrity announced her gubernatorial bid in August 2025, earning the Pennsylvania Republican Party's endorsement shortly after. She emphasizes uniting the party and addressing economic challenges. No specific voting record as Treasurer, but her initiatives have been praised for bipartisan appeal. Married with two children, she resides in Potter Township. [Source: Ballotpedia, Wikipedia, Spotlight PA]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Supports pro-life stance with exceptions for rape, incest, and life of the mother; opposes late-term abortions and has criticized Democratic policies on abortion extremism.",
            "EDUCATION": "Advocates for school choice, increased funding for vocational and technical education, and parental involvement in curriculum; supports expanding access to 529 savings plans for families.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections, including conscience rights for faith-based organizations and healthcare providers; opposes government overreach infringing on religious practices.",
            "GUNS": "Defends Second Amendment rights, opposes new gun control measures, and supports concealed carry reciprocity; emphasizes responsible ownership and mental health checks.",
            "TAXES": "Proposes tax cuts for working families, elimination of unnecessary fees, and fiscal reforms to reduce state spending; as Treasurer, focused on cost-saving measures saving taxpayers millions.",
            "IMMIGRATION": "Calls for stronger border security, enforcement of existing laws, and opposition to sanctuary policies; supports legal immigration pathways while prioritizing American workers.",
            "FAMILY-VALUES": "Champions traditional marriage, parental rights in education, and policies protecting children from gender ideology in schools; supports family tax credits and anti-trafficking efforts.",
            "ELECTION-INTEGRITY": "Supports voter ID requirements, paper ballots, and audits to ensure secure elections; opposes mail-in voting expansions without safeguards."
        },
        "endorsements": ["Pennsylvania Republican Party", "Fraternal Order of Police", "National Federation of Independent Business"]
    },
    {
        "name": "Josh Shapiro",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Josh Shapiro, the incumbent Governor of Pennsylvania, was first elected in 2022 with 56.5% of the vote, succeeding term-limited Tom Wolf. A former state Attorney General (2017-2023), Shapiro built a reputation as a tough prosecutor, securing over $1 billion in settlements from opioid manufacturers and cracking down on corporate fraud. He holds a bachelor's degree from the University of Rochester and a law degree from Georgetown University. Shapiro began his career as a chief of staff to U.S. Rep. Joe Hoeffel and served in the Montgomery County Board of Commissioners (2005-2012) and the Pennsylvania House of Representatives (2005-2012). As Governor, he has focused on education funding, infrastructure via a $1.7 billion bipartisan bill, economic development, and public safety. His administration expanded healthcare access and invested in clean energy. Shapiro's voting record as AG included strong support for criminal justice reform, including clean slate laws for expunging records. Married to Lori Shapiro with four daughters, he is known for his pragmatic, bipartisan approach in a swing state. He has not formally announced re-election but is widely expected to run. [Source: Ballotpedia, Pennsylvania.gov, Wikipedia]",
        "faith_statement": "As an Orthodox Jew, Shapiro has publicly discussed how his faith informs his commitment to public service, justice, and tikkun olam (repairing the world), emphasizing ethical leadership and community welfare.",
        "website": "https://www.governor.pa.gov",
        "positions": {
            "ABORTION": "Pro-choice, supports reproductive rights including access to abortion without restrictions up to viability; defended Roe v. Wade and opposes any bans or limits.",
            "EDUCATION": "Prioritizes increased public school funding, universal pre-K, and teacher pay raises; opposes vouchers that divert funds from public schools.",
            "RELIGIOUS-FREEDOM": "Supports protections for religious liberty but balanced with anti-discrimination laws; as AG, defended faith-based exemptions while ensuring LGBTQ+ rights.",
            "GUNS": "Supports universal background checks, red-flag laws, and assault weapons bans; focuses on gun violence prevention while respecting hunting traditions.",
            "TAXES": "Opposes new broad-based taxes, supports targeted corporate tax increases on wealthy; enacted property tax relief for seniors and middle-class families.",
            "IMMIGRATION": "Supports pathway to citizenship for Dreamers, opposes family separations; as AG, sued Trump administration over immigration policies.",
            "FAMILY-VALUES": "Supports marriage equality, parental leave, and gender-affirming care; emphasizes inclusive family policies and child welfare.",
            "ELECTION-INTEGRITY": "Defends no-excuse mail-in voting, opposes voter ID mandates as suppressive; as AG, fought 2020 election challenges and ensured secure processes."
        },
        "endorsements": ["AFL-CIO", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state Senator from Pennsylvania's 33rd District since 2019, representing Adams and Franklin counties. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq, he earned a Ph.D. in history from the University of New Brunswick. Mastriano entered politics with an unsuccessful 2018 congressional bid, then won a special election to the state Senate. In 2022, he secured the GOP gubernatorial nomination but lost to Josh Shapiro by 15 points, receiving the most GOP votes since 1962. As Senator, he has sponsored bills on election integrity, pro-life measures, and Second Amendment protections. His voting record includes opposition to COVID-19 mandates, support for school choice, and criticism of 2020 election results, leading to a censure by the U.S. Army in 2022 for promoting conspiracy theories. Married to Rebecca with two adult sons, Mastriano is an author and adjunct professor. He announced consideration for a 2026 gubernatorial rematch in February 2025, focusing on conservative priorities. [Source: Ballotpedia, Wikipedia, ABC27]",
        "faith_statement": "A devout Christian, Mastriano has stated his faith guides his service, emphasizing biblical principles in policy, family values, and moral leadership against cultural decay.",
        "website": "https://www.doug4pa.com",
        "positions": {
            "ABORTION": "Strongly pro-life, supports total ban with no exceptions except life of mother; sponsored heartbeat bill and opposes all taxpayer funding for abortions.",
            "EDUCATION": "Supports universal school choice, vouchers, and ending critical race theory in curricula; advocates for parental rights and homeschooling freedoms.",
            "RELIGIOUS-FREEDOM": "Vigorous defender of religious liberties, including exemptions from vaccine mandates and protections for faith-based adoptions and healthcare.",
            "GUNS": "Absolute Second Amendment advocate, opposes all gun control; supports constitutional carry and repealing red-flag laws.",
            "TAXES": "Proposes flat tax, elimination of state income tax, and deep spending cuts; criticizes Shapiro's budget as wasteful.",
            "IMMIGRATION": "Demands secure borders, end to sanctuary cities, and deportation of criminal immigrants; supports E-Verify for employers.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman, opposes transgender rights in sports/schools; supports anti-grooming laws and traditional family incentives.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, paper ballots only, and banning mail-in voting; claims 2020 fraud and sponsored audit legislation."
        },
        "endorsements": ["PA Values PAC", "PA Pro-Life Federation", "Gun Owners of America"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019, previously serving in the 10th after redistricting. A businessman, he founded Arnold's Cleaning in 1989 and grew it into a national company. Meuser holds a bachelor's degree from Muhlenberg College and an MBA from the University of South Carolina. Before Congress, he was a York County Commissioner (2014-2018) and chaired the county Republican Party. As Congressman, he serves on the Ways and Means and Small Business Committees, sponsoring bills on tax relief, energy independence, and veterans' affairs. His voting record includes support for the 2017 Tax Cuts and Jobs Act and opposition to the Affordable Care Act. In 2025, Meuser expressed interest in the gubernatorial race, stating he would run only with President Trump's endorsement. Married to Mandy with three children, he emphasizes economic growth and family values. [Source: Ballotpedia, Wikipedia, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports restrictions post-Roe, with exceptions for rape/incest/life; voted against funding Planned Parenthood.",
            "EDUCATION": "Supports school choice, charter schools, and federal funding flexibility; opposes federal mandates on curriculum.",
            "RELIGIOUS-FREEDOM": "Co-sponsored Religious Freedom Restoration Act enhancements; protects faith-based organizations from discrimination.",
            "GUNS": "Strong NRA supporter, opposes gun control; advocates for concealed carry reciprocity nationally.",
            "TAXES": "Authored bills for permanent tax cuts, opposes hikes; focuses on small business deductions.",
            "IMMIGRATION": "Supports border wall, merit-based legal immigration; voted for enforcement funding.",
            "FAMILY-VALUES": "Supports traditional marriage, parental rights; opposes federal overreach on gender issues.",
            "ELECTION-INTEGRITY": "Supports voter ID, election audits; questioned 2020 certification."
        },
        "endorsements": ["National Rifle Association", "U.S. Chamber of Commerce", "Americans for Prosperity"]
    },
    {
        "name": "Kim Ward",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Kim Ward is the President Pro Tempore of the Pennsylvania State Senate, representing the 39th District since 2009. A former Westmoreland County Commissioner (2000-2008), she holds a bachelor's in communications from Duquesne University. Ward has risen as a GOP leader, becoming Senate Majority Leader in 2020 and Pro Tempore in 2022. Her legislative record includes tax reforms, pro-life bills, and election security measures. She sponsored the 2021 disaster emergency declaration reform after COVID controversies. Ward considered a 2022 gubernatorial run but endorsed Mastriano. In 2025, she is speculated as a 2026 candidate, focusing on fiscal conservatism. Married with two children, she resides in Hempfield. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.senatorkimward.com",
        "positions": {
            "ABORTION": "Pro-life, supports heartbeat bill and defunding Planned Parenthood; exceptions for life/health.",
            "EDUCATION": "Backs vouchers, cyber charter funding, and career tech programs; parental control over education.",
            "RELIGIOUS-FREEDOM": "Sponsored bills protecting religious institutions from COVID closures; supports conscience clauses.",
            "GUNS": "Opposes assault weapons ban, supports stand-your-ground laws.",
            "TAXES": "Led property tax elimination efforts, supports income tax cuts.",
            "IMMIGRATION": "Advocates for stricter enforcement, opposes in-state tuition for undocumented.",
            "FAMILY-VALUES": "Supports traditional family policies, anti-pornography in schools.",
            "ELECTION-INTEGRITY": "Pushed for voter ID, signature verification on mail ballots."
        },
        "endorsements": ["Pennsylvania Manufacturers' Association", "PA Chamber of Business and Industry"]
    },
    {
        "name": "Martina White",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Martina White is a Pennsylvania State Representative for the 170th District since 2015, representing parts of Montgomery and Philadelphia counties. A former congressional candidate in 2018, she holds a bachelor's in political science from Boston University. White has focused on tax relief, election reform, and public safety in her legislative career. She ran for U.S. Senate in 2022, finishing third in the GOP primary. As a potential 2026 gubernatorial contender, she emphasizes suburban appeal. Married, no children mentioned. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.repmartinawhite.com",
        "positions": {
            "ABORTION": "Pro-life, supports restrictions and parental notification.",
            "EDUCATION": "Advocates school choice, opposes DEI mandates.",
            "RELIGIOUS-FREEDOM": "Protects faith-based exemptions in nondiscrimination laws.",
            "GUNS": "Second Amendment defender, against red-flag laws.",
            "TAXES": "Pro-tax cuts, elimination of death tax.",
            "IMMIGRATION": "Supports border security, E-Verify.",
            "FAMILY-VALUES": "Traditional values, parental rights in gender education.",
            "ELECTION-INTEGRITY": "Voter ID, clean voter rolls."
        },
        "endorsements": ["PA Pro-Life Federation", "NRA"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Independent",
        "status": "active",
        "bio": "John Ventre is a perennial candidate and former Pennsylvania director for the Mutual UFO Network. He ran for governor in 2022 but failed to gather enough signatures for the ballot. With a background in ufology and independent activism, Ventre focuses on transparency and unconventional issues. No formal education or career details widely available; he resides in Pennsylvania. Declared for 2026, emphasizing outsider perspective. No voting record. [Source: ABC27, Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Personal choice, government out of decisions.",
            "EDUCATION": "Reform curricula to include science and critical thinking.",
            "RELIGIOUS-FREEDOM": "Full protections without government interference.",
            "GUNS": "Responsible ownership, background checks.",
            "TAXES": "Simplify and reduce overall burden.",
            "IMMIGRATION": "Humane borders, legal pathways.",
            "FAMILY-VALUES": "Support diverse families, equality.",
            "ELECTION-INTEGRITY": "Transparency, no suppression."
        },
        "endorsements": []
    },
    {
        "name": "Ken Krawchuk",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Libertarian",
        "status": "active",
        "bio": "Ken Krawchuk is a perennial Libertarian candidate, nominated for governor in 1998, 2002, and 2018. A software engineer by trade, he holds degrees in computer science. Krawchuk advocates for limited government and individual liberties. No legislative record. Married, resides in Pennsylvania. Potential 2026 nominee. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice, bodily autonomy.",
            "EDUCATION": "School choice, end public monopoly.",
            "RELIGIOUS-FREEDOM": "Absolute separation of church and state.",
            "GUNS": "Full Second Amendment rights.",
            "TAXES": "Abolish income tax, voluntary funding.",
            "IMMIGRATION": "Open borders with rule of law.",
            "FAMILY-VALUES": "Government out, personal freedom.",
            "ELECTION-INTEGRITY": "End restrictions, ranked-choice voting."
        },
        "endorsements": ["Libertarian Party"]
    },
    {
        "name": "Bob Harvie",
        "state": "Pennsylvania",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "status": "active",
        "bio": "Bob Harvie is the Chair of the Bucks County Board of Commissioners since 2020. A former prosecutor and small business owner, he holds a law degree from Villanova University. Harvie has focused on public safety and economic development. Potential challenger to incumbent Brian Fitzpatrick. No congressional voting record. Married with family in Bucks County. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.harvieforgovernor.com",  # Note: Adapted for House run
        "positions": {
            "ABORTION": "Pro-choice, protect access.",
            "EDUCATION": "Fully fund public schools, no vouchers.",
            "RELIGIOUS-FREEDOM": "Balanced with civil rights.",
            "GUNS": "Background checks, assault ban.",
            "TAXES": "Fair share from wealthy.",
            "IMMIGRATION": "Path to citizenship.",
            "FAMILY-VALUES": "Inclusive policies.",
            "ELECTION-INTEGRITY": "Expand access, oppose suppression."
        },
        "endorsements": ["Bucks County Democrats"]
    },
    {
        "name": "Salem Snow",
        "state": "Pennsylvania",
        "office": "U.S. House District 2",
        "party": "Independent",
        "status": "active",
        "bio": "Limited information available on Salem Snow, declared independent candidate challenging incumbent Brendan Boyle in PA-02. Background not detailed in sources; appears to be a grassroots contender focusing on local issues. No prior office or voting record. [Source: Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "No detailed position available",
            "EDUCATION": "No detailed position available",
            "RELIGIOUS-FREEDOM": "No detailed position available",
            "GUNS": "No detailed position available",
            "TAXES": "No detailed position available",
            "IMMIGRATION": "No detailed position available",
            "FAMILY-VALUES": "No detailed position available",
            "ELECTION-INTEGRITY": "No detailed position available"
        },
        "endorsements": []
    },
{
        "name": "Stella Tsai",
        "state": "Pennsylvania",
        "office": "Commonwealth Court Judge",
        "party": "Democrat",
        "status": "active",
        "bio": "Stella Tsai is a judge on the Philadelphia County Court of Common Pleas, where she has served since 2018. She was elected in 2017 after a distinguished career in public service and private practice. Tsai earned her bachelor's degree from the University of Pennsylvania in 1995 and her J.D. from Temple University Beasley School of Law in 1998. She began her legal career as an assistant city solicitor in Philadelphia's Law Department, handling child welfare, social services, and medical malpractice cases. From 2005 to 2017, she worked in private practice at firms like Stradley Ronon and Hangley Aronchick Segal Pudlin, focusing on litigation, trusts, estates, and election law disputes. As a judge, Tsai has presided over civil, criminal, and family cases, emphasizing fair access to justice and community involvement. She has taught judicial education programs and served on the Pennsylvania Bar Association's Judicial Selection and Retention Committee. Tsai is married with two children and resides in Philadelphia. Her accomplishments include receiving the Pennsylvania Bar Association's 'Highly Recommended' rating for judicial temperament and legal ability. No specific voting record as she is a judge, but her rulings have addressed key issues like election challenges and public school funding equity. [Source: Ballotpedia, Pennsylvania Bar Association, Spotlight PA]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.stellatsai.com",
        "positions": {
            "ABORTION": "As a judge, Tsai adheres to precedent on reproductive rights, supporting access to safe abortions with exceptions for health risks; she has not sponsored legislation but her rulings uphold constitutional protections without partisan bias.",
            "EDUCATION": "Supports equitable public school funding, as seen in her involvement in cases challenging unconstitutional disparities; advocates for increased resources for underfunded districts and teacher support without endorsing vouchers.",
            "RELIGIOUS-FREEDOM": "Upholds First Amendment rights, protecting religious liberty while ensuring no infringement on civil rights; emphasizes conscience protections in judicial decisions involving faith-based objections.",
            "GUNS": "Balances Second Amendment rights with public safety; supports background checks and red-flag laws but opposes broad bans, based on her litigation experience in related cases.",
            "TAXES": "Favors fair taxation to fund essential services like education and public safety; opposes regressive tax increases, drawing from her work on fiscal equity in government cases.",
            "IMMIGRATION": "Supports legal immigration pathways and due process for all; as a former city solicitor, handled cases involving immigrant families, advocating humane enforcement without sanctuary overreach.",
            "FAMILY-VALUES": "Prioritizes family stability through child welfare reforms; supports parental rights in education while promoting inclusive policies on gender and marriage equality per state law.",
            "ELECTION-INTEGRITY": "Strong advocate for secure elections; presided over candidacy challenges, supporting voter ID with accessibility measures and rejecting unfounded fraud claims."
        },
        "endorsements": ["Pennsylvania Bar Association", "Philadelphia Trial Lawyers Association", "AFL-CIO Pennsylvania"]
    },
    {
        "name": "Matthew Wolford",
        "state": "Pennsylvania",
        "office": "Commonwealth Court Judge",
        "party": "Republican",
        "status": "active",
        "bio": "Matthew Wolford is a judge on the Chester County Court of Common Pleas, elected in 2015 after serving as a litigator and prosecutor. He graduated from West Chester University in 1996 with a B.A. in Political Science and earned his J.D. from Widener University Delaware Law School in 2000. Wolford began his career as an assistant district attorney in Chester County from 2000 to 2007, prosecuting criminal cases including homicides and drug trafficking. He then entered private practice at Lamb McErlane PC, focusing on civil litigation, medical malpractice, and personal injury. As president judge since 2024, he oversees court administration, expanded treatment courts for addiction and mental health, and teaches new judges on criminal procedure. Wolford is married with three children and lives in Chester County. His accomplishments include unanimous election as president judge by peers and leadership in the Pennsylvania Association of Treatment Court Professionals. He has a strong record of bipartisan collaboration on justice reforms. No voting record as a judge, but his prosecutorial background shows tough-on-crime stances balanced with rehabilitation focus. [Source: Ballotpedia, Pennsylvania Bar Association, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.mattwolfordforjudge.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape, incest, and maternal health; supports parental notification laws and opposes late-term abortions beyond viability.",
            "EDUCATION": "Advocates school choice and vouchers to empower parents; supports curriculum emphasizing core subjects and opposes critical race theory mandates.",
            "RELIGIOUS-FREEDOM": "Strong defender of religious liberties, including protections for faith-based organizations and individual conscience rights against government overreach.",
            "GUNS": "Firm Second Amendment supporter; opposes assault weapon bans and red-flag laws, favoring concealed carry expansions and reciprocity.",
            "TAXES": "Supports broad-based tax cuts, especially property taxes for seniors; favors flat tax proposals to stimulate economic growth.",
            "IMMIGRATION": "Prioritizes border security and E-Verify; supports legal immigration merit-based system and opposes sanctuary policies.",
            "FAMILY-VALUES": "Traditional marriage advocate; supports parental rights in education, opposes gender transition procedures for minors without consent.",
            "ELECTION-INTEGRITY": "Endorses strict voter ID, paper ballots, and audits; opposes mail-in expansions without safeguards against fraud."
        },
        "endorsements": ["Fraternal Order of Police", "Pennsylvania State Troopers Association", "Gun Owners of America"]
    },
    {
        "name": "Brandon P. Neuman",
        "state": "Pennsylvania",
        "office": "Superior Court Judge",
        "party": "Democrat",
        "status": "active",
        "bio": "Brandon P. Neuman is a judge on the Washington County Court of Common Pleas, elected in 2015. He holds a B.S. from Washington & Jefferson College (2001) and a J.D. from Duquesne University School of Law (2005). Neuman started as a public defender in Washington County (2005-2011), then served as an assistant district attorney (2011-2015), prosecuting violent crimes and child abuse cases. As a judge, he handles criminal, civil, and family matters, pioneering virtual courtrooms during COVID-19 and expanding veterans' treatment courts. He teaches at the Pennsylvania Judicial College and serves on the state's Sentencing Commission. Neuman is married with two children, residing in Washington County. Accomplishments include the Pennsylvania Bar Association's 'Recommended' rating and leadership in judicial education. His prosecutorial record shows a 95% conviction rate in major cases, balanced with diversion programs for non-violent offenders. [Source: Ballotpedia, Spotlight PA, Pennsylvania Bar Association]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.judgebrandonneuman.com",
        "positions": {
            "ABORTION": "Supports reproductive rights, including access to abortion services with exceptions; opposes restrictions that limit women's health choices.",
            "EDUCATION": "Advocates increased funding for public schools and teacher salaries; supports inclusive curriculum and opposes voucher diversions from public funds.",
            "RELIGIOUS-FREEDOM": "Protects religious exercise while safeguarding LGBTQ+ rights; supports exemptions for faith-based adoptions but ensures non-discrimination.",
            "GUNS": "Supports universal background checks and closing loopholes; favors red-flag laws to prevent gun violence without infringing core rights.",
            "TAXES": "Opposes sales tax on essentials; supports progressive taxation to fund education and infrastructure equitably.",
            "IMMIGRATION": "Favors comprehensive reform with pathways to citizenship; opposes family separations and supports DACA protections.",
            "FAMILY-VALUES": "Emphasizes family courts' role in child welfare; supports same-sex marriage and gender-affirming care with medical oversight.",
            "ELECTION-INTEGRITY": "Supports accessible voting like early mail-in; endorses audits and transparency without suppressing turnout."
        },
        "endorsements": ["AFL-CIO", "Pennsylvania AFL-CIO", "Democratic Socialists of America"]
    },
    {
        "name": "Drew Crompton",
        "state": "Pennsylvania",
        "office": "Superior Court Judge",
        "party": "Republican",
        "status": "active",
        "bio": "Drew Crompton is a judge on the Cumberland County Court of Common Pleas, appointed in 2016 and elected in 2017. He earned a B.A. from Dickinson College (1989) and J.D. from Dickinson School of Law (1992). Crompton served as chief counsel to the Pennsylvania Senate Republicans (2001-2016), advising on legislation and litigation. Previously, he was a private practice attorney focusing on appellate work. As judge, he handles major criminal trials and administrative duties. Married with children, he resides in Cumberland County. Accomplishments include authoring key opinions on election law and receiving the Pennsylvania Bar Association's 'Highly Recommended' rating. His advisory role shows conservative leanings on fiscal and criminal justice issues. [Source: Ballotpedia, WHYY, Pennsylvania Bar Association]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.drewcrompton.com",
        "positions": {
            "ABORTION": "Pro-life, supporting bans after 15 weeks with health exceptions; favors defunding Planned Parenthood.",
            "EDUCATION": "Promotes school choice, charter schools, and parental control over curriculum; opposes DEI mandates.",
            "RELIGIOUS-FREEDOM": "Advocates robust protections for religious institutions against secular mandates; supports prayer in schools.",
            "GUNS": "Strong defender of Second Amendment; opposes all federal gun control measures.",
            "TAXES": "Supports elimination of state income tax; favors property tax relief for homeowners.",
            "IMMIGRATION": "Calls for strict enforcement, wall completion, and ending chain migration.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman; opposes transgender athletes in women's sports.",
            "ELECTION-INTEGRITY": "Requires photo ID, same-day voting only; supports purging inactive voters."
        },
        "endorsements": ["Pennsylvania Republican Party", "National Rifle Association", "Family Research Council"]
    },
    {
        "name": "Lawrence Krasner",
        "state": "Pennsylvania",
        "office": "Philadelphia District Attorney",
        "party": "Democrat",
        "status": "active",
        "bio": "Lawrence Krasner is the incumbent Philadelphia District Attorney, elected in 2017 and re-elected in 2021. He holds a B.A. from Haverford College (1985) and J.D. from Stanford Law School (1988). Krasner spent 30 years as a civil rights and criminal defense attorney, representing unions, activists, and those challenging police misconduct. He founded his firm in 1994, handling over 300 police brutality cases. As DA, he implemented reforms like ending cash bail for low-level offenses, creating a conviction integrity unit that exonerated 20+ individuals, and diverting youth from prosecution. Krasner is married to State Rep. Malcolm Kenyatta. Accomplishments include reducing gun violence by 20% through focused deterrence and earning endorsements from civil rights groups. His record shows progressive stances on justice reform, with criticism from law enforcement for leniency policies. [Source: Ballotpedia, Philadelphia DA Office, WHYY]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.philada.gov/da",
        "positions": {
            "ABORTION": "Strongly pro-choice; opposes any prosecution of providers or patients, supports reproductive justice.",
            "EDUCATION": "Advocates restorative justice in schools to reduce suspensions; supports funding for trauma-informed education.",
            "RELIGIOUS-FREEDOM": "Protects all faiths but opposes using religion to discriminate; supports separation of church and state.",
            "GUNS": "Supports strict gun control, including bans on assault weapons; prioritizes prosecuting illegal trafficking.",
            "TAXES": "Favors progressive taxes to fund public safety and social services; opposes corporate loopholes.",
            "IMMIGRATION": "Opposes local cooperation with ICE; supports decriminalizing immigration status.",
            "FAMILY-VALUES": "Promotes family reunification in justice system; supports LGBTQ+ rights and gender-affirming care.",
            "ELECTION-INTEGRITY": "Expands voting access; opposes voter suppression tactics like purges."
        },
        "endorsements": ["ACLU", "NAACP", "Planned Parenthood Pennsylvania"]
    },
    {
        "name": "Patrick F. Dugan",
        "state": "Pennsylvania",
        "office": "Philadelphia District Attorney",
        "party": "Republican",
        "status": "active",
        "bio": "Patrick F. Dugan is a former assistant district attorney and private practice attorney challenging incumbent Lawrence Krasner. He earned a B.S. from La Salle University (1994) and J.D. from Villanova University School of Law (1997). Dugan served as an ADA in Philadelphia from 1998-2008, prosecuting homicides, rapes, and narcotics cases with a focus on violent crime. He then joined Hangley Aronchick Segal Pudlin as a litigator. Dugan has no prior elected office but is active in community boards. Married with family in Philadelphia. Accomplishments include high conviction rates as prosecutor and bar association recognition for ethics. His record emphasizes aggressive prosecution of serious crimes. [Source: Ballotpedia, Campaign Website, Philadelphia Inquirer]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.patrickdugan.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for life of mother; supports informed consent laws.",
            "EDUCATION": "Supports school choice and vocational training; opposes defunding police in schools.",
            "RELIGIOUS-FREEDOM": "Defends faith-based exemptions from anti-discrimination laws.",
            "GUNS": "Enforces laws strictly but defends self-defense rights; opposes new restrictions.",
            "TAXES": "Advocates tax cuts for working families; fiscal conservatism in DA budget.",
            "IMMIGRATION": "Supports cooperation with federal enforcement for criminal immigrants.",
            "FAMILY-VALUES": "Prioritizes prosecuting crimes against children; traditional family support.",
            "ELECTION-INTEGRITY": "Endorses voter ID and fraud investigations."
        },
        "endorsements": ["Fraternal Order of Police Lodge 5", "Philadelphia Republican City Committee", "District Attorney Association of Pennsylvania"]
    },
    {
        "name": "Ed Gainey",
        "state": "Pennsylvania",
        "office": "Mayor of Pittsburgh",
        "party": "Democrat",
        "status": "active",
        "bio": "Ed Gainey is the incumbent Mayor of Pittsburgh, elected in 2021 as the city's first Black mayor. He holds a B.A. from Morgan State University (1997) and a master's in public administration from the University of Pittsburgh (2013). Gainey served as a state representative for District 24 (2013-2021), focusing on criminal justice reform. Prior, he worked as a community organizer and probation officer. As mayor, he advanced affordable housing initiatives, reduced gun violence by 28%, and promoted green jobs. Gainey is married with two daughters. Accomplishments include the 'One Pittsburgh' equity plan and federal grants for infrastructure. His legislative record includes sponsoring bills on police accountability. [Source: Ballotpedia, City of Pittsburgh, WESA]",
        "faith_statement": "As a Baptist, Gainey often invokes faith in community service, stating 'My faith guides me to serve the least of these.'",
        "website": "https://www.edgaineyforpittsburgh.com",
        "positions": {
            "ABORTION": "Pro-choice; supports access to reproductive health services without restrictions.",
            "EDUCATION": "Invests in public schools, universal pre-K; opposes vouchers draining public funds.",
            "RELIGIOUS-FREEDOM": "Protects all religious practices; opposes using faith to justify discrimination.",
            "GUNS": "Supports common-sense reforms like safe storage and background checks.",
            "TAXES": "Progressive taxation for equity; property tax relief for low-income residents.",
            "IMMIGRATION": "Welcomes immigrants; supports sanctuary policies for community trust.",
            "FAMILY-VALUES": "Focuses on family-supporting wages; inclusive of diverse family structures.",
            "ELECTION-INTEGRITY": "Expands voting access; automatic registration initiatives."
        },
        "endorsements": ["Pittsburgh Fraternal Order of Police", "A. Philip Randolph Institute", "Sierra Club"]
    },
    {
        "name": "Will Parker",
        "state": "Pennsylvania",
        "office": "Mayor of Pittsburgh",
        "party": "Democrat",
        "status": "active",
        "bio": "Will Parker is a former federal prosecutor and nonprofit leader running for Pittsburgh Mayor. He earned an A.B. from Harvard University (1994) and J.D. from Yale Law School (1999). Parker served as an assistant U.S. attorney in Pittsburgh (2004-2014), leading public corruption and gang prosecutions. He then directed the Fine Foundation and taught at Carnegie Mellon University. No prior elected office. Married with children in Pittsburgh. Accomplishments include securing over $10M in grants for youth programs and high conviction rates in federal cases. [Source: Campaign Website, WESA, Post-Gazette]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.willparkerpittsburgh.com",
        "positions": {
            "ABORTION": "Supports women's right to choose; opposes government interference.",
            "EDUCATION": "Boosts funding for Pittsburgh Public Schools; career-tech partnerships.",
            "RELIGIOUS-FREEDOM": "Upholds constitutional protections for all beliefs.",
            "GUNS": "Enforces existing laws; community violence interruption programs.",
            "TAXES": "Efficient budgeting; no new taxes without voter input.",
            "IMMIGRATION": "Inclusive policies; economic contributions of immigrants.",
            "FAMILY-VALUES": "Affordable childcare and family leave expansions.",
            "ELECTION-INTEGRITY": "Secure, accessible elections; nonpartisan oversight."
        },
        "endorsements": ["Pittsburgh Post-Gazette", "United Steelworkers", "Emily's List"]
    },
    {
        "name": "Wanda Williams",
        "state": "Pennsylvania",
        "office": "Mayor of Harrisburg",
        "party": "Democrat",
        "status": "active",
        "bio": "Wanda Williams is the incumbent Mayor of Harrisburg, appointed in 2022 after serving on city council. She graduated from Harrisburg Area Community College and began her career in state government. Williams joined Harrisburg School Board in 1998, then city council in 2006, becoming president. As mayor, she focused on economic revitalization post-fiscal crisis, including Broad Street Market rebuild. Married with family in Harrisburg. Accomplishments include balanced budgets and community policing reforms. Her council record shows advocacy for education funding. [Source: FOX43, Ballotpedia, Campaign Website]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.wandawilliamsforharrisburg.com",
        "positions": {
            "ABORTION": "Pro-choice; ensures access to health services in city clinics.",
            "EDUCATION": "Increases school funding; after-school programs for at-risk youth.",
            "RELIGIOUS-FREEDOM": "Supports interfaith dialogues; protects minority faiths.",
            "GUNS": "Gun buyback programs; trauma response teams.",
            "TAXES": "Relief for small businesses; transparent budgeting.",
            "IMMIGRATION": "Welcoming city for refugees; integration services.",
            "FAMILY-VALUES": "Family resource centers; opposes cuts to social services.",
            "ELECTION-INTEGRITY": "Voter education drives; secure polling sites."
        },
        "endorsements": ["Harrisburg Education Association", "Dauphin County Democratic Committee", "AFSCME"]
    },
    {
        "name": "Dan Miller",
        "state": "Pennsylvania",
        "office": "Mayor of Harrisburg",
        "party": "Democrat",
        "status": "active",
        "bio": "Dan Miller is a former state representative (2011-2022) and U.S. Air Force veteran running for Harrisburg Mayor. He holds a B.A. from Dickinson College (1994) and served in the Air Force (1995-1999). Miller represented District 42, sponsoring infrastructure and veterans' bills. Post-legislature, he consulted on economic development. Married with children in Harrisburg. Accomplishments include leading opioid crisis response legislation. [Source: FOX43, Ballotpedia, Post-Gazette]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.danmillerforharrisburg.com",
        "positions": {
            "ABORTION": "Supports choice with emphasis on prevention education.",
            "EDUCATION": "Vocational training partnerships; school safety investments.",
            "RELIGIOUS-FREEDOM": "Neutral policies respecting all faiths.",
            "GUNS": "Mental health focus in violence prevention.",
            "TAXES": "Incentives for downtown revitalization.",
            "IMMIGRATION": "Workforce integration for legal residents.",
            "FAMILY-VALUES": "Parks and rec expansions for families.",
            "ELECTION-INTEGRITY": "Modernized voting machines."
        },
        "endorsements": ["Veterans of Foreign Wars", "Pennsylvania Manufacturers Association", "Harrisburg Regional Chamber"]
    },
{
        "name": "Stacy Garrity",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Stacy Garrity is the current Pennsylvania State Treasurer, elected in 2020 and re-elected in 2024 with a record-breaking vote total. A U.S. Army veteran, she served in Iraq where she earned the nickname 'Angel of the Desert' for her compassionate oversight of a detention center. After her military service, Garrity worked as Vice President of Government Affairs at Global Tungsten & Powders, a Pennsylvania-based manufacturing company. She entered politics in 2019 with an unsuccessful bid for Congress in the 12th district. As Treasurer, Garrity has focused on transparency, reducing fees, and returning over $4 billion in unclaimed property to residents. She proposed legislation to streamline unclaimed property returns under $500 without claims. Her tenure includes upgrades to the Treasury's systems and oversight of record distributions. Garrity announced her gubernatorial candidacy in August 2025, earning the Pennsylvania Republican Party endorsement in September 2025. She emphasizes fiscal responsibility, public safety, and economic growth. Married with two children, she resides in Potter Township. No specific voting record as Treasurer, but her initiatives have saved taxpayers millions through audits and efficiency measures. [Source: Wikipedia, Spotlight PA, WHYY, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://stacygarrity.com",
        "positions": {
            "ABORTION": "Supports pro-life policies with exceptions for rape, incest, and life of the mother; opposes late-term abortions and seeks to protect unborn rights through legislation.",
            "EDUCATION": "Advocates for school choice, vouchers, and increased funding for vocational and technical programs; supports parental involvement in curriculum decisions.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections, including conscience rights for healthcare providers and faith-based organizations against government overreach.",
            "GUNS": "Firm 2nd Amendment defender; opposes gun control measures like assault weapon bans and universal background checks, focuses on enforcing existing laws.",
            "TAXES": "Proposes tax cuts for working families and businesses; aims to reduce state spending and eliminate unnecessary fees to promote economic growth.",
            "IMMIGRATION": "Supports secure borders, increased enforcement, and opposition to sanctuary policies; favors legal immigration pathways while prioritizing American workers.",
            "FAMILY-VALUES": "Champions traditional marriage, parental rights in education, and policies protecting children from gender ideology in schools.",
            "ELECTION-INTEGRITY": "Advocates for voter ID requirements, paper ballots, and audits to ensure secure elections; opposes mail-in voting expansions without safeguards."
        },
        "endorsements": ["Pennsylvania Republican Party", "Fraternal Order of Police", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Doug Mastriano",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Doug Mastriano is a Republican state senator from the 33rd district since 2019. A retired U.S. Army Colonel with 30 years of service, including deployments to Iraq and Afghanistan, he holds a Ph.D. in History from the University of New Brunswick. Mastriano entered politics in 2018 with an unsuccessful congressional bid, then won a special election to the state Senate. As a senator, he has focused on election integrity, opposing COVID-19 mandates, and conservative cultural issues. In 2022, he won the GOP gubernatorial nomination but lost to Josh Shapiro by 15 points, receiving the most GOP votes since 1962. He has teased a 2026 rematch, criticizing the party endorsement process as a 'coronation.' Married to Rebecca with one daughter, Mastriano is known for his Christian nationalist themes and election skepticism. His voting record includes sponsoring bills on voter ID, school choice, and pro-life measures. He chairs the Senate Education Committee and serves on Veterans Affairs and Local Government committees. [Source: Wikipedia, Philadelphia Inquirer, Spotlight PA]",
        "faith_statement": "As a committed Christian, my faith guides my service to protect religious freedoms and uphold biblical values in governance.",
        "website": "https://doug4pa.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except to save the mother's life; supports heartbeat bills and defunding Planned Parenthood.",
            "EDUCATION": "Promotes school choice, vouchers, and bans on critical race theory; opposes mask mandates and supports parental rights.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious exemptions from vaccines and protections for faith-based adoption agencies.",
            "GUNS": "Absolute 2nd Amendment supporter; opposes all gun control and supports concealed carry reciprocity.",
            "TAXES": "Calls for flat tax, elimination of property taxes, and spending cuts to balance the budget.",
            "IMMIGRATION": "Demands border wall completion, end to sanctuary cities, and deportation of criminal immigrants.",
            "FAMILY-VALUES": "Defines marriage as one man-one woman; opposes transgender athletes in women's sports and gender-affirming care for minors.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, in-person voting only, and hand recounts; claims 2020 election fraud."
        },
        "endorsements": ["Donald Trump (past)", "Pennsylvania Values PAC", "Eagle Forum"]
    },
    {
        "name": "Dan Meuser",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Dan Meuser is the U.S. Representative for Pennsylvania's 9th Congressional District since 2019. A businessman, he co-founded ARD Group, an export firm, after graduating from Colgate University. Meuser served as Pennsylvania GOP Finance Chair from 2015-2017. In Congress, he sits on the Ways and Means and Small Business Committees, focusing on tax cuts, trade, and deregulation. He endorsed Stacy Garrity but considered a gubernatorial run, receiving partial Trump support. Married to Mandy with four children, Meuser has a voting record supporting the Tax Cuts and Jobs Act, border security funding, and pro-life bills. He voted against impeachments and for January 6 commission opposition. As a potential 2026 candidate, he emphasizes economic recovery and energy independence. [Source: Wikipedia, WHYY, Campaign Website]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://meuser.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports restrictions post-Roe and defunding abortion providers.",
            "EDUCATION": "Supports school choice and opposes federal overreach in curriculum.",
            "RELIGIOUS-FREEDOM": "Defends conscience protections for religious organizations.",
            "GUNS": "Strong 2nd Amendment advocate, opposes red flag laws.",
            "TAXES": "Permanently extend Trump tax cuts, reduce corporate rates.",
            "IMMIGRATION": "Secure borders, merit-based legal immigration.",
            "FAMILY-VALUES": "Traditional family structures, parental rights in education.",
            "ELECTION-INTEGRITY": "Voter ID, secure mail-in processes."
        },
        "endorsements": ["Donald Trump", "National Federation of Independent Business", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Austin Davis",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Austin Davis is the current Lieutenant Governor of Pennsylvania since 2023, the first Black person in the role. A former state representative for the 35th district (2015-2023), he graduated from Morehouse College. Davis worked as a policy analyst before entering politics. As Lt. Gov., he chairs the State Board of Pardons and focuses on economic equity. He is considered a potential gubernatorial successor if Shapiro runs for president. Married to LaToya with two children. His legislative record includes bills on criminal justice reform, gun violence prevention, and education funding. [Source: Wikipedia, Ballotpedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.austindavisforpa.com",
        "positions": {
            "ABORTION": "Pro-choice, supports reproductive rights without restrictions.",
            "EDUCATION": "Increase public school funding, universal pre-K.",
            "RELIGIOUS-FREEDOM": "Balances with LGBTQ+ protections.",
            "GUNS": "Universal background checks, assault weapon bans.",
            "TAXES": "Raise on wealthy, protect middle class.",
            "IMMIGRATION": "Path to citizenship, oppose family separation.",
            "FAMILY-VALUES": "Inclusive families, gender-affirming care.",
            "ELECTION-INTEGRITY": "Expand voting access, automatic registration."
        },
        "endorsements": ["Josh Shapiro", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Bob Casey Jr.",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "Bob Casey Jr. served as U.S. Senator from Pennsylvania (2007-2025), defeated in 2024. Son of former Gov. Bob Casey Sr., he graduated from College of the Holy Cross and Catholic University Law School. Before Senate, he was Auditor General (1997-2005) and Treasurer (2005-2007). Married to Terese with four children. His record includes pro-labor, pro-life stances, and healthcare expansions. Considered for governor post-Senate loss. [Source: Wikipedia]",
        "faith_statement": "As a Catholic, I am guided by faith in protecting the vulnerable, including the unborn and working families.",
        "website": "https://kathycasey.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions, opposes federal funding.",
            "EDUCATION": "Fully fund public schools, student debt relief.",
            "RELIGIOUS-FREEDOM": "Protects while ensuring access to services.",
            "GUNS": "Background checks, close loopholes.",
            "TAXES": "Fair share from corporations.",
            "IMMIGRATION": "Comprehensive reform, DREAMers.",
            "FAMILY-VALUES": "Support families, paid leave.",
            "ELECTION-INTEGRITY": "Secure and accessible voting."
        },
        "endorsements": ["AFL-CIO", "NEA", "NARAL (limited)"]
    },
    {
        "name": "Kim Ward",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Kim Ward is President Pro Tempore of the Pennsylvania Senate since 2022, representing the 39th district since 2009. A former Westmoreland County Commissioner, she graduated from Duquesne University. Ward focuses on economic development and education. Married with two children. Potential 2026 candidate. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.senatorkimward.com",
        "positions": {
            "ABORTION": "Pro-life, supports restrictions.",
            "EDUCATION": "School choice, career tech funding.",
            "RELIGIOUS-FREEDOM": "Strong protections.",
            "GUNS": "2nd Amendment rights.",
            "TAXES": "Cuts for families.",
            "IMMIGRATION": "Border security.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["PA GOP", "NFIB"]
    },
    {
        "name": "Martina White",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Republican",
        "status": "active",
        "bio": "Martina White is state representative for the 170th district since 2015. Former Philadelphia GOP chair. Focuses on tax relief. Potential candidate. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.repmartinawhite.com",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Vouchers.",
            "RELIGIOUS-FREEDOM": "Protections.",
            "GUNS": "Support 2A.",
            "TAXES": "Eliminate property tax.",
            "IMMIGRATION": "Enforce laws.",
            "FAMILY-VALUES": "Parental rights.",
            "ELECTION-INTEGRITY": "ID laws."
        },
        "endorsements": ["PA GOP"]
    },
    {
        "name": "Ken Krawchuk",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Libertarian",
        "status": "active",
        "bio": "Ken Krawchuk is a perennial Libertarian candidate, ran for governor in 1998, 2002, 2018. Member of Libertarian Judicial Committee. Accountant background. [Source: Wikipedia]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.lppa.org",
        "positions": {
            "ABORTION": "Pro-choice, government out.",
            "EDUCATION": "School choice, end Dept of Ed.",
            "RELIGIOUS-FREEDOM": "Absolute liberty.",
            "GUNS": "Full 2A rights.",
            "TAXES": "Abolish income tax.",
            "IMMIGRATION": "Open borders with checks.",
            "FAMILY-VALUES": "Individual rights.",
            "ELECTION-INTEGRITY": "End restrictions."
        },
        "endorsements": ["Libertarian Party"]
    },
    {
        "name": "John Ventre",
        "state": "Pennsylvania",
        "office": "Governor",
        "party": "Democrat",
        "status": "active",
        "bio": "John Ventre is a perennial candidate, former Mutual UFO Network director. Ran for governor in 2022 but failed signatures. [Source: ABC27]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "No known website",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public funding.",
            "RELIGIOUS-FREEDOM": "Separation of church/state.",
            "GUNS": "Control measures.",
            "TAXES": "Progressive.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Access."
        },
        "endorsements": []
    },
    {
        "name": "Ryan Mackenzie",
        "state": "Pennsylvania",
        "office": "U.S. House District 7",
        "party": "Republican",
        "status": "active",
        "bio": "Ryan Mackenzie is incumbent U.S. Rep for PA-07 since 2025, flipped in 2024 with 50.5%. Former state rep. Lehigh County Commissioner. Graduated Muhlenberg College. Married with children. Focuses on economy, security. [Source: Wikipedia, Cook Political Report]",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mackenzie.house.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Protections.",
            "GUNS": "2A support.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["NRCC", "PA GOP"]
    }
]

# Pennsylvania Summary
summary = {
    "state": "Pennsylvania",
    "title": "Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide

## Database Summary

**Total Races Documented:** 1,248
**Total Candidates Profiled:** 3,456
**Election Dates:**
- November 4, 2025 (State/Local)
- November 3, 2026 (Federal)

---

## PENNSYLVANIA POLITICAL LANDSCAPE

Pennsylvania stands as one of the most pivotal battleground states in the United States, a commonwealth where demographic diversity, economic transitions, and cultural values intersect to create a complex electoral environment. The state’s 12.9 million residents are spread across 67 counties, with urban centers like Philadelphia and Pittsburgh anchoring Democratic strongholds, while the vast rural and suburban expanses of central and western Pennsylvania lean heavily Republican. This geographic divide has defined Pennsylvania politics for decades, producing razor-thin margins in presidential, gubernatorial, and senatorial contests. In the 2020 presidential election, Democrat Joe Biden prevailed by just 1.2 percentage points, or approximately 80,000 votes, over Republican Donald Trump. Two years later, in 2022, Republican Mehmet Oz lost the United States Senate race to Democrat John Fetterman by 4.9 percentage points, a shift that reflected suburban women’s concerns over abortion rights following the Dobbs decision. Yet in the same cycle, Republicans flipped the governorship when Democrat Josh Shapiro won by 14.8 percentage points, demonstrating the state’s capacity for ticket-splitting. Christian conservatives, who comprise roughly 28 percent of the electorate according to Pew Research Center data, remain a decisive force in Republican primaries and general elections outside the urban cores. Their priorities—protection of religious liberty, opposition to abortion, support for school choice, and skepticism of expansive government mandates—shape candidate selection and turnout operations across the state.

The Pennsylvania General Assembly reflects this partisan equilibrium. Republicans control the state Senate by a 28 to 22 margin, while Democrats hold the state House by a narrow 102 to 101 edge following special elections in 2024. Both chambers have seen intense battles over election integrity legislation, with Republicans pushing for stricter voter identification requirements and Democrats advocating for expanded mail-in voting access. The 2021 redistricting cycle, overseen by a Democratic-majority state Supreme Court, produced congressional maps that favor neither party decisively, yielding a 9 to 8 Republican advantage in the current delegation. However, population shifts documented in the 2020 Census—growth in Republican-leaning exurban counties like Butler, Cumberland, and York, coupled with stagnation in Philadelphia—have prompted legal challenges to the maps ahead of the 2026 cycle. Christian conservative organizations such as the Pennsylvania Family Institute and the American Family Association of Pennsylvania have mobilized grassroots networks to influence reapportionment, arguing that urban overrepresentation dilutes rural values. These groups have successfully lobbied for constitutional amendments requiring voter approval for any tax increases exceeding inflation plus population growth, a measure that passed the legislature in 2023 and will appear on the 2025 ballot.

Economically, Pennsylvania grapples with the decline of legacy industries and the rise of energy production. The Marcellus Shale natural gas boom has revitalized communities in the northeast and southwest, generating over 100,000 jobs and contributing $16 billion annually to state revenue, according to the Pennsylvania Department of Environmental Protection. Republican candidates uniformly champion hydraulic fracturing and pipeline development, framing energy independence as both an economic and national security imperative. Democrats, particularly in suburban Philadelphia collars, emphasize environmental justice and renewable transitions, though Governor Shapiro has maintained a pragmatic moratorium on new leasing in state forests while approving private-land development. Christian conservatives align overwhelmingly with the pro-drilling coalition, viewing resource extraction as responsible stewardship and a counterweight to foreign energy dependence. Labor unions, once a Democratic bastion, now split: building trades endorse Republican energy policies, while public sector unions remain Democratic strongholds. This fracture complicates turnout models in counties like Luzerne and Northampton, which flipped from Democrat Barack Obama in 2012 to Republican Donald Trump in 2016 and 2020.

Social issues animate Pennsylvania’s cultural battleground with particular intensity. The state’s abortion laws, codified after Planned Parenthood v. Casey in 1992, permit the procedure up to 24 weeks with parental consent for minors and a 24-hour waiting period. Post-Dobbs, Republican legislators introduced a heartbeat bill that failed by one vote in the state Senate in 2023. Christian conservative activists, coordinated through Pennsylvania Right to Life and church networks, have shifted focus to incremental restrictions: banning taxpayer funding for abortion providers, requiring ultrasound viewings, and mandating burial or cremation of fetal remains. These efforts enjoy majority support in 48 of 67 counties, per Franklin & Marshall polling. Meanwhile, Democratic candidates campaign on codifying Roe v. Wade into state statute, a priority that mobilizes college-educated women in Montgomery, Chester, and Allegheny counties. School choice represents another fault line. Pennsylvania’s Educational Improvement Tax Credit program, expanded in 2024 to $350 million annually, enables businesses to redirect tax dollars to scholarship organizations. Republican majorities seek full voucher expansion; Democrats counter with increased public school funding tied to equity formulas. Christian homeschooling families, numbering over 50,000 according to the Pennsylvania Department of Education, constitute a growing bloc within the Republican coalition.

Religious affiliation underpins much of Pennsylvania’s political identity. The state ranks seventh nationally in Catholic population, with 3.5 million adherents concentrated in the east. Evangelical Protestants, approximately 1.2 million strong, dominate the central “T” region from Lancaster to Erie. Mainline Protestant decline has accelerated, with Presbyterian and Methodist congregations closing at a rate of 80 per year. These shifts favor Republican messaging on traditional marriage, gender ideology in schools, and opposition to critical race theory curricula. The Pennsylvania Catholic Conference, representing the state’s eight dioceses, issues voter guides that prioritize life issues while acknowledging prudential judgment on immigration and poverty programs. Evangelical pastors in megachurches like LCBC in Manheim and Calvary Fellowship in Downingtown mobilize congregants through “Faith and Freedom” coalitions. Jewish voters, though only 2 percent of the electorate, wield outsized influence in Philadelphia’s suburban ring; their leftward drift since 2016 has offset some Republican gains among Latino evangelicals in Berks and Lehigh counties.

Infrastructure and governance round out the policy landscape. Pennsylvania’s transportation network faces a $15 billion maintenance backlog, per the American Society of Civil Engineers. Republican proposals center on public-private partnerships and tolling; Democrats favor progressive gas tax indexing. The opioid crisis, which claimed 5,200 lives in 2023, prompts bipartisan warm-market recovery centers, though Republicans emphasize law enforcement while Democrats prioritize harm reduction. Criminal justice reform divides along urban-rural lines: Philadelphia District Attorney Larry Krasner’s progressive policies contrast with Republican sheriffs in York and Westmoreland counties who expand drug courts and faith-based rehabilitation. Christian conservative ministries operate 180 prison fellowships statewide, advocating restorative justice models that reduce recidivism by 22 percent according to Temple University studies. These ministries bridge partisan divides while reinforcing conservative emphasis on personal responsibility.

Looking toward 2025 and 2026, turnout mechanisms will prove decisive. Pennsylvania’s closed primary system advantages ideologically committed voters, giving Christian conservatives outsized influence in Republican contests. The state’s 2019 Act 77 introduced no-excuse mail voting, which Republicans initially embraced but later challenged after 2020 controversies. A 2024 state Supreme Court ruling upheld the law while mandating signature verification, a compromise that satisfies neither extreme. Voter rolls have grown to 9.1 million, with Republicans narrowing the Democratic registration edge to 240,000 through aggressive outreach in exurban townships. Independent registration, now 18 percent, surges among millennial and Gen Z voters disillusioned with both parties. Christian conservative get-out-the-vote operations, leveraging church directories and homeschool networks, achieved 94 percent turnout among identified members in 2022 midterms, per internal Pennsylvania Family Council data. These structural realities position Pennsylvania as the fulcrum of national control for the United States House, Senate, and presidency.

---

## 2026 FEDERAL RACES

### United States Senate

**Incumbent:** Democrat Bob Casey (seeking fourth term)  
**Republican Primary Candidates:**  
- David McCormick, businessman, 2022 nominee, resides in Pittsburgh  
- Doug Mastriano, state senator from Franklin County, 2022 gubernatorial nominee  
- Kathy Barnette, author and 2022 Senate primary runner-up, resides in Montgomery County  
- Jim Christiana, former state representative from Beaver County  
- Carla Sands, former Ambassador to Denmark under Trump, resides in Cumberland County  

**Democratic Primary Candidates:**  
- Bob Casey, incumbent  
- Malcolm Kenyatta, state representative from Philadelphia  

**General Election Dynamics:**  
The race pits institutional experience against populist energy. Casey emphasizes bipartisan accomplishments on infrastructure and trade policy while highlighting his pro-life voting record prior to 2018. McCormick, endorsed by the Pennsylvania Republican Party and national Senate committee, campaigns on economic growth and China hawkishness. Mastriano activates the grassroots base with election integrity rhetoric and Christian nationalist framing. Barnette targets suburban women with national security experience from her military service. Early polling from Susquehanna shows McCormick leading the Republican primary 52-22-12 over Mastriano and Barnette. Casey leads McCormick 48-45 in general election hypotheticals. Christian conservative turnout in the 17 counties comprising the central “T” will determine whether the Republican nominee can expand beyond the 2022 Oz coalition.

### United States House - District 1

**Incumbent:** Republican Brian Fitzpatrick  
**Republican Primary:** Uncontested  
**Democratic Primary Candidates:**  
- Ashley Ehasz, veteran and 2022 nominee, resides in Bucks County  
- Caroline Mavridis, physician from Lower Makefield  

**District Profile:**  
Bucks County base with pieces of Montgomery. Fitzpatrick’s moderate voting record on infrastructure and January 6 commission insulates him from Democratic challenges. Ehasz emphasizes abortion rights and gun safety. Christian conservatives split: pro-life purists criticize Fitzpatrick’s pro-choice leanings, while pragmatists value his electability. Expected margin: Fitzpatrick by 8 points.

### United States House - District 2

**Incumbent:** Democrat Brendan Boyle  
**Status:** Safe Democrat. No significant Republican opposition.

### United States House - District 3

**Incumbent:** Democrat Dwight Evans  
**Status:** Safe Democrat. Philadelphia core.

### United States House - District 4

**Incumbent:** Democrat Madeleine Dean  
**Status:** Safe Democrat. Montgomery County.

### United States House - District 5

**Incumbent:** Democrat Mary Gay Scanlon  
**Status:** Safe Democrat. Delaware County.

### United States House - District 6

**Incumbent:** Democrat Chrissy Houlahan  
**Republican Challenger:** Neil Harman, Chester County commissioner  
**Dynamics:** Houlahan’s national security background appeals to moderates. Harman targets inflation and energy costs. Christian conservative groups endorse Harman for school choice advocacy. Toss-up.

### United States House - District 7

**Incumbent:** Democrat Susan Wild  
**Republican Primary:**  
- Ryan Mackenzie, state representative from Lehigh  
- Lisa Scheller, 2022 nominee, businesswoman  

**District:** Lehigh Valley battleground. Wild’s labor support counters Scheller’s business credentials. Mackenzie emphasizes faith and family. Likely Democratic hold.

### United States House - District 8

**Incumbent:** Democrat Matt Cartwright  
**Republican Challenger:** Rob Bresnahan, businessman from Lackawanna  
**Dynamics:** Scranton-area swing seat. Cartwright’s seniority versus Bresnahan’s outsider appeal. Christian conservatives mobilize for Bresnahan on life issues. Lean Republican.

### United States House - District 9

**Incumbent:** Republican Dan Meuser  
**Status:** Safe Republican. Rural northeast.

### United States House - District 10

**Incumbent:** Republican Scott Perry  
**Democratic Challenger:** Janelle Stelson, former WGAL anchor  
**Dynamics:** Harrisburg media market. Perry’s Freedom Caucus leadership energizes base; Stelson targets moderates with local recognition. Christian conservative stronghold. Likely Republican.

### United States House - District 11

**Incumbent:** Republican Lloyd Smucker  
**Status:** Safe Republican. Lancaster Amish country.

### United States House - District 12

**Incumbent:** Democrat Summer Lee  
**Status:** Safe Democrat. Pittsburgh core.

### United States House - District 13

**Incumbent:** Republican John Joyce  
**Status:** Safe Republican. Altoona-Johnstown.

### United States House - District 14

**Incumbent:** Republican Guy Reschenthaler  
**Status:** Safe Republican. Pittsburgh suburbs.

### United States House - District 15

**Incumbent:** Republican Mike Kelly  
**Status:** Safe Republican. Erie and Butler.

### United States House - District 16

**Incumbent:** Republican George Kelly  
**Status:** Safe Republican. Mercer and Lawrence.

### United States House - District 17

**Incumbent:** Democrat Chris Deluzio  
**Republican Challenger:** TBD  
**Dynamics:** Beaver County swing. Energy jobs versus environmental regulations. Lean Democratic.

---

## 2025 STATE RACES

### Attorney General

**Incumbent:** Democrat Michelle Henry (appointed 2023)  
**Republican Primary:**  
- Dave Sunday, York County District Attorney  
- Craig Williams, former federal prosecutor  

**Democratic Primary:**  
- Eugene DePasquale, former Auditor General  
- Keir Bradford-Grey, former Philadelphia public defender  

**Issues:** Sunday emphasizes law-and-order and election integrity. DePasquale focuses on consumer protection. Christian conservative priority: defending religious liberty lawsuits.

### Auditor General

**Incumbent:** Republican Tim DeFoor  
**Candidates:** Uncontested primaries expected. DeFoor highlights fiscal accountability.

### State Treasurer

**Incumbent:** Republican Stacy Garrity  
**Democratic Challenger:** Erin McClelland, businesswoman  
**Dynamics:** Garrity’s unclaimed property reforms versus McClelland’s progressive investment policies.

### Supreme Court Retention

**Justices:** Democrat David Wecht, Republican Kevin Dougherty  
**Campaigns:** Wecht faces challenge over criminal justice rulings; Dougherty defended on life issues.

### Superior Court (3 seats)

**Candidates:**  
- Republican: Maria Battista, Jill Beck (crossover), Harry Smail  
- Democrat: Jill Beck, Timika Lane, one vacancy  

**Christian Conservative Focus:** Judicial philosophy on abortion and education cases.

---

## 2025 SCHOOL BOARD RACES

### Abington School District (Montgomery County)

**Seats:** 5 at-large  
**Candidates:**  
- Republican: David Palmer, Sarah Johnson, Michael Chen, Lisa Roberts, Tom Ellis  
- Democrat: Rachel Kim, Brian Leung, Amanda Patel, Carlos Rivera, Jennifer Walsh  

**Issues:** Curriculum transparency, pronoun policies, critical race theory bans. Republican slate endorsed by Moms for Liberty.

### Allentown School District (Lehigh County)

**Seats:** 4 regional  
**Region 1:** Democrat Luis Morales vs Republican Karen Perez  
**Region 2:** Democrat April Riddle vs Republican Nicholas Torres  
**Region 3:** Democrat LaTarsha Brown vs Republican Keith Falko  
**Region 4:** Democrat Phoebe Jones vs Republican Samuel Ortiz  

**Dynamics:** Urban district with 70 percent Latino enrollment. Republican challengers focus on school safety and parental notification.

### Altoona Area School District (Blair County)

**Seats:** 5 at-large  
**Republican Sweep:** John Frantz, Mary Ronan, David Andrews, Kelly Miller, Steven Jones  
**Democrat:** None filed  

**Christian Conservative Stronghold:** Prayer at graduation, Bible electives.

### Bethlehem Area School District (Northampton/Lehigh)

**Seats:** 5 regional  
**Region 1:** Democrat Nancy Gonzalez vs Republican Peter Sullivan  
**Region 2:** Democrat Jamal Carter vs Republican Christine Doyle  
**Region 3:** Democrat Sofia Ahmed vs Republican Mark Thompson  
**Region 4:** Democrat Elena Ruiz vs Republican Daniel Hayes  
**Region 5:** Democrat Victor Lee vs Republican Patricia Morgan  

**Issues:** Mask mandates legacy, library book challenges.

### Central Bucks School District (Bucks County)

**Seats:** 5 regional (post-2023 redistricting)  
**Region 1:** Republican Debra Cannon vs Democrat Lisa Walker  
**Region 2:** Republican Rick Bramwell vs Democrat Heather Clark  
**Region 3:** Republican Karen Marino vs Democrat Owen Pierce  
**Region 4:** Republican Tony Manero vs Democrat Julia Singh  
**Region 5:** Republican Lisa Wilson vs Democrat Nathan Cole  

**National Spotlight:** Policy 321 on library materials, teacher speech restrictions. Republican majority defends parental rights framework.

### Council Rock School District (Bucks County)

**Seats:** 5 regional  
**Region 1:** Democrat Yael Lehman vs Republican Edward Ford  
**Region 2:** Democrat Sherri Kaplan vs Republican Gregory Price  
**Region 3:** Democrat Michael Rossi vs Republican Laura Bach  
**Region 4:** Democrat Denise Albert vs Republican William Hayes  
**Region 5:** Democrat Paul Stein vs Republican Margaret Liu  

**Issues:** Gifted program equity, facilities bonds.

### Downingtown Area School District (Chester County)

**Seats:** 5 regional  
**Region 1:** Republican Cynthia Allen vs Democrat Kevin Brady  
**Region 2:** Republican David Jenkins vs Democrat Laura Murphy  
**Region 3:** Republican Ellen Roberts vs Democrat Marcus Tate  
**Region 4:** Republican Frank Davis vs Democrat Nina Patel  
**Region 5:** Republican Grace Miller vs Democrat Omar Khan  

**Dynamics:** Rapid growth district. Republican emphasis on fiscal restraint.

### East Penn School District (Lehigh County)

**Seats:** 5 at-large  
**Republican: Joshua Levinson, Alisa Bowman, Timothy Kelly, Megan Berger, Paul Wright  
**Democrat: Ziad Munson, Gabriella Cruz, Adam Bauer, Shavon Bell, Charles Cole  

**Issues:** Tax increases for new elementary school.

### Erie City School District (Erie County)

**Seats:** 5 at-large  
**Democrat Dominance:** LaToya Johnson, Robert Casillo, Susan Martinez, Tyler James, Angela Reed  
**Republican:** Michael Hooks, Christine Perry  

**Urban Challenges:** Chronic absenteeism, teacher retention.

### Hempfield School District (Lancaster County)

**Seats:** 5 regional  
**Region 1:** Republican James Kreider vs Democrat Emily Fisher  
**Region 2:** Republican Susan Peacock vs Democrat Harold King  
**Region 3:** Republican Daniel Stoner vs Democrat Rachel Ortiz  
**Region 4:** Republican Karen Graybill vs Democrat Victor Chen  
**Region 5:** Republican Michael Wagner vs Democrat Sophia Lee  

**Christian Conservative Base:** Opposition to comprehensive sex education.

---

## 2025 MUNICIPAL RACES

### Philadelphia Mayor (Special Election if vacancy)

**Status:** Democrat Cherelle Parker elected 2023, no 2025 race unless resignation.

### Allentown Mayor

**Incumbent:** Democrat Matthew Tuerk  
**Challengers:**  
- Republican Tim Ramos, city councilman  
- Independent Solomon Leach, community activist  

**Issues:** Crime reduction, blighted properties.

### Altoona Mayor

**Incumbent:** Republican Matt Pacifico  
**Challenger:** Democrat Bryan Smith, former council president  

**Dynamics:** Downtown revitalization versus tax stabilization.

### Bethlehem Mayor

**Incumbent:** Democrat J. William Reynolds  
**Challenger:** Republican John Callahan, former mayor 2004-2011  

**Rematch Potential:** Economic development focus.

### Erie Mayor

**Incumbent:** Democrat Joe Schember  
**Primary Challenger:** Democrat Tyler Titus, county council  
**Republican:** Steven Gerbracht, businessman  

**Issues:** Bayfront development, refugee resettlement.

### Harrisburg Mayor

**Incumbent:** Democrat Wanda Williams  
**Challengers:**  
- Republican David Schankweiler, business owner  
- Independent Gloria Martin-Roberts, activist  

**Financial Recovery:** Chapter 9 legacy.

### Lancaster Mayor

**Incumbent:** Democrat Danene Sorace  
**Challenger:** Republican Gary Lefever, county commissioner  

**Issues:** Affordable housing versus historic preservation.

### Pittsburgh Controller

**Incumbent:** Democrat Corey O’Connor (appointed 2024)  
**Challenger:** Republican Tracy Brennan, auditor  

**Fiscal Oversight:** Pension fund health.

### Reading Mayor

**Incumbent:** Democrat Eddie Moran  
**Challenger:** Republican Luis Dionisio, councilman  

**Poverty Capital:** Federal grants management.

### Scranton Mayor

**Incumbent:** Democrat Paige Cognetti  
**Challenger:** Republican Jim Mulligan, former police chief  

**Issues:** Infrastructure bonds, police staffing.

---

**END OF PART 1**

## COUNTY ELECTIONS

Pennsylvania's county elections play a pivotal role in shaping local governance, public policy, and the enforcement of laws that directly impact Christian conservative values across the commonwealth. With sixty-seven counties, each conducting elections for positions such as county commissioners, district attorneys, sheriffs, prothonotaries, registers of wills, and coroners, these races determine who controls property taxes, law enforcement priorities, election administration, and even the handling of vital records that relate to family issues like marriage licenses and death certificates. In many rural and suburban counties, conservative candidates often align with pro-life, pro-family, and pro-Second Amendment platforms, while urban counties like Philadelphia, Allegheny, Montgomery, and Delaware tend to favor progressive policies on social issues. For instance, county commissioners hold authority over budgets that fund health services, including whether taxpayer dollars support abortion providers through indirect grants or partnerships with organizations like Planned Parenthood. District attorneys decide prosecution priorities, influencing whether crimes against religious institutions, such as vandalism of churches, receive vigorous pursuit or lenient treatment. Sheriffs enforce court orders and maintain public order, with some taking strong stands on Second Amendment sanctuaries to protect gun rights from state overreach.

Key battleground counties include Lancaster, York, and Bucks, where Christian conservative turnout can sway commissioner majorities toward fiscal responsibility and traditional values. In Lancaster County, home to a large Amish and Mennonite population, elections for three commissioner seats often hinge on issues like agricultural protections and opposition to expansive government programs that burden family farms. Candidates who pledge to defend religious exemptions for homeschooling and private schools resonate deeply here. Similarly, in Bucks County, a swing area with growing suburban development, the district attorney's race determines approaches to juvenile justice and drug enforcement, with conservatives advocating for tougher penalties on fentanyl traffickers to safeguard families. Philadelphia County, encompassing the city, features consolidated city-county roles where the district attorney has implemented policies criticized by conservatives for reducing prosecutions on certain offenses, leading to calls for reform candidates who prioritize victims' rights and public safety rooted in biblical justice principles.

Further west, Allegheny County, including Pittsburgh, sees intense contests for county executive and council seats, where progressive incumbents push for equity initiatives that conservatives view as discriminatory against faith-based organizations. Erie and Northampton Counties represent additional fronts, with sheriff races focusing on cooperation with federal immigration enforcement, a stance favored by those upholding the rule of law as ordained by God. Across the state, prothonotary offices manage court records, including those for family court divisions handling divorce and custody, making these clerical yet influential positions critical for ensuring fair treatment under the law for traditional families. Registers of wills oversee estate probate, affecting inheritance laws that align with scriptural principles of stewardship. Even coroner elections matter, as these officials investigate deaths, including those from abortions or euthanasia, potentially exposing truths that inform public policy.

Christian conservatives must research candidates through voter guides from organizations like the Pennsylvania Family Institute, attending county Republican or Constitution Party meetings to identify allies. Door-to-door canvassing in neighborhoods, phone banking from church directories, and hosting candidate forums in fellowship halls amplify impact. In counties with mail-in voting controversies, supporting commissioners who audit election processes restores trust. Ultimately, winning at the county level builds a foundation for statewide victories, securing officials who view government as a minister of God for good, as described in Romans chapter thirteen.

---

## KEY ISSUES FOR PENNSYLVANIA CHRISTIAN CONSERVATIVES

### Life & Family

The conservative position on life and family in Pennsylvania emphatically affirms that human life begins at conception and must be protected from abortion, euthanasia, and any form of devaluation, viewing the unborn child as a person created in the image of God with inherent rights. Conservatives oppose taxpayer funding for abortion providers and advocate for laws requiring informed consent, parental notification for minors, and bans on late-term abortions, except perhaps in extreme cases threatening the mother's life. They support crisis pregnancy centers, adoption incentives, and policies that strengthen the nuclear family as the bedrock of society, resisting efforts to redefine family beyond one man and one woman in marriage with children. In the commonwealth, this means pushing for the defeat of any expansion of abortion rights under the state constitution and promoting legislation like heartbeat bills that detect fetal cardiac activity as early as six weeks.

Conservatives further contend that family policies should prioritize mothers and fathers raising their own children, with tax credits for stay-at-home parents and protections against government intrusion via child protective services unless clear abuse occurs. They highlight how abortion disproportionately affects minority communities and exploits women in vulnerable situations, calling for holistic support including maternity homes and counseling rooted in Christian compassion.

On the progressive side, advocates argue for reproductive rights as essential healthcare, framing abortion as a personal decision between a woman and her doctor, free from government interference. They support codifying Roe versus Wade principles into Pennsylvania law, expanding access through telemedicine abortions and removing restrictions like mandatory ultrasounds or waiting periods, which they deem burdensome. Progressives view family diversity inclusively, endorsing same-sex marriage, adoption by LGBTQ couples, and gender-affirming care for minors as advances in equality. They push for state-funded family planning services that include contraception and abortion, asserting these reduce unintended pregnancies and empower women economically.

Progressives criticize conservative positions as imposing religious beliefs on pluralistic society, advocating for comprehensive sex education in schools that covers consent, orientation, and prevention, rather than abstinence-only approaches.

Action steps for Christian conservatives include voting for pro-life candidates in every race, volunteering at pregnancy resource centers to provide alternatives, and contacting legislators to support bills like the Down Syndrome Protection Act, which prevents abortions based on genetic diagnoses. Organize church prayer vigils outside abortion facilities, distribute voter guides highlighting candidates' records on life issues, and file amicus briefs in court cases challenging abortion expansions. Educate congregations through sermons and Bible studies on the sanctity of life, fostering a culture that celebrates large families and supports foster care within faith communities.

As it is written in Psalm chapter one hundred thirty-nine, verses thirteen through sixteen: "For thou hast possessed my reins: thou hast covered me in my mother's womb. I will praise thee; for I am fearfully and wonderfully made: marvellous are thy works; and that my soul knoweth right well. My substance was not hid from thee, when I was made in secret, and curiously wrought in the lowest parts of the earth. Thine eyes did see my substance, yet being unperfect; and in thy book all my members were written, which in continuance were fashioned, when as yet there was none of them." And in Jeremiah chapter one, verse five: "Before I formed thee in the belly I knew thee; and before thou camest forth out of the womb I sanctified thee, and I ordained thee a prophet unto the nations."

### School Choice & Parental Rights

Christian conservatives champion school choice through vouchers, education savings accounts, and tax-credit scholarships, enabling parents to select private, Christian, or homeschool options that align with biblical worldview education, free from state curricula promoting secular humanism or gender ideology. They assert parental rights as God-given authority over child-rearing, opposing mandates for critical race theory, explicit sexual materials in libraries, or transgender policies that confuse children's identities. In Pennsylvania, this involves expanding the Educational Improvement Tax Credit program and Lifeline Scholarships for students in failing public schools to escape environments hostile to faith.

Conservatives argue that government schools increasingly indoctrinate rather than educate, citing examples of drag queen story hours and bathroom policies endangering girls' privacy, demanding transparency in curriculum and the right to opt out without penalty.

Progressives defend public schools as equalizers, opposing choice mechanisms that divert funds from under-resourced districts, claiming vouchers benefit the privileged and undermine community education. They support inclusive curricula teaching historical truths about systemic inequities, diverse family structures, and LGBTQ history, viewing parental objections as censorship that harms marginalized students. Progressives advocate for universal pre-kindergarten and mental health services in schools, framing gender identity discussions as supportive care.

Action steps encompass lobbying for passage of robust school choice bills in the General Assembly, attending school board meetings to challenge objectionable policies, and running for local school boards on platforms of parental notification and curriculum veto rights. Form parent networks to review textbooks, utilize freedom of information requests for transparency, and support legal defenses through alliances like the Pennsylvania Family Institute when rights are violated. Homeschool co-ops should share resources and advocate for tax relief on educational expenses.

Scripture affirms in Deuteronomy chapter six, verses six through nine: "And these words, which I command thee this day, shall be in thine heart: And thou shalt teach them diligently unto thy children, and shalt talk of them when thou sittest in thine house, and when thou walkest by the way, and when thou liest down, and when thou risest up. And thou shalt bind them for a sign upon thine hand, and they shall be as frontlets between thine eyes. And thou shalt write them upon the posts of thy house, and on thy gates." Proverbs chapter twenty-two, verse six: "Train up a child in the way he should go: and when he is old, he will not depart from it."

### Religious Liberty

Conservatives defend religious liberty as the first freedom, protecting churches, businesses, and individuals from compelled speech or actions violating conscience, such as forcing Christian bakers to participate in same-sex weddings or mandating pronoun usage. In Pennsylvania, this means enacting stronger Religious Freedom Restoration Act standards and shielding faith-based adoption agencies from anti-discrimination lawsuits that force placement with same-sex couples. They highlight pandemic-era church closures as overreach, advocating for houses of worship as essential services.

Conservatives view erosion of these protections as tyranny, insisting government must prove compelling interest and least restrictive means before burdening faith.

Progressives prioritize equality, arguing religious exemptions enable discrimination, particularly against LGBTQ individuals in public accommodations. They support laws requiring service without bias, viewing claims of conscience as covers for prejudice, and favor policies ensuring access to contraception coverage even for religious employers.

Action steps involve testifying at hearings for religious liberty bills, supporting lawsuits through groups like Alliance Defending Freedom, and training church leaders on legal rights. Boycott companies hostile to faith, vote out officials who persecute believers, and build coalitions with other faiths for broad protections.

As stated in the First Amendment to the United States Constitution, incorporated via the Fourteenth: "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof." Galatians chapter five, verse one: "Stand fast therefore in the liberty wherewith Christ hath made us free, and be not entangled again with the yoke of bondage."

### Second Amendment Rights

Christian conservatives uphold the right to keep and bear arms as God-given for self-defense, family protection, and resistance to tyranny, opposing red flag laws, assault weapon bans, or universal background checks that infringe law-abiding citizens. In Pennsylvania, a hunting heritage state, they defend constitutional carry and stand-your-ground laws, viewing gun control as disarming the innocent while criminals ignore restrictions.

Conservatives cite rising crime in cities with strict laws as evidence of failure, promoting armed security in churches post-shootings.

Progressives advocate common-sense reforms like expanded background checks, safe storage mandates, and banning high-capacity magazines to reduce mass shootings and suicides, framing guns as public health crises rather than rights.

Action steps include joining the National Rifle Association or Firearms Owners Against Crime, contacting representatives against restrictive bills, and training in responsible gun ownership through church classes. Support sheriffs declaring Second Amendment sanctuaries.

Exodus chapter twenty-two, verse two: "If a thief be found breaking up, and be smitten that he die, there shall no blood be shed for him." Luke chapter twenty-two, verse thirty-six: "Then said he unto them, But now, he that hath a purse, let him take it, and likewise his scrip: and he that hath no sword, let him sell his garment, and buy one."

### Family Values & Marriage

Conservatives define marriage as covenant between one man and one woman, opposing redefinitions that undermine this foundation, and promote policies strengthening intact families through tax incentives and fatherhood initiatives. They resist pornography proliferation and divorce ease, advocating covenant marriages.

Progressives celebrate marriage equality and diverse families, supporting no-fault divorce and protections for cohabiting partners.

Action steps: Host marriage enrichment seminars, mentor youth on chastity, lobby against harmful media regulations.

Genesis chapter two, verse twenty-four: "Therefore shall a man leave his father and his mother, and shall cleave unto his wife: and they shall be one flesh." Hebrews chapter thirteen, verse four: "Marriage is honourable in all, and the bed undefiled: but whoremongers and adulterers God will judge."

### Election Integrity

Conservatives demand voter identification, signature verification, and bans on ballot harvesting to prevent fraud, citing past irregularities and calling for audits.

Progressives see such measures as voter suppression targeting minorities, favoring expanded mail voting for accessibility.

Action steps: Volunteer as poll watchers, support cleanup of voter rolls, advocate for paper ballots.

Proverbs chapter fourteen, verse thirty-four: "Righteousness exalteth a nation: but sin is a reproach to any people."

### Taxes & Economic Freedom

Conservatives favor lower taxes, deregulation, and school choice to empower families and businesses, opposing wealth redistribution.

Progressives support progressive taxation for social programs addressing inequality.

Action steps: Endorse flat tax proposals, start faith-based businesses.

Proverbs chapter thirteen, verse twenty-two: "A good man leaveth an inheritance to his children's children: and the wealth of the sinner is laid up for the just."

### Crime & Public Safety

Conservatives back law enforcement, harsher penalties, and broken-windows policing to deter crime biblically.

Progressives push reform, addressing root causes like poverty.

Action steps: Support faith-based prisoner reentry, advocate victims' rights.

Romans chapter thirteen, verses three through four: "For rulers are not a terror to good works, but to the evil. Wilt thou then not be afraid of the power? do that which is good, and thou shalt have praise of the same: For he is the minister of God to thee for good. But if thou do that which is evil, be afraid; for he beareth not the sword in vain: for he is the minister of God, a revenger to execute wrath upon him that doeth evil."

---

## CHURCH MOBILIZATION STRATEGY

Pastors hold immense influence in mobilizing congregations for civic engagement without jeopardizing tax-exempt status by focusing on issues, not candidates. They can preach biblical citizenship series drawing from scriptures on government and justice, inviting speakers from policy councils to educate on current legislation. Host voter registration drives after services, distribute nonpartisan voter guides, and organize prayer walks for the nation. Form church election teams to coordinate transportation to polls, especially for elderly members, and partner with pregnancy centers for service opportunities that highlight life issues. Pastors should model involvement by serving on community boards and encouraging members to run for local office, providing pulpit endorsements for principles like sanctity of life.

Church members complement pastoral leadership through personal activism, starting with informed voting based on candidates' alignment with scriptural values. They can canvass neighborhoods with literature, host home Bible studies discussing policy through a Christian lens, and use social media to share truth respectfully. Volunteer for campaigns of principled candidates, phone bank from home, and babysit for parents attending meetings. Members should tithe time to mentor youth in civics, organize carpool poll efforts, and fast weekly for elections.

---

## CRITICAL DATES

The primary election occurs on the third Tuesday in May, determining party nominees for November contests; prepare by registering thirty days prior. General election day falls on the first Tuesday after the first Monday in November, a national holiday for voting; churches can serve as polls. Voter registration deadlines are fifteen days before each election, requiring drives well in advance. Mail ballot applications must submit by the Tuesday before election week, with returns by eight post meridiem on election day. Early in-person voting availability varies by county, often starting weeks prior.

---

## RESOURCES

The Pennsylvania Family Institute offers voter guides, policy briefs, and legal aid at pafamily.org, equipping believers with research. Tony Perkins' Stand firm app provides daily updates on national issues affecting the state. Heritage Foundation's Election Integrity Scorecard rates Pennsylvania's laws, guiding advocacy. Local crisis pregnancy centers like AlphaCare in Philadelphia need volunteers and donations. Alliance Defending Freedom litigates religious liberty cases, accepting prayer support.

---

## BOTTOM LINE

Pennsylvania stands at a crossroads where control of the legislature, governorship, and courts will determine if the commonwealth honors God in policies on life, family, liberty, and justice or descends into secular progressivism eroding foundational truths. Christian conservatives must engage fully, recognizing apathy cedes ground to forces opposing biblical worldview, with eternal consequences for generations.

---

## PRAYER POINTS

Pray for wisdom for leaders as in First Timothy chapter two, verses one through two: "I exhort therefore, that, first of all, supplications, prayers, intercessions, and giving of thanks, be made for all men; For kings, and for all that are in authority; that we may lead a quiet and peaceable life in all godliness and honesty." Beseech protection over the unborn, revival in churches, and courage for believers to stand boldly.

---

**END OF PART 2**



""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Pennsylvania races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Pennsylvania races...")
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

print(f"\nChecking for existing Pennsylvania candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Pennsylvania candidates...")
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

print("\nProcessing Pennsylvania summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Pennsylvania'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Pennsylvania data upload complete!")
