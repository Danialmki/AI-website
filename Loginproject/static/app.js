document.getElementById('Register').addEventListener('click', function() {
    document.getElementById('moving-border').style.left = '0';
});

document.getElementById('Login').addEventListener('click', function() {
    document.getElementById('moving-border').style.left = 'calc(50% + 1px)';
});

document.getElementById('Register').addEventListener('click', function() {
    var loginForm = document.querySelector('.login-form');
    var registerForm = document.querySelector('.register-form');
    
    loginForm.style.opacity = 0;
    setTimeout(function() {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        setTimeout(function() {
            registerForm.style.opacity = 1;
        }, 50);
    }, 300);
});

document.getElementById('Login').addEventListener('click', function() {
    var loginForm = document.querySelector('.login-form');
    var registerForm = document.querySelector('.register-form');
    
    registerForm.style.opacity = 0;
    setTimeout(function() {
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
        setTimeout(function() {
            loginForm.style.opacity = 1;
        }, 50);
    }, 300);
});
