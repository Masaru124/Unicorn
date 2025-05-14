"""
WSGI config for unicorn_analysis project.

It exposes the WSGI callable as a module-level variable named ``application``.

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unicorn_analysis.settings')

application = get_wsgi_application()
