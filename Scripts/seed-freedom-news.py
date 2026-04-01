import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# Religious freedom news sources
FREEDOM_SOURCES = [
    {
        'name': 'Becket Fund for Religious Liberty',
        'type': 'Legal Advocacy',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Religious Liberty Litigation',
        'description': 'Leading non-profit law firm defending religious freedom for all faiths.',
        'url': 'https://www.becketlaw.org'
    },
    {
        'name': 'First Liberty Institute',
        'type': 'Legal Advocacy',
        'city': 'Plano',
        'state': 'Texas',
        'focus': 'Religious Freedom Defense',
        'description': 'Nation\'s largest legal organization dedicated exclusively to defending religious liberty.',
        'url': 'https://www.firstliberty.org'
    },
    {
        'name': 'Alliance Defending Freedom',
        'type': 'Legal Advocacy',
        'city': 'Scottsdale',
        'state': 'Arizona',
        'focus': 'Religious Freedom & Free Speech',
        'description': 'Alliance of Christian attorneys defending religious freedom worldwide.',
        'url': 'https://www.adflegal.org'
    },
    {
        'name': 'Liberty Counsel',
        'type': 'Legal Advocacy',
        'city': 'Orlando',
        'state': 'Florida',
        'focus': 'Religious Liberty & Family',
        'description': 'Nonprofit litigation and education organization defending religious freedom.',
        'url': 'https://www.lc.org'
    },
    {
        'name': 'American Center for Law and Justice',
        'type': 'Legal Advocacy',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Constitutional Law',
        'description': 'Jay Sekulow\'s organization defending constitutional freedoms.',
        'url': 'https://www.aclj.org'
    },
    {
        'name': 'Pacific Justice Institute',
        'type': 'Legal Advocacy',
        'city': 'Sacramento',
        'state': 'California',
        'focus': 'Religious Freedom & Parental Rights',
        'description': 'Legal defense organization specializing in religious freedom cases.',
        'url': 'https://www.pacificjustice.org'
    },
    {
        'name': 'Thomas More Society',
        'type': 'Legal Advocacy',
        'city': 'Chicago',
        'state': 'Illinois',
        'focus': 'Religious Liberty & Life',
        'description': 'National public interest law firm defending religious freedom and life.',
        'url': 'https://www.thomasmoresociety.org'
    },
    {
        'name': 'Christian Legal Society',
        'type': 'Legal Advocacy',
        'city': 'Springfield',
        'state': 'Virginia',
        'focus': 'Christian Attorneys Network',
        'description': 'Membership organization of Christian attorneys and law students.',
        'url': 'https://www.christianlegalsociety.org'
    },
    {
        'name': 'Religious Freedom Institute',
        'type': 'Research Institute',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Religious Freedom Research',
        'description': 'Think tank dedicated to achieving broad acceptance of religious liberty.',
        'url': 'https://www.religiousfreedominstitute.org'
    },
    {
        'name': 'International Religious Freedom Roundtable',
        'type': 'Watchdog Group',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Global Religious Freedom',
        'description': 'Coalition advocating for international religious freedom.',
        'url': 'https://www.irfroundtable.org'
    },
    {
        'name': 'U.S. Commission on International Religious Freedom',
        'type': 'Government Agency',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'International Religious Freedom',
        'description': 'Independent federal commission monitoring religious freedom violations worldwide.',
        'url': 'https://www.uscirf.gov'
    },
    {
        'name': 'Family Research Council',
        'type': 'Research Institute',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Faith, Family & Freedom',
        'description': 'Conservative Christian policy and lobbying organization.',
        'url': 'https://www.frc.org'
    },
    {
        'name': 'Ethics & Religious Liberty Commission',
        'type': 'Research Institute',
        'city': 'Nashville',
        'state': 'Tennessee',
        'focus': 'Southern Baptist Public Policy',
        'description': 'Southern Baptist Convention\'s public policy arm.',
        'url': 'https://www.erlc.com'
    },
    {
        'name': 'The Christian Post',
        'type': 'News Organization',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Christian News',
        'description': 'One of the most read Christian news sites covering religious freedom.',
        'url': 'https://www.christianpost.com'
    },
    {
        'name': 'The Federalist Society',
        'type': 'Research Institute',
        'city': 'Washington',
        'state': 'District of Columbia',
        'focus': 'Constitutional Law',
        'description': 'Conservative legal organization promoting religious liberty principles.',
        'url': 'https://www.fedsoc.org'
    }
]

def create_resource(resource):
    resource_id = f"freedom_{int(time.time() * 1000)}_{resource['type'].replace(' ', '_')}"
    
    payload = {
        'id': resource_id,
        'name': resource['name'],
        'category': ['Religious Freedom', 'Religion'],
        'subcategory': resource['type'],
        'city': resource.get('city'),
        'state': resource.get('state'),
        'focus': resource.get('focus'),
        'url': resource['url'],
        'description': resource['description']
    }
    
    try:
        response = requests.post(
            f"{API_URL}?action=create",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Created: {resource['name']}")
            return True
        else:
            print(f"❌ Failed: {resource['name']} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {resource['name']} - {str(e)}")
        return False

def seed_resources():
    print("🌱 Seeding religious freedom news sources...\n")
    
    total = len(FREEDOM_SOURCES)
    success = 0
    
    for resource in FREEDOM_SOURCES:
        if create_resource(resource):
            success += 1
        time.sleep(0.2)
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting religious freedom news source seeding...")
    print(f"This will create {len(FREEDOM_SOURCES)} news sources.\n")
    seed_resources()
