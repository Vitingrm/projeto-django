# Portal Web com Autenticação e Bootstrap 4

## O que foi implementado

Criamos um **portal web simples e responsivo** com autenticação de usuários (login/logout), separado do painel admin do Grappelli.

### Arquitetura

```
├── /                    → Página inicial (home)
├── /login/             → Login de usuários
├── /dashboard/         → Dashboard protegido (apenas autenticados)
├── /logout/            → Logout
├── /admin/             → Painel administrativo (Grappelli)
└── /grappelli/         → URLs do Grappelli
```

## Estrutura de Arquivos

### Templates Criados

1. **templates/base.html** 
   - Template base com Bootstrap 4
   - Navbar com navegação e indicação de usuário
   - Footer
   - Sistema de mensagens Django
   - CSS customizado (fonte, cores, responsividade)

2. **templates/login.html**
   - Formulário de login responsivo
   - Validação de erros
   - Design limpo e profissional

3. **templates/dashboard.html**
   - Dashboard pós-autenticação
   - Cards com informações do usuário
   - Link para admin (se autorizado)
   - Bem-vindo personalizado

4. **templates/home.html**
   - Página inicial pública
   - Hero section
   - Cards de recursos
   - Call-to-action

### Views Criadas (core/views.py)

```python
# Classe personalizada para Login
CustomLoginView(LoginView)
    - Usa template 'login.html'
    - Redireciona usuários já autenticados

# Classe personalizada para Logout
CustomLogoutView(LogoutView)
    - Redireciona para home

# Class-based view do Dashboard
DashboardView(LoginRequiredMixin, TemplateView)
    - Protegida com @LoginRequiredMixin
    - Requer autenticação

# Function-based views
home()                    → Página inicial
dashboard()              → Dashboard (com @login_required)
```

### URLs Configuradas (aluguel_veiculos/urls.py)

```python
''                   → home (name='home')
'login/'             → CustomLoginView (name='login')
'logout/'            → CustomLogoutView (name='logout')
'dashboard/'         → dashboard view (name='dashboard')
'admin/'             → Django Admin com Grappelli
'grappelli/'         → URLs do Grappelli
```

### Configurações adicionadas (aluguel_veiculos/settings.py)

```python
LOGIN_URL = 'login'              # URL para redirecionar usuários não autenticados
LOGIN_REDIRECT_URL = 'dashboard' # URL pós-login
LOGOUT_REDIRECT_URL = 'home'     # URL pós-logout
```

## Design & Responsividade

### Bootstrap 4 (via CDN)
- **Navbar** responsiva com toggle em mobile
- **Cards** para organizar informações
- **Grid system** (12 colunas) para layout responsivo
- **Formulários** com Bootstrap styling
- **Alerts** para mensagens do sistema

### Customizações CSS
- Cores consistentes (#2563eb para primário)
- Contraste adequado para acessibilidade
- Hover states para melhor UX
- Footer fixed no bottom
- Responsive em mobile, tablet, desktop

## Como Usar

### 1. Iniciar o servidor
```bash
python manage.py runserver
```

### 2. Acessar o portal
- Home: http://localhost:8000/
- Login: http://localhost:8000/login/
- Dashboard: http://localhost:8000/dashboard/ (requer autenticação)
- Admin: http://localhost:8000/admin/ (requer staff)

### 3. Criar usuários de teste

```bash
python manage.py createsuperuser
# ou
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user(username='teste', password='senha123')
```

### 4. Testar o fluxo

1. Acesse http://localhost:8000/
2. Clique em "Fazer Login"
3. Digite credenciais (user: teste, password: senha123)
4. Será redirecionado para /dashboard/
5. Clique em "Sair" para fazer logout

## Segurança

- ✅ CSRF Protection ({% csrf_token %} em formulários)
- ✅ Senhas nunca são exibidas
- ✅ @login_required protege views
- ✅ Sessões gerenciadas pelo Django
- ✅ Autenticação via Django's built-in auth

## Principais características

| Recurso | Status |
|---------|--------|
| Login/Logout | ✅ Completo |
| Dashboard | ✅ Completo |
| Responsividade | ✅ Completo |
| Bootstrap 4 | ✅ Integrado via CDN |
| Mensagens de erro | ✅ Integradas |
| Dark mode CSS | ✅ Suportado |
| Proteção de rotas | ✅ Ativa |

## Próximos passos opcionais

1. Adicionar página de perfil do usuário
2. Criar page para trocar senha
3. Adicionar recuperação de senha (forgot password)
4. Integrar com suas models (Veiculo, Aluguel, etc.)
5. Criar dashboard com estatísticas

## Todos os modelos continuam funcionando

- ✅ Validações clean() continuam ativas
- ✅ Admin models continuam no Grappelli
- ✅ Banco de dados relacional intacto
- ✅ Filtros e inline admins continuam
- ✅ JSONField features continuam funcionando

---

**Nota**: Django's built-in authentication é simples, maduro e seguro para este projeto. Apenas login/logout foi implementado como solicitado.
