# chatgpt/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('interact/', views.chatgpt_interact, name='chatgpt_interact'),
    path('history/', views.chatgpt_history, name='chatgpt_history'),
]
