document.addEventListener('DOMContentLoaded', () => {
    window.Register = new Register();
});

class Register {
    constructor() {
        this.submit = document.getElementById('btnSignup');
        this.googleBtn = document.getElementById('btnGoogle');
        this.microsoftBtn = document.getElementById('btnMicrosoft');
        this.first_name = document.getElementById('firstName');
        this.last_name = document.getElementById('lastName');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.c_password = document.getElementById('cPassword');
        this.error_msg = document.getElementById('errorMsg');
        this.dataManager = window.DataManager;
        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.error_msg);
        this.init();
    }

    init() {
        this.initBtnSubmitListener();
        this.initOAuthButtons();
        this.initInputFields();
    }

    async initBtnSubmitListener() {
        this.submit.addEventListener('click', async () => {
            const userData = {
                first_name: this.first_name.value.trim(),
                last_name: this.last_name.value.trim(),
                email: this.email.value.trim(),
                password: this.password.value.trim(),
                c_password: this.c_password.value.trim(),
                role: 'user'
            };

            if (!userData.first_name || !userData.last_name || !userData.email || !userData.password || !userData.c_password) {
                this.ErrorMessage.show('Please fill in all fields');
                return;
            }

            if (userData.password !== userData.c_password) {
                this.ErrorMessage.show('Passwords do not match');
                return;
            }

            try {
                const response = await this.dataManager.postRequest('/rr/register_user/', userData);
                
                if (response.success) {
                    alert(response.message);
                    window.location.href = "/rr/login/";
                } else {
                    this.ErrorMessage.show(response.error || 'Registration failed');
                }
            } catch (error) {
                this.ErrorMessage.show('Network error occurred');
                console.error('Registration error:', error);
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
                // Redirect to OAuth provider
                window.location.href = response.oauth_url;
            } else {
                this.ErrorMessage.show(response.error || 'OAuth initialization failed');
            }
        } catch (error) {
            this.ErrorMessage.show('OAuth error occurred');
            console.error('OAuth error:', error);
        }
    }

    initInputFields() {
        this.email.addEventListener('input', () => {
            if (this.error_msg.textContent.includes("Email already exists")) {
                this.ErrorMessage.remove();
            }
        });

        [this.password, this.c_password].forEach(field => {
            field.addEventListener('input', () => {
                if (this.error_msg.textContent.includes("Passwords do not match")) {
                    this.ErrorMessage.remove();
                }
            });
        });
    }
}