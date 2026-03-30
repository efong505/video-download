import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('family-mountain.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_section = '''            <div class="action-card">
                <h3>📖 Share Family Resources</h3>
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
                <h3>👨👩👧👦 Family Ministry Templates</h3>
                <p>Access ready-to-use templates for family ministry articles — marriage, parenting, and more.</p>
                <a href="create-article.html?template=mountain_family&mountain=family" class="action-btn">Use Template</a>
            </div>
            <div class="action-card">
                <h3>📺 Family Content Library</h3>
                <p>Browse inspiring videos and articles celebrating biblical family values and success stories.</p>
                <a href="videos.html?category=family" class="action-btn">Watch Videos</a>
                <a href="articles.html?category=family" class="action-btn" style="margin-top:8px;">Read Articles</a>
            </div>'''

new_section = '''            <div class="action-card">
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
            </div>'''

content = content.replace(old_section, new_section)

with open('family-mountain.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Updated family-mountain.html with specialized page links')
