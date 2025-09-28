document.addEventListener('DOMContentLoaded', () => {
    window.Login = new Login();
});

class Login {
    constructor() {
        this.submit = document.getElementById('btnSignin');
        this.googleBtn = document.getElementById('btnGoogle');
        this.microsoftBtn = document.getElementById('btnMicrosoft');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.error_msg = document.getElementById('errorMsg');
        this.forgot_pass = document.getElementById('forgotPassword');
        this.dataManager = window.DataManager;
        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.error_msg);
        this.init();
    }

    init() {
        this.initBtnSubmitListener();
        this.initOAuthButtons();
        this.initInputFields();
        this.initLblForgotPassword();
        
        // Check if user is already logged in
        if (this.dataManager.auth.isAuthenticated()) {
            this.redirectToDashboard();
        }
    }

    async initBtnSubmitListener() {
        this.submit.addEventListener('click', async () => {
            const email = this.email.value.trim();
            const password = this.password.value.trim();

            if (!email || !password) {
                this.ErrorMessage.show('Please fill in all fields');
                return;
            }

            try {
                const response = await this.dataManager.postRequest('/rr/login_user/', { email, password });
                
                if (response.success) {
                    // Store session data
                    this.dataManager.auth.setSession(response.session, response.user);
                    
                    alert(response.message);
                    this.redirectToDashboard();
                } else {
                    this.ErrorMessage.show(response.error || 'Login failed');
                }
            } catch (error) {
                this.ErrorMessage.show('Network error occurred');
                console.error('Login error:', error);
            }
        });
    }

    initOAuthButtons() {
        if (this.googleBtn) {
            this.googleBtn.addEventListener('click', () => this.handleOAuth('google'));
        }
        
        if (this.microsoftBtn) {
            this.microsoftBtn.addEventListener('click', () => this.handleOAuth('azure'));
        }
    }

    async handleOAuth(provider) {
        try {
            const response = await this.dataManager.postRequest('/rr/oauth-signin/', { provider });
            
            if (response.success && response.oauth_url) {
                window.location.href = response.oauth_url;
            } else {
                this.ErrorMessage.show(response.error || 'OAuth initialization failed');
            }
        } catch (error) {
            this.ErrorMessage.show('OAuth error occurred');
            console.error('OAuth error:', error);
        }
    }

    redirectToDashboard() {
        const user = this.dataManager.auth.user;
        if (user && user.is_admin) {
            window.location.href = "/rr/admin-dashboard/";
        } else {
            window.location.href = "/rr/dashboard/";
        }
    }

    initLblForgotPassword() {
        this.forgot_pass.addEventListener('click', () => {
            window.location.href = "/rr/forgot_password/";
        });
    }

    initInputFields() {
        [this.email, this.password].forEach(field => {
            field.addEventListener('input', () => {
                this.ErrorMessage.remove();
            });
        });
    }
}