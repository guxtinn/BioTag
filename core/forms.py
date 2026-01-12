# core/forms.py (Atualizado)
from .models import Animal
from django import forms

class LoginForm(forms.Form):
    # O campo é chamado 'username' porque a view de login padrão espera esse nome
    # mas o rótulo e o placeholder indicam que é o email/username.
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Email ou Usuário'}), # <--- Atualizado
        label='Email ou Usuário' # <--- Atualizado
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        label='Senha'
    )
class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        # Excluímos campos de controle (admin_responsavel, datas) 
        # e campos que o admin não deve ver (id_tag_nfc deve ser preenchido)
        exclude = ('admin_responsavel', 'data_cadastro', 'ultima_atualizacao', 'id_tag_nfc')
        
        # Opcional: Adicionar classes Bootstrap aos campos
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Animal'}),
            'especie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Espécie'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Idade em anos (opcional)'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'historico_veterinario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cuidados_essenciais': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # ImageField já é gerenciado pelo Django, mas precisa do 'enctype' no template
        }