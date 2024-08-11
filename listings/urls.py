from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('new/', views.listing_create, name='listing_create'),
    path('<int:pk>/edit/', views.listing_update, name='listing_update'),
    path('<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('<int:listing_pk>/images/', views.image_list, name='image_list'),
    path('<int:listing_pk>/images/new/', views.image_create, name='image_create'),
    path('<int:listing_pk>/images/<int:image_pk>/delete/', views.image_delete, name='image_delete'),
]
