from django.urls import path 
from graphql_api import views

urlpatterns = [
    path('ton-price/', views.TON_price_json, name="ton-price-url"),
    path('backup-database/', views.backup_database_view, name='backup_database'),
    path('functions_admin/', views.admin_custom_page, name='functions_page'),
]