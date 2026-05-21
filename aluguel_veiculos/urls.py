from django.contrib import admin
from django.urls import path

# Customização do site admin
admin.site.site_header = "Aluguel de Veículos - Administração"
admin.site.site_title = "Admin - Aluguel de Veículos"
admin.site.index_title = "Bem-vindo ao painel administrativo"

urlpatterns = [
    path('admin/', admin.site.urls),
]
