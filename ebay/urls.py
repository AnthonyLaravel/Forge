from django.urls import path
from . import views

urlpatterns = [
    path('api-test/', views.api_test_view, name='api_test'),
    path('authorize/', views.ebay_authorize, name='ebay_authorize'),
    path('callback/', views.ebay_callback, name='ebay_callback'),
    path('suggest-category/', views.suggest_category, name='suggest_category'),
    path('category-aspects/<str:category_id>/<str:category_tree_id>/', views.retrieve_category_aspects, name='category_aspects'),
]
