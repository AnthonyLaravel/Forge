# chatgpt/urls.py
from django.urls import path
from . import views
from .views import chat_request_history

urlpatterns = [
    path('', views.chatgpt_interact, name='chatgpt_index'),
    path('interact/', views.chatgpt_interact, name='chatgpt_interact'),
    path('history/', views.chatgpt_history, name='chatgpt_history'),
    path('chat-history/', chat_request_history, name='chatgpt_request_history'),
    path('analyze-images/<int:listing_id>/', views.analyze_images, name='analyze_images'),
]
