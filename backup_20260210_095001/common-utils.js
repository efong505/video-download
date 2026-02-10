/**
 * Common Utilities - Shared JavaScript functions
 * Used across Christian Conservatives Today platform
 */

// API Endpoints
const API_ENDPOINTS = {
    AUTH: 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth',
    ADMIN: 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/admin',
    TAG: 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/tags',
    ARTICLES: 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/articles',
    NEWS: 'https://yvqx5yjqo3.execute-api.us-east-1.amazonaws.com/prod/news',
    RESOURCES: 'https://hzursivfuk.execute-api.us-east-1.amazonaws.com/prod/resources',
    CONTRIBUTORS: 'https://hzursivfuk.execute-api.us-east-1.amazonaws.com/prod/contributors',
    COMMENTS: 'https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/comments',
    PAYPAL: 'https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/paypal',
    ROUTER: 'https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/download'
};

// Authentication Functions
function getAuthToken() {
    return localStorage.getItem('auth_token');
}

function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

function getUserRole() {
    const userData = getUserData();
    return userData ? userData.role : null;
}

function isAuthenticated() {
    return !!getAuthToken();
}

function isAdmin() {
    const role = getUserRole();
    return role === 'admin' || role === 'super_user';
}

function isSuperUser() {
    return getUserRole() === 'super_user';
}

function isEditor() {
    const role = getUserRole();
    return role === 'editor' || role === 'admin' || role === 'super_user';
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}

function requireAuth(redirectUrl = 'login.html') {
    if (!isAuthenticated()) {
        window.location.href = redirectUrl;
        return false;
    }
    return true;
}

function requireAdmin(redirectUrl = 'index.html') {
    if (!isAdmin()) {
        alert('Admin access required');
        window.location.href = redirectUrl;
        return false;
    }
    return true;
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(endpoint, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            logout();
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Notification System
function showNotification(message, type = 'success', duration = 3000) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#ffc107'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 500;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Error Handler
function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    showNotification(userMessage, 'error');
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copy to Clipboard
async function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    try {
        await navigator.clipboard.writeText(text);
        showNotification(successMessage, 'success');
        return true;
    } catch (error) {
        console.error('Copy failed:', error);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showNotification(successMessage, 'success');
            return true;
        } catch (err) {
            showNotification('Failed to copy', 'error');
            return false;
        } finally {
            document.body.removeChild(textArea);
        }
    }
}

// Loading Spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Validate Email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Sanitize HTML (basic)
function sanitizeHTML(html) {
    const div = document.createElement('div');
    div.textContent = html;
    return div.innerHTML;
}

// Get Query Parameter
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Set Query Parameter
function setQueryParam(param, value) {
    const url = new URL(window.location);
    url.searchParams.set(param, value);
    window.history.pushState({}, '', url);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        API_ENDPOINTS,
        getAuthToken,
        getUserData,
        getUserRole,
        isAuthenticated,
        isAdmin,
        isSuperUser,
        isEditor,
        logout,
        requireAuth,
        requireAdmin,
        apiRequest,
        showNotification,
        handleError,
        formatDate,
        formatFileSize,
        debounce,
        copyToClipboard,
        showLoading,
        hideLoading,
        isValidEmail,
        sanitizeHTML,
        getQueryParam,
        setQueryParam
    };
}
