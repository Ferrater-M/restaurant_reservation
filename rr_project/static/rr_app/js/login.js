class Login {
    constructor() {
        this.submit = document.getElementById('btnSignin');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.error_msg = document.getElementById('errorMsg');
        this.dataManager = window.DataManager;
        this.errorMessage = window.ErrorMessage;
        this.errorMessage.setElement(this.error_msg);
        this.init();
    }

    init() {
        this.initBtnSubmitListener();
        this.initInputFields();
    }

    async initBtnSubmitListener() {
        this.submit.addEventListener('click', async () => {
            const email = this.email.value.trim();
            const password = this.password.value.trim();

            const em_pass = {email: email, password: password}
            
            try {
                this.dataManager.postRequest('/rr/login_user/', em_pass).then(response =>{
                    if(response.success){
                        alert("Login successful");
                    }else{
                        this.errorMessage.show(response.error || "Error login");
                    }
                })
            }catch (err) {
                console.error(err);
            }
        })
    }

    initInputFields() {
        this.email.addEventListener('input', () => {
            if (this.error_msg.textContent === "Email not found")
                this.errorMessage.remove();
        });

        this.password.addEventListener('input', () => {
            if (this.error_msg.textContent === "Password is incorrect")
                this.errorMessage.remove();
        });
    }
}
