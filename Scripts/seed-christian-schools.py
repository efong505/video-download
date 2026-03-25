"""Seed Christian Schools and Resources directly into DynamoDB."""
import boto3, uuid, sys, json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
table = session.resource('dynamodb').Table('business-directory')

OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

LISTINGS = [
    # === Christian Schools ===
    {"name": "Liberty University", "category": "Christian Schools", "website": "https://www.liberty.edu", "city": "Lynchburg", "state": "Virginia",
     "description": "Largest Christian university in the world. Offers 700+ programs of study from certificate to doctoral level, online and residential."},
    {"name": "Grand Canyon University", "category": "Christian Schools", "website": "https://www.gcu.edu", "city": "Phoenix", "state": "Arizona",
     "description": "Private Christian university offering over 300 academic programs. Integrates faith into every aspect of the educational experience."},
    {"name": "Biola University", "category": "Christian Schools", "website": "https://www.biola.edu", "city": "La Mirada", "state": "California",
     "description": "Nationally ranked private evangelical Christian university. Known for biblical integration across all programs."},
    {"name": "Wheaton College", "category": "Christian Schools", "website": "https://www.wheaton.edu", "city": "Wheaton", "state": "Illinois",
     "description": "Premier evangelical liberal arts college. Consistently ranked among the top Christian colleges in America."},
    {"name": "Hillsdale College", "category": "Christian Schools", "website": "https://www.hillsdale.edu", "city": "Hillsdale", "state": "Michigan",
     "description": "Private conservative liberal arts college. Refuses federal funding to maintain independence. Strong classical education focus."},
    {"name": "Cedarville University", "category": "Christian Schools", "website": "https://www.cedarville.edu", "city": "Cedarville", "state": "Ohio",
     "description": "Baptist university offering over 175 programs. Known for academic excellence and intentional discipleship."},
    {"name": "Patrick Henry College", "category": "Christian Schools", "website": "https://www.phc.edu", "city": "Purcellville", "state": "Virginia",
     "description": "Classical liberal arts college for Christian students. Strong focus on government, journalism, and strategic intelligence."},
    {"name": "Bob Jones University", "category": "Christian Schools", "website": "https://www.bju.edu", "city": "Greenville", "state": "South Carolina",
     "description": "Christian liberal arts university offering undergraduate and graduate programs with a biblical worldview foundation."},
    {"name": "Regent University", "category": "Christian Schools", "website": "https://www.regent.edu", "city": "Virginia Beach", "state": "Virginia",
     "description": "Christian university founded by Pat Robertson. Offers programs in law, business, education, communication, and divinity."},
    {"name": "Oral Roberts University", "category": "Christian Schools", "website": "https://www.oru.edu", "city": "Tulsa", "state": "Oklahoma",
     "description": "Spirit-empowered Christian university. Educates students in mind, body, and spirit with a charismatic Christian foundation."},
    {"name": "Pensacola Christian College", "category": "Christian Schools", "website": "https://www.pcci.edu", "city": "Pensacola", "state": "Florida",
     "description": "Independent Baptist college offering over 70 undergraduate and 10 graduate programs in a conservative Christian environment."},
    {"name": "The Master's University", "category": "Christian Schools", "website": "https://www.masters.edu", "city": "Santa Clarita", "state": "California",
     "description": "Christian liberal arts university led by John MacArthur. Committed to biblical inerrancy and academic rigor."},
    {"name": "Covenant College", "category": "Christian Schools", "website": "https://www.covenant.edu", "city": "Lookout Mountain", "state": "Georgia",
     "description": "Liberal arts college of the Presbyterian Church in America. Located on Lookout Mountain with a Reformed worldview."},
    {"name": "Moody Bible Institute", "category": "Christian Schools", "website": "https://www.moody.edu", "city": "Chicago", "state": "Illinois",
     "description": "Evangelical institution focused on Bible education, ministry training, and media. Tuition-paid undergraduate education."},
    {"name": "Dallas Baptist University", "category": "Christian Schools", "website": "https://www.dbu.edu", "city": "Dallas", "state": "Texas",
     "description": "Christ-centered university integrating faith and learning. Offers over 90 undergraduate and 30 graduate programs."},

    # === Christian School Resources ===
    {"name": "Association of Christian Schools International (ACSI)", "category": "Christian School Resources", "website": "https://www.acsi.org",
     "description": "Largest Protestant educational organization worldwide. Provides accreditation, curriculum support, teacher certification, and professional development for Christian schools."},
    {"name": "Classical Conversations", "category": "Christian School Resources", "website": "https://www.classicalconversations.com",
     "description": "Classical Christian education community. Provides curriculum, training, and local community groups for homeschool and Christian school families."},
    {"name": "BJU Press", "category": "Christian School Resources", "website": "https://www.bjupress.com",
     "description": "Christian educational publisher offering textbooks, curriculum, and distance learning for Christian schools and homeschools. K-12 materials."},
    {"name": "Abeka", "category": "Christian School Resources", "website": "https://www.abeka.com",
     "description": "Christian curriculum and textbook publisher for PreK-12. Offers video streaming classes, homeschool curriculum, and Christian school materials."},
    {"name": "Answers in Genesis", "category": "Christian School Resources", "website": "https://answersingenesis.org",
     "description": "Apologetics ministry providing creation-based science curriculum, worldview training, and educational resources for Christian schools and families."},
    {"name": "Summit Ministries", "category": "Christian School Resources", "website": "https://www.summit.org",
     "description": "Christian worldview training for students. Offers curriculum, conferences, and summer programs to equip young Christians to think biblically."},
    {"name": "Veritas Press", "category": "Christian School Resources", "website": "https://www.veritaspress.com",
     "description": "Classical Christian education publisher. Offers self-paced online courses, curriculum, and resources for Christian schools and homeschools."},
    {"name": "Christian Schools International (CSI)", "category": "Christian School Resources", "website": "https://www.csionline.org",
     "description": "Network supporting Christian schools with professional development, school improvement services, and advocacy for Christian education."},
    {"name": "The Gospel Coalition - Education Resources", "category": "Christian School Resources", "website": "https://www.thegospelcoalition.org/topics/education",
     "description": "Theological resources and articles on Christian education, schooling choices, and integrating faith with learning."},
    {"name": "Focus on the Family - Education", "category": "Christian School Resources", "website": "https://www.focusonthefamily.com/parenting/education",
     "description": "Resources for Christian parents on education choices including Christian schools, homeschooling, and navigating public school as a Christian family."},

    # === Homeschool Resources ===
    {"name": "Home School Legal Defense Association (HSLDA)", "category": "Christian School Resources", "website": "https://hslda.org",
     "description": "Legal advocacy organization for homeschool families. Provides legal defense, legislative advocacy, and resources for homeschooling parents nationwide."},
    {"name": "Sonlight Curriculum", "category": "Christian School Resources", "website": "https://www.sonlight.com",
     "description": "Literature-based Christian homeschool curriculum. Complete packages from preschool through high school with a missions-minded worldview."},
    {"name": "My Father's World", "category": "Christian School Resources", "website": "https://www.mfwbooks.com",
     "description": "Christian homeschool curriculum combining Charlotte Mason, classical education, and unit studies. PreK through high school programs."},
    {"name": "The Good and the Beautiful", "category": "Christian School Resources", "website": "https://www.goodandbeautiful.com",
     "description": "Family-centered homeschool curriculum with free and affordable options. Language arts, math, science, and history with wholesome content."},
    {"name": "Apologia Educational Ministries", "category": "Christian School Resources", "website": "https://www.apologia.com",
     "description": "Award-winning Christian homeschool science and worldview curriculum. Known for conversational writing style and creation-based science."},
    {"name": "Teaching Textbooks", "category": "Christian School Resources", "website": "https://www.teachingtextbooks.com",
     "description": "Self-teaching math curriculum popular with Christian homeschool families. Interactive lessons with automated grading for grades 3-12."},
    {"name": "Easy Peasy All-in-One Homeschool", "category": "Christian School Resources", "website": "https://allinonehomeschool.com",
     "description": "Completely free Christian homeschool curriculum for all grades. Bible-based with daily lesson plans covering all core subjects."},
    {"name": "Memoria Press", "category": "Christian School Resources", "website": "https://www.memoriapress.com",
     "description": "Classical Christian curriculum publisher. Latin-centered education with structured programs for homeschool and Christian school use."},
    {"name": "Alpha Omega Publications", "category": "Christian School Resources", "website": "https://www.aop.com",
     "description": "Christian homeschool curriculum provider offering Monarch (online), Switched-On Schoolhouse (computer-based), and LIFEPAC (workbook) formats."},
]

if __name__ == '__main__':
    now = datetime.now().isoformat()
    ok = 0
    for l in LISTINGS:
        item = {
            'business_id': str(uuid.uuid4()),
            'name': l['name'],
            'category': l['category'],
            'website': l.get('website', ''),
            'description': l.get('description', ''),
            'city': l.get('city', ''),
            'state': l.get('state', ''),
            'phone': l.get('phone', ''),
            'email': l.get('email', ''),
            'submitted_by': OWNER_ID,
            'created_at': now,
            'status': 'approved',
            'featured': False
        }
        try:
            table.put_item(Item=item)
            print(f"  OK: {l['name']}")
            ok += 1
        except Exception as e:
            print(f"  FAIL: {l['name']} - {e}")

    print(f"\nDone: {ok}/{len(LISTINGS)} listings added.")
