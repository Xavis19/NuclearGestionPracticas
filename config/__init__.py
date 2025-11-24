"""
Este módulo hace que Celery se cargue cuando Django se inicia.
"""

from __future__ import absolute_import, unicode_literals

# Esto asegurará que la app Celery siempre se importe cuando Django se inicie
# Comentado temporalmente hasta instalar celery
# from .celery import app as celery_app

# __all__ = ('celery_app',)
