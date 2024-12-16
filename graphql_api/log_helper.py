from .models import Logs, UserLogs, Users
from threading import Lock
from django.db import transaction
import uuid
import enum
from django.apps import apps
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

class LogLevel(enum.Enum):
    WARN = "WARN"
    ERROR = "ERROR"
    INFO = "INFO" 

@transaction.atomic
def create_logs(interaction_type: str, log_type: str, name: str, username: str):
    try:
        log = Logs(
            interaction_type=interaction_type, 
            log_type=log_type,
            name=name,
            is_auto_created=True
        )
        log.save()
        print(f"Log created with ID {log.id}")
        
        user = Users.objects.get(login=username)
        user_log = UserLogs(
            user=user,
            log=log,
            uuid=uuid.uuid4()
        )
        user_log.save()
        print(f"UserLog created with ID {user_log.id}")
        
    except Users.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
    except Exception as e:
        print(f"Error occurred: {e}")


