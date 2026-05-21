# Exemplos de Uso: Clean Validation e List Field

## 📚 Exemplos Práticos de Como Usar

### 1. Trabalhar com Veiculo (List Field - Features)

#### Adicionando features via Admin
No Django Admin, vá para adicionar/editar um Veículo e no campo "Features/Equipamentos" adicione uma lista JSON:

```json
["ar condicionado", "direção hidráulica", "vidro elétrico", "teto solar"]
```

#### Acessar features no código

```python
from core.models import Veiculo

# Recuperar um veículo
veiculo = Veiculo.objects.get(placa="ABC1234")

# Acessar as features
print(veiculo.features)
# Saída: ['ar condicionado', 'direção hidráulica', 'vidro elétrico']

# Adicionar uma nova feature
veiculo.features.append("bluetooth")
veiculo.save()

# Verificar se tem uma feature
if "ar condicionado" in veiculo.features:
    print("Tem ar condicionado!")

# Remover uma feature
veiculo.features.remove("vidro elétrico")
veiculo.save()

# Limpar todas as features
veiculo.features = []
veiculo.save()
```

#### Filtrar veículos por features

```python
from django.db.models import Q
import json

# Encontrar todos os veículos que têm "ar condicionado"
# (Nota: depende do banco de dados suportar buscas JSON)
veiculos = Veiculo.objects.filter(features__contains="ar condicionado")

# Ou via Python (funciona em qualquer BD)
veiculos_com_ac = [v for v in Veiculo.objects.all() if "ar condicionado" in v.features]
```

---

### 2. Validações com Clean()

#### Exemplo 1: Criar uma Categoria com validação

```python
from core.models import Categoria
from django.core.exceptions import ValidationError

# Tentativa 1: Preço negativo (vai falhar)
try:
    categoria = Categoria(nome="Econômico", preco_diaria=-50)
    categoria.full_clean()  # Vai levantar ValidationError
except ValidationError as e:
    print(f"Erro: {e.message_dict}")
    # Saída: {'preco_diaria': ['O preço da diária deve ser maior que zero.']}

# Tentativa 2: Preço correto (vai funcionar)
categoria = Categoria(nome="Econômico", preco_diaria=100.00)
categoria.full_clean()  # ✓ Válido
categoria.save()        # ✓ Salvo
```

#### Exemplo 2: Criar um Cliente com validação

```python
from core.models import Cliente
from datetime import date
from django.core.exceptions import ValidationError

# Tentativa 1: CPF em formato errado
try:
    cliente = Cliente(
        nome="João Silva",
        cpf="12345678901",  # Formato errado
        cnh="1234567890",
        email="joao@example.com",
        telefone="11987654321",
        data_nascimento=date(1990, 5, 15)
    )
    cliente.full_clean()
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'cpf': ['CPF deve estar no formato: XXX.XXX.XXX-XX']}

# Tentativa 2: Cliente menor de 18 anos
try:
    cliente = Cliente(
        nome="João Silva",
        cpf="123.456.789-01",  # Formato correto
        cnh="1234567890",
        email="joao@example.com",
        telefone="11987654321",
        data_nascimento=date(2015, 5, 15)  # Muito novo
    )
    cliente.full_clean()
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'data_nascimento': ['Cliente deve ser maior de 18 anos.']}

# Tentativa 3: Dados corretos
cliente = Cliente(
    nome="João Silva",
    cpf="123.456.789-01",
    cnh="1234567890",
    email="joao@example.com",
    telefone="11987654321",
    data_nascimento=date(1990, 5, 15)
)
cliente.full_clean()  # ✓ Válido
cliente.save()        # ✓ Salvo
```

#### Exemplo 3: Criar um Aluguel com validação

```python
from core.models import Aluguel, Cliente, Veiculo, Funcionario
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# Recuperar objetos necessários
cliente = Cliente.objects.first()
veiculo = Veiculo.objects.first()
funcionario = Funcionario.objects.first()

data_retirada = datetime.now()
data_devolucao_errada = data_retirada - timedelta(days=1)  # Antes da retirada!

# Tentativa 1: Data de devolução antes da retirada
try:
    aluguel = Aluguel(
        cliente=cliente,
        veiculo=veiculo,
        funcionario=funcionario,
        data_retirada=data_retirada,
        data_devolucao_prevista=data_devolucao_errada,  # Errado!
        km_inicial=100000,
        status='aberto'
    )
    aluguel.full_clean()
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'data_devolucao_prevista': ['A data de devolução prevista deve ser posterior...']}

# Tentativa 2: Valores corretos
data_devolucao = data_retirada + timedelta(days=5)
aluguel = Aluguel(
    cliente=cliente,
    veiculo=veiculo,
    funcionario=funcionario,
    data_retirada=data_retirada,
    data_devolucao_prevista=data_devolucao,
    km_inicial=100000,
    status='aberto'
)
aluguel.full_clean()  # ✓ Válido
aluguel.save()        # ✓ Salvo

# Tentativa 3: Encerrar sem data_devolucao_real
try:
    aluguel.status = 'encerrado'
    aluguel.full_clean()  # Vai falhar
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'data_devolucao_real': ['Data de devolução real é obrigatória...']}

# Tentativa 4: Encerrar com dados corretos
aluguel.data_devolucao_real = datetime.now()
aluguel.km_final = 100250
aluguel.status = 'encerrado'
aluguel.full_clean()  # ✓ Válido
aluguel.save()        # ✓ Salvo
```

