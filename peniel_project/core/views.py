from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'core/home.html')

def check_session(request):
    """
    Verifica se a sessão do usuário ainda está ativa.
    Retorna JSON {'is_authenticated': True/False}.
    """
    # Evita que esta requisição estenda a sessão (opcional, dependendo da config de sessão)
    request.session.modified = False 
    return JsonResponse({'is_authenticated': request.user.is_authenticated})
