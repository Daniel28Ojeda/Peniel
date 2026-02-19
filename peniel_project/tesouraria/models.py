from django.db import models
from django.utils.translation import gettext_lazy as _

class TipoDespesa(models.Model):
    """
    Tabela de itens/categorias para seleção de despesa (Ex: Alimentação, Combustível).
    """
    nome = models.CharField(max_length=100, verbose_name=_("Nome do Item/Despesa"))
    descricao = models.TextField(blank=True, null=True, verbose_name=_("Descrição"))
    ativo = models.BooleanField(default=True, verbose_name=_("Ativo"))
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Tipo de Despesa")
        verbose_name_plural = _("Tipos de Despesa")
        ordering = ['nome']

    def __str__(self):
        return self.nome
