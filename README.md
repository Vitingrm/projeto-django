# Sistema de Aluguel de Veículos - Django

Sistema de gerenciamento de aluguel de veículos com interface administrativa.

---

Integrantes do Grupo: Victor Gabriel e Bruno Souza

## 🚀 Como Rodar o Projeto

### 🪟 Windows (PowerShell)

#### 1️⃣ Criar e Ativar o Ambiente Virtual

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

#### 2️⃣ Instalar Dependências

```powershell
pip install -r requirements.txt
```

#### 3️⃣ Executar Migrations

```powershell
python manage.py migrate
```

#### 4️⃣ Criar Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Preencha com seus dados:

- Username: `admin`
- Email: seu email
- Password: sua senha

#### 5️⃣ Rodar o Servidor

```powershell
python manage.py runserver
```

Acesse: 
- **Admin**: http://127.0.0.1:8000/admin/
- **Portal**: http://127.0.0.1:8000/

---

### 🐧 Linux (Bash/Zsh)

#### 1️⃣ Criar e Ativar o Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar (Linux/macOS)
source venv/bin/activate
```

#### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 3️⃣ Executar Migrations

```bash
python manage.py migrate
```

#### 4️⃣ Criar Superuser (Admin)

```bash
python manage.py createsuperuser
```

Preencha com seus dados:

- Username: `admin`
- Email: seu email
- Password: sua senha

#### 5️⃣ Rodar o Servidor

```bash
python manage.py runserver
```

Acesse: 
- **Admin**: http://127.0.0.1:8000/admin/
- **Portal**: http://127.0.0.1:8000/

---

## 📁 Estrutura do Projeto

```
projeto-django/
├── aluguel_veiculos/          # Configuração principal
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # URLs principais
│   ├── wsgi.py                # WSGI config
│   └── asgi.py                # ASGI config
│
├── core/                       # App principal
│   ├── models.py              # Modelos com validações clean()
│   ├── views.py               # Views do portal com busca
│   ├── forms.py               # Formulários customizados
│   ├── admin.py               # Admin com filtros customizados
│   ├── middleware.py          # Middleware customizado
│   ├── migrations/            # Migrações do banco
│   └── apps.py                # Configuração app
│
├── templates/
│   ├── base.html              # Template base
│   ├── dashboard.html         # Dashboard do usuário
│   ├── login.html             # Página de login
│   └── portal/                # Templates do portal
│       ├── categoria_list.html    # Listagem com busca
│       ├── veiculo_list.html      # Listagem com busca
│       ├── cliente_list.html      # Listagem com busca
│       ├── funcionario_list.html  # Listagem com busca
│       ├── aluguel_list.html      # Listagem com status e busca
│       ├── pagamento_list.html    # Listagem com valor e busca
│       └── (arquivos de formulário e detalhe)
│
├── static/
│   └── admin/css/             # Estilos customizados
│
├── db.sqlite3                 # Banco de dados
├── manage.py                  # Gerenciador Django
├── requirements.txt           # Dependências
└── README.md                  # Este arquivo
```

---

## ✨ Recursos Implementados

### 🏠 Portal do Usuário

Sistema completo de gerenciamento com autenticação:

- ✅ **Login/Logout**: Acesso seguro ao portal
- ✅ **Dashboard**: Página inicial para usuários autenticados
- ✅ **CRUD Completo**: Criar, ler, atualizar e deletar para todas as entidades
- ✅ **Interface Responsiva**: Com Bootstrap 5

### 🔍 Busca e Filtro

Todas as listagens possuem barra de busca integrada:

- **Categorias**: Busca por nome e descrição
- **Veículos**: Busca por placa, marca, modelo
- **Clientes**: Busca por nome, CPF, email
- **Funcionários**: Busca por nome, cargo, email
- **Aluguéis**: Busca por cliente, placa de veículo, status
- **Pagamentos**: Busca por ID do aluguel, status, método

### 🔐 Validações com `clean()`

Todos os modelos possuem validações robustas de regras de negócio:

- **Categoria**: Preço da diária > 0 ✅ CORRIGIDO (preco_diaria adicionado ao formulário)
- **Veiculo**: Quilometragem, ano válido, status válido, features como lista
- **Cliente**: CPF formato válido, CNH apenas números, cliente ≥ 18 anos
- **Funcionario**: CPF formato válido, cargo obrigatório
- **Aluguel**: Datas válidas, quilometragem válida, regras de encerramento
- **Pagamento**: Valor > 0, datas válidas, regras de status

### 📋 Listagens Melhoradas

- ✅ **Status Visível**: Aluguéis e pagamentos mostram status com badges coloridas
- ✅ **Valores Visíveis**: Categoria mostra preço da diária, pagamentos mostram valor total
- ✅ **Botões de Ação**: Deletar funcionários e pagamentos agora disponíveis
- ✅ **Paginação**: 10 itens por página em todas as listagens

### 📋 List Field (JSONField)

O modelo **Veiculo** possui um campo `features` para armazenar uma lista de equipamentos:

```python
features = models.JSONField(default=list, blank=True)
```

**Exemplos de features:**

- "ar condicionado"
- "GPS"
- "Bluetooth"
- "teto solar"
- "vidro elétrico"

### 🔍 Filtro Customizado de Features

No admin de Veículos, existe um filtro dinâmico que:

- Extrai automaticamente todas as features cadastradas
- Permite filtrar veículos por feature selecionada
- Atualiza dinamicamente quando novas features são adicionadas
- Funciona em qualquer banco de dados (incluindo SQLite)

---

## 🌐 URLs do Portal

Após fazer login, você tem acesso aos seguintes recursos:

```
Dashboard:        /dashboard/

