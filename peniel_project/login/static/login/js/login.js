document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('#togglePassword');
    const lockoutPopup = document.getElementById('lockout-popup');
    const password = document.querySelector('#password');
    const eyeIcon = document.querySelector('#eyeIcon');

    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);

        eyeIcon.src = (type === 'password') ? eyeOff : eyeOn;
    });

    // Lógica para o pop-up de bloqueio de login
    if (lockoutPopup) {
        const countdownElement = document.getElementById('countdown-timer');
        const closeButton = document.getElementById('popup-close-btn');
        let timeLeft = parseInt(countdownElement.textContent, 10);

        // Desabilita todos os inputs do formulário enquanto o popup estiver ativo
        document.querySelectorAll('.login-form input, .login-form button').forEach(el => el.disabled = true);
        closeButton.disabled = true; // Garante que o botão do popup comece desabilitado

        const timer = setInterval(() => {
            timeLeft--;
            countdownElement.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timer);
                countdownElement.textContent = '0';
                closeButton.disabled = false;
                closeButton.textContent = 'OK';
                closeButton.addEventListener('click', () => window.location.reload()); // Recarrega a página para tentar de novo
            }
        }, 1000);
    }
});