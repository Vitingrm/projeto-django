# 📋 Checkpoint 1 - Documentação Completa do Projeto

---

## 📦 Dependências Instaladas

### `requirements.txt`

```
Django==5.0.1
django-unfold==0.31.0
python-dateutil==2.8.2: adicionado para cálculos de idade na validação de Cliente.
```

---

## ⚙️ Configurações Django

### `aluguel_veiculos/settings.py`

- ✅ Unfold registrado **antes** de `django.contrib.admin`
- ✅ App `core` adicionado a `INSTALLED_APPS`
- ✅ Banco de dados: SQLite
- ✅ Idioma: Português brasileiro (`pt-br`)
- ✅ Timezone: São Paulo (`America/Sao_Paulo`)

---

## 📊 Modelos de Dados com Validações

### `core/models.py` - 6 Entidades

#### 1️⃣ **Categoria**

```python
- nome (CharField 100, único)
- descricao (TextField, opcional)
- preco_diaria (DecimalField 8,2)

Validações:
  ✓ Preço da diária deve ser > 0
```

#### 2️⃣ **Veiculo** ⭐ COM FEATURES

```python
- categoria (ForeignKey → Categoria)
- placa (CharField 20, único)
- marca (CharField 50)
- modelo (CharField 50)
- ano (IntegerField)
- quilometragem (IntegerField)
- status (Choices: disponível, alugado, manutenção)
- features (JSONField) ← Lista de equipamentos

Validações:
  ✓ Quilometragem ≥ 0
  ✓ Ano entre 1900 e ano atual
  ✓ Status deve estar nas opções válidas
  ✓ Features deve ser uma lista
```

#### 3️⃣ **Cliente**

```python
- nome (CharField 150)
- cpf (CharField 14, único)
- cnh (CharField 20, único)
- email (EmailField, único)
- telefone (CharField 20)
- data_nascimento (DateField)

Validações:
  ✓ CPF formato XXX.XXX.XXX-XX
  ✓ CNH apenas números
  ✓ Data de nascimento não no futuro
  ✓ Cliente deve ser ≥ 18 anos
```

#### 4️⃣ **Funcionario**

```python
- nome (CharField 150)
- cpf (CharField 14, único)
- cargo (CharField 100)
- email (EmailField, único)

Validações:
  ✓ CPF formato XXX.XXX.XXX-XX
  ✓ Cargo obrigatório
```

#### 5️⃣ **Aluguel**

```python
- cliente (ForeignKey → Cliente, PROTECT)
- veiculo (ForeignKey → Veiculo, PROTECT)
- funcionario (ForeignKey → Funcionario, PROTECT)
- data_retirada (DateTimeField)
- data_devolucao_prevista (DateTimeField)
- data_devolucao_real (DateTimeField, opcional)
- km_inicial (IntegerField)
- km_final (IntegerField, opcional)
- status (Choices: aberto, encerrado, cancelado)

Validações:
  ✓ Data devolução > data retirada
  ✓ Quilometragem ≥ 0
  ✓ KM final ≥ KM inicial
  ✓ Encerrado requer data_devolucao_real
  ✓ Data real não anterior à data retirada
```

#### 6️⃣ **Pagamento**

```python
- aluguel (OneToOneField → Aluguel, CASCADE)
- valor_total (DecimalField 10,2)
- metodo (Choices: crédito, débito, pix, dinheiro)
- status (Choices: pendente, pago, cancelado)
- data_pagamento (DateTimeField, opcional)

Validações:
  ✓ Valor total > 0
  ✓ Pago requer data_pagamento
  ✓ Data não no futuro
```

---

## 🎨 Admin Interface

### `core/admin.py` - Totalmente Configurado

#### CategoriaAdmin

```python
list_display: [nome, preco_diaria]
search_fields: [nome]
ordering: [nome]
fieldsets: Informações Básicas | Descrição
Validação: full_clean() no save_model()
```

#### VeiculoAdmin COM FILTRO DE FEATURES

```python
list_display: [placa, marca, modelo, ano, categoria, status]
search_fields: [placa, marca, modelo]
list_filter: [status, categoria, ano, FeatureListFilter] ← NOVO
ordering: [placa]
fieldsets:
  - Informações do Veículo
  - Condição
  - Features/Equipamentos
Validação: full_clean() no save_model()
```

#### ClienteAdmin

