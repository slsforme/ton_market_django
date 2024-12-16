from .models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
import threading

signal_processing = threading.local()
signal_processing.in_progress = False

def create_logs(interaction_type, log_type, name, username, is_auto_created=False):
    """
    Создаёт запись в модели Logs.
    """
    Logs.objects.create(
        interaction_type=interaction_type,
        log_type=log_type,
        name=name,
        is_auto_created=is_auto_created
    )

def handle_log_creation(instance, created, username):
    """
    Логика обработки создания/обновления объекта.
    """
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username
        )

def handle_log_deletion(instance, username):
    """
    Логика обработки удаления объекта.
    """
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username
    )

# Универсальный обработчик сигналов post_save для всех моделей
@receiver(post_save)
def create_log_on_save(sender, instance, created, **kwargs):
    if sender is Logs:  # Пропускаем сигналы от модели Logs, чтобы избежать рекурсии
        return

    # Проверяем, не выполняется ли обработка сигналов
    if getattr(signal_processing, "in_progress", False):
        return

    try:
        # Устанавливаем флаг, чтобы предотвратить повторное срабатывание
        signal_processing.in_progress = True

        username = 'slsforme'
        handle_log_creation(instance, created, username)
    finally:
        # Сбрасываем флаг
        signal_processing.in_progress = False

# Универсальный обработчик сигналов pre_delete для всех моделей
@receiver(pre_delete)
def create_log_on_delete(sender, instance, **kwargs):
    if sender is Logs:  # Пропускаем сигналы от модели Logs, чтобы избежать рекурсии
        return

    username = 'slsforme'
    handle_log_deletion(instance, username)
