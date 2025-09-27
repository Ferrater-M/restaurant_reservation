document.addEventListener('DOMContentLoaded', () => {
    window.DataManager = new DataManager();        
    window.ErrorMessage = new ErrorMessage();

    if (document.getElementById("btnSignin")) {
        console.log("Login page detected");
        window.Login = new Login();
    }

    if (document.getElementById("btnSignup")) {
        console.log("Register page detected");
        window.Register = new Register();
    }
});

class ErrorMessage{
    constructor(error_msg){
        this.error_msg = error_msg;
    }
    setElement(error_msg){
        this.error_msg = error_msg;
    }
    show(message){
        this.error_msg.textContent = message;
    }
    remove(){
        this.error_msg.textContent = '';
    }
}