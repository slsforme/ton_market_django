from django.contrib import admin
from django.urls import path, include
from strawberry.django.views import GraphQLView
from graphql_api import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("graphql_api.urls")),
    path("graphqlapi", GraphQLView.as_view(schema=schema.schema))
]   
