import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# Additional theological resources
THEOLOGICAL_RESOURCES = [
    # Christian Colleges
    {
        'name': 'Liberty University',
        'type': 'Seminary/Training',
        'description': 'Christian university offering undergraduate and graduate programs with biblical worldview.',
        'url': 'https://www.liberty.edu'
    },
    {
        'name': 'Biola University',
        'type': 'Seminary/Training',
        'description': 'Biblically-centered Christian university in Southern California.',
        'url': 'https://www.biola.edu'
    },
    {
        'name': 'Moody Bible Institute',
        'type': 'Seminary/Training',
        'description': 'Bible college and seminary training Christian leaders since 1886.',
        'url': 'https://www.moody.edu'
    },
    {
        'name': 'Dallas Theological Seminary',
        'type': 'Seminary/Training',
        'description': 'Leading evangelical seminary with rigorous theological education.',
        'url': 'https://www.dts.edu'
    },
    {
        'name': 'The Master\'s University',
        'type': 'Seminary/Training',
        'description': 'Christ-centered university committed to biblical inerrancy.',
        'url': 'https://www.masters.edu'
    },
    {
        'name': 'Wheaton College',
        'type': 'Seminary/Training',
        'description': 'Premier Christian liberal arts college with evangelical heritage.',
        'url': 'https://www.wheaton.edu'
    },
    {
        'name': 'Grove City College',
        'type': 'Seminary/Training',
        'description': 'Independent Christian college emphasizing faith and freedom.',
        'url': 'https://www.gcc.edu'
    },
    {
        'name': 'Hillsdale College',
        'type': 'Seminary/Training',
        'description': 'Classical liberal arts college with Judeo-Christian values.',
        'url': 'https://www.hillsdale.edu'
    },
    # Apologists and Ministries
    {
        'name': 'William Federer - American Minute',
        'type': 'Apologetics',
        'description': 'Historian and speaker on America\'s Christian heritage and founding principles.',
        'url': 'https://www.americanminute.com'
    },
    {
        'name': 'Frank Turek - CrossExamined',
        'type': 'Apologetics',
        'description': 'Christian apologetics ministry defending the truth of Christianity.',
        'url': 'https://www.crossexamined.org'
    },
    {
        'name': 'Ravi Zacharias International Ministries',
        'type': 'Apologetics',
        'description': 'Apologetics ministry addressing life\'s great existential questions.',
        'url': 'https://www.rzim.org'
    },
    {
        'name': 'Stand to Reason',
        'type': 'Apologetics',
        'description': 'Training Christians to think clearly about their faith with Greg Koukl.',
        'url': 'https://www.str.org'
    },
    {
        'name': 'Reasonable Faith',
        'type': 'Apologetics',
        'description': 'William Lane Craig\'s ministry providing scholarly defense of Christianity.',
        'url': 'https://www.reasonablefaith.org'
    },
    {
        'name': 'Answers in Genesis',
        'type': 'Apologetics',
        'description': 'Creation apologetics ministry defending biblical authority.',
        'url': 'https://www.answersingenesis.org'
    },
    {
        'name': 'Cold-Case Christianity',
        'type': 'Apologetics',
        'description': 'J. Warner Wallace applying detective skills to Christian case-making.',
        'url': 'https://www.coldcasechristianity.com'
    }
]

def create_resource(resource):
    resource_id = f"theology_{int(time.time() * 1000)}_{resource['type'].replace(' ', '_').replace('/', '_')}"
    
    payload = {
        'id': resource_id,
        'name': resource['name'],
        'category': ['Theology', 'Religion'],
        'subcategory': resource['type'],
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
    print("🌱 Seeding theological resources...\n")
    
    total = len(THEOLOGICAL_RESOURCES)
    success = 0
    
    for resource in THEOLOGICAL_RESOURCES:
        if create_resource(resource):
            success += 1
        time.sleep(0.2)
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting theological resource seeding...")
    print(f"This will create {len(THEOLOGICAL_RESOURCES)} theological resources.\n")
    seed_resources()
