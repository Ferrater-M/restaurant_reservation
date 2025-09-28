document.addEventListener('DOMContentLoaded', () => {
    window.ForgotPassword = new ForgotPassword();
});

class ForgotPassword {
    constructor() {
        this.elements = {
            email: document.getElementById('email'),
            verif: document.getElementById('verification'),
            password: document.getElementById('password'),
            c_password: document.getElementById('cPassword'),
            btnSubmit: document.getElementById('btnSubmit'),
            error_msg: document.getElementById('errorMsg')
        };

        this.ErrorMessage = window.ErrorMessage;
        this.ErrorMessage.setElement(this.elements.error_msg);
        this.DataManager = window.DataManager;
        
        this.stateKey = 'forgotPasswordState';
        this.emailKey = 'forgotPasswordEmail';
        
        this.steps = {
            email_verif: {
                title: 'email_verif',
                visibleElements: ['email'],
                hiddenElements: ['verif', 'password', 'c_password'],
                requiredFields: ['email']
            },
            code_verif: {
                title: 'code_verif',
                visibleElements: ['verif'],
                hiddenElements: ['email', 'password', 'c_password'],
                requiredFields: ['email', 'verif']
            },
            password_verif: {
                title: 'password_verif',
                visibleElements: ['password', 'c_password'],
                hiddenElements: ['email', 'verif'],
                requiredFields: ['email', 'password', 'c_password']
            }
        };

        this.init();
    }

    init() {
        this.restoreState();
        this.initBtnSubmit();
    }

    restoreState() {
        const savedState = sessionStorage.getItem(this.stateKey);
        const savedEmail = sessionStorage.getItem(this.emailKey);
        
        if (savedState && this.steps[savedState]) {
            this.currentStep = savedState;
            if (savedEmail) {
                this.elements.email.value = savedEmail;
            }
        } else {
            this.currentStep = 'email_verif';
        }
        
        this.updateUI();
    }

    saveState() {
        sessionStorage.setItem(this.stateKey, this.currentStep);
        if (this.elements.email.value.trim()) {
            sessionStorage.setItem(this.emailKey, this.elements.email.value.trim());
        }
    }

    clearState() {
        sessionStorage.removeItem(this.stateKey);
        sessionStorage.removeItem(this.emailKey);
    }

    updateUI() {
        const step = this.steps[this.currentStep];
        if (!step) return;

        Object.values(this.elements).forEach(element => {
            if (element && ['email', 'verif', 'password', 'c_password'].includes(element.id)) {
                element.style.display = 'none';
            }
        });

        step.visibleElements.forEach(elementName => {
            if (this.elements[elementName]) {
                this.elements[elementName].style.display = 'block';
            }
        });
    }

    validateCurrentStep() {
        const step = this.steps[this.currentStep];
        const errors = [];

        step.requiredFields.forEach(fieldName => {
            const element = this.elements[fieldName];
            if (!element || !element.value.trim()) {
                errors.push(`${fieldName.replace('_', ' ')} is required`);
            }
        });

        if (this.currentStep === 'password_verif') {
            const password = this.elements.password.value.trim();
            const cPassword = this.elements.c_password.value.trim();
            
            if (password && cPassword && password !== cPassword) {
                errors.push('Passwords do not match');
            }
            
            if (password && password.length < 6) {
                errors.push('Password must be at least 6 characters long');
            }
        }

        return errors;
    }

    buildRequest() {
        const request = {
            request: this.currentStep,
            email: sessionStorage.getItem(this.emailKey) || this.elements.email.value.trim()
        };

        switch (this.currentStep) {
            case 'code_verif':
                request.code = this.elements.verif.value.trim();
                break;
            case 'password_verif':
                request.password = this.elements.password.value.trim();
                request.c_password = this.elements.c_password.value.trim();
                break;
        }

        return request;
    }

    handleStepTransition(response) {
        const transitions = {
            email_verif: 'code_verif',
            code_verif: 'password_verif',
            password_verif: null // End of flow
        };

        if (response.success) {
            alert(response.message);
            
            const nextStep = transitions[this.currentStep];
            if (nextStep) {
                this.currentStep = nextStep;
                this.saveState();
                this.updateUI();
            } else {
                this.clearState();
                window.location.href = "/rr/login/";
            }
        } else {
            this.ErrorMessage.show(response.error || `Error in ${this.currentStep.replace('_', ' ')}`);
        }
    }

    initBtnSubmit() {
        this.elements.btnSubmit.addEventListener('click', async (e) => {
            e.preventDefault();
            
            const validationErrors = this.validateCurrentStep();
            if (validationErrors.length > 0) {
                this.ErrorMessage.show(validationErrors.join(', '));
                return;
            }

            try {
                this.elements.btnSubmit.disabled = true;
                
                const request = this.buildRequest();
                const response = await this.DataManager.postRequest('/rr/fpass_request/', request);
                
                this.handleStepTransition(response);
                
            } catch (error) {
                console.error('Request failed:', error);
                this.ErrorMessage.show('Network error. Please try again.');
            } finally {
                this.elements.btnSubmit.disabled = false;
            }
        });
    }
}