from django.urls import path 
from graphql_api import views

urlpatterns = [
    path('ton-price/', views.TON_price_json, name="ton-price-url"),
    path('ton-capitalization/', views.TON_capitalization_json, name="ton-capitalization-url")
]