```python
list_display: [nome, cpf, cnh, email, telefone]
search_fields: [nome, cpf, email]
list_filter: [data_nascimento]
fieldsets: Dados Pessoais | Documentação | Contato
Validação: full_clean() no save_model()
```

#### FuncionarioAdmin

```python
list_display: [nome, cpf, cargo, email]
search_fields: [nome, cpf, email]
list_filter: [cargo]
fieldsets: Dados Pessoais | Informações Profissionais
Validação: full_clean() no save_model()
```

#### AluguelAdmin COM INLINE

```python
list_display: [id, cliente, veiculo, data_retirada, data_devolucao_prevista, status]
list_filter: [status, data_retirada]
search_fields: [cliente__nome, veiculo__placa]
inlines: [PagamentoInline]
fieldsets:
  - Informações do Aluguel
  - Datas
  - Quilometragem (collapse)
Validação: full_clean() no save_model()
```

#### PagamentoAdmin

```python
list_display: [id, aluguel, valor_total, metodo, status]
list_filter: [status, metodo, data_pagamento]
search_fields: [aluguel__id]
fieldsets:
  - Informações de Pagamento
  - Data de Pagamento (collapse)
Validação: ✅ full_clean() no save_model()

Inline: Usado dentro de AluguelAdmin ✅
```

---

## 🔍 Filtro Customizado de Features

### `FeatureListFilter`

```python
class FeatureListFilter(admin.SimpleListFilter):
    title = 'Features/Equipamentos'
    parameter_name = 'feature'

    def lookups(self, request, model_admin):
        # Extrai todas as features únicas dos veículos
        # Retorna em ordem alfabética
        # Só mostra features que existem em algum veículo

    def queryset(self, request, queryset):
        # Filtra veículos com a feature selecionada
        # Funciona em SQLite (filtra em Python)
        # Não usa contains (que SQLite não suporta)
```

**Como funciona:**

1. Usuário abre listagem de Veículos no Admin
2. No painel lateral, vê "Features/Equipamentos"
3. Lista apenas as features cadastradas
4. Clica em uma feature
5. Vê apenas veículos com essa feature

---

## 📝 Validações Implementadas

### Sistema de `clean()` em Todos os Modelos

```python
# Padrão implementado em cada modelo:
def clean(self):
    """Validações customizadas para [Modelo]."""
    errors = {}

    # Validações específicas...

    if errors:
        raise ValidationError(errors)
```

**Vantagens:**

- ✅ Validações executadas no Admin automaticamente
- ✅ Mensagens de erro claras para o usuário
- ✅ Mantém integridade dos dados
- ✅ Regras de negócio enforçadas

**Como funciona:**

```
1. Usuário tenta salvar um objeto inválido no Admin
2. Admin chama obj.full_clean()
3. Método clean() é executado
4. ValidationError é levantado com mensagem
5. Usuário vê mensagem de erro e não consegue salvar
```

---

## 🎯 Recursos Principais

### ✅ Implementados

- [x] 6 Modelos completos
- [x] Validações `clean()` em todos os modelos
- [x] JSONField para armazenar features
- [x] Admin totalmente customizado
- [x] Filtro dinâmico de features
- [x] Inline para Pagamento em Aluguel
- [x] Fieldsets organizados
- [x] Search e list_filter configurados

---

## 🔧 Como Usar

### 1. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 2. Aplicar Migrations

```powershell
python manage.py migrate
```

### 3. Criar Superuser

```powershell
python manage.py createsuperuser
```

### 4. Rodar Servidor

```powershell
python manage.py runserver
```

### 5. Acessar Admin

```
http://127.0.0.1:8000/admin/
```

---

## 🚀 Próximos Passos

1. Crie ambiente virtual: `python -m venv venv`
2. Ative-o: `venv\Scripts\activate` (Windows)
3. Instale dependências: `pip install -r requirements.txt`
4. Execute o comando de setup em `SETUP_COMMANDS.md`
5. Acesse: http://127.0.0.1:8000/admin

---

## 📌 Notas

- Todos os modelos possuem `__str__()` para melhor identificação
- Foreign Keys com `on_delete=PROTECT` garantem integridade referencial
- Unfold oferece interface melhorada em relação ao admin padrão
- SQLite é perfeito para desenvolvimento local
- Admin está totalmente configurado com Unfold (sem templates padrão do Django)

---
