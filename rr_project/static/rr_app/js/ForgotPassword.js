document.addEventListener('DOMContentLoaded', () => {
    window.ForgotPassword = new ForgotPassword();
});

class ForgotPassword {
    constructor() {
        this.email = document.getElementById('email');
        this.btnSubmit = document.getElementById('btnSubmit');
        this.error_msg = document.getElementById('errorMsg');
        this.success_msg = document.getElementById('successMsg');
        this.dataManager = window.DataManager;
        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.error_msg);
        this.init();
    }

    init() {
        this.initBtnSubmit();
    }

    initBtnSubmit() {
        this.btnSubmit.addEventListener('click', async () => {
            const email = this.email.value.trim();
            
            if (!email) {
                this.ErrorMessage.show('Please enter your email');
                return;
            }

            try {
                const response = await this.dataManager.postRequest('/rr/forgot_password_request/', { email });
                
                if (response.success) {
                    if (this.success_msg) {
                        this.success_msg.textContent = response.message;
                        this.success_msg.style.display = 'block';
                    } else {
                        alert(response.message);
                    }
                    this.email.style.display = 'none';
                    this.btnSubmit.style.display = 'none';
                } else {
                    this.ErrorMessage.show(response.error || 'Failed to send reset email');
                }
            } catch (error) {
                this.ErrorMessage.show('Network error occurred');
                console.error('Password reset error:', error);
            }
        });
    }
}