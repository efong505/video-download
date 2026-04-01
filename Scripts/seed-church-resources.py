import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# Church resources
CHURCH_RESOURCES = [
    {
        'name': 'First Baptist Church (Dallas, TX)',
        'type': 'Baptist',
        'description': 'Historic Southern Baptist church with strong biblical teaching.',
        'url': 'https://www.firstdallas.org'
    },
    {
        'name': 'Saddleback Church (Lake Forest, CA)',
        'type': 'Baptist',
        'description': 'Purpose-driven church founded by Rick Warren.',
        'url': 'https://www.saddleback.com'
    },
    {
        'name': 'Calvary Chapel (Costa Mesa, CA)',
        'type': 'Non-Denominational',
        'description': 'Verse-by-verse Bible teaching church.',
        'url': 'https://www.calvarychapel.com'
    },
    {
        'name': 'Christ Community Church (Omaha, NE)',
        'type': 'Non-Denominational',
        'description': 'Gospel-centered church making disciples.',
        'url': 'https://www.christcommunityomaha.org'
    },
    {
        'name': 'Tenth Presbyterian Church (Philadelphia, PA)',
        'type': 'Presbyterian',
        'description': 'Historic PCA church with expository preaching.',
        'url': 'https://www.tenth.org'
    },
    {
        'name': 'Park Cities Presbyterian Church (Dallas, TX)',
        'type': 'Presbyterian',
        'description': 'Reformed church committed to biblical authority.',
        'url': 'https://www.pcpc.org'
    },
    {
        'name': 'Bethel Church (Redding, CA)',
        'type': 'Pentecostal',
        'description': 'Spirit-filled church with worship and healing ministry.',
        'url': 'https://www.bethel.com'
    },
    {
        'name': 'The Potter\'s House (Dallas, TX)',
        'type': 'Non-Denominational',
        'description': 'Multicultural megachurch led by T.D. Jakes.',
        'url': 'https://www.thepottershouse.org'
    },
    {
        'name': 'Grace Community Church (Sun Valley, CA)',
        'type': 'Reformed',
        'description': 'John MacArthur\'s church with expository preaching.',
        'url': 'https://www.gracechurch.org'
    },
    {
        'name': 'Capitol Hill Baptist Church (Washington, DC)',
        'type': 'Baptist',
        'description': 'Mark Dever\'s church emphasizing biblical church membership.',
        'url': 'https://www.capitolhillbaptist.org'
    },
    {
        'name': 'The Village Church (Dallas, TX)',
        'type': 'Baptist',
        'description': 'Gospel-centered church with multiple campuses.',
        'url': 'https://www.thevillagechurch.net'
    },
    {
        'name': 'Redeemer Presbyterian Church (New York, NY)',
        'type': 'Presbyterian',
        'description': 'Tim Keller\'s church reaching urban professionals.',
        'url': 'https://www.redeemer.com'
    },
    {
        'name': 'Harvest Bible Chapel (Rolling Meadows, IL)',
        'type': 'Non-Denominational',
        'description': 'Bible-teaching church with bold proclamation.',
        'url': 'https://www.harvestbiblechapel.org'
    },
    {
        'name': 'Cornerstone Church (San Antonio, TX)',
        'type': 'Non-Denominational',
        'description': 'John Hagee\'s church with strong Israel support.',
        'url': 'https://www.sacornerstone.org'
    },
    {
        'name': 'Christ Church (Moscow, ID)',
        'type': 'Reformed',
        'description': 'Doug Wilson\'s Reformed church with classical Christian education.',
        'url': 'https://www.christkirk.com'
    }
]

def create_resource(resource):
    resource_id = f"church_{int(time.time() * 1000)}_{resource['type'].replace(' ', '_')}"
    
    payload = {
        'id': resource_id,
        'name': resource['name'],
        'category': ['Church', 'Religion'],
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
    print("🌱 Seeding church resources...\n")
    
    total = len(CHURCH_RESOURCES)
    success = 0
    
    for resource in CHURCH_RESOURCES:
        if create_resource(resource):
            success += 1
        time.sleep(0.2)
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting church resource seeding...")
    print(f"This will create {len(CHURCH_RESOURCES)} church resources.\n")
    seed_resources()
