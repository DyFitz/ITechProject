"""
WSGI config for srcwebproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Sets default Django settings module for WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srcwebproject.settings')

# Initialises WSGI application to serve Django project
application = get_wsgi_application()