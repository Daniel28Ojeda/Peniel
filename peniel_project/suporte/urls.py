from django.urls import path
from . import views

app_name = 'suporte'

urlpatterns = [
    path('fale-conosco/', views.enviar_mensagem_suporte, name='enviar_mensagem'),
    path('meus-tickets/', views.listar_tickets, name='listar_tickets'),
    path('novo-ticket/', views.criar_ticket, name='criar_ticket'),
    path('ticket/<int:ticket_id>/', views.detalhe_ticket, name='detalhe_ticket'),
]
