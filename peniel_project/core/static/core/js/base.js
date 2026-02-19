/**
 * base.js
 *
 * Contém scripts globais que são executados em todas as páginas
 * que herdam de 'base.html'.
 */

document.addEventListener('DOMContentLoaded', function() {

    /**
     * Lógica para o Modal de Notificação de Ticket de Suporte.
     */
    const modalTicket = document.getElementById('modalTicketPendente');
    if (modalTicket) {
        const btnOk = document.getElementById('btnOkModalTicket');

        // Mostra o modal
        modalTicket.style.display = 'flex';

        // Fecha o modal ao clicar em "OK"
        btnOk.addEventListener('click', () => modalTicket.style.display = 'none');

        // Fecha o modal ao clicar fora da área de conteúdo
        modalTicket.addEventListener('click', (event) => {
            if (event.target === modalTicket) modalTicket.style.display = 'none';
        });
    }
});
