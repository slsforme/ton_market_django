from django.apps import AppConfig


class GraphqlApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphql_api'
    
    def ready(self):
        from graphql_api import log_helper
        log_helper.register_signals()