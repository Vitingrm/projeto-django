"""
Middleware para tratamento de logout
Redireciona requisições GET em /admin/logout/ para nosso logout seguro
"""

from django.shortcuts import redirect
from django.urls import reverse


class LogoutRedirectMiddleware:
    """
    Middleware que intercepta GET requests em /admin/logout/
    e redireciona para /logout/ (POST)
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Se é GET em /admin/logout/, redireciona para /logout/
        if request.method == 'GET' and request.path == '/admin/logout/':
            return redirect(reverse('logout'))
        
        response = self.get_response(request)
        return response
