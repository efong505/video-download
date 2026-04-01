/**
 * Mountain Hub Authentication Check
 * Redirects to login if user is not authenticated
 * Saves current page URL for return after login
 */

(function() {
    const authToken = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    
    if (!authToken || !userData) {
        // Save current page for redirect after login
        const currentUrl = window.location.href;
        localStorage.setItem('redirect_after_login', currentUrl);
        
        // Redirect to login with return URL parameter
        const loginUrl = `login.html?redirect=${encodeURIComponent(currentUrl)}`;
        window.location.href = loginUrl;
    }
})();
