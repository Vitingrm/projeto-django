from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from core.models import Categoria, Veiculo, Cliente, Funcionario, Aluguel, Pagamento
from core.forms import (
    CategoriaForm, VeiculoForm, ClienteForm, FuncionarioForm, 
    AluguelForm, PagamentoForm
)


class SearchMixin:
    """Mixin para adicionar busca em ListView"""
    search_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(q_objects)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class FormMixin:
    """Mixin para adicionar cancel_url em CreateView e UpdateView"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mapeia o model para o nome da lista
        model_name = self.model.__name__.lower()
        list_url_name = f'{model_name}-list'
        context['cancel_url'] = reverse_lazy(list_url_name)
        context['title_form'] = getattr(self, 'title_form', f'{model_name.capitalize()}')
        return context


class DeleteMixin:
    """Mixin para tratar erros de deleção com foreign keys protegidas"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model.__name__.lower()
        list_url_name = f'{model_name}-list'
        context['cancel_url'] = reverse_lazy(list_url_name)
        return context
    
    def post(self, request, *args, **kwargs):
        """Sobrescreve post para capturar ProtectedError"""
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(self.request, f'{self.model.__name__} deletado com sucesso!')
            model_name = self.model.__name__.lower()
            return redirect(reverse(f'{model_name}-list'))
        except ProtectedError as e:
            messages.error(
                self.request,
                f'Não é possível deletar este {self.model.__name__.lower()} pois ele está vinculado a outros registros. Remova as referências primeiro.'
            )
            model_name = self.model.__name__.lower()
            return redirect(reverse(f'{model_name}-list'))


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

class CategoriaListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todas as categorias"""
    model = Categoria
    template_name = 'portal/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['nome', 'descricao']


class CategoriaDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de uma categoria"""
    model = Categoria
    template_name = 'portal/categoria_detail.html'
    context_object_name = 'categoria'
    login_url = 'login'


class CategoriaCreateView(LoginRequiredMixin, FormMixin, CreateView):
    """Criar nova categoria"""
    model = Categoria
    form_class = CategoriaForm
    template_name = 'portal/categoria_form.html'
    success_url = reverse_lazy('categoria-list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar categoria. Verifique os dados.')
        return super().form_invalid(form)


class CategoriaUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class CategoriaDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar categoria"""
    model = Categoria
    template_name = 'portal/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
    login_url = 'login'


# ========================================
# VEÍCULOS
# ========================================

class VeiculoListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todos os veículos"""
    model = Veiculo
    template_name = 'portal/veiculo_list.html'
    context_object_name = 'veiculos'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['placa', 'marca', 'modelo']


class VeiculoDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um veículo"""
    model = Veiculo
    template_name = 'portal/veiculo_detail.html'
    context_object_name = 'veiculo'
    login_url = 'login'


class VeiculoCreateView(LoginRequiredMixin, FormMixin, CreateView):
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


class VeiculoUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class VeiculoDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar veículo"""
    model = Veiculo
    template_name = 'portal/veiculo_confirm_delete.html'
    success_url = reverse_lazy('veiculo-list')
    login_url = 'login'


# ========================================
# CLIENTES
# ========================================

class ClienteListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todos os clientes"""
    model = Cliente
    template_name = 'portal/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['nome', 'cpf', 'email']


class ClienteDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um cliente"""
    model = Cliente
    template_name = 'portal/cliente_detail.html'
    context_object_name = 'cliente'
    login_url = 'login'


class ClienteCreateView(LoginRequiredMixin, FormMixin, CreateView):
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


class ClienteUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class ClienteDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar cliente"""
    model = Cliente
    template_name = 'portal/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')
    login_url = 'login'


# ========================================
# FUNCIONÁRIOS
# ========================================

class FuncionarioListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todos os funcionários"""
    model = Funcionario
    template_name = 'portal/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['nome', 'cargo', 'email']


class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um funcionário"""
    model = Funcionario
    template_name = 'portal/funcionario_detail.html'
    context_object_name = 'funcionario'
    login_url = 'login'


class FuncionarioCreateView(LoginRequiredMixin, FormMixin, CreateView):
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


class FuncionarioUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class FuncionarioDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar funcionário"""
    model = Funcionario
    template_name = 'portal/funcionario_confirm_delete.html'
    success_url = reverse_lazy('funcionario-list')
    login_url = 'login'


# ========================================
# ALUGUÉIS
# ========================================

class AluguelListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todos os aluguéis"""
    model = Aluguel
    template_name = 'portal/aluguel_list.html'
    context_object_name = 'alugueis'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['cliente__nome', 'veiculo__placa', 'status']


class AluguelDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um aluguel"""
    model = Aluguel
    template_name = 'portal/aluguel_detail.html'
    context_object_name = 'aluguel'
    login_url = 'login'


class AluguelCreateView(LoginRequiredMixin, FormMixin, CreateView):
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


class AluguelUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class AluguelDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar aluguel"""
    model = Aluguel
    template_name = 'portal/aluguel_confirm_delete.html'
    success_url = reverse_lazy('aluguel-list')
    login_url = 'login'


# ========================================
# PAGAMENTOS
# ========================================

class PagamentoListView(LoginRequiredMixin, SearchMixin, ListView):
    """Listar todos os pagamentos"""
    model = Pagamento
    template_name = 'portal/pagamento_list.html'
    context_object_name = 'pagamentos'
    paginate_by = 10
    login_url = 'login'
    search_fields = ['aluguel__id', 'status', 'metodo']


class PagamentoDetailView(LoginRequiredMixin, DetailView):
    """Ver detalhes de um pagamento"""
    model = Pagamento
    template_name = 'portal/pagamento_detail.html'
    context_object_name = 'pagamento'
    login_url = 'login'


class PagamentoCreateView(LoginRequiredMixin, FormMixin, CreateView):
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


class PagamentoUpdateView(LoginRequiredMixin, FormMixin, UpdateView):
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


class PagamentoDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Deletar pagamento"""
    model = Pagamento
    template_name = 'portal/pagamento_confirm_delete.html'
    success_url = reverse_lazy('pagamento-list')
    login_url = 'login'

