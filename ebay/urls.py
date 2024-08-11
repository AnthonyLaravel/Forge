from django.urls import path
from . import views

urlpatterns = [
    path('ebay/authorize/', views.ebay_authorize, name='ebay_authorize'),
    path('ebay/callback/', views.ebay_callback, name='ebay_callback'),
]
