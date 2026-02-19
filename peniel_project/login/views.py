import time
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    # 1. Verifica se o usuário já está bloqueado por excesso de tentativas
    lockout_time = request.session.get('lockout_time')
    if lockout_time and time.time() < lockout_time:
        remaining_time = int(lockout_time - time.time())
        # Em vez de uma mensagem, passamos o contexto para ativar o popup
        context = {
            'form': LoginForm(),
            'lockout_active': True,
            'lockout_duration': remaining_time
        }
        return render(request, 'login/login.html', context)

    # Se já estiver logado, redireciona para a home do sistema
    if request.user.is_authenticated:
        return redirect('core:home')

    form = LoginForm() # Instancia para o caso de ser um GET
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # 2. Sucesso no login
            user = form.get_user()
            login(request, user)

            # Limpa o contador de falhas da sessão em caso de sucesso
            if 'failed_attempts' in request.session:
                del request.session['failed_attempts']
            if 'lockout_time' in request.session:
                del request.session['lockout_time']

            return redirect('core:home')
        else:
            # 3. Falha no login: adiciona feedback e controle de força bruta
            # Incrementa o contador de tentativas falhas na sessão
            failed_attempts = request.session.get('failed_attempts', 0) + 1
            request.session['failed_attempts'] = failed_attempts

            if failed_attempts >= 5:
                # Bloqueia por 60 segundos e remove o contador de tentativas
                lockout_duration = 60
                request.session['lockout_time'] = time.time() + lockout_duration
                if 'failed_attempts' in request.session:
                    del request.session['failed_attempts']
                # Passa o contexto para ativar o popup na primeira vez que o bloqueio ocorre
                context = {
                    'form': LoginForm(),
                    'lockout_active': True,
                    'lockout_duration': lockout_duration
                }
                return render(request, 'login/login.html', context)
            else:
                # A mensagem de erro do AuthenticationForm já é genérica e segura.
                # Adicionamos uma mensagem explícita para garantir o feedback.
                messages.error(request, 'E-mail ou senha inválidos.')
    
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login:login')