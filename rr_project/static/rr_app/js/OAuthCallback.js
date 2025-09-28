class OAuthCallback {
    constructor() {
        this.init();
    }

    init() {
        // Handle OAuth callback from URL hash
        this.handleCallback();
    }

    async handleCallback() {
        try {
            // Get session from URL hash (Supabase OAuth callback)
            const hash = window.location.hash.substring(1);
            const params = new URLSearchParams(hash);
            
            const accessToken = params.get('access_token');
            const refreshToken = params.get('refresh_token');
            const expiresAt = params.get('expires_at');
            
            if (accessToken) {
                // Get user info from backend
                const response = await fetch('/rr/current-user/', {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Store session
                    const dataManager = new DataManager();
                    dataManager.auth.setSession({
                        access_token: accessToken,
                        refresh_token: refreshToken,
                        expires_at: expiresAt
                    }, data.user);
                    
                    // Redirect to dashboard
                    if (data.user.is_admin) {
                        window.location.href = "/rr/admin-dashboard/";
                    } else {
                        window.location.href = "/rr/dashboard/";
                    }
                } else {
                    throw new Error('Failed to get user info');
                }
            } else {
                throw new Error('No access token in callback');
            }
        } catch (error) {
            console.error('OAuth callback error:', error);
            alert('OAuth login failed. Please try again.');
            window.location.href = '/rr/login/';
        }
    }
}

// Initialize OAuth callback handler if on callback page
if (window.location.pathname.includes('/oauth-callback/')) {
    document.addEventListener('DOMContentLoaded', () => {
        new OAuthCallback();
    });
}