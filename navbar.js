// Unified Navbar Script - Call initNavbar() after loading navbar.html
function initNavbar() {
    const container = document.getElementById('navbar-container');
    if (!container) return;
    
    const currentPage = container.dataset.page || 'index';
    const pageIcon = container.dataset.icon || '';
    const iconStyle = container.dataset.iconStyle || 'emoji';
    
    const contentLinks = [
        {page: 'videos', label: 'Videos', emoji: '🎥', fa: 'fa-video'},
        {page: 'video-analytics', label: 'Analytics', emoji: '📊', fa: 'fa-chart-bar', requiresAuth: true},
        {page: 'articles', label: 'Articles', emoji: '📖', fa: 'fa-book'},
        {page: 'news', label: 'News', emoji: '📰', fa: 'fa-newspaper'}
    ];
    
    const ministryLinks = [
        {page: 'election-map', label: 'Election Map', emoji: '🗺️', fa: 'fa-map'},
        {page: 'prayer-wall', label: 'Prayer Wall', emoji: '🙏', fa: 'fa-praying-hands'},
        {page: 'events-calendar', label: 'Events', emoji: '📅', fa: 'fa-calendar'},
        {page: 'resources', label: 'Resources', emoji: '📚', fa: 'fa-book-open'},
        {page: 'the-necessary-evil-book', label: 'The Necessary Evil', emoji: '📕', fa: 'fa-book'}
    ];
    
    const adminLinks = [
        {page: 'authors', label: 'Authors', emoji: '👥', fa: 'fa-users'},
        {page: 'user-upload', label: 'Upload Video', emoji: '⬆️', fa: 'fa-upload'},
        {page: 'admin-contributors', label: 'Contributors', emoji: '🗺️', fa: 'fa-map-marked'},
        {page: 'admin-resources', label: 'Manage Resources', emoji: '📚', fa: 'fa-tasks'},
        {page: 'admin-templates', label: 'Templates', emoji: '📄', fa: 'fa-file-alt'},
        {page: 'admin-book-subscribers', label: 'Book Subscribers', emoji: '📖', fa: 'fa-book'}
    ];
    
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    const user = userData ? JSON.parse(userData) : null;
    const isLoggedIn = !!token && !!user;
    
    // Update brand if page-specific
    if (pageIcon) {
        const allLinks = [...contentLinks, ...ministryLinks, ...adminLinks];
        document.getElementById('navbar-logo').style.display = 'none';
        document.getElementById('navbar-title').textContent = pageIcon + ' ' + (allLinks.find(l => l.page === currentPage || l.page === 'the-necessary-evil-book' && currentPage === 'book')?.label || '');
    }
    
    // Build nav links
    const navLinks = document.getElementById('nav-links');
    let html = '';
    
    // Content dropdown
    const contentIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-video me-1"></i>' : '🎥 ';
    html += `<li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">${contentIcon}Content</a>
        <ul class="dropdown-menu">`;
    contentLinks.forEach(link => {
        if (link.page === currentPage) return;
        if (link.requiresAuth && !isLoggedIn) return;
        const icon = iconStyle === 'fontawesome' ? `<i class="fas ${link.fa} me-2"></i>` : link.emoji + ' ';
        html += `<li><a class="dropdown-item" href="${link.page}.html">${icon}${link.label}</a></li>`;
    });
    html += `</ul></li>`;
    
    // Ministry dropdown
    const ministryIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-church me-1"></i>' : '⛪ ';
    html += `<li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">${ministryIcon}Ministry</a>
        <ul class="dropdown-menu">`;
    ministryLinks.forEach(link => {
        if (link.page === currentPage) return;
        const icon = iconStyle === 'fontawesome' ? `<i class="fas ${link.fa} me-2"></i>` : link.emoji + ' ';
        html += `<li><a class="dropdown-item" href="${link.page}.html">${icon}${link.label}</a></li>`;
    });
    html += `</ul></li>`;
    
    // Subscribe link (standalone)
    if (currentPage !== 'subscribe') {
        const subIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-envelope me-1"></i>' : '📧 ';
        html += `<li class="nav-item"><a class="nav-link" href="subscribe.html">${subIcon}Subscribe</a></li>`;
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
        const notifIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-bell me-2"></i>' : '🔔 ';
        const adminIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-cog me-2"></i>' : '⚙️ ';
        const logoutIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-sign-out-alt me-2"></i>' : '🚪 ';
        
        const myPageUrl = `user-page.html?user=${encodeURIComponent(user.email)}`;
        
        // Notification bell
        html += `
            <li class="nav-item">
                <a class="nav-link position-relative" href="notification-settings.html">
                    🔔
                    <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" id="notif-badge" style="display: none; font-size: 0.6rem;">0</span>
                </a>
            </li>`;
        
        // Build admin submenu if user is admin
        let adminSubmenu = '';
        if (user.role === 'admin' || user.role === 'super_user') {
            adminSubmenu = `<li><hr class="dropdown-divider"></li>
                <li><h6 class="dropdown-header">${adminIcon}Admin</h6></li>
                <li><a class="dropdown-item" href="admin.html"><i class="fas fa-tachometer-alt me-2"></i>Dashboard</a></li>`;
            adminLinks.forEach(link => {
                if (link.page === currentPage) return;
                const icon = iconStyle === 'fontawesome' ? `<i class="fas ${link.fa} me-2"></i>` : link.emoji + ' ';
                adminSubmenu += `<li><a class="dropdown-item" href="${link.page}.html">${icon}${link.label}</a></li>`;
            });
        }
        
        html += `
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                    ${userIcon}${user.first_name || user.email}
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="profile.html">${profileIcon}Profile</a></li>
                    <li><a class="dropdown-item" href="notification-settings.html">${notifIcon}Notification Settings</a></li>
                    ${currentPage !== 'profile' && currentPage !== 'authors' ? `<li><a class="dropdown-item" href="${myPageUrl}">${myPageIcon}My Page</a></li>` : ''}
                    ${adminSubmenu}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout()">${logoutIcon}Logout</a></li>
                </ul>
            </li>`;
    } else {
        // Not logged in - show public ministry links and login
        const loginIcon = iconStyle === 'fontawesome' ? '<i class="fas fa-sign-in-alt me-1"></i>' : '🔐 ';
        html += `<li class="nav-item"><a class="nav-link" href="login.html">${loginIcon}Login</a></li>`;
    }
    
    navLinks.innerHTML = html;
    
    // Load unread notification count
    if (isLoggedIn) {
        loadNotificationCount(user.email);
    }
}

function loadNotificationCount(email) {
    fetch(`https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/notifications?action=get_user_notifications&email=${encodeURIComponent(email)}`)
        .then(r => r.json())
        .then(data => {
            const unread = (data.notifications || []).filter(n => !n.read).length;
            const badge = document.getElementById('notif-badge');
            if (badge && unread > 0) {
                badge.textContent = unread;
                badge.style.display = 'inline-block';
            }
        })
        .catch(err => console.log('Notification count error:', err));
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}
