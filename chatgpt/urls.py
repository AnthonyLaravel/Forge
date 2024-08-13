# chatgpt/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatgpt_interact, name='chatgpt_index'),
    path('interact/', views.chatgpt_interact, name='chatgpt_interact'),
    path('history/', views.chatgpt_history, name='chatgpt_history'),
    path('analyze-images/<int:listing_id>/', views.analyze_images, name='analyze_images'),
]
