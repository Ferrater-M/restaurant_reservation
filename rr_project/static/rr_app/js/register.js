document.addEventListener('DOMContentLoaded', () => {
    window.Register = new Register();
});
class Register {
    constructor() {
        this.submit = document.getElementById('btnSignup');
        this.first_name = document.getElementById('firstName');
        this.last_name = document.getElementById('lastName');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.c_password = document.getElementById('cPassword');
        this.user = {}
        this.dataManager = window.DataManager;
        this.error_msg = document.getElementById('errorMsg');
        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.error_msg);
        this.init();
    }

    init() {
        this.initBtnSubmitListener();
        this.initInputFields();
    }

    async initBtnSubmitListener() {
        this.submit.addEventListener('click', () => {
            this.user.first_name = this.first_name.value.trim();
            this.user.last_name = this.last_name.value.trim();
            const password = this.password.value.trim();
            const c_password = this.c_password.value.trim();
            const email = this.email.value.trim();

            this.user.email = email;
            this.user.password = password;
            this.user.c_password = c_password;
            this.dataManager.postRequest('/rr/register_user/', this.user).then(
                response => {
                    if (response.success) {
                        alert(response.message)
                        window.location.href = "/rr/login/";
                    } else {
                        this.ErrorMessage.show(response.error || 'Error creating user');
                    }
                }
            );
        });
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