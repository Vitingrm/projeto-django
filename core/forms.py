from django import forms
from core.models import Categoria, Veiculo, Cliente, Funcionario, Aluguel, Pagamento


class CategoriaForm(forms.ModelForm):
    """Formulário para criar/editar categorias"""
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição',
                'rows': 3
            }),
        }


class VeiculoForm(forms.ModelForm):
    """Formulário para criar/editar veículos"""
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'marca', 'ano', 'categoria', 'quilometragem', 'status', 'features']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XXX-9999'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Civic'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Honda'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '1900',
                'max': '2099'
            }),
            'quilometragem': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Ar-condicionado\nBanco de couro\nCâmera de ré\nUm item por linha',
                'rows': 3
            }),
        }

    def clean_features(self):
        """Converte textarea em lista Python"""
        features_raw = self.cleaned_data.get('features')
        if isinstance(features_raw, str):
            # Converte linhas em lista
            features = [f.strip() for f in features_raw.split('\n') if f.strip()]
            return features
        return features_raw


class ClienteForm(forms.ModelForm):
    """Formulário para criar/editar clientes"""
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'cnh', 'email', 'telefone', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'cnh': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da CNH'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class FuncionarioForm(forms.ModelForm):
    """Formulário para criar/editar funcionários"""
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'cargo', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Gerente, Vendedor'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
        }


class AluguelForm(forms.ModelForm):
    """Formulário para criar/editar aluguéis"""
    class Meta:
        model = Aluguel
        fields = ['veiculo', 'cliente', 'funcionario', 'data_retirada', 'data_devolucao_prevista', 'km_inicial', 'status']
        widgets = {
            'veiculo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'funcionario': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_retirada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'data_devolucao_prevista': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'km_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class PagamentoForm(forms.ModelForm):
    """Formulário para criar/editar pagamentos"""
    class Meta:
        model = Pagamento
        fields = ['aluguel', 'valor_total', 'metodo', 'status', 'data_pagamento']
        widgets = {
            'aluguel': forms.Select(attrs={
                'class': 'form-control'
            }),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'type': 'number'
            }),
            'metodo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_pagamento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
