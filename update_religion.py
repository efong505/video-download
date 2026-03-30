import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('religion-mountain.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_section = '''            <div class="action-card">
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
                <h3>⛪ Ministry Resources</h3>
                <p>Access sermon outlines, small group materials, and evangelism tools for your ministry.</p>
                <a href="create-article.html?template=mountain_religion&mountain=religion" class="action-btn">Use Template</a>
            </div>
            <div class="action-card">
                <h3>📺 Spiritual Content</h3>
                <p>Watch inspiring messages, worship sessions, and testimonies of faith and miracles.</p>
                <a href="videos.html?category=religion" class="action-btn">Watch Videos</a>
                <a href="articles.html?category=religion" class="action-btn" style="margin-top:8px;">Read Articles</a>
            </div>'''

new_section = '''            <div class="action-card">
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
            </div>'''

content = content.replace(old_section, new_section)

with open('religion-mountain.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated religion-mountain.html with specialized page links')
