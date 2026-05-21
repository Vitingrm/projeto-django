# Instalar o Python

Se necessário, instale o Python pelo link: https://www.python.org/downloads/

Verifique a versão instalada:

```powershell
python --version
```

---

# Instalar o Pip

Se necessário, instale o pip:

```powershell
python -m pip install --upgrade pip
```

Verifique a versão instalada:

```powershell
python -m pip --version
```

---

# Abrir o Visual Studio Code

Abra a pasta do projeto no VS Code:

```powershell
code .
```

---

# Criar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```powershell
python -m venv venv
```

**Observação:** no exemplo acima, o segundo `venv` é o nome que escolhemos para o nosso ambiente virtual (isso pode ser alterado).

---

# Ativar o Ambiente Virtual

Ative o ambiente virtual no seu computador utilizando o comando:

```powershell
venv\Scripts\activate
```

Para sair do ambiente virtual:

```powershell
deactivate
```

---

# Instalar as Dependências

Instale as dependências do projeto (Django e django-unfold):

```powershell
pip install -r requirements.txt
```

Verifique a versão instalada:

```powershell
pip show django
```

ou

```powershell
python -m pip show django
```

---

# Criar o Projeto Django

Crie o projeto Django com o nome especificado:

```powershell
django-admin startproject aluguel_veiculos .
```

---

# Criar a Aplicação Core

Crie a aplicação core dentro do projeto:

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
