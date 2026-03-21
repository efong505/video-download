// Mountain Hub Featured Content Loader
// Usage: Call loadMountainContent('category-name') on page load

async function loadMountainContent(mountainCategory) {
    // Load latest articles
    try {
        const articlesResponse = await fetch('https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/articles?action=get_all_articles');
        const articlesData = await articlesResponse.json();
        const articles = articlesData.articles || [];
        
        // Filter by mountain category and get latest 3
        const mountainArticles = articles
            .filter(a => a.category === mountainCategory)
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .slice(0, 3);
        
        const articlesContainer = document.getElementById('featured-articles');
        if (mountainArticles.length > 0) {
            articlesContainer.innerHTML = mountainArticles.map(article => `
                <div class="col-md-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${article.title}</h5>
                            <p class="card-text text-muted small">By ${article.author || 'Anonymous'} • ${new Date(article.created_at).toLocaleDateString()}</p>
                            <a href="article.html?id=${article.article_id}" class="btn btn-sm" style="background: var(--mountain-primary); color: white;">Read More</a>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            articlesContainer.innerHTML = '<div class="col-12"><p class="text-center text-muted">No articles yet. <a href="create-article.html">Be the first to contribute!</a></p></div>';
        }
    } catch (error) {
        console.error('Error loading articles:', error);
        document.getElementById('featured-articles').innerHTML = '<div class="col-12"><p class="text-center text-danger">Error loading articles</p></div>';
    }

    // Load featured videos
    try {
        const videosResponse = await fetch('https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/videos?action=list_videos');
        const videosData = await videosResponse.json();
        const videos = videosData.videos || [];
        
        // Filter by mountain category and get latest 3
        const mountainVideos = videos
            .filter(v => v.category === mountainCategory)
            .slice(0, 3);
        
        const videosContainer = document.getElementById('featured-videos');
        if (mountainVideos.length > 0) {
            videosContainer.innerHTML = mountainVideos.map(video => `
                <div class="col-md-4">
                    <div class="card h-100 shadow-sm">
                        <img src="${video.thumbnail_url || 'https://via.placeholder.com/300x200?text=Video'}" class="card-img-top" alt="${video.title}" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">${video.title}</h5>
                            <a href="videos.html?id=${video.video_id}" class="btn btn-sm" style="background: var(--mountain-primary); color: white;">Watch Now</a>
                        </div>
                    </div>
                </div>
            `).join('');
        } else {
            videosContainer.innerHTML = '<div class="col-12"><p class="text-center text-muted">No videos yet. <a href="user-upload.html">Upload the first video!</a></p></div>';
        }
    } catch (error) {
        console.error('Error loading videos:', error);
        document.getElementById('featured-videos').innerHTML = '<div class="col-12"><p class="text-center text-danger">Error loading videos</p></div>';
    }
}
