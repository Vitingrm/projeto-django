from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import re


class Categoria(models.Model):
    """Modelo para categorias de veículos."""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    preco_diaria = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

    def clean(self):
        """Validações customizadas para Categoria."""
        errors = {}
        
        # Validar preço da diária
        if self.preco_diaria <= 0:
            errors['preco_diaria'] = 'O preço da diária deve ser maior que zero.'
        
        if errors:
            raise ValidationError(errors)


class Veiculo(models.Model):
    """Modelo para veículos disponíveis para aluguel."""
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Manutenção'),
    ]

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='veiculos')
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    quilometragem = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    features = models.JSONField(
        default=list,
        blank=True,
        help_text='Lista de features/equipamentos do veículo (ex: ar condicionado, direção hidráulica, etc.)'
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

    def clean(self):
        """Validações customizadas para Veiculo."""
        errors = {}
        
        # Validar quilometragem
        if self.quilometragem < 0:
            errors['quilometragem'] = 'A quilometragem não pode ser negativa.'
        
        # Validar ano do veículo
        ano_atual = datetime.now().year
        if self.ano < 1900:
            errors['ano'] = 'O ano do veículo deve ser maior que 1900.'
        elif self.ano > ano_atual:
            errors['ano'] = f'O ano do veículo não pode ser maior que {ano_atual}.'
        
        # Validar status
        status_validos = [choice[0] for choice in self.STATUS_CHOICES]
        if self.status not in status_validos:
            errors['status'] = f'Status inválido. Escolha entre: {", ".join(status_validos)}'
        
        # Validar features (deve ser uma lista)
        if not isinstance(self.features, list):
            errors['features'] = 'Features deve ser uma lista.'
        
        if errors:
            raise ValidationError(errors)


class Cliente(models.Model):
    """Modelo para clientes que alugam veículos."""
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    cnh = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome

    def clean(self):
        """Validações customizadas para Cliente."""
        errors = {}
        
        # Validar formato do CPF (xxx.xxx.xxx-xx)
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', self.cpf):
            errors['cpf'] = 'CPF deve estar no formato: XXX.XXX.XXX-XX'
        
        # Validar CNH (número com até 20 dígitos)
        if not self.cnh.replace(' ', '').isdigit():
            errors['cnh'] = 'CNH deve conter apenas números.'
        
        # Validar data de nascimento
        data_hoje = timezone.now().date()
        if self.data_nascimento > data_hoje:
            errors['data_nascimento'] = 'A data de nascimento não pode ser no futuro.'
        
        # Validar idade mínima (maior de idade - 18 anos)
        from dateutil.relativedelta import relativedelta
        idade_minima = data_hoje - relativedelta(years=18)
        if self.data_nascimento > idade_minima:
            errors['data_nascimento'] = 'Cliente deve ser maior de 18 anos.'
        
        if errors:
            raise ValidationError(errors)


class Funcionario(models.Model):
    """Modelo para funcionários que processam aluguéis."""
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    cargo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome

    def clean(self):
        """Validações customizadas para Funcionario."""
        errors = {}
        
        # Validar formato do CPF (xxx.xxx.xxx-xx)
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', self.cpf):
            errors['cpf'] = 'CPF deve estar no formato: XXX.XXX.XXX-XX'
        
        # Validar se cargo não está vazio
        if not self.cargo.strip():
            errors['cargo'] = 'Cargo é obrigatório.'
        
        if errors:
            raise ValidationError(errors)


class Aluguel(models.Model):
    """Modelo para registros de aluguel de veículos."""
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('encerrado', 'Encerrado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='aluguels')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='aluguels')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='aluguels')
    data_retirada = models.DateTimeField()
    data_devolucao_prevista = models.DateTimeField()
    data_devolucao_real = models.DateTimeField(blank=True, null=True)
    km_inicial = models.IntegerField()
    km_final = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')

    class Meta:
        verbose_name = "Aluguel"
        verbose_name_plural = "Aluguéis"

    def __str__(self):
        return f"Aluguel #{self.id} - {self.cliente.nome}"

    def clean(self):
        """Validações customizadas para Aluguel."""
        errors = {}
        
        # Validar se data_devolucao_prevista é posterior a data_retirada
        if self.data_retirada and self.data_devolucao_prevista:
            if self.data_devolucao_prevista <= self.data_retirada:
                errors['data_devolucao_prevista'] = 'A data de devolução prevista deve ser posterior à data de retirada.'
        
        # Validar quilometragem inicial e final
        if self.km_inicial < 0:
            errors['km_inicial'] = 'A quilometragem inicial não pode ser negativa.'
        
        if self.km_final is not None and self.km_final < 0:
            errors['km_final'] = 'A quilometragem final não pode ser negativa.'
        
        if self.km_final is not None and self.km_final < self.km_inicial:
            errors['km_final'] = 'A quilometragem final não pode ser menor que a inicial.'
        
        # Validar se encerrado requer data_devolucao_real
        if self.status == 'encerrado' and not self.data_devolucao_real:
            errors['data_devolucao_real'] = 'Data de devolução real é obrigatória quando o aluguel está encerrado.'
        
        # Se data_devolucao_real está preenchida, não pode ser anterior a data_retirada
        if self.data_devolucao_real and self.data_retirada:
            if self.data_devolucao_real < self.data_retirada:
                errors['data_devolucao_real'] = 'A data de devolução real não pode ser anterior à data de retirada.'
        
        if errors:
            raise ValidationError(errors)


class Pagamento(models.Model):
    """Modelo para registros de pagamento de aluguéis."""
    METODO_CHOICES = [
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    aluguel = models.OneToOneField(Aluguel, on_delete=models.CASCADE, related_name='pagamento')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_pagamento = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def __str__(self):
        return f"Pagamento Aluguel #{self.aluguel.id} - R$ {self.valor_total}"

    def clean(self):
        """Validações customizadas para Pagamento."""
        errors = {}
        
        # Validar valor total
        if self.valor_total <= 0:
            errors['valor_total'] = 'O valor total deve ser maior que zero.'
        
        # Validar se status pago requer data_pagamento
        if self.status == 'pago' and not self.data_pagamento:
            errors['data_pagamento'] = 'Data de pagamento é obrigatória quando o status é "Pago".'
        
        # Se data_pagamento está preenchida, não pode ser no futuro
        if self.data_pagamento and self.data_pagamento > timezone.now():
            errors['data_pagamento'] = 'A data de pagamento não pode ser no futuro.'
        
        if errors:
            raise ValidationError(errors)
