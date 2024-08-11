from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('new/', views.listing_create, name='listing_create'),
    path('<int:pk>/edit/', views.listing_update, name='listing_update'),
    path('<int:pk>/delete/', views.listing_delete, name='listing_delete'),
]