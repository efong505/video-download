"""Seed all 7 mountain hub cards into DynamoDB hub-cards table."""
import boto3, uuid, sys
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
table = session.resource('dynamodb').Table('hub-cards')

def card(mountain, tab, sort_order, icon, title, description, buttons):
    return {
        'mountain': mountain, 'card_id': str(uuid.uuid4()), 'tab': tab,
        'sort_order': sort_order, 'icon': icon, 'title': title,
        'description': description, 'buttons': buttons,
        'updated_at': datetime.now().isoformat()
    }

def btn(label, url, external=False):
    return {'label': label, 'url': url, 'external': external}

CARDS = [
    # ── FAMILY ──────────────────────────────────────────────────────────────
    card('family','promote',0,'📖','Share Family Resources','Upload articles, videos, and testimonies about biblical family values and parenting wisdom.',[btn('Upload Video','user-upload.html?mountain=family'),btn('Write Article','create-article.html?template=mountain_family&mountain=family')]),
    card('family','promote',1,'🙏','Family Prayer Wall','Post prayer requests for families in crisis and pray for others walking through challenges.',[btn('Visit Prayer Wall','prayer-wall.html')]),
    card('family','promote',2,'👨‍👩‍👧‍👦','Family Ministry Templates','Access ready-to-use templates for family ministry articles — marriage, parenting, and more.',[btn('Use Template','create-article.html?template=mountain_family&mountain=family')]),
    card('family','promote',3,'📺','Family Content Library','Browse inspiring videos and articles celebrating biblical family values and success stories.',[btn('Watch Videos','videos.html?category=family'),btn('Read Articles','articles.html?category=family')]),
    card('family','expose',0,'🚨','Report Anti-Family Policies','Document and expose legislation, school policies, and cultural trends undermining families.',[btn('Upload Video Report','user-upload.html?mountain=family'),btn('Write Report','create-article.html?template=mountain_family&mountain=family')]),
    card('family','expose',1,'📰','Family News & Alerts','Stay informed about threats to parental rights, religious freedom, and family values.',[btn('Read Articles','articles.html?category=family')]),
    card('family','expose',2,'⚖️','Legal Resources','Legal organizations defending parental rights and family freedoms.',[btn('Alliance Defending Freedom','https://adflegal.org',True),btn('First Liberty Institute','https://firstliberty.org',True),btn('Liberty Counsel','https://lc.org',True),btn('HSLDA (Parental Rights)','https://hslda.org',True)]),
    card('family','expose',3,'🎯','Action Campaigns','Join coordinated efforts to oppose anti-family legislation and cultural attacks.',[btn('View Campaigns','events-calendar.html')]),
    card('family','involved',0,'✍️','Take the Family Pledge','Commit to biblical family values and join thousands standing for marriage and parenting.',[btn('Take Pledge','mountain-pledge.html')]),
    card('family','involved',1,'📅','Family Events','Find marriage conferences, parenting workshops, and family ministry events near you.',[btn('Find Events','events-calendar.html')]),
    card('family','involved',2,'🤝','Start a Family Group','Launch a small group focused on marriage enrichment, parenting support, or family discipleship.',[btn('Use Template','create-article.html?template=mountain_family&mountain=family')]),
    card('family','involved',3,'💬','Family Forums','Connect with other believers navigating family challenges and celebrating victories.',[btn('Join Discussion','forum.html?mountain=family')]),

    # ── RELIGION ────────────────────────────────────────────────────────────
    card('religion','promote',0,'📖','Share Sermons & Teachings','Upload powerful sermons, Bible teachings, and testimonies of God\'s transforming power.',[btn('Upload Video','user-upload.html?mountain=religion'),btn('Write Article','create-article.html?template=mountain_religion&mountain=religion')]),
    card('religion','promote',1,'🙏','Prayer Wall','Post prayer requests and intercede for revival, awakening, and spiritual breakthrough.',[btn('Visit Prayer Wall','prayer-wall.html')]),
    card('religion','promote',2,'⛪','Ministry Resources','Access sermon outlines, small group materials, and evangelism tools for your ministry.',[btn('Use Template','create-article.html?template=mountain_religion&mountain=religion')]),
    card('religion','promote',3,'📺','Spiritual Content','Watch inspiring messages, worship sessions, and testimonies of faith and miracles.',[btn('Watch Videos','videos.html?category=religion'),btn('Read Articles','articles.html?category=religion')]),
    card('religion','expose',0,'🚨','Report Religious Persecution','Document cases of religious discrimination, church closures, and attacks on believers.',[btn('Upload Video Report','user-upload.html?mountain=religion'),btn('Write Report','create-article.html?template=mountain_religion&mountain=religion')]),
    card('religion','expose',1,'📰','Religious Freedom News','Stay informed about threats to religious liberty and church freedoms worldwide.',[btn('Read Articles','articles.html?category=religion'),btn('Becket Fund News','https://www.becketlaw.org/media/',True),btn('First Liberty News','https://firstliberty.org/news/',True)]),
    card('religion','expose',2,'⚖️','Legal Defense','Legal organizations defending churches, pastors, and religious freedom rights.',[btn('Alliance Defending Freedom','https://adflegal.org',True),btn('First Liberty Institute','https://firstliberty.org',True),btn('Liberty Counsel','https://lc.org',True),btn('Becket Fund','https://www.becketlaw.org',True)]),
    card('religion','expose',3,'🎯','Spiritual Warfare','Join prayer campaigns against spiritual darkness and demonic strongholds in culture.',[btn('Join Prayer','prayer-wall.html')]),
    card('religion','involved',0,'✍️','Take the Faith Pledge','Commit to bold faith, evangelism, and standing firm for biblical truth in every sphere.',[btn('Take Pledge','mountain-pledge.html')]),
    card('religion','involved',1,'📅','Revival Events','Find prayer gatherings, revival meetings, and evangelistic events in your area.',[btn('Find Events','events-calendar.html')]),
    card('religion','involved',2,'🤝','Start a Prayer Group','Launch an intercessory prayer group focused on revival and cultural transformation.',[btn('Use Template','create-article.html?template=mountain_religion&mountain=religion')]),
    card('religion','involved',3,'💬','Theology Forums','Engage in biblical discussions and theological training with fellow believers.',[btn('Join Discussion','forum.html?mountain=religion')]),

    # ── EDUCATION ───────────────────────────────────────────────────────────
    card('education','promote',0,'📚','Share Educational Content','Upload curriculum, teaching resources, and success stories from Christian education.',[btn('Upload Video','user-upload.html?mountain=education'),btn('Write Article','create-article.html?template=mountain_education&mountain=education')]),
    card('education','promote',1,'🏫','Homeschool Resources','Access biblical curriculum, lesson plans, and homeschooling support materials.',[btn('Get Resources','resources.html?category=education')]),
    card('education','promote',2,'🎓','Christian Schools Directory','Find and promote Christian schools, classical academies, and faith-based education.',[btn('Find Schools','business-directory.html?category=Christian Schools'),btn('School Resources','business-directory.html?category=Christian School Resources')]),
    card('education','promote',3,'📺','Educational Videos','Watch teaching videos on biblical worldview, history, science, and critical thinking.',[btn('Watch Videos','videos.html?category=education')]),
    card('education','expose',0,'🚨','Report Indoctrination','Document CRT, gender ideology, and anti-Christian bias in schools and universities.',[btn('Report & Discuss','forum.html?mountain=education'),btn('Upload Video Report','user-upload.html?mountain=education'),btn('Write Report','create-article.html?template=mountain_education&mountain=education')]),
    card('education','expose',1,'📰','Education News','Stay informed about curriculum battles, school board issues, and parental rights.',[btn('Read Articles','articles.html?category=education')]),
    card('education','expose',2,'📋','Review School Policies','Analyze and expose problematic school policies, textbooks, and teaching materials.',[btn('Discuss Policies','forum.html?mountain=education'),btn('Read Policy Articles','articles.html?category=education')]),
    card('education','expose',3,'🎯','School Board Campaigns','Support conservative school board candidates and parental rights initiatives.',[btn('View Campaigns','events-calendar.html')]),
    card('education','involved',0,'✍️','Take the Education Pledge','Commit to biblical education and protecting children from secular indoctrination.',[btn('Take Pledge','mountain-pledge.html')]),
    card('education','involved',1,'🚀','Write About Education','Use our Education Mountain template to write about biblical education principles.',[btn('Use Template','create-article.html?template=mountain_education&mountain=education')]),
    card('education','involved',2,'📅','Education Events','Attend school board meetings, parent rallies, and education reform conferences.',[btn('Find Events','events-calendar.html')]),
    card('education','involved',3,'💬','Parent Forums','Connect with parents fighting for educational freedom and biblical values.',[btn('Join Discussion','forum.html?mountain=education')]),

    # ── MEDIA ───────────────────────────────────────────────────────────────
    card('media','promote',0,'📰','Share News & Articles','Upload articles, investigative reports, and truthful journalism from a biblical perspective.',[btn('Upload Video','user-upload.html?mountain=media'),btn('Write Article','create-article.html?template=mountain_media&mountain=media')]),
    card('media','promote',1,'📺','Video Journalism','Create and share video reports, interviews, and documentary content exposing truth.',[btn('Watch Videos','videos.html?category=media')]),
    card('media','promote',2,'🎙️','Podcast Directory','Discover and promote Christian conservative podcasts and audio content.',[btn('Find Podcasts','resources.html?category=Podcasts')]),
    card('media','promote',3,'📱','Social Media Toolkit','Get hashtags, content tips, design tools, and platform guides to spread truth on social media.',[btn('Get Toolkit','social-media-toolkit.html')]),
    card('media','expose',0,'🚨','Report Fake News','Document mainstream media lies, propaganda, and censorship of conservative voices.',[btn('Upload Video Report','user-upload.html?mountain=media'),btn('Write Report','create-article.html?template=mountain_media&mountain=media')]),
    card('media','expose',1,'🔍','Fact-Check Database','Access fact-checks debunking liberal media narratives and false reporting.',[btn('View Fact-Checks','fact-check.html')]),
    card('media','expose',2,'📊','Media Bias Tracker','Track and expose bias in major news outlets, journalists, and media companies.',[btn('Report & Discuss Bias','forum.html?mountain=media'),btn('Read Articles','articles.html?category=media')]),
    card('media','expose',3,'🎯','Counter-Narrative Campaigns','Join coordinated efforts to challenge false narratives with truth and evidence.',[btn('Join Campaigns','forum.html?mountain=media'),btn('Get Toolkit','social-media-toolkit.html')]),
    card('media','involved',0,'✍️','Take the Media Pledge','Commit to sharing truth, boycotting fake news, and supporting honest journalism.',[btn('Take Pledge','mountain-pledge.html')]),
    card('media','involved',1,'🚀','Become a Citizen Journalist','Use our Media Mountain template to write about truth in media and journalism.',[btn('Use Template','create-article.html?template=mountain_media&mountain=media')]),
    card('media','involved',2,'📅','Media Events','Attend journalism workshops, media conferences, and content creator meetups.',[btn('Find Events','events-calendar.html')]),
    card('media','involved',3,'💬','Media Forums','Connect with Christian journalists, content creators, and media professionals.',[btn('Join Discussion','forum.html?mountain=media')]),

    # ── ART ─────────────────────────────────────────────────────────────────
    card('art','promote',0,'🎬','Share Christian Films','Upload and promote faith-based movies, documentaries, and video content.',[btn('Upload Video','user-upload.html?mountain=art'),btn('Write Article','create-article.html?template=mountain_art&mountain=art')]),
    card('art','promote',1,'🎵','Christian Music','Discover and share worship music, Christian artists, and faith-inspired songs.',[btn('Explore Music','videos.html?category=art')]),
    card('art','promote',2,'🎨','Visual Arts Gallery','Showcase Christian art, photography, and creative works that honor God.',[btn('View Gallery','videos.html?category=art')]),
    card('art','promote',3,'📚','Christian Literature','Promote books, poetry, and written works from a biblical worldview.',[btn('Read More','articles.html?category=art')]),
    card('art','expose',0,'🚨','Report Immoral Content','Document Hollywood\'s promotion of immorality, blasphemy, and anti-Christian themes.',[btn('Upload Video Report','user-upload.html?mountain=art'),btn('Write Report','create-article.html?template=mountain_art&mountain=art')]),
    card('art','expose',1,'🎭','Entertainment Reviews','Read biblical reviews of movies, TV shows, music, and entertainment content.',[btn('Read Reviews','articles.html?category=art')]),
    card('art','expose',2,'💰','Boycott Tracker','Track companies and entertainers promoting anti-Christian values and immorality.',[btn('View Boycotts','boycott-tracker.html')]),
    card('art','expose',3,'🎯','Cultural Campaigns','Join efforts to oppose blasphemous content and support family-friendly entertainment.',[btn('View Campaigns','events-calendar.html')]),
    card('art','involved',0,'✍️','Take the Arts Pledge','Commit to creating and supporting art that glorifies God and promotes truth.',[btn('Take Pledge','mountain-pledge.html')]),
    card('art','involved',1,'🚀','Become a Creator','Use our Art Mountain template to write about Christian creativity and culture.',[btn('Use Template','create-article.html?template=mountain_art&mountain=art')]),
    card('art','involved',2,'📅','Arts Events','Find film festivals, concerts, art shows, and creative conferences near you.',[btn('Find Events','events-calendar.html')]),
    card('art','involved',3,'💬','Artist Forums','Connect with Christian filmmakers, musicians, writers, and visual artists.',[btn('Join Discussion','forum.html?mountain=art')]),

    # ── ECONOMICS ───────────────────────────────────────────────────────────
    card('economics','promote',0,'💼','Christian Business Directory','Find and promote Christian-owned businesses and faith-based entrepreneurs.',[btn('Browse Businesses','business-directory.html')]),
    card('economics','promote',1,'📊','Share Economic Content','Share articles and videos on biblical economics, free markets, and financial wisdom.',[btn('Upload Video','user-upload.html?mountain=economics'),btn('Write Article','create-article.html?template=mountain_economics&mountain=economics')]),
    card('economics','promote',2,'🤝','Kingdom Partnerships','Connect Christian businesses for collaboration, networking, and mutual support.',[btn('Discuss Partnerships','forum.html?mountain=economics')]),
    card('economics','promote',3,'💰','Financial Stewardship','Access biblical teaching on money management, investing, and generosity.',[btn('Watch Videos','videos.html?category=economics')]),
    card('economics','expose',0,'🚨','Report Corporate Wokeness','Document companies pushing ESG, DEI, and anti-Christian corporate policies.',[btn('Upload Video Report','user-upload.html?mountain=economics'),btn('Write Report','create-article.html?template=mountain_economics&mountain=economics')]),
    card('economics','expose',1,'📰','Economic News','Stay informed about socialist policies, economic tyranny, and market manipulation.',[btn('Read Articles','articles.html?category=economics')]),
    card('economics','expose',2,'💳','Boycott Tracker','Track and boycott companies discriminating against Christians and conservatives.',[btn('View Boycotts','boycott-tracker.html')]),
    card('economics','expose',3,'🎯','Economic Campaigns','Join efforts to oppose socialist legislation and promote free market principles.',[btn('View Campaigns','events-calendar.html')]),
    card('economics','involved',0,'✍️','Take the Business Pledge','Commit to biblical business practices and supporting Christian entrepreneurs.',[btn('Take Pledge','mountain-pledge.html')]),
    card('economics','involved',1,'🚀','Start a Kingdom Business','Use our Economics Mountain template to write about biblical business principles.',[btn('Use Template','create-article.html?template=mountain_economics&mountain=economics')]),
    card('economics','involved',2,'📅','Business Events','Attend Christian business conferences, networking events, and economic forums.',[btn('Find Events','events-calendar.html')]),
    card('economics','involved',3,'💬','Entrepreneur Forums','Connect with Christian business owners, investors, and economic leaders.',[btn('Join Discussion','forum.html?mountain=economics')]),

    # ── GOVERNMENT ──────────────────────────────────────────────────────────
    card('government','promote',0,'📊','50-State Voter Guides','Access comprehensive election information and candidate profiles for all 50 states.',[btn('View Voter Guides','election-map.html')]),
    card('government','promote',1,'📰','Political Commentary','Share biblical analysis of current government issues and political developments.',[btn('Upload Video','user-upload.html?mountain=government'),btn('Write Article','create-article.html?template=mountain_government&mountain=government')]),
    card('government','promote',2,'🎓','Patriot Academy','Constitutional training and civic education for engaged citizens and leaders.',[btn('Visit Patriot Academy','https://www.patriotacademy.com',True)]),
    card('government','promote',3,'📚','Founding Documents','Study the Constitution, Declaration of Independence, and America\'s biblical heritage.',[btn('Read at National Archives','https://www.archives.gov/founding-docs',True)]),
    card('government','expose',0,'🚨','Report Corruption','Document political corruption, constitutional violations, and government overreach.',[btn('Upload Video Report','user-upload.html?mountain=government'),btn('Write Report','create-article.html?template=mountain_government&mountain=government')]),
    card('government','expose',1,'📰','Political News','Stay informed about tyrannical policies and threats to constitutional freedoms.',[btn('Read Articles','articles.html?category=government')]),
    card('government','expose',2,'⚖️','Legal Action','Christian legal organizations defending constitutional rights and religious freedom.',[btn('Liberty Counsel','https://lc.org',True),btn('Alliance Defending Freedom','https://adflegal.org',True),btn('First Liberty Institute','https://firstliberty.org',True),btn('ACLJ','https://aclj.org',True),btn('Thomas More Law Center','https://thomasmore.org',True)]),
    card('government','expose',3,'🔍','Fact-Check Politicians','Verify claims made by politicians and hold leaders accountable with evidence.',[btn('View Fact-Checks','fact-check.html')]),
    card('government','involved',0,'✍️','Take the Government Pledge','Commit to biblical citizenship and defending constitutional principles.',[btn('Take Pledge','mountain-pledge.html')]),
    card('government','involved',1,'🚀','Write About Government','Use our Government Mountain template to write about constitutional principles.',[btn('Use Template','create-article.html?template=mountain_government&mountain=government')]),
    card('government','involved',2,'📅','Political Events','Attend town halls, candidate forums, and civic engagement training events.',[btn('Find Events','events-calendar.html')]),
    card('government','involved',3,'💬','Government Forums','Discuss policy, elections, and constitutional issues with fellow patriots.',[btn('Join Discussion','forum.html?mountain=government')]),
]

if __name__ == '__main__':
    ok = 0
    for c in CARDS:
        try:
            table.put_item(Item=c)
            ok += 1
        except Exception as e:
            print(f"  FAIL: {c['mountain']}/{c['tab']}/{c['title']} - {e}")
    print(f"Done: {ok}/{len(CARDS)} cards seeded across 7 mountains.")
