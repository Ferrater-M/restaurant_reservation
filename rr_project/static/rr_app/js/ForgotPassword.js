document.addEventListener('DOMContentLoaded', () => {
    window.ForgotPassword = new ForgotPassword();
});

class ForgotPassword{
    constructor(){
        this.email = document.getElementById('email');
        this.verif = document.getElementById('verification');
        this.password = document.getElementById('password');
        this.c_password = document.getElementById('cPassword');
        this.btnSubmit = document.getElementById('btnSubmit');
        this.error_msg = document.getElementById('errorMsg');
        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.error_msg);
        this.DataManager = window.DataManager;
        this.requestTitle = "email_verif";
        this.init();
    }

    init() {
        this.initBtnSubmit();
    }

    initBtnSubmit() {
        console.log("click");
        this.btnSubmit.addEventListener('click', ()=>{
            const request = {}
            const email = this.email.value.trim();
            request.email = email;
            if(this.requestTitle === "email_verif"){
                request.request = this.requestTitle;
                this.DataManager.postRequest('/rr/fpass_request/', request).then(response =>{
                    if(response.success){
                        alert(response.message);
                        this.verif.style = 'display: block';
                        this.email.style = 'display: none';
                        this.requestTitle = "code_verif";
                    }else{
                        this.ErrorMessage.show(response.error || "Error Email Verification");
                    }
                })
            }
            if(this.requestTitle === "code_verif"){
                const code = this.verif.value.trim();
                request.request = this.requestTitle;
                request.code = code; 
                this.DataManager.postRequest('/rr/fpass_request/', request).then(response =>{
                    if(response.success){
                        alert(response.message);
                        this.verif.style ='display: none';
                        this.password.style = 'display: block';
                        this.c_password.style = 'display: block';
                        this.requestTitle = "password_verif";
                    }else{
                        this.ErrorMessage.show(response.error || "Error Code Verification");
                    }
                })
            }
            if(this.requestTitle === "password_verif"){
                const password = this.password.value.trim();
                const c_password = this.c_password.value.trim();
                request.request = this.requestTitle;
                request.password = password;
                request.c_password = c_password;
                this.DataManager.postRequest('/rr/fpass_request/', request).then(response =>{
                    if(response.success){
                        alert(response.message)
                    }else{
                        this.ErrorMessage.show(response.error || "Error Password Verification");
                    }
                })
            }
        })
    }
}