# core/admin.py
from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista do painel
    list_display = ('nome', 'especie', 'id_tag_nfc', 'admin_responsavel', 'ultima_atualizacao')
    
    # Campos que podem ser usados para buscar
    search_fields = ('nome', 'id_tag_nfc', 'especie')
    
    # Campos de filtro lateral
    list_filter = ('especie', 'admin_responsavel', 'data_cadastro')
    
    # Define a ordem dos campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('nome', 'especie', 'id_tag_nfc', 'data_nascimento', 'idade', 'foto')
        }),
        ('Informações de Saúde e Cuidados', {
            'fields': ('historico_veterinario', 'cuidados_essenciais'),
            'classes': ('collapse',) # Torna a seção recolhível para economizar espaço
        }),
        ('Controle do Sistema', {
            'fields': ('admin_responsavel', 'data_cadastro', 'ultima_atualizacao'),
            'classes': ('collapse',),
        }),
    )

    # Preenche automaticamente o campo 'admin_responsavel' com o usuário logado
    def save_model(self, request, obj, form, change):
        if not obj.admin_responsavel:
            obj.admin_responsavel = request.user
        super().save_model(request, obj, form, change)
    def has_change_permission(self, request, obj=None):
        if obj is None: # Permite ver a lista
            return True
        # Superusuários (equipe de TI) podem editar tudo
        if request.user.is_superuser:
            return True
        # Permite edição se o usuário logado for o responsável
        return obj.admin_responsavel == request.user

    # 2. Permite deletar apenas se for o admin responsável ou um superusuário
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.admin_responsavel == request.user
    # Garante que campos de controle (como admin e datas) não sejam editáveis manualmente
    readonly_fields = ('admin_responsavel', 'data_cadastro', 'ultima_atualizacao')