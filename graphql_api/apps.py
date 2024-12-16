from django.apps import AppConfig


class GraphqlApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphql_api'
    
    def ready(self):
        import graphql_api.signals
        