#### Exemplo 4: Criar um Pagamento com validação

```python
from core.models import Pagamento
from django.core.exceptions import ValidationError
from decimal import Decimal

aluguel = Aluguel.objects.first()

# Tentativa 1: Valor negativo
try:
    pagamento = Pagamento(
        aluguel=aluguel,
        valor_total=Decimal('-100.00'),  # Negativo!
        metodo='credito',
        status='pendente'
    )
    pagamento.full_clean()
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'valor_total': ['O valor total deve ser maior que zero.']}

# Tentativa 2: Status pago sem data
try:
    pagamento = Pagamento(
        aluguel=aluguel,
        valor_total=Decimal('500.00'),
        metodo='credito',
        status='pago'  # Pago mas sem data!
    )
    pagamento.full_clean()
except ValidationError as e:
    print(e.message_dict)
    # Saída: {'data_pagamento': ['Data de pagamento é obrigatória...']}

# Tentativa 3: Dados corretos
from django.utils import timezone
pagamento = Pagamento(
    aluguel=aluguel,
    valor_total=Decimal('500.00'),
    metodo='credito',
    status='pago',
    data_pagamento=timezone.now()
)
pagamento.full_clean()  # ✓ Válido
pagamento.save()        # ✓ Salvo
```

---

### 3. No Django Admin

Todas as validações funcionam automaticamente no Django Admin! Quando você tenta salvar um objeto inválido, você verá mensagens de erro como:

**Exemplo visual:**
```
⚠️ Erros ao salvar:

• preco_diaria: O preço da diária deve ser maior que zero.

[Salvar e continuar editando] [Salvar] [Excluir] [Voltar]
```

---

### 4. Script de Teste Completo

```python
# save as test_validations.py e execute com:
# python manage.py shell < test_validations.py

from core.models import Veiculo, Cliente, Categoria
from datetime import date
from django.core.exceptions import ValidationError
from decimal import Decimal

print("=" * 60)
print("TESTANDO VALIDAÇÕES")
print("=" * 60)

# Teste 1: Categoria
print("\n[TEST 1] Categoria com preço negativo")
try:
    cat = Categoria(nome="Teste", preco_diaria=Decimal('-50.00'))
    cat.full_clean()
    print("❌ FALHA: Deveria ter levantado ValidationError")
except ValidationError as e:
    print(f"✓ SUCESSO: {e.message_dict['preco_diaria'][0]}")

# Teste 2: Veiculo com ano inválido
print("\n[TEST 2] Veiculo com ano no futuro")
try:
    cat = Categoria.objects.first() or Categoria.objects.create(
        nome="Teste", preco_diaria=Decimal('100.00')
    )
    veh = Veiculo(
        categoria=cat,
        placa="XYZ9999",
        marca="Toyota",
        modelo="Corolla",
        ano=2030,  # Ano no futuro
        quilometragem=0
    )
    veh.full_clean()
    print("❌ FALHA: Deveria ter levantado ValidationError")
except ValidationError as e:
    print(f"✓ SUCESSO: {e.message_dict['ano'][0]}")

# Teste 3: Veiculo com features correto
print("\n[TEST 3] Veiculo com features válidas")
try:
    veh = Veiculo(
        categoria=cat,
        placa="ABC5678",
        marca="Honda",
        modelo="Civic",
        ano=2022,
        quilometragem=50000,
        features=["ar condicionado", "GPS"]
    )
    veh.full_clean()
    print("✓ SUCESSO: Veiculo com features válidas")
except ValidationError as e:
    print(f"❌ FALHA: {e.message_dict}")

# Teste 4: Cliente menor de idade
print("\n[TEST 4] Cliente menor de 18 anos")
try:
    cliente = Cliente(
        nome="Menor",
        cpf="123.456.789-01",
        cnh="1234567890",
        email="menor@test.com",
        telefone="11987654321",
        data_nascimento=date(2020, 1, 1)  # Menor
    )
    cliente.full_clean()
    print("❌ FALHA: Deveria ter levantado ValidationError")
except ValidationError as e:
    print(f"✓ SUCESSO: {e.message_dict['data_nascimento'][0]}")

print("\n" + "=" * 60)
print("TESTES CONCLUÍDOS")
print("=" * 60)
```

---

## 🎓 Dicas Importantes

1. **Sempre chame `full_clean()` antes de `save()`** quando validações são críticas
2. **O admin Django chama automaticamente** `full_clean()`, então as validações funcionam perfeitamente lá
3. **JSONField é flexível**: você pode adicionar qualquer estrutura JSON válida no campo `features`
4. **Mensagens de erro são customizáveis**: edite as strings em `models.py` conforme desejar

---

## 🔗 Referências

- [Django ValidationError](https://docs.djangoproject.com/en/5.0/ref/exceptions/#validationerror)
- [Django Model Validation](https://docs.djangoproject.com/en/5.0/ref/models/instances/#django.db.models.Model.full_clean)
- [Django JSONField](https://docs.djangoproject.com/en/5.0/ref/models/fields/#jsonfield)
