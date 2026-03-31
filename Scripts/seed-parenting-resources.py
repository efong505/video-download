import sys
import json
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

# Parenting resources
PARENTING_RESOURCES = [
    {
        'name': 'Classical Conversations',
        'type': 'Homeschooling',
        'description': 'Classical Christian homeschool curriculum and community support for families.',
        'url': 'https://www.classicalconversations.com'
    },
    {
        'name': 'Abeka Academy',
        'type': 'Homeschooling',
        'description': 'Christian homeschool curriculum with video instruction and traditional textbooks.',
        'url': 'https://www.abeka.com'
    },
    {
        'name': 'Apologia Educational Ministries',
        'type': 'Books & Curriculum',
        'description': 'Award-winning Christian science curriculum for homeschool families.',
        'url': 'https://www.apologia.com'
    },
    {
        'name': 'Focus on the Family Parenting',
        'type': 'Parenting Tips',
        'description': 'Biblical parenting advice, resources, and support for Christian families.',
        'url': 'https://www.focusonthefamily.com/parenting'
    },
    {
        'name': 'Shepherding a Child\'s Heart',
        'type': 'Books & Curriculum',
        'description': 'Tedd Tripp\'s biblical approach to parenting focused on the heart, not just behavior.',
        'url': 'https://www.shepherdpress.com'
    },
    {
        'name': 'Growing Kids God\'s Way',
        'type': 'Parenting Tips',
        'description': 'Biblical parenting curriculum teaching moral and character development.',
        'url': 'https://www.gfi.org'
    },
    {
        'name': 'Raising Godly Children',
        'type': 'Child Development',
        'description': 'Resources for raising children with biblical values and character.',
        'url': 'https://www.raisinggodlychildren.org'
    },
    {
        'name': 'Biblical Discipline Methods',
        'type': 'Discipline & Training',
        'description': 'Scriptural approaches to child discipline with grace and truth.',
        'url': 'https://www.biblicaldiscipline.org'
    },
    {
        'name': 'HSLDA - Home School Legal Defense',
        'type': 'Homeschooling',
        'description': 'Legal advocacy and support for homeschooling families nationwide.',
        'url': 'https://www.hslda.org'
    },
    {
        'name': 'Sonlight Curriculum',
        'type': 'Books & Curriculum',
        'description': 'Literature-based Christian homeschool curriculum with global perspective.',
        'url': 'https://www.sonlight.com'
    },
    {
        'name': 'My Father\'s World',
        'type': 'Books & Curriculum',
        'description': 'Creation-based, Christ-centered homeschool curriculum.',
        'url': 'https://www.mfwbooks.com'
    },
    {
        'name': 'Christian Parenting Support Groups',
        'type': 'Support Groups',
        'description': 'Local and online support groups for Christian parents.',
        'url': 'https://www.christianparentingsupport.org'
    },
    {
        'name': 'Homeschool Co-ops Network',
        'type': 'Support Groups',
        'description': 'Find and connect with homeschool co-ops in your area.',
        'url': 'https://www.homeschoolcoops.org'
    },
    {
        'name': 'Positive Parenting with Biblical Principles',
        'type': 'Parenting Tips',
        'description': 'Practical parenting advice rooted in Scripture and grace.',
        'url': 'https://www.positiveparenting.org'
    },
    {
        'name': 'Character Training Institute',
        'type': 'Child Development',
        'description': 'Biblical character development resources for children and teens.',
        'url': 'https://www.characterhealth.com'
    },
    {
        'name': 'Doorposts - Character Training',
        'type': 'Discipline & Training',
        'description': 'Scripture-based character training tools for families.',
        'url': 'https://www.doorposts.com'
    },
    {
        'name': 'The Well-Trained Mind',
        'type': 'Homeschooling',
        'description': 'Classical education approach for homeschooling families.',
        'url': 'https://www.welltrainedmind.com'
    },
    {
        'name': 'Teaching Textbooks',
        'type': 'Books & Curriculum',
        'description': 'Self-teaching math curriculum with video instruction.',
        'url': 'https://www.teachingtextbooks.com'
    },
    {
        'name': 'Raising Boys and Girls',
        'type': 'Child Development',
        'description': 'Gender-specific parenting guidance from a biblical perspective.',
        'url': 'https://www.raisingboysandgirls.com'
    },
    {
        'name': 'Parenting with Grace',
        'type': 'Parenting Tips',
        'description': 'Catholic perspective on raising children with faith and love.',
        'url': 'https://www.catholiccounseling.com'
    }
]

def create_resource(resource):
    resource_id = f"parenting_{int(time.time() * 1000)}_{resource['type'].replace(' ', '_')}"
    
    payload = {
        'id': resource_id,
        'name': resource['name'],
        'category': ['Parenting', 'Family'],
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
    print("🌱 Seeding parenting resources...\n")
    
    total = len(PARENTING_RESOURCES)
    success = 0
    
    for resource in PARENTING_RESOURCES:
        if create_resource(resource):
            success += 1
        time.sleep(0.2)
    
    print(f"\n\n✅ Seeding complete!")
    print(f"📊 Total: {total} | Success: {success} | Failed: {total - success}")

if __name__ == '__main__':
    print("Starting parenting resource seeding...")
    print(f"This will create {len(PARENTING_RESOURCES)} parenting resources.\n")
    seed_resources()
