document.addEventListener('DOMContentLoaded', () => {
    window.DataManager = new DataManager();        
    window.ErrorMessage = new ErrorMessage();

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