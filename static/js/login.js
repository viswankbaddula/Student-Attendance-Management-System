// Login page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    // Form validation
    loginForm.addEventListener('submit', function(e) {
        let isValid = true;
        
        if (!usernameInput.value.trim()) {
            isValid = false;
            usernameInput.style.borderColor = '#e74c3c';
        } else {
            usernameInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
        
        if (!passwordInput.value.trim()) {
            isValid = false;
            passwordInput.style.borderColor = '#e74c3c';
        } else {
            passwordInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
    
    // Input validation on blur
    usernameInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    });
    
    passwordInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    });
});
