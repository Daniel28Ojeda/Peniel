document.addEventListener('DOMContentLoaded', () => {
    // Lógica para o popup de bloqueio
    const lockoutPopup = document.getElementById('lockout-popup');

    if (lockoutPopup) {
        const countdownElement = document.getElementById('countdown-timer');
        const closeButton = document.getElementById('popup-close-btn');
        
        let timeLeft = parseInt(countdownElement.textContent, 10);

        // Atualiza o texto do botão com a contagem inicial
        closeButton.textContent = `Aguarde... (${timeLeft}s)`;

        const timer = setInterval(() => {
            timeLeft--;
            countdownElement.textContent = timeLeft;
            closeButton.textContent = `Aguarde... (${timeLeft}s)`;

            if (timeLeft <= 0) {
                clearInterval(timer);
                countdownElement.textContent = "0";
                closeButton.disabled = false;
                closeButton.textContent = "Tentar Novamente";
                
                // Ao clicar no botão habilitado, a página será recarregada.
                // Isso limpa o estado de bloqueio e permite uma nova tentativa.
                closeButton.addEventListener('click', () => {
                    location.reload();
                });
            }
        }, 1000);
    }
});
