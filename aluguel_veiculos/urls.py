from django.contrib import admin
from django.urls import path, include
from core.views import (
    CustomLoginView, logout_view, home, dashboard, admin_logout_redirect,
    # Categorias
    CategoriaListView, CategoriaDetailView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    # Veículos
    VeiculoListView, VeiculoDetailView, VeiculoCreateView, VeiculoUpdateView, VeiculoDeleteView,
    # Clientes
    ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    # Funcionários
    FuncionarioListView, FuncionarioDetailView, FuncionarioCreateView, FuncionarioUpdateView, FuncionarioDeleteView,
    # Aluguéis
    AluguelListView, AluguelDetailView, AluguelCreateView, AluguelUpdateView, AluguelDeleteView,
    # Pagamentos
    PagamentoListView, PagamentoDetailView, PagamentoCreateView, PagamentoUpdateView, PagamentoDeleteView,
)

# Customização do site admin
admin.site.site_header = "Aluguel de Veículos - Administração"
admin.site.site_title = "Admin - Aluguel de Veículos"
admin.site.index_title = "Bem-vindo ao painel administrativo"

urlpatterns = [
    # Portal de usuários
    path('', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Categorias
    path('portal/categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('portal/categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    path('portal/categorias/nova/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('portal/categorias/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('portal/categorias/<int:pk>/deletar/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    
    # Veículos
    path('portal/veiculos/', VeiculoListView.as_view(), name='veiculo-list'),
    path('portal/veiculos/<int:pk>/', VeiculoDetailView.as_view(), name='veiculo-detail'),
    path('portal/veiculos/novo/', VeiculoCreateView.as_view(), name='veiculo-create'),
    path('portal/veiculos/<int:pk>/editar/', VeiculoUpdateView.as_view(), name='veiculo-update'),
    path('portal/veiculos/<int:pk>/deletar/', VeiculoDeleteView.as_view(), name='veiculo-delete'),
    
    # Clientes
    path('portal/clientes/', ClienteListView.as_view(), name='cliente-list'),
    path('portal/clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('portal/clientes/novo/', ClienteCreateView.as_view(), name='cliente-create'),
    path('portal/clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente-update'),
    path('portal/clientes/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente-delete'),
    
    # Funcionários
    path('portal/funcionarios/', FuncionarioListView.as_view(), name='funcionario-list'),
    path('portal/funcionarios/<int:pk>/', FuncionarioDetailView.as_view(), name='funcionario-detail'),
    path('portal/funcionarios/novo/', FuncionarioCreateView.as_view(), name='funcionario-create'),
    path('portal/funcionarios/<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('portal/funcionarios/<int:pk>/deletar/', FuncionarioDeleteView.as_view(), name='funcionario-delete'),
    
    # Aluguéis
    path('portal/alugueis/', AluguelListView.as_view(), name='aluguel-list'),
    path('portal/alugueis/<int:pk>/', AluguelDetailView.as_view(), name='aluguel-detail'),
    path('portal/alugueis/novo/', AluguelCreateView.as_view(), name='aluguel-create'),
    path('portal/alugueis/<int:pk>/editar/', AluguelUpdateView.as_view(), name='aluguel-update'),
    path('portal/alugueis/<int:pk>/deletar/', AluguelDeleteView.as_view(), name='aluguel-delete'),
    
    # Pagamentos
    path('portal/pagamentos/', PagamentoListView.as_view(), name='pagamento-list'),
    path('portal/pagamentos/<int:pk>/', PagamentoDetailView.as_view(), name='pagamento-detail'),
    path('portal/pagamentos/novo/', PagamentoCreateView.as_view(), name='pagamento-create'),
    path('portal/pagamentos/<int:pk>/editar/', PagamentoUpdateView.as_view(), name='pagamento-update'),
    path('portal/pagamentos/<int:pk>/deletar/', PagamentoDeleteView.as_view(), name='pagamento-delete'),
    
    # Admin
    path('admin/logout/', admin_logout_redirect, name='admin_logout_redirect'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
]
