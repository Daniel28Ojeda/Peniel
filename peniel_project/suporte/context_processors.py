from .models import Ticket

def notificacoes_suporte(request):
    """
    Verifica se o usuário logado tem tickets de suporte aguardando sua resposta.
    """
    if request.user.is_authenticated:
        tickets_pendentes = Ticket.objects.filter(
            solicitante=request.user,
            status='aguardando_usuario'
        ).order_by('status_atualizado_em') # Pega o mais antigo pendente primeiro

        primeiro_ticket_pendente = tickets_pendentes.first()

        return {
            'tickets_pendentes_count': tickets_pendentes.count(),
            'primeiro_ticket_pendente': primeiro_ticket_pendente,
        }
    return {}