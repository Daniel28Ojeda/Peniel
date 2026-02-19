from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Filial(models.Model):
    """
    Representa as filiais da igreja (Sede + 2 filiais, por exemplo).
    """
    nome = models.CharField(max_length=100, verbose_name=_("Nome da Filial"))
    codigo = models.CharField(max_length=10, unique=True, verbose_name=_("Código/Sigla"))
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Endereço"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Filial")
        verbose_name_plural = _("Filiais")

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Ministerio(models.Model):
    """
    Representa os ministérios/departamentos da igreja (Ex: Louvor, Infantil, Jovens).
    """
    nome = models.CharField(max_length=100, verbose_name=_("Nome do Ministério"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Ministério")
        verbose_name_plural = _("Ministérios")

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    """
    Usuário personalizado para o sistema Peniel.
    """
    # Perfis adaptados para o contexto de tesouraria
    PERFIL_CHOICES = [
        ('admin', _('Administrador do Sistema')), # Acesso total
        ('tesouraria', _('Tesouraria')),          # Pode aprovar e lançar contas
        ('lider', _('Líder/Solicitante')),        # Apenas solicita adiantamentos/reembolsos
    ]

    filial = models.ForeignKey(
        Filial,
        on_delete=models.PROTECT, # Não permite deletar filial se tiver usuários
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name=_("Filial")
    )

    ministerio = models.ForeignKey(
        Ministerio,
        on_delete=models.SET_NULL, # Se o ministério for deletado, o usuário fica sem ministério, mas não é apagado
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name=_("Ministério Padrão")
    )
    
    perfil = models.CharField(
        max_length=20, 
        choices=PERFIL_CHOICES, 
        default='lider',
        verbose_name=_("Perfil de Acesso")
    )
    
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
