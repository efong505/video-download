// Unified Navbar Script - Call initNavbar() after loading navbar.html
function initNavbar() {
    const container = document.getElementById('navbar-container');
    if (!container) return;
    
    const currentPage = container.dataset.page || 'index';
    const pageIcon = container.dataset.icon || '';
    const iconStyle = container.dataset.iconStyle || 'emoji';
    
    const allLinks = [
        {page: 'videos', label: 'Videos', emoji: '🎥', fa: 'fa-video', public: true},
        {page: 'articles', label: 'Articles', emoji: '📖', fa: 'fa-book', public: true},
        {page: 'news', label: 'News', emoji: '📰', fa: 'fa-newspaper', public: true},
        {page: 'election-map', label: 'Election Map', emoji: '🗺️', fa: 'fa-map', public: true},
        {page: 'prayer-wall', label: 'Prayer', emoji: '🙏', fa: 'fa-praying-hands', public: true},
        {page: 'events-calendar', label: 'Events', emoji: '📅', fa: 'fa-calendar', public: true},
        {page: 'subscribe', label: 'Subscribe', emoji: '📧', fa: 'fa-envelope', public: true},
        {page: 'resources', label: 'Resources', emoji: '📚', fa: 'fa-book-open', public: true},
        {page: 'authors', label: 'Authors', emoji: '👥', fa: 'fa-users', adminOnly: true},
        {page: 'user-upload', label: 'Upload Video', emoji: '⬆️', fa: 'fa-upload', adminOnly: true},
        {page: 'admin-contributors', label: 'Contributors', emoji: '🗺️', fa: 'fa-map-marked', adminOnly: true},
        {page: 'admin-resources', label: 'Manage Resources', emoji: '📚', fa: 'fa-tasks', adminOnly: true},
        {page: 'admin-templates', label: 'Templates', emoji: '📄', fa: 'fa-file-alt', adminOnly: true}
    ];
    
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    const user = userData ? JSON.parse(userData) : null;
    const isLoggedIn = !!token && !!user;
    
    // Update brand if page-specific
    if (pageIcon) {
        document.getElementById('navbar-logo').style.display = 'none';
        document.getElementById('navbar-title').textContent = pageIcon + ' ' + (allLinks.find(l => l.page === currentPage)?.label || '');
    }
    
    // Build nav links
    const navLinks = document.getElementById('nav-links');
    let html = '';
    
    allLinks.forEach(link => {
        if (link.page === currentPage) return;
        if (!isLoggedIn && !link.public) return;
        
        // Skip admin-only links - they're in secondary menu on admin page
        if (link.adminOnly) return;
        
        const icon = iconStyle === 'fontawesome' ? `<i class="fas ${link.fa} me-1"></i>` : link.emoji + ' ';
        html += `<li class="nav-item"><a class="nav-link" href="${link.page}.html">${icon}${link.label}</a></li>`;
    });
    
    // Add Upload Video link only on videos page for logged-in users
    if (currentPage === 'videos' && isLoggedIn) {
        const uploadLink = allLinks.find(l => l.page === 'user-upload');
        if (uploadLink) {
            const icon = iconStyle === 'fontawesome' ? `<i class="fas ${uploadLink.fa} me-1"></i>` : uploadLink.emoji + ' ';
            html += `<li class="nav-item"><a class="nav-link" href="${uploadLink.page}.html">${icon}${uploadLink.label}</a></li>`;
        }
    }
    
    // Add My Page link on profile and authors pages
    if ((currentPage === 'profile' || currentPage === 'authors') && isLoggedIn) {
        const myPageIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-file-alt me-1"></i>' : '📄 ';
        const myPageUrl = `user-page.html?user=${encodeURIComponent(user.email)}`;
        html += `<li class="nav-item"><a class="nav-link" href="${myPageUrl}">${myPageIcon}My Page</a></li>`;
    }
    
    // Auth link
    if (isLoggedIn) {
        const userIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-user me-1"></i>' : '👤 ';
        const profileIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-user-circle me-2"></i>' : '👤 ';
        const myPageIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-file-alt me-2"></i>' : '📄 ';
        const adminIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-cog me-2"></i>' : '⚙️ ';
        const logoutIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-sign-out-alt me-2"></i>' : '🚪 ';
        
        const myPageUrl = `user-page.html?user=${encodeURIComponent(user.email)}`;
        
        html += `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    ${userIcon}${user.first_name || user.email}
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="profile.html">${profileIcon}Profile</a></li>
                    ${currentPage !== 'profile' && currentPage !== 'authors' ? `<li><a class="dropdown-item" href="${myPageUrl}">${myPageIcon}My Page</a></li>` : ''}
                    ${(user.role === 'admin' || user.role === 'super_user') && currentPage !== 'admin' ? `<li><a class="dropdown-item" href="admin.html">${adminIcon}Admin Dashboard</a></li>` : ''}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()">${logoutIcon}Logout</a></li>
                </ul>
            </li>`;
    } else {
        const loginIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-sign-in-alt me-1"></i>' : '🔐 ';
        html += `<li class="nav-item"><a class="nav-link" href="login.html">${loginIcon}Login</a></li>`;
    }
    
    navLinks.innerHTML = html;
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}
