from django.urls import path 
from graphql_api import views

urlpatterns = [
    path('ton-price/', views.TON_price_json, name="ton-price-url"),
    path('backup-database/', views.backup_database_view, name='backup_database'),
    path('functions_admin/', views.functions_admin_view, name='functions_admin'),
    path('import_data/', views.import_data, name='import_data'),
    path('export_data/', views.export_data, name='export_data'),
    path('virtual_views/', views.virtual_views, name='virtual_views'),

]