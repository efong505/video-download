// JWT Token Validation - Check token expiration on page load
function checkTokenExpiration() {
    const token = localStorage.getItem('auth_token');
    if (!token) return;
    
    try {
        const parts = token.split('.');
        if (parts.length !== 3) {
            logout();
            return;
        }
        
        const payload = JSON.parse(atob(parts[1]));
        const exp = payload.exp;
        const now = Math.floor(Date.now() / 1000);
        
        if (exp && exp < now) {
            console.log('Token expired, logging out...');
            alert('Your session has expired. Please log in again.');
            logout();
        }
    } catch (error) {
        console.error('Token validation error:', error);
        logout();
    }
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}

// Run on page load
window.addEventListener('load', checkTokenExpiration);
