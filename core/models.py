from django.db import models
from decimal import Decimal


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

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"


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
