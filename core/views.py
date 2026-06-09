from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from core.models import Categoria, Veiculo, Cliente, Funcionario, Aluguel, Pagamento
from core.forms import (
    CategoriaForm, VeiculoForm, ClienteForm, FuncionarioForm, 
    AluguelForm, PagamentoForm
)


class CustomLoginView(LoginView):
    """View customizada para login usando o template personalizado"""
    template_name = 'login.html'
    redirect_authenticated_user = True


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    View de logout que aceita GET e POST
    Faz logout e redireciona para home
    """
    logout(request)
    return redirect('home')


class DashboardView(LoginRequiredMixin, TemplateView):
    """View do dashboard - apenas para usuários autenticados"""
    template_name = 'dashboard.html'
    login_url = 'login'


def home(request):
    """Página inicial do portal"""
    return render(request, 'home.html')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard do usuário autenticado"""
    return render(request, 'dashboard.html')


@require_http_methods(["GET", "POST"])
def admin_logout_redirect(request):
    """Redireciona qualquer acesso a /admin/logout/ para nosso logout"""
    return redirect('logout')


# ========================================
# CATEGORIAS
# ========================================

class CategoriaListView(LoginRequiredMixin, ListView):
    """Listar todas as categorias"""
    model = Categoria
    template_name = 'portal/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10
    login_url = 'login'


class CategoriaDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de uma categoria"""
    model = Categoria
    template_name = 'portal/categoria_detail.html'
    context_object_name = 'categoria'
    login_url = 'login'


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    """Criar nova categoria"""
    model = Categoria
    form_class = CategoriaForm
    template_name = 'portal/categoria_form.html'
    success_url = reverse_lazy('categoria-list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_form'] = 'Nova Categoria'
        context['cancel_url'] = reverse_lazy('categoria-list')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar categoria. Verifique os dados.')
        return super().form_invalid(form)


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar categoria existente"""
    model = Categoria
    form_class = CategoriaForm
    template_name = 'portal/categoria_form.html'
    success_url = reverse_lazy('categoria-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar categoria. Verifique os dados.')
        return super().form_invalid(form)


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar categoria"""
    model = Categoria
    template_name = 'portal/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Categoria deletada com sucesso!')
        return super().delete(request, *args, **kwargs)


# ========================================
# VEÍCULOS
# ========================================

class VeiculoListView(LoginRequiredMixin, ListView):
    """Listar todos os veículos"""
    model = Veiculo
    template_name = 'portal/veiculo_list.html'
    context_object_name = 'veiculos'
    paginate_by = 10
    login_url = 'login'


class VeiculoDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um veículo"""
    model = Veiculo
    template_name = 'portal/veiculo_detail.html'
    context_object_name = 'veiculo'
    login_url = 'login'


class VeiculoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo veículo"""
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'portal/veiculo_form.html'
    success_url = reverse_lazy('veiculo-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Veículo criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar veículo. Verifique os dados.')
        return super().form_invalid(form)


class VeiculoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar veículo existente"""
    model = Veiculo
    form_class = VeiculoForm
    template_name = 'portal/veiculo_form.html'
    success_url = reverse_lazy('veiculo-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Veículo atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar veículo. Verifique os dados.')
        return super().form_invalid(form)


class VeiculoDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar veículo"""
    model = Veiculo
    template_name = 'portal/veiculo_confirm_delete.html'
    success_url = reverse_lazy('veiculo-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Veículo deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ========================================
# CLIENTES
# ========================================

class ClienteListView(LoginRequiredMixin, ListView):
    """Listar todos os clientes"""
    model = Cliente
    template_name = 'portal/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    login_url = 'login'


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um cliente"""
    model = Cliente
    template_name = 'portal/cliente_detail.html'
    context_object_name = 'cliente'
    login_url = 'login'


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """Criar novo cliente"""
    model = Cliente
    form_class = ClienteForm
    template_name = 'portal/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar cliente. Verifique os dados.')
        return super().form_invalid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """Editar cliente existente"""
    model = Cliente
    form_class = ClienteForm
    template_name = 'portal/cliente_form.html'
    success_url = reverse_lazy('cliente-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar cliente. Verifique os dados.')
        return super().form_invalid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar cliente"""
    model = Cliente
    template_name = 'portal/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ========================================
# FUNCIONÁRIOS
# ========================================

class FuncionarioListView(LoginRequiredMixin, ListView):
    """Listar todos os funcionários"""
    model = Funcionario
    template_name = 'portal/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10
    login_url = 'login'


class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um funcionário"""
    model = Funcionario
    template_name = 'portal/funcionario_detail.html'
    context_object_name = 'funcionario'
    login_url = 'login'


class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    """Criar novo funcionário"""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'portal/funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Funcionário criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar funcionário. Verifique os dados.')
        return super().form_invalid(form)


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    """Editar funcionário existente"""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'portal/funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Funcionário atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar funcionário. Verifique os dados.')
        return super().form_invalid(form)


class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar funcionário"""
    model = Funcionario
    template_name = 'portal/funcionario_confirm_delete.html'
    success_url = reverse_lazy('funcionario-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Funcionário deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ========================================
# ALUGUÉIS
# ========================================

class AluguelListView(LoginRequiredMixin, ListView):
    """Listar todos os aluguéis"""
    model = Aluguel
    template_name = 'portal/aluguel_list.html'
    context_object_name = 'alugueis'
    paginate_by = 10
    login_url = 'login'


class AluguelDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um aluguel"""
    model = Aluguel
    template_name = 'portal/aluguel_detail.html'
    context_object_name = 'aluguel'
    login_url = 'login'


class AluguelCreateView(LoginRequiredMixin, CreateView):
    """Criar novo aluguel"""
    model = Aluguel
    form_class = AluguelForm
    template_name = 'portal/aluguel_form.html'
    success_url = reverse_lazy('aluguel-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Aluguel criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar aluguel. Verifique os dados.')
        return super().form_invalid(form)


class AluguelUpdateView(LoginRequiredMixin, UpdateView):
    """Editar aluguel existente"""
    model = Aluguel
    form_class = AluguelForm
    template_name = 'portal/aluguel_form.html'
    success_url = reverse_lazy('aluguel-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Aluguel atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar aluguel. Verifique os dados.')
        return super().form_invalid(form)


class AluguelDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar aluguel"""
    model = Aluguel
    template_name = 'portal/aluguel_confirm_delete.html'
    success_url = reverse_lazy('aluguel-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Aluguel deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


# ========================================
# PAGAMENTOS
# ========================================

class PagamentoListView(LoginRequiredMixin, ListView):
    """Listar todos os pagamentos"""
    model = Pagamento
    template_name = 'portal/pagamento_list.html'
    context_object_name = 'pagamentos'
    paginate_by = 10
    login_url = 'login'


class PagamentoDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um pagamento"""
    model = Pagamento
    template_name = 'portal/pagamento_detail.html'
    context_object_name = 'pagamento'
    login_url = 'login'


class PagamentoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo pagamento"""
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'portal/pagamento_form.html'
    success_url = reverse_lazy('pagamento-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Pagamento criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar pagamento. Verifique os dados.')
        return super().form_invalid(form)


class PagamentoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar pagamento existente"""
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'portal/pagamento_form.html'
    success_url = reverse_lazy('pagamento-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Pagamento atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar pagamento. Verifique os dados.')
        return super().form_invalid(form)


class PagamentoDeleteView(LoginRequiredMixin, DeleteView):
    """Deletar pagamento"""
    model = Pagamento
    template_name = 'portal/pagamento_confirm_delete.html'
    success_url = reverse_lazy('pagamento-list')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pagamento deletado com sucesso!')
        return super().delete(request, *args, **kwargs)

