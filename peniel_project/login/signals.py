from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.sessions.models import Session

@receiver(user_logged_in)
def remover_sessoes_antigas(sender, request, user, **kwargs):
    """
    Garante que apenas uma sessão exista por usuário.

    Quando um usuário faz um novo login, este sinal é acionado.
    A função verifica se há uma chave de sessão antiga armazenada para o usuário.
    Se houver, a sessão correspondente é excluída, desconectando o usuário
    no dispositivo antigo. A nova chave de sessão é então salva.
    """
    # 1. Busca e deleta a sessão antiga, se existir
    if user.session_key:
        try:
            Session.objects.get(session_key=user.session_key).delete()
        except Session.DoesNotExist:
            pass # A sessão antiga pode já ter expirado ou sido removida

    # 2. Salva a nova chave de sessão no perfil do usuário
    user.session_key = request.session.session_key
    user.save(update_fields=['session_key'])