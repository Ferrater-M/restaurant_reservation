document.addEventListener('DOMContentLoaded', () => {
    window.Login = new Login();            
});

class Login {
    constructor() {
        this.submit = document.getElementById('btnSignin');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.error_msg = document.getElementById('errorMsg')
        this.dataManager = window.DataManager;
        this.init();
    }
    
    init() {
        this.initBtnSubmitListener();
        this.initInputFields();
    }

    initBtnSubmitListener(){
      this.submit.addEventListener('click', ()=>{
        this.dataManager.getRequest('/rr/getUsers/').then(users => {
            const email = this.email.value.trim();
            const password = this.password.value.trim();
            const user = users.find(u => u.email === email)
            // how is .find structured?
            // let's create our own find function
            // function find(array, callback){
            //     for (let i = 0; i < array.size; i++){
            //         const element = array[i];
            //         if(callback(element)){
            //             return element;  
            //         }
            //     }
            //     return undefined;
            //  }
            // the callback is a lambda expression (functions without names)
            // this argument gets called in the if statement inside our find function
            // if the lambda returns true, the find function returns an element
            if(!user){
                this.showError("Email not found");
                return;
            }
            if(user.password != password){
                this.showError("Password is incorrect");
                return;
            }
            this.removeError();
          }).catch(err => {
            console.error(err);
            this.showError("Error fetching user data");
          });
      });
    }

    initInputFields(){
        this.email.addEventListener('input', ()=>{
          if(this.error_msg.textContent === "Email not found")
          this.removeError();
        })
        this.password.addEventListener('input', ()=>{
          if(this.error_msg.textContent === "Password is incorrect")
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