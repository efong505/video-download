// Authentication helper functions

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

function getAuthHeaders() {
    return {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
    };
}

function isAdmin() {
    const email = localStorage.getItem('email');
    return ADMIN_EMAILS.includes(email);
}
