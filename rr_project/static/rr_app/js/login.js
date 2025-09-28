document.addEventListener('DOMContentLoaded', () => {
    window.Login = new Login();
});

class Login {
    constructor() {
        this.submit = document.getElementById('btnSignin');
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
        this.initInputFields();
        this.initLblForgotPassword();
    }

    async initBtnSubmitListener() {
        console.log("click");
        this.submit.addEventListener('click', async () => {
            const email = this.email.value.trim();
            const password = this.password.value.trim();

            const em_pass = { email: email, password: password }

            try {
                this.dataManager.postRequest('/rr/login_user/', em_pass).then(response => {
                    if (response.success) {
                        alert(response.message);
                    } else {
                        this.ErrorMessage.show(response.error || "Error login");
                    }
                })
            } catch (err) {
                console.error(err);
            }
        })
    }

    initLblForgotPassword() {
        this.forgot_pass.addEventListener('click', ()=>{
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
