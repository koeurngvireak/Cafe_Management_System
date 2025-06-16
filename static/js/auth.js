document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.querySelector('input[type="password"]');

    passwordToggle.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Toggle eye icon
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });

    // Form validation
    const loginForm = document.querySelector('.login-form');
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = this.querySelector('input[name="email"]').value;
        const password = this.querySelector('input[name="password"]').value;

        if (!email || !password) {
            showError('Please fill in all fields');
            return;
        }

        // Submit the form
        this.submit();
    });

    function showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-3';
        alert.textContent = message;
        loginForm.insertBefore(alert, loginForm.firstChild);
        
        setTimeout(() => alert.remove(), 3000);
    }
});