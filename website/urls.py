from django.urls import path
from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.user_registration, name='registration'),
]