Categorias:       /portal/categorias/
Veículos:         /portal/veiculos/
Clientes:         /portal/clientes/
Funcionários:     /portal/funcionarios/
Aluguéis:         /portal/alugueis/
Pagamentos:       /portal/pagamentos/

Admin Django:     /admin/
```

---

### 🏷️ Categoria

- **nome**: CharField 100, único
- **descricao**: TextField, opcional
- **preco_diaria**: DecimalField 8,2

### 🚗 Veiculo

- **categoria**: ForeignKey → Categoria
- **placa**: CharField 20, único
- **marca**, **modelo**: CharField 50
- **ano**: IntegerField
- **quilometragem**: IntegerField
- **status**: Choices (disponível, alugado, manutenção)
- **features**: JSONField - Lista de equipamentos ⭐ NOVO

### 👤 Cliente

- **nome**: CharField 150
- **cpf**: CharField 14, único (formato: XXX.XXX.XXX-XX)
- **cnh**: CharField 20, único
- **email**: EmailField, único
- **telefone**: CharField 20
- **data_nascimento**: DateField (validado ≥ 18 anos)

### 👨‍💼 Funcionario

- **nome**: CharField 150
- **cpf**: CharField 14, único (formato: XXX.XXX.XXX-XX)
- **cargo**: CharField 100, obrigatório
- **email**: EmailField, único

### 🔖 Aluguel

- **cliente**: ForeignKey → Cliente (PROTECT)
- **veiculo**: ForeignKey → Veiculo (PROTECT)
- **funcionario**: ForeignKey → Funcionario (PROTECT)
- **data_retirada**: DateTimeField
- **data_devolucao_prevista**: DateTimeField
- **data_devolucao_real**: DateTimeField, opcional
- **km_inicial**: IntegerField
- **km_final**: IntegerField, opcional
- **status**: Choices (aberto, encerrado, cancelado)

### 💳 Pagamento

- **aluguel**: OneToOneField → Aluguel (CASCADE)
- **valor_total**: DecimalField 10,2
- **metodo**: Choices (crédito, débito, pix, dinheiro)
- **status**: Choices (pendente, pago, cancelado)
- **data_pagamento**: DateTimeField, opcional

---

## 🎯 Recursos do Admin

### VeiculoAdmin - Destaque

- ✅ Filtro por features (dinâmico)
- ✅ Campo features com editor JSON
- ✅ Validações ao salvar

### Todos os Admins

- ✅ Método `save_model()` com `full_clean()` para validações
- ✅ `list_display` otimizado
- ✅ `search_fields` implementados
- ✅ `list_filter` customizados
- ✅ `fieldsets` organizados

---

##  Notas Importantes

1. **Validações**: Funcionam automaticamente no Admin Django através do método `clean()` em todos os modelos
2. **Features**: Use como lista JSON no campo features do Veículo
3. **Filtro de Features**: Atualiza automaticamente conforme novos veículos são adicionados
4. **SQLite**: Todas as funcionalidades foram otimizadas para SQLite
5. **Admin Customizado**: Interface com django-unfold para melhor UX

---

## 📝 Comandos Úteis

### Windows PowerShell

```powershell
# Criar migrations para mudanças nos modelos
python manage.py makemigrations

# Ver status das migrations
python manage.py showmigrations

# Acessar o shell Django
python manage.py shell

# Resetar migrations (cuidado!)
python manage.py migrate core zero

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

### Linux/macOS

```bash
# Criar migrations para mudanças nos modelos
python manage.py makemigrations

# Ver status das migrations
python manage.py showmigrations

# Acessar o shell Django
python manage.py shell

# Resetar migrations (cuidado!)
python manage.py migrate core zero

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

---

## 🛠️ Configurações Importantes

### Idioma e Timezone

- **Idioma**: Português (Brasil)
- **Timezone**: America/Sao_Paulo

### Banco de Dados

- **Tipo**: SQLite (desenvolvimento)
- **Arquivo**: `db.sqlite3`

### Admin Django

- **URL**: http://127.0.0.1:8000/admin/
- **Usuário Padrão**: admin
- **Interface**: Customizada com django-unfold

---

## 📦 Dependências

- **Django 5.0.1**: Framework web
- **django-unfold 0.31.0**: Admin customizado e moderno
- **python-dateutil 2.8.2**: Utilitários para manipulação de datas

---
