"""Seed Christian conservative podcasts into the resources table."""
import boto3, sys, time
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
table = session.resource('dynamodb').Table('resources-table')

PODCASTS = [
    {"name": "The Ben Shapiro Show", "url": "https://www.dailywire.com/show/the-ben-shapiro-show",
     "description": "Daily political podcast from a conservative, religiously observant perspective. One of the most popular conservative podcasts in America."},
    {"name": "The Matt Walsh Show", "url": "https://www.dailywire.com/show/the-matt-walsh-show",
     "description": "Daily commentary on culture, politics, and faith from a traditional Christian worldview. Known for bold takes on cultural issues."},
    {"name": "Allie Beth Stuckey - Relatable", "url": "https://www.blazetv.com/shows/relatable-w-allie-beth-stuckey",
     "description": "Christian conservative commentary on faith, politics, and culture. Interviews with pastors, authors, and thought leaders."},
    {"name": "The Charlie Kirk Show", "url": "https://www.charliekirk.com/podcasts",
     "description": "Daily podcast covering politics, culture, and faith from a Christian conservative perspective. Founder of Turning Point USA."},
    {"name": "John MacArthur - Grace to You", "url": "https://www.gty.org/library/resources/sermons-library",
     "description": "Bible teaching podcast from pastor John MacArthur. Verse-by-verse exposition and biblical commentary on current issues."},
    {"name": "Focus on the Family Daily Broadcast", "url": "https://www.focusonthefamily.com/episodes/",
     "description": "Daily broadcast covering marriage, parenting, and faith. Practical biblical wisdom for families from Focus on the Family."},
    {"name": "The Eric Metaxas Show", "url": "https://metaxastalk.com",
     "description": "Daily radio show and podcast discussing faith, culture, and politics. Author of Bonhoeffer and other bestselling Christian books."},
    {"name": "Voddie Baucham - Voddie Baucham Ministries", "url": "https://www.voddiebaucham.org/sermons/",
     "description": "Sermons and teaching from pastor and author Voddie Baucham. Strong biblical worldview on family, culture, and social justice."},
    {"name": "The Megyn Kelly Show", "url": "https://www.youtube.com/@MegynKelly",
     "description": "Daily podcast covering news, politics, and culture. Frequently features faith-based discussions and Christian conservative guests."},
    {"name": "Truth for Life - Alistair Begg", "url": "https://www.truthforlife.org/programs/truth-for-life/",
     "description": "Daily Bible teaching from pastor Alistair Begg. Clear, practical exposition of Scripture for everyday Christian living."},
    {"name": "The Babylon Bee Podcast", "url": "https://babylonbee.com/podcast",
     "description": "Comedy podcast from the Christian satire site. Interviews, cultural commentary, and humor from a faith-based perspective."},
    {"name": "Breakpoint with John Stonestreet", "url": "https://www.breakpoint.org/breakpoint-podcast/",
     "description": "Daily worldview commentary from the Colson Center. Analyzes news and culture through a biblical lens."},
    {"name": "The Gospel Coalition Podcast", "url": "https://www.thegospelcoalition.org/podcasts/",
     "description": "Multiple podcast series covering theology, culture, book reviews, and pastoral ministry from a Reformed evangelical perspective."},
    {"name": "Ask Pastor John - Desiring God", "url": "https://www.desiringgod.org/ask-pastor-john",
     "description": "John Piper answers listener questions on theology, Christian living, and cultural issues. Short, focused biblical answers."},
    {"name": "The Briefing - Albert Mohler", "url": "https://albertmohler.com/the-briefing",
     "description": "Daily analysis of news and events from a Christian worldview by the president of Southern Baptist Theological Seminary."},
    {"name": "Louder with Crowder", "url": "https://www.louderwithcrowder.com",
     "description": "Conservative comedy and political commentary. Covers cultural issues, media bias, and faith from a Christian conservative angle."},
    {"name": "The Rubin Report", "url": "https://rubinreport.com",
     "description": "Long-form interviews and commentary on free speech, politics, and culture. Features many Christian conservative voices."},
    {"name": "Wretched Radio - Todd Friel", "url": "https://www.wretched.org",
     "description": "Daily Christian radio show and podcast. Apologetics, theology, and cultural commentary with humor and biblical depth."},
    {"name": "Stand to Reason - Greg Koukl", "url": "https://www.str.org/podcast",
     "description": "Christian apologetics podcast teaching believers to think clearly about their faith and engage culture with confidence."},
    {"name": "The Sean McDowell Podcast", "url": "https://seanmcdowell.org/podcast",
     "description": "Apologetics and worldview podcast. Interviews with scholars, authors, and thought leaders on defending the Christian faith."},
]

if __name__ == '__main__':
    ts = str(int(time.time() * 1000))
    ok = 0
    for i, p in enumerate(PODCASTS):
        rid = f"podcast_{ts}_{i}"
        try:
            table.put_item(Item={
                'resource_id': rid,
                'name': p['name'],
                'category': ['Podcasts'],
                'url': p['url'],
                'description': p['description']
            })
            print(f"  OK: {p['name']}")
            ok += 1
        except Exception as e:
            print(f"  FAIL: {p['name']} - {e}")

    print(f"\nDone: {ok}/{len(PODCASTS)} podcasts added.")
