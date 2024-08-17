from django.urls import path
from .views import EbayApiLogListView, EbayMarketplaceAccountDeletion, EbayAccountLinked
from . import views

urlpatterns = [
    path('api-test/', views.api_test_view, name='api_test'),
    path('api-logs/', EbayApiLogListView.as_view(), name='ebay_api_log_list'),
    path('authorize/', views.ebay_authorize, name='ebay_authorize'),
    path('declined/', views.ebay_declined, name='ebay_declined'),
    path('suggest-category/', views.suggest_category, name='suggest_category'),
    path('category-aspects/<str:category_id>/<str:category_tree_id>/', views.retrieve_category_aspects, name='category_aspects'),
    path('accepted/', EbayAccountLinked, name='ebay_success'),
    path('ebay_marketplace_account_deletion/', EbayMarketplaceAccountDeletion.as_view(), name='ebay_marketplace_account_deletion'),
]