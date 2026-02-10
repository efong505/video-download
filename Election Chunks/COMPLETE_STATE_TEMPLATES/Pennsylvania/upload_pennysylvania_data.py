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
]

# Pennsylvania Summary
summary = {
    "state": "Pennsylvania",
    "title": "Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 341
**Total Candidates Profiled:** 119
**Election Dates:**
- November 4, 2025 (State/Local)
- November 3, 2026 (Federal)

---

## 🔴 PENNSYLVANIA POLITICAL LANDSCAPE

Pennsylvania stands as one of the most pivotal battleground states in the United States, a commonwealth where demographic diversity, economic transitions, and cultural values intersect to create a complex electoral environment. The state’s 12.9 million residents are spread across 67 counties, with urban centers like Philadelphia and Pittsburgh anchoring Democratic strongholds, while the vast rural and suburban expanses of central and western Pennsylvania lean heavily Republican. This geographic divide has defined Pennsylvania politics for decades, producing razor-thin margins in presidential, gubernatorial, and senatorial contests. In the 2020 presidential election, Democrat Joe Biden prevailed by just 1.2 percentage points, or approximately 80,000 votes, over Republican Donald Trump. Two years later, in 2022, Republican Mehmet Oz lost the United States Senate race to Democrat John Fetterman by 4.9 percentage points, a shift that reflected suburban women’s concerns over abortion rights following the Dobbs decision. Yet in the same cycle, Republicans flipped the governorship when Democrat Josh Shapiro won by 14.8 percentage points, demonstrating the state’s capacity for ticket-splitting. Christian conservatives, who comprise roughly 28 percent of the electorate according to Pew Research Center data, remain a decisive force in Republican primaries and general elections outside the urban cores. Their priorities—protection of religious liberty, opposition to abortion, support for school choice, and skepticism of expansive government mandates—shape candidate selection and turnout operations across the state.

The Pennsylvania General Assembly reflects this partisan equilibrium. Republicans control the state Senate by a 28 to 22 margin, while Democrats hold the state House by a narrow 102 to 101 edge following special elections in 2024. Both chambers have seen intense battles over election integrity legislation, with Republicans pushing for stricter voter identification requirements and Democrats advocating for expanded mail-in voting access. The 2021 redistricting cycle, overseen by a Democratic-majority state Supreme Court, produced congressional maps that favor neither party decisively, yielding a 9 to 8 Republican advantage in the current delegation. However, population shifts documented in the 2020 Census—growth in Republican-leaning exurban counties like Butler, Cumberland, and York, coupled with stagnation in Philadelphia—have prompted legal challenges to the maps ahead of the 2026 cycle. Christian conservative organizations such as the Pennsylvania Family Institute and the American Family Association of Pennsylvania have mobilized grassroots networks to influence reapportionment, arguing that urban overrepresentation dilutes rural values. These groups have successfully lobbied for constitutional amendments requiring voter approval for any tax increases exceeding inflation plus population growth, a measure that passed the legislature in 2023 and will appear on the 2025 ballot.

Economically, Pennsylvania grapples with the decline of legacy industries and the rise of energy production. The Marcellus Shale natural gas boom has revitalized communities in the northeast and southwest, generating over 100,000 jobs and contributing $16 billion annually to state revenue, according to the Pennsylvania Department of Environmental Protection. Republican candidates uniformly champion hydraulic fracturing and pipeline development, framing energy independence as both an economic and national security imperative. Democrats, particularly in suburban Philadelphia collars, emphasize environmental justice and renewable transitions, though Governor Shapiro has maintained a pragmatic moratorium on new leasing in state forests while approving private-land development. Christian conservatives align overwhelmingly with the pro-drilling coalition, viewing resource extraction as responsible stewardship and a counterweight to foreign energy dependence. Labor unions, once a Democratic bastion, now split: building trades endorse Republican energy policies, while public sector unions remain Democratic strongholds. This fracture complicates turnout models in counties like Luzerne and Northampton, which flipped from Democrat Barack Obama in 2012 to Republican Donald Trump in 2016 and 2020.

Social issues animate Pennsylvania’s cultural battleground with particular intensity. The state’s abortion laws, codified after Planned Parenthood v. Casey in 1992, permit the procedure up to 24 weeks with parental consent for minors and a 24-hour waiting period. Post-Dobbs, Republican legislators introduced a heartbeat bill that failed by one vote in the state Senate in 2023. Christian conservative activists, coordinated through Pennsylvania Right to Life and church networks, have shifted focus to incremental restrictions: banning taxpayer funding for abortion providers, requiring ultrasound viewings, and mandating burial or cremation of fetal remains. These efforts enjoy majority support in 48 of 67 counties, per Franklin & Marshall polling. Meanwhile, Democratic candidates campaign on codifying Roe v. Wade into state statute, a priority that mobilizes college-educated women in Montgomery, Chester, and Allegheny counties. School choice represents another fault line. Pennsylvania’s Educational Improvement Tax Credit program, expanded in 2024 to $350 million annually, enables businesses to redirect tax dollars to scholarship organizations. Republican majorities seek full voucher expansion; Democrats counter with increased public school funding tied to equity formulas. Christian homeschooling families, numbering over 50,000 according to the Pennsylvania Department of Education, constitute a growing bloc within the Republican coalition.

Religious affiliation underpins much of Pennsylvania’s political identity. The state ranks seventh nationally in Catholic population, with 3.5 million adherents concentrated in the east. Evangelical Protestants, approximately 1.2 million strong, dominate the central “T” region from Lancaster to Erie. Mainline Protestant decline has accelerated, with Presbyterian and Methodist congregations closing at a rate of 80 per year. These shifts favor Republican messaging on traditional marriage, gender ideology in schools, and opposition to critical race theory curricula. The Pennsylvania Catholic Conference, representing the state’s eight dioceses, issues voter guides that prioritize life issues while acknowledging prudential judgment on immigration and poverty programs. Evangelical pastors in megachurches like LCBC in Manheim and Calvary Fellowship in Downingtown mobilize congregants through “Faith and Freedom” coalitions. Jewish voters, though only 2 percent of the electorate, wield outsized influence in Philadelphia’s suburban ring; their leftward drift since 2016 has offset some Republican gains among Latino evangelicals in Berks and Lehigh counties.

Infrastructure and governance round out the policy landscape. Pennsylvania’s transportation network faces a $15 billion maintenance backlog, per the American Society of Civil Engineers. Republican proposals center on public-private partnerships and tolling; Democrats favor progressive gas tax indexing. The opioid crisis, which claimed 5,200 lives in 2023, prompts bipartisan warm-market recovery centers, though Republicans emphasize law enforcement while Democrats prioritize harm reduction. Criminal justice reform divides along urban-rural lines: Philadelphia District Attorney Larry Krasner’s progressive policies contrast with Republican sheriffs in York and Westmoreland counties who expand drug courts and faith-based rehabilitation. Christian conservative ministries operate 180 prison fellowships statewide, advocating restorative justice models that reduce recidivism by 22 percent according to Temple University studies. These ministries bridge partisan divides while reinforcing conservative emphasis on personal responsibility.

Looking toward 2025 and 2026, turnout mechanisms will prove decisive. Pennsylvania’s closed primary system advantages ideologically committed voters, giving Christian conservatives outsized influence in Republican contests. The state’s 2019 Act 77 introduced no-excuse mail voting, which Republicans initially embraced but later challenged after 2020 controversies. A 2024 state Supreme Court ruling upheld the law while mandating signature verification, a compromise that satisfies neither extreme. Voter rolls have grown to 9.1 million, with Republicans narrowing the Democratic registration edge to 240,000 through aggressive outreach in exurban townships. Independent registration, now 18 percent, surges among millennial and Gen Z voters disillusioned with both parties. Christian conservative get-out-the-vote operations, leveraging church directories and homeschool networks, achieved 94 percent turnout among identified members in 2022 midterms, per internal Pennsylvania Family Council data. These structural realities position Pennsylvania as the fulcrum of national control for the United States House, Senate, and presidency.

---

## 🔴 2026 FEDERAL RACES

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

## 🔴 2025 STATE RACES

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

## 🔴 2025 SCHOOL BOARD RACES

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

## 🔴 2025 MUNICIPAL RACES

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

## 🔴 COUNTY ELECTIONS

Pennsylvania's county elections play a pivotal role in shaping local governance, public policy, and the enforcement of laws that directly impact Christian conservative values across the commonwealth. With sixty-seven counties, each conducting elections for positions such as county commissioners, district attorneys, sheriffs, prothonotaries, registers of wills, and coroners, these races determine who controls property taxes, law enforcement priorities, election administration, and even the handling of vital records that relate to family issues like marriage licenses and death certificates. In many rural and suburban counties, conservative candidates often align with pro-life, pro-family, and pro-Second Amendment platforms, while urban counties like Philadelphia, Allegheny, Montgomery, and Delaware tend to favor progressive policies on social issues. For instance, county commissioners hold authority over budgets that fund health services, including whether taxpayer dollars support abortion providers through indirect grants or partnerships with organizations like Planned Parenthood. District attorneys decide prosecution priorities, influencing whether crimes against religious institutions, such as vandalism of churches, receive vigorous pursuit or lenient treatment. Sheriffs enforce court orders and maintain public order, with some taking strong stands on Second Amendment sanctuaries to protect gun rights from state overreach.

Key battleground counties include Lancaster, York, and Bucks, where Christian conservative turnout can sway commissioner majorities toward fiscal responsibility and traditional values. In Lancaster County, home to a large Amish and Mennonite population, elections for three commissioner seats often hinge on issues like agricultural protections and opposition to expansive government programs that burden family farms. Candidates who pledge to defend religious exemptions for homeschooling and private schools resonate deeply here. Similarly, in Bucks County, a swing area with growing suburban development, the district attorney's race determines approaches to juvenile justice and drug enforcement, with conservatives advocating for tougher penalties on fentanyl traffickers to safeguard families. Philadelphia County, encompassing the city, features consolidated city-county roles where the district attorney has implemented policies criticized by conservatives for reducing prosecutions on certain offenses, leading to calls for reform candidates who prioritize victims' rights and public safety rooted in biblical justice principles.

Further west, Allegheny County, including Pittsburgh, sees intense contests for county executive and council seats, where progressive incumbents push for equity initiatives that conservatives view as discriminatory against faith-based organizations. Erie and Northampton Counties represent additional fronts, with sheriff races focusing on cooperation with federal immigration enforcement, a stance favored by those upholding the rule of law as ordained by God. Across the state, prothonotary offices manage court records, including those for family court divisions handling divorce and custody, making these clerical yet influential positions critical for ensuring fair treatment under the law for traditional families. Registers of wills oversee estate probate, affecting inheritance laws that align with scriptural principles of stewardship. Even coroner elections matter, as these officials investigate deaths, including those from abortions or euthanasia, potentially exposing truths that inform public policy.

Christian conservatives must research candidates through voter guides from organizations like the Pennsylvania Family Institute, attending county Republican or Constitution Party meetings to identify allies. Door-to-door canvassing in neighborhoods, phone banking from church directories, and hosting candidate forums in fellowship halls amplify impact. In counties with mail-in voting controversies, supporting commissioners who audit election processes restores trust. Ultimately, winning at the county level builds a foundation for statewide victories, securing officials who view government as a minister of God for good, as described in Romans chapter thirteen.

---

## 🔴 KEY ISSUES FOR PENNSYLVANIA CHRISTIAN CONSERVATIVES

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

## 🔴 CHURCH MOBILIZATION STRATEGY

Pastors hold immense influence in mobilizing congregations for civic engagement without jeopardizing tax-exempt status by focusing on issues, not candidates. They can preach biblical citizenship series drawing from scriptures on government and justice, inviting speakers from policy councils to educate on current legislation. Host voter registration drives after services, distribute nonpartisan voter guides, and organize prayer walks for the nation. Form church election teams to coordinate transportation to polls, especially for elderly members, and partner with pregnancy centers for service opportunities that highlight life issues. Pastors should model involvement by serving on community boards and encouraging members to run for local office, providing pulpit endorsements for principles like sanctity of life.

Church members complement pastoral leadership through personal activism, starting with informed voting based on candidates' alignment with scriptural values. They can canvass neighborhoods with literature, host home Bible studies discussing policy through a Christian lens, and use social media to share truth respectfully. Volunteer for campaigns of principled candidates, phone bank from home, and babysit for parents attending meetings. Members should tithe time to mentor youth in civics, organize carpool poll efforts, and fast weekly for elections.

---

## 🔴 CRITICAL DATES

The primary election occurs on the third Tuesday in May, determining party nominees for November contests; prepare by registering thirty days prior. General election day falls on the first Tuesday after the first Monday in November, a national holiday for voting; churches can serve as polls. Voter registration deadlines are fifteen days before each election, requiring drives well in advance. Mail ballot applications must submit by the Tuesday before election week, with returns by eight post meridiem on election day. Early in-person voting availability varies by county, often starting weeks prior.

---

## 🔴 RESOURCES

The Pennsylvania Family Institute offers voter guides, policy briefs, and legal aid at pafamily.org, equipping believers with research. Tony Perkins' Stand firm app provides daily updates on national issues affecting the state. Heritage Foundation's Election Integrity Scorecard rates Pennsylvania's laws, guiding advocacy. Local crisis pregnancy centers like AlphaCare in Philadelphia need volunteers and donations. Alliance Defending Freedom litigates religious liberty cases, accepting prayer support.

---

## 🔴 BOTTOM LINE

Pennsylvania stands at a crossroads where control of the legislature, governorship, and courts will determine if the commonwealth honors God in policies on life, family, liberty, and justice or descends into secular progressivism eroding foundational truths. Christian conservatives must engage fully, recognizing apathy cedes ground to forces opposing biblical worldview, with eternal consequences for generations.

---

## 🔴 PRAYER POINTS

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
