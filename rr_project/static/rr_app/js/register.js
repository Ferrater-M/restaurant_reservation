document.addEventListener('DOMContentLoaded', () => {   
    window.Register = new Register();
});

class Register {
    constructor(){
        this.submit = document.getElementById('btnSignup');
        this.first_name = document.getElementById('firstName');
        this.last_name = document.getElementById('lastName');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.c_password = document.getElementById('cPassword');
        this.user = {}
        this.dataManager = window.DataManager;
        this.error_msg = document.getElementById('errorMsg');
        this.init();
    }

    init(){
        this.initBtnSubmitListener();
        this.initInputFields();
    }

    initBtnSubmitListener(){
        this.submit.addEventListener('click', ()=>{
            this.user.first_name = this.first_name.value.trim();
            this.user.last_name = this.last_name.value.trim();

            this.dataManager.getRequest('/rr/getUsers/').then(users => {
                const email = this.email.value.trim();
                const user = users.find(u => u.email == email);
                if(user){
                    this.showError("Email already exists");
                    return;
                }
                const password = this.password.value.trim();
                const c_password = this.c_password.value.trim();
                if(c_password != password){
                    this.showError("Passwords do not match");
                    return;
                }
                this.user.email = email;
                this.user.password = password;
                this.dataManager.postRequest('/rr/addUser/', this.user).then(
                    response =>{
                        if(response.success){
                            window.location.href = "/rr/login/";
                        }else{
                            this.showError(response.error || 'Error creating user');
                        }
                    }
                );
            }).catch(err => {
            console.error(err);
            this.showError("Error creating user");
          });
        })
    }

    initInputFields(){
        this.email.addEventListener('input', ()=>{
            if(this.error_msg.textContent == "Email already exists")
            this.removeError();
        })
        
        this.password.addEventListener('input', ()=>{
            if(this.error_msg.textContent == "Passwords do not match")
            this.removeError();
        })
        this.c_password.addEventListener('input', ()=>{
            if(this.error_msg.textContent == "Passwords do not match")
            this.removeError();
        })
    }

    showError(message){
      this.error_msg.textContent = message;
    }
    removeError(){
      this.error_msg.textContent = '';
    }
}