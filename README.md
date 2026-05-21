# Sistema de Aluguel de Veículos - Django

Sistema de gerenciamento de aluguel de veículos com interface administrativa completa.

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Criar e Ativar o Ambiente Virtual

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 2️⃣ Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 3️⃣ Executar Migrations

```powershell
python manage.py migrate
```

### 4️⃣ Criar Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Preencha com seus dados:
- Username: `admin`
- Email: seu email
- Password: sua senha

### 5️⃣ Rodar o Servidor

```powershell
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000/admin/**

---

## 📁 Estrutura do Projeto

```
aluguel_veiculos/
├── aluguel_veiculos/          # Configuração principal
│   ├── settings.py            # Configurações Django
│   ├── urls.py                # URLs principais
│   ├── wsgi.py                # WSGI config
│   └── asgi.py                # ASGI config
│
├── core/                       # App principal
│   ├── models.py              # Modelos de dados
│   ├── admin.py               # Configuração admin
│   ├── views.py               # Views (futura)
│   ├── urls.py                # URLs (futura)
│   ├── migrations/            # Migrações do banco
│   └── apps.py                # Configuração app
│
├── templates/
│   └── admin/
│       └── extra_head.html    # Customizações admin
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

## 📊 Modelos de Dados

### 🏷️ Categoria
- Nome da categoria (ex: Economy, SUV, Luxury)
- Descrição
- Preço diário em reais

### 🚗 Veículo
- Categoria (relação com Categoria)
- Placa (única)
- Marca
- Modelo
- Ano
- Quilometragem
- Status: disponível, alugado, manutenção

### 👤 Cliente
- Nome
- CPF (único)
- CNH (única)
- Email (único)
- Telefone
- Data de nascimento

### 👨‍💼 Funcionário
- Nome
- CPF (único)
- Cargo
- Email (único)

### 📋 Aluguel
- Cliente (relação)
- Veículo (relação)
- Funcionário responsável (relação)
- Data de início
- Data de fim prevista
- Data de fim real
- Quilometragem inicial
- Quilometragem final
- Status: aberto, encerrado, cancelado

### 💳 Pagamento
- Aluguel (relação 1:1)
- Valor total
- Método: crédito, débito, PIX, dinheiro
- Status: pendente, pago, cancelado
- Data do pagamento

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
- **Interface**: Padrão Django com customizações

---

## 📝 Comandos Úteis

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

---

## 📦 Dependências

- **Django 5.0.1**: Framework web
- **django-unfold 0.31.0**: Admin customizado (opcional)

---

## ✅ Checkpoint 1 - Entregáveis

- ✅ Modelos de dados completos (6 entidades)
- ✅ Banco de dados criado e migrado
- ✅ Interface admin funcional
- ✅ Admin customizado com fieldsets
- ✅ Busca e filtros configurados
- ✅ Relacionamentos funcionando
- ✅ Documento de setup

---

## 📧 Suporte

Para dúvidas sobre o projeto, consulte a documentação do Django em https://docs.djangoproject.com/