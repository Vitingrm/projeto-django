# 📋 Checkpoint 1 - Documentação do Projeto

## ✅ Arquivos Criados

### 1. `requirements.txt`
**Dependências do projeto:**
- Django 5.0.1
- django-unfold 0.31.1

---

### 2. `aluguel_veiculos/settings.py`
**Configurações principais:**
- ✅ Unfold registrado **antes** de `django.contrib.admin`
- ✅ App `core` adicionado a `INSTALLED_APPS`
- ✅ Banco de dados: SQLite
- ✅ Idioma: Português brasileiro (`pt-br`)
- ✅ Timezone: São Paulo (`America/Sao_Paulo`)

---

### 3. `core/models.py`
**6 Entidades criadas:**

#### Categoria
- `nome` (CharField 100, único)
- `descricao` (TextField, opcional)
- `preco_diaria` (DecimalField 8,2)

#### Veiculo
- `categoria` (ForeignKey → Categoria)
- `placa` (CharField 20, único)
- `marca`, `modelo` (CharField 50)
- `ano` (IntegerField)
- `quilometragem` (IntegerField)
- `status` (Choices: disponível, alugado, manutenção)

#### Cliente
- `nome` (CharField 150)
- `cpf`, `cnh` (CharField, únicos)
- `email` (EmailField, único)
- `telefone` (CharField 20)
- `data_nascimento` (DateField)

#### Funcionario
- `nome` (CharField 150)
- `cpf` (CharField 14, único)
- `cargo` (CharField 100)
- `email` (EmailField, único)

#### Aluguel
- `cliente` (ForeignKey → Cliente, PROTECT)
- `veiculo` (ForeignKey → Veiculo, PROTECT)
- `funcionario` (ForeignKey → Funcionario, PROTECT)
- `data_retirada`, `data_devolucao_prevista` (DateTimeField)
- `data_devolucao_real` (DateTimeField, opcional)
- `km_inicial` (IntegerField)
- `km_final` (IntegerField, opcional)
- `status` (Choices: aberto, encerrado, cancelado)

#### Pagamento
- `aluguel` (OneToOneField → Aluguel, CASCADE)
- `valor_total` (DecimalField 10,2)
- `metodo` (Choices: crédito, débito, pix, dinheiro)
- `status` (Choices: pendente, pago, cancelado)
- `data_pagamento` (DateTimeField, opcional)

---

### 4. `core/admin.py`
**Admin usando Unfold:**

#### CategoriaAdmin
- `list_display`: nome, preco_diaria
- `search_fields`: nome

#### VeiculoAdmin ⭐
- `list_display`: placa, marca, modelo, ano, categoria, status
- `search_fields`: placa, marca, modelo
- `list_filter`: status, categoria

#### ClienteAdmin
- `list_display`: nome, cpf, cnh, email, telefone
- `search_fields`: nome, cpf, email

#### FuncionarioAdmin
- `list_display`: nome, cpf, cargo, email
- `search_fields`: nome, cpf, email

#### AluguelAdmin ⭐ com Inline
- `list_display`: id, cliente, veiculo, data_retirada, data_devolucao_prevista, status
- `list_filter`: status
- `search_fields`: cliente__nome, veiculo__placa
- **PagamentoInline** (StackedInline) configurado

#### PagamentoAdmin
- `list_display`: id, aluguel, valor_total, metodo, status
- `list_filter`: status, metodo
- `search_fields`: aluguel__id

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

## ✨ Checkpoint 1 Concluído!

Agora está pronto para o Checkpoint 2 (Views, Templates e URLs).
