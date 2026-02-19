from django import forms
from .models import Ticket, TicketResposta
from django.utils.translation import gettext_lazy as _

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # O campo 'empresa' é omitido intencionalmente, pois será nulo para este formulário.
        fields = ['nome', 'email', 'assunto', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your full name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('your.email@example.com')}),
            'assunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('What is your message about?')}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': _('Describe your problem or question here...')}),
        }
        labels = {
            'nome': _('Your Name'),
            'email': _('Your E-mail'),
            'assunto': _('Subject'),
            'mensagem': _('Message'),
        }

class TicketInternoForm(forms.ModelForm):
    """Formulário para usuários logados abrirem um ticket."""
    class Meta:
        model = Ticket
        fields = ['assunto', 'mensagem']
        widgets = {
            'assunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('A brief summary of the issue')}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': _('Describe the issue with as much detail as possible...')}),
        }
        labels = {
            'assunto': _('Subject'),
            'mensagem': _('Problem Description'),
        }

class TicketRespostaForm(forms.ModelForm):
    """Formulário para adicionar uma resposta a um ticket."""
    class Meta:
        model = TicketResposta
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Type your reply or question here...')}),
        }
        labels = {
            'mensagem': ''  # The label is intentionally left blank for template flexibility
        }