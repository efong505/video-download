import sys
sys.stdout.reconfigure(encoding='utf-8')

# Update Family Mountain
with open('family-mountain.html', 'r', encoding='utf-8') as f:
    family = f.read()

# Find and replace the Promote section
start = family.find('<div id="promote" class="tab-content active">')
end = family.find('<div id="expose" class="tab-content">')

new_promote = '''<div id="promote" class="tab-content active">
        <h2>Promote Strong Families</h2>
        <div class="action-grid">
            <div class="action-card">
                <h3>💑 Marriage Resources</h3>
                <p>Discover marriage enrichment programs, counseling services, books, and conferences.</p>
                <a href="marriage-resources.html" class="action-btn">Explore Resources</a>
            </div>
            <div class="action-card">
                <h3>👶 Parenting Hub</h3>
                <p>Access homeschooling resources, parenting tips, child development guidance, and curriculum.</p>
                <a href="parenting-hub.html" class="action-btn">Visit Hub</a>
            </div>
            <div class="action-card">
                <h3>🤱 Pro-Life Resources</h3>
                <p>Find pregnancy centers, adoption agencies, foster care support, and advocacy organizations.</p>
                <a href="pro-life-resources.html" class="action-btn">View Resources</a>
            </div>
            <div class="action-card">
                <h3>📖 Share Family Content</h3>
                <p>Upload articles, videos, and testimonies about biblical family values and parenting wisdom.</p>
                <a href="user-upload.html?mountain=family" class="action-btn">Upload Video</a>
                <a href="create-article.html?template=mountain_family&mountain=family" class="action-btn" style="margin-top:8px;">Write Article</a>
            </div>
            <div class="action-card">
                <h3>🙏 Family Prayer Wall</h3>
                <p>Post prayer requests for families in crisis and pray for others walking through challenges.</p>
                <a href="prayer-wall.html" class="action-btn">Visit Prayer Wall</a>
            </div>
            <div class="action-card">
                <h3>📺 Family Content Library</h3>
                <p>Browse inspiring videos and articles celebrating biblical family values and success stories.</p>
                <a href="videos.html?category=family" class="action-btn">Watch Videos</a>
                <a href="articles.html?category=family" class="action-btn" style="margin-top:8px;">Read Articles</a>
            </div>
        </div>
    </div>

    '''

family = family[:start] + new_promote + family[end:]

with open('family-mountain.html', 'w', encoding='utf-8') as f:
    f.write(family)

print('✅ Updated family-mountain.html')

# Update Religion Mountain
with open('religion-mountain.html', 'r', encoding='utf-8') as f:
    religion = f.read()

start = religion.find('<div id="promote" class="tab-content active">')
end = religion.find('<div id="expose" class="tab-content">')

new_promote = '''<div id="promote" class="tab-content active">
        <h2>Promote the Gospel & Revival</h2>
        <div class="action-grid">
            <div class="action-card">
                <h3>⛪ Church Directory</h3>
                <p>Find Bible-believing churches committed to truth and biblical authority.</p>
                <a href="church-directory.html" class="action-btn">Browse Churches</a>
            </div>
            <div class="action-card">
                <h3>📖 Theological Resources</h3>
                <p>Access doctrine, apologetics, Bible study tools, and theological training.</p>
                <a href="theological-resources.html" class="action-btn">Explore Resources</a>
            </div>
            <div class="action-card">
                <h3>🌍 Missionary Support</h3>
                <p>Discover mission organizations and opportunities to support the Great Commission.</p>
                <a href="missionary-support.html" class="action-btn">View Missions</a>
            </div>
            <div class="action-card">
                <h3>📖 Share Sermons & Teachings</h3>
                <p>Upload powerful sermons, Bible teachings, and testimonies of God's transforming power.</p>
                <a href="user-upload.html?mountain=religion" class="action-btn">Upload Video</a>
                <a href="create-article.html?template=mountain_religion&mountain=religion" class="action-btn" style="margin-top:8px;">Write Article</a>
            </div>
            <div class="action-card">
                <h3>🙏 Prayer Wall</h3>
                <p>Post prayer requests and intercede for revival, awakening, and spiritual breakthrough.</p>
                <a href="prayer-wall.html" class="action-btn">Visit Prayer Wall</a>
            </div>
            <div class="action-card">
                <h3>📺 Spiritual Content</h3>
                <p>Watch inspiring messages, worship sessions, and testimonies of faith and miracles.</p>
                <a href="videos.html?category=religion" class="action-btn">Watch Videos</a>
                <a href="articles.html?category=religion" class="action-btn" style="margin-top:8px;">Read Articles</a>
            </div>
        </div>
    </div>

    '''

religion = religion[:start] + new_promote + religion[end:]

with open('religion-mountain.html', 'w', encoding='utf-8') as f:
    f.write(religion)

print('✅ Updated religion-mountain.html')
