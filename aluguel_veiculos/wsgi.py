"""
WSGI config for aluguel_veiculos project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aluguel_veiculos.settings')

application = get_wsgi_application()
