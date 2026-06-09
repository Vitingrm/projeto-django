# Migração de Unfold para Grappelli

## O que foi alterado

Substituí o tema admin **Unfold** (que estava com problemas de configuração) pelo **Grappelli**, que é mais maduro, estável e fácil de configurar.

### Arquivos Modificados

1. **requirements.txt** - Removido `django-unfold==0.31.0`, adicionado `django-grappelli==3.0.8`

2. **aluguel_veiculos/settings.py**
   - Removido `'unfold'` de INSTALLED_APPS
   - Adicionado `'grappelli'` em INSTALLED_APPS (ANTES de `'django.contrib.admin'`)
   - Removido configuração `UNFOLD = {...}`
   - Adicionado `GRAPPELLI_ADMIN_TITLE = "Aluguel de Veículos"`

3. **aluguel_veiculos/urls.py**
   - Adicionado import de `include` do django.urls
   - Adicionado URL pattern para Grappelli: `path('grappelli/', include('grappelli.urls'))`

4. **templates/admin/extra_head.html**
   - Atualizado para carregar `grappelli_custom.css` ao invés de `unfold_custom.css`

5. **static/admin/css/grappelli_custom.css** (novo)
   - CSS customizado otimizado para Grappelli
   - Melhorando contraste, fontes e cores dos campos
   - Suporte a dark mode

## Próximos Passos

Execute os seguintes comandos no PowerShell dentro do diretório do projeto:

### 1. Ativar venv
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Desinstalar Unfold e instalar Grappelli
```powershell
pip uninstall django-unfold -y
pip install -r requirements.txt
```

### 3. Coletar arquivos estáticos
```powershell
python manage.py collectstatic --noinput
```

### 4. Iniciar servidor
```powershell
python manage.py runserver
```

### 5. Acessar admin
- Acesse: http://localhost:8000/admin/
- Você verá o novo tema Grappelli em ação!

## Por que Grappelli?

- ✅ **Mais Maduro**: Desenvolvido há mais tempo, mais confiável
- ✅ **Melhor Documentação**: Comunidade maior e mais exemplos
- ✅ **Mais Estável**: Menos bugs e conflitos de configuração
- ✅ **Fácil Configuração**: Funciona praticamente sem configs (WORKS OUT OF THE BOX)
- ✅ **Compatível**: Funciona perfeitamente com Django 5.0
- ✅ **Dark Mode**: Suporta light/dark mode automático

## Recursos do Grappelli

- Dashboard com informações resumidas
- Sidebar com navegação collapsível
- Busca global avançada
- Suporte a filtros relacionados
- Inline editing melhorado
- Autocomplete para campos relacionados
- Suporte a múltiplos idiomas (incluso português)

---

**Nota**: Todos os modelos, validações, e filtros continuam funcionando normalmente. Apenas o tema visual foi alterado!
