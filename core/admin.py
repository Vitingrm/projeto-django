from django.contrib import admin
from .models import Categoria, Veiculo, Cliente, Funcionario, Aluguel, Pagamento


# Inline para Pagamento dentro de Aluguel
class PagamentoInline(admin.StackedInline):
    """Inline para exibir Pagamento dentro do Aluguel."""
    model = Pagamento
    extra = 0
    fields = ('valor_total', 'metodo', 'status', 'data_pagamento')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para Categoria."""
    list_display = ['nome', 'preco_diaria']
    search_fields = ['nome']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'preco_diaria')
        }),
        ('Descrição', {
            'fields': ('descricao',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    """Admin para Veículo."""
    list_display = ['placa', 'marca', 'modelo', 'ano', 'categoria', 'status']
    search_fields = ['placa', 'marca', 'modelo']
    list_filter = ['status', 'categoria', 'ano']
    ordering = ['placa']
    
    fieldsets = (
        ('Informações do Veículo', {
            'fields': ('placa', 'marca', 'modelo', 'ano', 'categoria')
        }),
        ('Condição', {
            'fields': ('quilometragem', 'status')
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para Cliente."""
    list_display = ['nome', 'cpf', 'cnh', 'email', 'telefone']
    search_fields = ['nome', 'cpf', 'email']
    list_filter = ['data_nascimento']
    ordering = ['nome']
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'cpf', 'data_nascimento')
        }),
        ('Documentação', {
            'fields': ('cnh',)
        }),
        ('Contato', {
            'fields': ('email', 'telefone')
        }),
    )


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    """Admin para Funcionário."""
    list_display = ['nome', 'cpf', 'cargo', 'email']
    search_fields = ['nome', 'cpf', 'email']
    list_filter = ['cargo']
    ordering = ['nome']
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'cpf')
        }),
        ('Informações Profissionais', {
            'fields': ('cargo', 'email')
        }),
    )


@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    """Admin para Aluguel."""
    list_display = ['id', 'cliente', 'veiculo', 'data_retirada', 'data_devolucao_prevista', 'status']
    list_filter = ['status', 'data_retirada']
    search_fields = ['cliente__nome', 'veiculo__placa']
    inlines = [PagamentoInline]
    ordering = ['-data_retirada']
    
    fieldsets = (
        ('Informações do Aluguel', {
            'fields': ('cliente', 'veiculo', 'funcionario', 'status')
        }),
        ('Datas', {
            'fields': ('data_retirada', 'data_devolucao_prevista', 'data_devolucao_real')
        }),
        ('Quilometragem', {
            'fields': ('km_inicial', 'km_final'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    """Admin para Pagamento."""
    list_display = ['id', 'aluguel', 'valor_total', 'metodo', 'status']
    list_filter = ['status', 'metodo', 'data_pagamento']
    search_fields = ['aluguel__id']
    ordering = ['-data_pagamento']
    
    fieldsets = (
        ('Informações de Pagamento', {
            'fields': ('aluguel', 'valor_total', 'metodo', 'status')
        }),
        ('Data de Pagamento', {
            'fields': ('data_pagamento',),
            'classes': ('collapse',)
        }),
    )


# Customizar headers do site
admin.site.site_header = "Aluguel de Veículos - Administração"
admin.site.site_title = "Admin - Aluguel de Veículos"
admin.site.index_title = "Bem-vindo ao painel administrativo"
