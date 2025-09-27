class Login {
    constructor() {
        this.submit = document.getElementById('btnSignin');
        this.email = document.getElementById('email');
        this.password = document.getElementById('password');
        this.error_msg = document.getElementById('errorMsg')
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

        if (!email || !password) {
            this.errorMessage.show("Please input all fields");
            return;
        }

        try {
            const [pendingUsers, users] = await Promise.all([
                this.dataManager.getRequest('/rr/getPendingUsers/'),
                this.dataManager.getRequest('/rr/getUsers/')
            ]);

            if (pendingUsers.some(p => p.email === email)) {
                alert("Account is pending. Please check your inbox to verify your account");
                return;
            }

            const user = users.find(u => u.email === email);

            if (!user) {
                this.errorMessage.show("Email not found");
                return;
            }

            if (user.password !== password) {
                this.errorMessage.show("Password is incorrect");
                return;
            }

            alert("login successful");

        } catch (err) {
            console.error(err);
            this.errorMessage.show("Something went wrong. Please try again.");
        }
    });
}

    // initBtnSubmitListener(){
    //   this.submit.addEventListener('click', ()=>{
    //     const email = this.email.value.trim();
    //     this.dataManager.getRequest('/rr/getPendingUsers/').then(p_users => {
    //           if(p_users.find(p_u => p_u.email === email)){
    //             alert("Account is pending. Please check your inbox to verify your account");
    //             return;
    //           }
    //         }).catch(err => {
    //           console.error(err);
    //         });

    //     this.dataManager.getRequest('/rr/getUsers/').then(users => {
    //         const password = this.password.value.trim();
    //         const user = users.find(u => u.email === email)
    //         // how is .find structured?
    //         // let's create our own find function
    //         // function find(array, callback){
    //         //     for (let i = 0; i < array.size; i++){
    //         //         const element = array[i];
    //         //         if(callback(element)){
    //         //             return element;  
    //         //         }
    //         //     }
    //         //     return undefined;
    //         //  }
    //         // the callback is a lambda expression (functions without names)
    //         // this argument gets called in the if statement inside our find function
    //         // if the lambda returns true, the find function returns an element
    //         if(!email || !password){
    //             this.errorMessage.show("Please input all fields");
    //             return;
    //         }
    //         if(!user){
    //             this.errorMessage.show("Email not found");
    //             return;
    //         }
    //         if(user.password != password){
    //             this.errorMessage.show("Password is incorrect");
    //             return;
    //         }
    //       }).catch(err => {
    //         console.error(err);
    //       });
    //   });
    // }

    initInputFields(){
        this.email.addEventListener('input', ()=>{
          if(this.error_msg.textContent === "Email not found")
          this.errorMessage.remove();
        })
        this.password.addEventListener('input', ()=>{
          if(this.error_msg.textContent === "Password is incorrect")
          this.errorMessage.remove();
        })
    }
}