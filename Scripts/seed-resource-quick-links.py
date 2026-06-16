"""Seed Quick Links as hub-cards with tab=resources for all 7 mountains."""
import boto3, uuid, sys
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
table = session.resource('dynamodb').Table('hub-cards')

# Common links shared by all mountains (will be customized per mountain)
def common_links(m, label, template_name, prayer_desc, events_desc, upload_desc, pledge_desc):
    return [
        {'title': f'{label} Ministry Template', 'desc': f'Write articles using our {label} Mountain template', 'url': f'create-article.html?template=mountain_{template_name}&mountain={m}'},
        {'title': f'{label} Articles', 'desc': f'Browse all {label.lower()} articles', 'url': f'articles.html?category={m}'},
        {'title': f'{label} Videos', 'desc': f'Watch {label.lower()} videos', 'url': f'videos.html?category={m}'},
        {'title': 'All Ministry Templates', 'desc': 'Browse all 7 Mountains article templates', 'url': 'ministry-templates.html'},
        {'title': 'Prayer Wall', 'desc': prayer_desc, 'url': 'prayer-wall.html'},
        {'title': 'Events Calendar', 'desc': events_desc, 'url': 'events-calendar.html'},
        {'title': 'Upload Content', 'desc': upload_desc, 'url': f'user-upload.html?mountain={m}'},
        {'title': 'Take the Pledge', 'desc': pledge_desc, 'url': 'mountain-pledge.html'},
    ]

mountains = {
    'family': common_links('family', 'Family', 'family',
        'Pray for families and family restoration',
        'Find family conferences and workshops',
        'Share your own family videos',
        'Commit to biblical family values'),
    'religion': common_links('religion', 'Religion', 'religion',
        'Pray for revival and spiritual awakening',
        'Find revival meetings and prayer gatherings',
        'Share your own sermons and teachings',
        'Commit to advancing the Gospel'),
    'education': common_links('education', 'Education', 'education',
        'Pray for education reform and biblical truth in schools',
        'Find school board meetings and education conferences',
        'Share your own education videos',
        'Commit to biblical education'),
    'media': common_links('media', 'Media', 'media',
        'Pray for truth in media and honest journalism',
        'Find media conferences and journalism workshops',
        'Share your own media videos and reports',
        'Commit to truth in media'),
    'art': common_links('art', 'Art & Entertainment', 'art',
        'Pray for Christian artists and cultural transformation',
        'Find film festivals, concerts, and art shows',
        'Share your own creative videos and films',
        'Commit to godly art and entertainment'),
    'economics': [
        {'title': 'Kingdom Entrepreneur Template', 'desc': 'Write articles using our Economics Mountain template', 'url': 'create-article.html?template=mountain_economics&mountain=economics'},
        {'title': 'Economics Articles', 'desc': 'Browse all economics and business articles', 'url': 'articles.html?category=economics'},
        {'title': 'Economics Videos', 'desc': 'Watch economics and business videos', 'url': 'videos.html?category=economics'},
        {'title': 'All Ministry Templates', 'desc': 'Browse all 7 Mountains article templates', 'url': 'ministry-templates.html'},
        {'title': 'Prayer Wall', 'desc': 'Pray for kingdom businesses and economic transformation', 'url': 'prayer-wall.html'},
        {'title': 'Events Calendar', 'desc': 'Find business conferences and economic forums', 'url': 'events-calendar.html'},
        {'title': 'Upload Content', 'desc': 'Share your own economics videos', 'url': 'user-upload.html?mountain=economics'},
        {'title': 'Take the Pledge', 'desc': 'Commit to biblical business practices', 'url': 'mountain-pledge.html'},
    ],
    'government': [
        {'title': '50-State Voter Guides', 'desc': 'Election info and candidate profiles for every state', 'url': 'election-map.html'},
        {'title': 'Government Mountain Template', 'desc': 'Write articles using our Government template', 'url': 'create-article.html?template=mountain_government&mountain=government'},
        {'title': 'Government Articles', 'desc': 'Browse all government and political articles', 'url': 'articles.html?category=government'},
        {'title': 'Government Videos', 'desc': 'Watch political commentary and constitutional content', 'url': 'videos.html?category=government'},
        {'title': 'All Ministry Templates', 'desc': 'Browse all 7 Mountains article templates', 'url': 'ministry-templates.html'},
        {'title': 'Prayer Wall', 'desc': 'Pray for government leaders and righteous policy', 'url': 'prayer-wall.html'},
        {'title': 'Events Calendar', 'desc': 'Find town halls, rallies, and civic events', 'url': 'events-calendar.html'},
        {'title': 'Upload Content', 'desc': 'Share your own political commentary videos', 'url': 'user-upload.html?mountain=government'},
        {'title': 'Take the Pledge', 'desc': 'Commit to biblical citizenship', 'url': 'mountain-pledge.html'},
    ],
}

count = 0
for mountain, links in mountains.items():
    for i, link in enumerate(links):
        item = {
            'mountain': mountain,
            'card_id': str(uuid.uuid4()),
            'tab': 'resources',
            'icon': '',
            'title': link['title'],
            'description': link['desc'],
            'buttons': [{'label': link['title'], 'url': link['url'], 'external': link['url'].startswith('http')}],
            'sort_order': (i + 1) * 10,
        }
        table.put_item(Item=item)
        count += 1
        print(f"  {mountain} #{i+1}: {link['title']}")

print(f"\nDone! Seeded {count} resource cards.")
