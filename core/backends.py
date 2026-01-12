# core/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Obtém o modelo de usuário padrão do Django
UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Permite a autenticação usando email OU username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta encontrar o usuário pelo username ou pelo email.
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Usuário não encontrado
            return None
        
        # Verifica a senha para o usuário encontrado
        if user.check_password(password):
            return user
        
        # Senha inválida
        return None