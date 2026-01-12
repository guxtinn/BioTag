# core/urls.py (Atualizado)
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.cadastro_view, name='registro'), # Rota para cadastro de novos usuários
    # Rotas de Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home_view, name='home'),
    path('consulta/<str:tag_id>/', views.consulta_publica_view, name='consulta_publica'),
    path('cadastro/', views.cadastro_animal_view, name='cadastro_animal'),
    path('scanner/', views.scanner_view, name='scanner'), # <--- NOVA ROTA
    path('animal/excluir/<str:id_tag_nfc>/', views.excluir_animal, name='excluir_animal'),
    path('animal/editar/<str:id_tag_nfc>/', views.editar_animal, name='editar_animal'),
    path('qr-code/<str:tag_id>/', views.gerar_qr_code, name='gerar_qr_code'),

]