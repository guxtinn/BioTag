

# Create your models here.
# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Animal(models.Model):
    # A tag NFC como chave primária é uma boa ideia, mas tags são strings longas. 
    # Usaremos um ID automático do Django e a tag como campo único.
    id_tag_nfc = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="ID da Tag NFC/QR Code",
        help_text="Usado para consulta pública"
    )
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea')], blank=True, null=True)
    idade = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True, verbose_name="Foto do Animal")
    historico_veterinario = models.TextField(blank=True)
    cuidados_essenciais = models.TextField(blank=True)
    
    # O Django já tem uma tabela User, vamos usá-la.
    # Usando ForeignKey para registrar o administrador responsável.
    admin_responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, # Se o user for deletado, o campo fica nulo.
        null=True, 
        blank=True, 
        verbose_name="Admin Responsável"
    )
    
    data_cadastro = models.DateTimeField(default=timezone.now)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.id_tag_nfc})"

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        ordering = ['nome']


# A tabela 'Usuarios' da sua proposta (com o campo tipo_perfil)
# pode ser gerenciada com o sistema de permissões embutido do Django.
# Se precisar customizar muito, você usaria AbstractUser/AbstractBaseUser.
# Por enquanto, focaremos na tabela Animal.