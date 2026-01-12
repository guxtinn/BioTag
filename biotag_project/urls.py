# biotag_project/urls.py (Atualizado)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <--- Importar settings
from django.conf.urls.static import static # <--- Importar static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Apenas no ambiente de desenvolvimento, adiciona rotas para servir arquivos de mídia e estáticos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Se você quiser garantir que os estáticos também são servidos (opcional, mas bom ter)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)