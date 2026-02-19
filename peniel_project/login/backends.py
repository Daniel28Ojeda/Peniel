from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Autentica utilizando o e-mail em vez do username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Tenta buscar o usuário pelo e-mail
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            # Verifica a senha e se o usuário pode logar (ativo)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
