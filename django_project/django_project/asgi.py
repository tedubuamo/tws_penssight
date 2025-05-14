"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from my_app.fastapi import app as fastapi_app
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

django_asgi_app = get_asgi_application()

application = Starlette(routes=[
    Mount("/api", app=fastapi_app),
    Mount("/", app=django_asgi_app),
])

