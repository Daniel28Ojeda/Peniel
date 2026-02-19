from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Filial, Ministerio, Usuario
from django.utils.translation import gettext_lazy as _

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'ativo', 'criado_em')
    search_fields = ('nome', 'codigo')
    list_filter = ('ativo',)

@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    """
    Configuração da interface de administração para o modelo de Usuário customizado.
    """
    # Adiciona os campos customizados aos fieldsets (edição de usuário)
    fieldsets = UserAdmin.fieldsets + (
        (_('Informações da Igreja'), {'fields': ('filial', 'ministerio', 'perfil', 'telefone')}),
    )
    
    # Adiciona os campos customizados ao formulário de criação de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Informações da Igreja'), {'fields': ('filial', 'ministerio', 'perfil', 'telefone')}),
    )
    
    # Colunas que aparecem na lista de usuários
    list_display = ('username', 'email', 'first_name', 'filial', 'ministerio', 'perfil', 'is_active')
    list_filter = ('filial', 'ministerio', 'perfil', 'is_active')
    search_fields = ('username', 'first_name', 'email')
