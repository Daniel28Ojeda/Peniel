from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .forms import TicketForm, TicketInternoForm, TicketRespostaForm
from .models import Ticket
from django.utils.translation import gettext as _

def enviar_mensagem_suporte(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your message has been sent successfully! We will contact you soon.'))
            return redirect('suporte:enviar_mensagem') # Redireciona para a mesma página para mostrar a mensagem
        else:
            messages.error(request, _('Please correct the errors in the form.'))
    else:
        form = TicketForm()

    return render(request, 'suporte/suporte_form.html', {'form': form})


@login_required
def listar_tickets(request):
    """
    Lista os tickets de suporte do usuário logado.
    """
    # Parâmetros de ordenação da URL
    sort_by = request.GET.get('sort', '-criado_em') # Padrão: mais recentes primeiro
    direction = request.GET.get('direction', 'desc')

    # Lista de campos permitidos para ordenação para segurança
    allowed_sort_fields = ['pk', 'assunto', 'nome', 'status', 'criado_em', 'status_atualizado_em']
    if sort_by.strip('-') not in allowed_sort_fields:
        sort_by = '-criado_em' # Campo padrão seguro

    # Define a direção da ordenação
    order_prefix = '' if direction == 'asc' else '-'
    # Se o sort_by já tem um prefixo (padrão), não adiciona outro
    order_field = sort_by if sort_by.startswith('-') else f"{order_prefix}{sort_by}"

    # Busca os tickets onde o usuário logado é o solicitante
    tickets_list = Ticket.objects.filter(solicitante=request.user).order_by(order_field)

    # Adiciona paginação para o caso de muitos tickets
    paginator = Paginator(tickets_list, 10)  # 10 tickets por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tickets': page_obj,
        'current_sort': sort_by.strip('-'),
        'current_direction': direction,
    }
    return render(request, 'suporte/listar_tickets.html', context)


@login_required
def criar_ticket(request):
    """
    Permite que um usuário logado crie um novo ticket de suporte.
    """
    if request.method == 'POST':
        form = TicketInternoForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.solicitante = request.user
            ticket.nome = request.user.get_full_name() or request.user.username
            ticket.email = request.user.email
            ticket.save()
            messages.success(request, _('Your ticket has been opened successfully! Our support team will review it shortly.'))
            return redirect('suporte:listar_tickets')
    else:
        form = TicketInternoForm()

    return render(request, 'suporte/criar_ticket.html', {'form': form})


@login_required
def detalhe_ticket(request, ticket_id):
    """
    Exibe os detalhes de um ticket, seu histórico de respostas,
    e permite que o usuário adicione uma nova resposta.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id, solicitante=request.user)
    respostas = ticket.respostas.select_related('usuario').order_by('criado_em')

    if request.method == 'POST':
        # REGRA: Chamados com status 'resolvido' não podem ser respondidos.
        if ticket.status == 'resolvido':
            messages.error(request, _('This ticket is already resolved and cannot be replied to.'))
            return redirect('suporte:detalhe_ticket', ticket_id=ticket.pk)

        form = TicketRespostaForm(request.POST)
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.ticket = ticket
            resposta.usuario = request.user
            resposta.save()
            
            # REGRA: Sempre que um usuário da empresa responde, o status muda para 'aberto'.
            # Isso garante que a equipe de suporte veja a nova interação do cliente.
            ticket.status = 'aberto'
            ticket.save(update_fields=['status', 'status_atualizado_em'])
            
            messages.success(request, _('Your reply has been sent.'))
            return redirect('suporte:detalhe_ticket', ticket_id=ticket.pk)
    else:
        form = TicketRespostaForm()

    context = {'ticket': ticket, 'respostas': respostas, 'form': form}
    return render(request, 'suporte/detalhe_ticket.html', context)