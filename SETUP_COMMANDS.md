# 📚 Comandos de Setup - Sistema de Aluguel de Veículos

## 1️⃣ Instalar o Python

Se necessário, instale o Python pelo link: https://www.python.org/downloads/

Verifique a versão instalada:

```powershell
python --version
```

**Versão recomendada**: Python 3.10+

---

## 2️⃣ Instalar o Pip

Se necessário, instale o pip:

```powershell
python -m pip install --upgrade pip
```

Verifique a versão instalada:

```powershell
python -m pip --version
```

---

## 3️⃣ Abrir o Visual Studio Code

Abra a pasta do projeto no VS Code:

```powershell
code .
```

---

## 4️⃣ Criar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```powershell
python -m venv venv
```

**Observação**: o segundo `venv` é o nome do ambiente virtual (pode ser alterado).

---

## 5️⃣ Ativar o Ambiente Virtual

Ative o ambiente virtual no seu computador:

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**

```cmd
venv\Scripts\activate.bat
```

**Para sair do ambiente virtual:**

```powershell
deactivate
```

---

## 6️⃣ Instalar as Dependências

Instale as dependências do projeto:

```powershell
pip install -r requirements.txt
```

**Dependências instaladas:**

- Django 5.0.1
- django-unfold 0.31.0
- python-dateutil 2.8.2 (novo - para validações)

Verifique as versões:

```powershell
pip show django
pip show django-unfold
pip show python-dateutil
```

---

## 7️⃣ Criar Migrações (se necessário)

Se fez alterações nos modelos, crie uma migração:

```powershell
python manage.py makemigrations
```

---

## 8️⃣ Executar Migrações

Aplique as migrações ao banco de dados:

```powershell
python manage.py migrate
```

---

## 9️⃣ Criar Superuser (Admin)

Crie um usuário administrador:

```powershell
python manage.py createsuperuser
```

Você será solicitado a informar:

- **Username**: seu nome de usuário (ex: `admin`)
- **Email**: seu email
- **Password**: sua senha segura

---

## 🔟 Executar o Servidor

Inicie o servidor Django:

```powershell
python manage.py runserver
```

Você verá:

```
Starting development server at http://127.0.0.1:8000/
```

---

## 1️⃣1️⃣ Acessar o Admin

Abra seu navegador e acesse:

```
http://127.0.0.1:8000/admin/
```

Faça login com o superuser criado.

---

## 🧪 Testando o Sistema

### 1. Criar uma Categoria

1. No Admin, vá para **Categorias**
2. Clique em **+ Adicionar Categoria**
3. Preencha:
   - Nome: "Econômico"
   - Preço Diária: 100.00
4. Clique em **Salvar**

### 2. Criar um Veículo com Features

1. No Admin, vá para **Veículos**
2. Clique em **+ Adicionar Veículo**
3. Preencha os campos obrigatórios
4. No campo **Features/Equipamentos**, adicione:
   ```json
   ["ar condicionado", "GPS", "Bluetooth"]
   ```
5. Clique em **Salvar**

### 3. Testar o Filtro de Features

1. Na listagem de **Veículos**
2. No painel lateral, procure por **"Features/Equipamentos"**
3. Selecione uma feature (ex: "GPS")
4. Observe que apenas veículos com essa feature aparecem

### 4. Testar Validações

1. Tente criar um veículo com **Ano no futuro**
2. Você verá uma mensagem de erro
3. Tente criar um cliente com **menos de 18 anos**
4. Você verá uma mensagem de erro

---

## 📝 Comandos Úteis

### Ver todas as migrações

```powershell
python manage.py showmigrations
```

### Aplicar migração específica

```powershell
python manage.py migrate core 0001
```

### Reverter migrações

```powershell
python manage.py migrate core zero
```

### Abrir shell Django

```powershell
python manage.py shell
```

### Resetar banco de dados (desenvolvimento)

```powershell
python manage.py migrate zero
python manage.py migrate
```

---

## ⚠️ Solução de Problemas

### "Module not found: django"

**Solução**: Ativar ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### "Port 8000 already in use"

**Solução**: Usar outra porta

```powershell
python manage.py runserver 8080
```

### "No migrations applied"

**Solução**: Executar migrations

```powershell
python manage.py migrate
```

### Erro ao filtrar por features

**Solução**: Certifique-se de que há veículos com features cadastradas

---

```powershell
python manage.py startapp core
```

---

# Gerar as Migrations

Gere as migrations baseadas nos modelos criados:

```powershell
python manage.py makemigrations
```

---

# Aplicar as Migrations

Aplique as migrations no banco de dados:

```powershell
python manage.py migrate
```

---

# Criar o Superusuário

Crie um usuário administrador para acessar o admin:

```powershell
python manage.py createsuperuser
```

---

# Executar o Servidor

Inicie o servidor de desenvolvimento Django:

```powershell
python manage.py runserver
```

Acesse o admin em: **http://127.0.0.1:8000/admin**
