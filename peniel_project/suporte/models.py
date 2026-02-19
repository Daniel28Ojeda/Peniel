from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_analise', 'Em Análise'),
        ('aguardando_usuario', 'Aguardando Usuário'),
        ('resolvido', 'Resolvido'),
    ]

    # Solicitante opcional para permitir tickets anônimos ou via formulário público
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name='Solicitante'
    )
    
    # Campos para identificar o usuário (logado ou não) e o conteúdo
    nome = models.CharField(max_length=100, verbose_name='Nome', null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', null=True, blank=True)
    assunto = models.CharField(max_length=200, verbose_name='Assunto')
    mensagem = models.TextField(verbose_name='Mensagem')
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name='Status'
    )
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    status_atualizado_em = models.DateTimeField(default=timezone.now, verbose_name='Status atualizado em')

    class Meta:
        verbose_name = 'Ticket de Suporte'
        verbose_name_plural = 'Tickets de Suporte'
        ordering = ['-criado_em']

    def __str__(self):
        return f"#{self.id} - {self.assunto}"
    
    def save(self, *args, **kwargs):
        # Se for uma edição e o status mudou, atualiza o timestamp do status
        if self.pk:
            old_instance = Ticket.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                self.status_atualizado_em = timezone.now()
        super().save(*args, **kwargs)

class TicketResposta(models.Model):
    """ Armazena uma resposta ou comentário em um ticket de suporte. """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='respostas', verbose_name=_("Ticket"))
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("User"))
    mensagem = models.TextField(verbose_name=_("Message"))
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))

    def __str__(self):
        author = self.usuario.get_full_name() if self.usuario else _("System")
        return _("Reply from {author} on Ticket #{ticket_pk}").format(author=author, ticket_pk=self.ticket.pk)

    class Meta:
        verbose_name = _("Ticket Reply")
        verbose_name_plural = _("Ticket Replies")
        ordering = ['criado_em']