import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# National organizations with state chapters
NATIONAL_ORGS = [
    {
        'name': 'Care Net Pregnancy Center',
        'type': 'Pregnancy Center',
        'description': 'Compassionate help and support for women facing unplanned pregnancies. Free pregnancy tests, ultrasounds, and counseling.',
        'url': 'https://www.care-net.org'
    },
    {
        'name': 'Heartbeat International Pregnancy Help Center',
        'type': 'Pregnancy Center',
        'description': 'Life-affirming pregnancy help including medical services, material assistance, and post-abortion support.',
        'url': 'https://www.heartbeatinternational.org'
    },
    {
        'name': 'Birthright',
        'type': 'Pregnancy Center',
        'description': 'Non-judgmental support for pregnant women. Free pregnancy tests and practical help.',
        'url': 'https://www.birthright.org'
    },
    {
        'name': 'Bethany Christian Services',
        'type': 'Adoption Agency',
        'description': 'Christian adoption agency providing adoption services, foster care, and family support.',
        'url': 'https://www.bethany.org'
    },
    {
        'name': 'Gladney Center for Adoption',
        'type': 'Adoption Agency',
        'description': 'Comprehensive adoption services including domestic, international, and foster care adoption.',
        'url': 'https://www.gladney.org'
    },
    {
        'name': 'National Right to Life',
        'type': 'Advocacy Organization',
        'description': 'Leading pro-life advocacy organization working to protect innocent human life.',
        'url': 'https://www.nrlc.org'
    },
    {
        'name': 'Americans United for Life',
        'type': 'Legal Defense',
        'description': 'Legal advocacy for pro-life laws and policies at state and federal levels.',
        'url': 'https://www.aul.org'
    },
    {
        'name': 'Rachel\'s Vineyard',
        'type': 'Post-Abortion Support',
        'description': 'Healing retreats for those suffering from abortion trauma. Confidential and compassionate care.',
        'url': 'https://www.rachelsvineyard.org'
    },
    {
        'name': 'Silent No More Awareness Campaign',
        'type': 'Post-Abortion Support',
        'description': 'Support and healing for those hurt by abortion. Share your story and find hope.',
        'url': 'https://www.silentnomoreawareness.org'
    }
]

US_STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 
    'Wisconsin', 'Wyoming'
]

# Major cities per state for more specific resources
STATE_CITIES = {
    'Alabama': ['Birmingham', 'Montgomery', 'Mobile'],
    'Alaska': ['Anchorage', 'Fairbanks', 'Juneau'],
    'Arizona': ['Phoenix', 'Tucson', 'Mesa'],
    'Arkansas': ['Little Rock', 'Fort Smith', 'Fayetteville'],
    'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'Fresno'],
    'Colorado': ['Denver', 'Colorado Springs', 'Aurora'],
    'Connecticut': ['Hartford', 'New Haven', 'Stamford'],
    'Delaware': ['Wilmington', 'Dover', 'Newark'],
    'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Tallahassee'],
    'Georgia': ['Atlanta', 'Savannah', 'Augusta'],
    'Hawaii': ['Honolulu', 'Hilo', 'Kailua'],
    'Idaho': ['Boise', 'Meridian', 'Nampa'],
    'Illinois': ['Chicago', 'Springfield', 'Peoria'],
    'Indiana': ['Indianapolis', 'Fort Wayne', 'Evansville'],
    'Iowa': ['Des Moines', 'Cedar Rapids', 'Davenport'],
    'Kansas': ['Wichita', 'Overland Park', 'Kansas City'],
    'Kentucky': ['Louisville', 'Lexington', 'Bowling Green'],
    'Louisiana': ['New Orleans', 'Baton Rouge', 'Shreveport'],
    'Maine': ['Portland', 'Lewiston', 'Bangor'],
    'Maryland': ['Baltimore', 'Annapolis', 'Frederick'],
    'Massachusetts': ['Boston', 'Worcester', 'Springfield'],
    'Michigan': ['Detroit', 'Grand Rapids', 'Lansing'],
    'Minnesota': ['Minneapolis', 'St. Paul', 'Rochester'],
    'Mississippi': ['Jackson', 'Gulfport', 'Hattiesburg'],
    'Missouri': ['Kansas City', 'St. Louis', 'Springfield'],
    'Montana': ['Billings', 'Missoula', 'Great Falls'],
    'Nebraska': ['Omaha', 'Lincoln', 'Bellevue'],
    'Nevada': ['Las Vegas', 'Reno', 'Henderson'],
    'New Hampshire': ['Manchester', 'Nashua', 'Concord'],
    'New Jersey': ['Newark', 'Jersey City', 'Trenton'],
    'New Mexico': ['Albuquerque', 'Santa Fe', 'Las Cruces'],
    'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany'],
    'North Carolina': ['Charlotte', 'Raleigh', 'Greensboro'],
    'North Dakota': ['Fargo', 'Bismarck', 'Grand Forks'],
    'Ohio': ['Columbus', 'Cleveland', 'Cincinnati'],
    'Oklahoma': ['Oklahoma City', 'Tulsa', 'Norman'],
    'Oregon': ['Portland', 'Salem', 'Eugene'],
    'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Harrisburg'],
    'Rhode Island': ['Providence', 'Warwick', 'Cranston'],
    'South Carolina': ['Charleston', 'Columbia', 'Greenville'],
    'South Dakota': ['Sioux Falls', 'Rapid City', 'Aberdeen'],
    'Tennessee': ['Nashville', 'Memphis', 'Knoxville'],
    'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
    'Utah': ['Salt Lake City', 'Provo', 'West Valley City'],
    'Vermont': ['Burlington', 'Montpelier', 'Rutland'],
    'Virginia': ['Virginia Beach', 'Richmond', 'Norfolk'],
    'Washington': ['Seattle', 'Spokane', 'Tacoma'],
    'West Virginia': ['Charleston', 'Huntington', 'Morgantown'],
    'Wisconsin': ['Milwaukee', 'Madison', 'Green Bay'],
    'Wyoming': ['Cheyenne', 'Casper', 'Laramie']
}

def create_resource(org, state, city=None):
    resource_id = f"prolife_{int(time.time() * 1000)}_{state.replace(' ', '_')}_{org['type'].replace(' ', '_')}"
    
    name = f"{org['name']} - {city if city else state}"
    
    payload = {
        'id': resource_id,
        'name': name,
        'category': ['Pro-Life', 'Family'],
        'subcategory': org['type'],
        'state': state,
        'city': city,
        'url': org['url'],
        'description': org['description']
    }
    
    try:
        response = requests.post(
            f"{API_URL}?action=create",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Created: {name}")
            return True
        else:
            print(f"❌ Failed: {name} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {name} - {str(e)}")
        return False

def seed_resources():
    print("🌱 Seeding pro-life resources for all 50 states...\n")
    
    total = 0
    success = 0
    
    for state in US_STATES:
        print(f"\n📍 {state}")
        cities = STATE_CITIES.get(state, [state])
        
        # Add 2-3 resources per major city
        for city in cities[:3]:  # Limit to top 3 cities per state
            for org in NATIONAL_ORGS[:3]:  # Add top 3 org types per city
                if create_resource(org, state, city):
                    success += 1
                total += 1
                time.sleep(0.2)  # Rate limiting
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting pro-life resource seeding...")
    print("This will create ~450 resources across all 50 states.\n")
    seed_resources()
