import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# Missionary resources
MISSIONARY_RESOURCES = [
    {
        'name': 'Wycliffe Bible Translators',
        'type': 'Bible Translation',
        'description': 'Global ministry translating the Bible into every language.',
        'url': 'https://www.wycliffe.org'
    },
    {
        'name': 'The Seed Company',
        'type': 'Bible Translation',
        'description': 'Accelerating Bible translation through partnerships worldwide.',
        'url': 'https://www.theseedcompany.org'
    },
    {
        'name': 'YWAM - Youth With A Mission',
        'type': 'Mission Organization',
        'description': 'International movement of Christians from many denominations dedicated to presenting Jesus.',
        'url': 'https://www.ywam.org'
    },
    {
        'name': 'OM International',
        'type': 'Mission Organization',
        'description': 'Global missions organization mobilizing people to share God\'s love.',
        'url': 'https://www.om.org'
    },
    {
        'name': 'Pioneers',
        'type': 'Church Planting',
        'description': 'Church planting movement among unreached people groups.',
        'url': 'https://www.pioneers.org'
    },
    {
        'name': 'Frontiers',
        'type': 'Church Planting',
        'description': 'Planting churches among Muslim peoples worldwide.',
        'url': 'https://www.frontiersusa.org'
    },
    {
        'name': 'SIM - Serving In Mission',
        'type': 'Mission Organization',
        'description': 'International mission organization serving in over 70 countries.',
        'url': 'https://www.sim.org'
    },
    {
        'name': 'Compassion International',
        'type': 'Humanitarian Aid',
        'description': 'Child sponsorship and development programs in Jesus\' name.',
        'url': 'https://www.compassion.com'
    },
    {
        'name': 'World Vision',
        'type': 'Humanitarian Aid',
        'description': 'Christian humanitarian organization serving children and communities.',
        'url': 'https://www.worldvision.org'
    },
    {
        'name': 'Samaritan\'s Purse',
        'type': 'Humanitarian Aid',
        'description': 'International relief and evangelism led by Franklin Graham.',
        'url': 'https://www.samaritanspurse.org'
    },
    {
        'name': 'The Mission Society',
        'type': 'Mission Organization',
        'description': 'Sending missionaries to make disciples and multiply churches.',
        'url': 'https://www.themissionsociety.org'
    },
    {
        'name': 'Adventures in Missions',
        'type': 'Short-Term Missions',
        'description': 'Short-term mission trips and gap year programs worldwide.',
        'url': 'https://www.adventures.org'
    },
    {
        'name': 'Mission Aviation Fellowship',
        'type': 'Mission Organization',
        'description': 'Flying light aircraft to reach isolated people with the Gospel.',
        'url': 'https://www.maf.org'
    },
    {
        'name': 'Voice of the Martyrs',
        'type': 'Mission Organization',
        'description': 'Serving persecuted Christians worldwide.',
        'url': 'https://www.persecution.com'
    },
    {
        'name': 'Campus Crusade for Christ (Cru)',
        'type': 'Mission Organization',
        'description': 'Evangelism and discipleship on college campuses and beyond.',
        'url': 'https://www.cru.org'
    },
    {
        'name': 'The Navigators',
        'type': 'Mission Organization',
        'description': 'Discipleship ministry helping people know Christ and make Him known.',
        'url': 'https://www.navigators.org'
    },
    {
        'name': 'InterVarsity Christian Fellowship',
        'type': 'Mission Organization',
        'description': 'Campus ministry building witnessing communities on college campuses.',
        'url': 'https://www.intervarsity.org'
    },
    {
        'name': 'Gospel for Asia',
        'type': 'Mission Organization',
        'description': 'Supporting indigenous missionaries in Asia.',
        'url': 'https://www.gfa.org'
    },
    {
        'name': 'Ethnos360 (New Tribes Mission)',
        'type': 'Church Planting',
        'description': 'Church planting among unreached tribal peoples.',
        'url': 'https://www.ethnos360.org'
    },
    {
        'name': 'Missionary Ventures International',
        'type': 'Mission Organization',
        'description': 'Equipping national church leaders and missionaries worldwide.',
        'url': 'https://www.mvi.org'
    }
]

def create_resource(resource):
    resource_id = f"mission_{int(time.time() * 1000)}_{resource['type'].replace(' ', '_')}"
    
    payload = {
        'id': resource_id,
        'name': resource['name'],
        'category': ['Missions', 'Religion'],
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
    print("🌱 Seeding missionary resources...\n")
    
    total = len(MISSIONARY_RESOURCES)
    success = 0
    
    for resource in MISSIONARY_RESOURCES:
        if create_resource(resource):
            success += 1
        time.sleep(0.2)
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting missionary resource seeding...")
    print(f"This will create {len(MISSIONARY_RESOURCES)} missionary resources.\n")
    seed_resources()
