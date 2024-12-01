from django.apps import AppConfig


class GraphqlApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphql_api'
    
    def ready(self):
        import graphql_api.log_helper  # Путь к файлу signals.py
        graphql_api.log_helper.register_signals()  # Регистрируем сигналы для всех моделей