# Configuração de Clean Validation e List Field

Este documento descreve as mudanças implementadas no projeto para adicionar validações customizadas (`clean()`) e campos de lista (`list_field`) aos modelos.

## 🎯 O que foi implementado

### 1. **Validações com `clean()`**

Adicionamos método `clean()` em todos os modelos para realizar validações de regra de negócio:

#### **Categoria**

- ✓ Preço da diária deve ser maior que zero

#### **Veiculo**

- ✓ Quilometragem não pode ser negativa
- ✓ Ano do veículo entre 1900 e ano atual
- ✓ Status deve estar nas opções válidas
- ✓ Campo `features` deve ser uma lista válida

#### **Cliente**

- ✓ CPF deve estar no formato: `XXX.XXX.XXX-XX`
- ✓ CNH deve conter apenas números
- ✓ Data de nascimento não pode ser no futuro
- ✓ Cliente deve ser maior de 18 anos

#### **Funcionario**

- ✓ CPF deve estar no formato: `XXX.XXX.XXX-XX`
- ✓ Cargo é obrigatório

#### **Aluguel**

- ✓ Data de devolução prevista deve ser posterior à data de retirada
- ✓ Quilometragem inicial não pode ser negativa
- ✓ Quilometragem final deve ser >= quilometragem inicial
- ✓ Se status = "encerrado", data_devolucao_real é obrigatória
- ✓ Data de devolução real não pode ser anterior à data de retirada

#### **Pagamento**

- ✓ Valor total deve ser maior que zero
- ✓ Se status = "pago", data_pagamento é obrigatória
- ✓ Data de pagamento não pode ser no futuro

### 2. **List Field (JSONField)**

Adicionamos um novo campo `features` no modelo `Veiculo`:

```python
features = models.JSONField(
    default=list,
    blank=True,
    help_text='Lista de features/equipamentos do veículo'
)
```

**Uso:**

```python
# No admin, você pode adicionar features assim:
veiculo.features = ["ar condicionado", "direção hidráulica", "vidro elétrico"]
```

### 3. **Integração com Django Admin**

Todos os `Admin` classes agora chamam `full_clean()` antes de salvar:

```python
def save_model(self, request, obj, form, change):
    """Chama clean() antes de salvar."""
    obj.full_clean()
    super().save_model(request, obj, form, change)
```

### 4. Testar validações

As validações serão ativadas automaticamente:

- **No Django Admin**: Ao tentar salvar um objeto inválido, você verá mensagens de erro
- **Na API/ORM**: Ao chamar `full_clean()` antes de salvar

**Exemplo:**

```python
from core.models import Categoria

# Isso vai gerar ValidationError
cat = Categoria(nome="Luxo", preco_diaria=-10)
cat.full_clean()  # Levanta ValidationError
```

## ⚠️ Notas Importantes

1. **Validações também acontecem no `.save()`**: Se você chamar apenas `save()` sem `full_clean()`, algumas validações do Django padrão serão executadas (como uniqueness de campos). Para validações completas, sempre use `full_clean()`.

2. **Admin já valida automaticamente**: O Django Admin chama `full_clean()` automaticamente, então as validações funcionam perfeitamente na interface.

3. **API/ORM**: Se você usar a ORM direto no código (não via Admin), lembre-se de chamar `full_clean()`:
   ```python
   obj = MyModel(field1=value1)
   obj.full_clean()  # Valida
   obj.save()        # Salva se válido
   ```
