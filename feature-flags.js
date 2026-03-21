/**
 * Feature Flags Helper
 * Include this script on pages that need to check feature flags
 * Usage: await FeatureFlags.isEnabled('election_system')
 */

const FeatureFlags = {
    API_URL: 'https://0h9mj9ul9j.execute-api.us-east-1.amazonaws.com/prod/feature-flags',
    cache: {},
    cacheExpiry: 5 * 60 * 1000, // 5 minutes
    
    /**
     * Check if a feature is enabled
     * @param {string} featureId - The feature ID to check
     * @returns {Promise<boolean>} - True if enabled, false otherwise
     */
    async isEnabled(featureId) {
        try {
            const flag = await this.getFlag(featureId);
            return flag && flag.enabled === true;
        } catch (error) {
            console.error('Error checking feature flag:', error);
            return false; // Fail closed - feature disabled on error
        }
    },
    
    /**
     * Get full feature flag details
     * @param {string} featureId - The feature ID to get
     * @returns {Promise<object>} - Feature flag object
     */
    async getFlag(featureId) {
        // Check cache first
        const cached = this.cache[featureId];
        if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
            return cached.data;
        }
        
        try {
            const response = await fetch(`${this.API_URL}?action=get&feature_id=${featureId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch feature flag');
            }
            
            const flag = await response.json();
            
            // Cache the result
            this.cache[featureId] = {
                data: flag,
                timestamp: Date.now()
            };
            
            return flag;
        } catch (error) {
            console.error('Error fetching feature flag:', error);
            return null;
        }
    },
    
    /**
     * Get all feature flags
     * @returns {Promise<array>} - Array of feature flags
     */
    async getAllFlags() {
        try {
            const response = await fetch(`${this.API_URL}?action=list`);
            if (!response.ok) {
                throw new Error('Failed to fetch feature flags');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error fetching feature flags:', error);
            return [];
        }
    },
    
    /**
     * Check if user has admin access to disabled feature
     * @param {string} featureId - The feature ID to check
     * @returns {Promise<boolean>} - True if admin can access, false otherwise
     */
    async canAdminAccess(featureId) {
        try {
            const flag = await this.getFlag(featureId);
            if (!flag) return false;
            
            // Check if feature allows admin access when disabled
            if (!flag.admin_only_access) return false;
            
            // Check if user is admin
            const userData = localStorage.getItem('user_data');
            if (!userData) return false;
            
            const user = JSON.parse(userData);
            return user.role === 'admin' || user.role === 'super_user';
        } catch (error) {
            console.error('Error checking admin access:', error);
            return false;
        }
    },
    
    /**
     * Get feature status message for display
     * @param {string} featureId - The feature ID
     * @returns {Promise<object>} - Status object with message and type
     */
    async getStatusMessage(featureId) {
        try {
            const flag = await this.getFlag(featureId);
            if (!flag) {
                return {
                    type: 'error',
                    message: 'Feature not found'
                };
            }
            
            if (flag.enabled) {
                let message = `✅ ${flag.name} is active`;
                
                if (flag.volunteer_dependent && flag.active_volunteers) {
                    message += ` (${flag.active_volunteers} volunteers)`;
                }
                
                return {
                    type: 'success',
                    message: message,
                    flag: flag
                };
            } else {
                let message = `⚠️ ${flag.name} is currently inactive`;
                
                if (flag.disable_reason) {
                    message += `: ${flag.disable_reason}`;
                }
                
                if (flag.seasonal && flag.season_start) {
                    const nextSeason = new Date(flag.season_start);
                    if (nextSeason > new Date()) {
                        message += ` (Returns ${nextSeason.toLocaleDateString()})`;
                    }
                }
                
                return {
                    type: 'warning',
                    message: message,
                    flag: flag
                };
            }
        } catch (error) {
            console.error('Error getting status message:', error);
            return {
                type: 'error',
                message: 'Unable to check feature status'
            };
        }
    },
    
    /**
     * Show feature status banner on page
     * @param {string} featureId - The feature ID
     * @param {string} containerId - DOM element ID to insert banner
     */
    async showStatusBanner(featureId, containerId) {
        const status = await this.getStatusMessage(featureId);
        const container = document.getElementById(containerId);
        
        if (!container) {
            console.error('Container not found:', containerId);
            return;
        }
        
        const alertClass = status.type === 'success' ? 'alert-success' : 
                          status.type === 'warning' ? 'alert-warning' : 'alert-danger';
        
        let html = `<div class="alert ${alertClass} mb-3">${status.message}`;
        
        // Add volunteer signup link if applicable
        if (status.flag && !status.flag.enabled && status.flag.volunteer_signup_url) {
            html += ` <a href="${status.flag.volunteer_signup_url}" class="alert-link">Volunteer to help maintain this feature</a>`;
        }
        
        html += '</div>';
        
        container.innerHTML = html;
    },
    
    /**
     * Hide navigation link if feature is disabled
     * @param {string} featureId - The feature ID
     * @param {string} linkSelector - CSS selector for the nav link
     */
    async hideNavLinkIfDisabled(featureId, linkSelector) {
        const enabled = await this.isEnabled(featureId);
        const canAccess = await this.canAdminAccess(featureId);
        
        const link = document.querySelector(linkSelector);
        if (!link) return;
        
        if (!enabled && !canAccess) {
            // Hide link for non-admins when feature is disabled
            link.style.display = 'none';
        } else if (!enabled && canAccess) {
            // Show admin preview badge
            link.innerHTML += ' <span class="badge bg-warning text-dark ms-1">Admin Preview</span>';
        }
    },
    
    /**
     * Redirect if feature is disabled and user is not admin
     * @param {string} featureId - The feature ID
     * @param {string} redirectUrl - URL to redirect to (default: index.html)
     */
    async requireFeature(featureId, redirectUrl = 'index.html') {
        const enabled = await this.isEnabled(featureId);
        
        if (enabled) return; // Feature is enabled, allow access
        
        // Check if admin can access
        const canAccess = await this.canAdminAccess(featureId);
        
        if (canAccess) {
            // Show admin preview banner
            this.showAdminPreviewBanner(featureId);
            return;
        }
        
        // Feature disabled and user is not admin - redirect
        alert('This feature is currently unavailable.');
        window.location.href = redirectUrl;
    },
    
    /**
     * Show admin preview banner at top of page
     * @param {string} featureId - The feature ID
     */
    showAdminPreviewBanner(featureId) {
        const banner = document.createElement('div');
        banner.className = 'alert alert-warning position-fixed top-0 start-50 translate-middle-x mt-3';
        banner.style.zIndex = '9999';
        banner.style.maxWidth = '600px';
        banner.innerHTML = `
            <strong>⚠️ Admin Preview Mode</strong><br>
            This feature is currently disabled for public users. You're viewing it as an administrator.
            <a href="admin-feature-flags.html" class="alert-link ms-2">Manage Feature Flags</a>
        `;
        document.body.insertBefore(banner, document.body.firstChild);
    },
    
    /**
     * Clear cache (useful after updating flags)
     */
    clearCache() {
        this.cache = {};
    }
};

// Auto-initialize on DOM load
if (typeof window !== 'undefined') {
    window.FeatureFlags = FeatureFlags;
}
