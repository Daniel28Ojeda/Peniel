/**
 * session_check.js
 *
 * Este script verifica periodicamente o status da sessão do usuário com o servidor
 * para implementar um logout automático por inatividade.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Pega a URL para verificação da sessão, que deve ser fornecida no template base.html
    const body = document.body;
    const sessionCheckUrl = body.dataset.sessionCheckUrl;
    const loginUrl = body.dataset.loginUrl || '/'; // Fallback para a raiz se não definido

    // Se a URL não for encontrada, o script não faz nada e avisa no console.
    if (!sessionCheckUrl) {
        return;
    }

    // Intervalo de verificação em milissegundos (ex: 60000ms = 1 minuto)
    const CHECK_INTERVAL = 60000;

    let sessionInterval;

    /**
     * Função que faz a chamada fetch para o backend para verificar o status da sessão.
     */
    const checkSessionStatus = async () => {
        try {
            const response = await fetch(sessionCheckUrl);

            if (!response.ok) {
                // Se a resposta não for OK (ex: erro 500), para de verificar para evitar loops de erro.
                console.error('Erro ao verificar a sessão. Interrompendo verificações.', response.statusText);
                clearInterval(sessionInterval);
                return;
            }

            const data = await response.json();

            // Se o backend informar que a sessão não está mais ativa...
            if (data.session_active === false) {
                clearInterval(sessionInterval); // Para de verificar
                
                // Tenta abrir o modal definido no base.html
                const modalElement = document.getElementById('sessionExpiredModal');
                if (modalElement) {
                    const modal = new bootstrap.Modal(modalElement);
                    modal.show();

                    // Configura o botão OK do modal para redirecionar
                    const okBtn = document.getElementById('sessionExpiredOkButton');
                    if (okBtn) {
                        okBtn.addEventListener('click', () => {
                            window.location.href = loginUrl;
                        });
                    }
                } else {
                    // Fallback caso o modal não exista no HTML
                    alert('Sua sessão expirou. Você será redirecionado.');
                    window.location.href = loginUrl;
                }
            }
        } catch (error) {
            console.error('Erro de rede ao verificar a sessão:', error);
            clearInterval(sessionInterval); // Para em caso de falha de rede
        }
    };

    // Inicia a verificação periódica
    sessionInterval = setInterval(checkSessionStatus, CHECK_INTERVAL);
});
