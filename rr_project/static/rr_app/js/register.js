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
        this.errorMessage = window.ErrorMessage;
        this.errorMessage.setElement(this.error_msg);
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
                        alert("Register successful! Please check your inbox to verify your account.")
                        window.location.href = "/rr/login/";
                    } else {
                        this.errorMessage.show(response.error || 'Error creating user');
                    }
                }
            );
        });
    }

    initInputFields() {
        this.email.addEventListener('input', () => {
            if (this.error_msg.textContent == "Email already exists")
                this.errorMessage.remove();
        })

        this.password.addEventListener('input', () => {
            if (this.error_msg.textContent == "Passwords do not match")
                this.errorMessage.remove();
        })
        this.c_password.addEventListener('input', () => {
            if (this.error_msg.textContent == "Passwords do not match")
                this.errorMessage.remove();
        });
    }
}