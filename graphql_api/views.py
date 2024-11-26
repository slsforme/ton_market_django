from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import ( 
    HttpRequest, JsonResponse, HttpResponseBadRequest,
    HttpResponseNotFound, Http404, HttpResponse
)
from django.core.exceptions import (
    ObjectDoesNotExist, 
)
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.conf import settings

from tvDatafeed import TvDatafeed, Interval
import json
import hashlib
from pathlib import Path
import subprocess
from datetime import datetime

from .models import Roles, Users

@staff_member_required
def admin_custom_page(request):
    return render(request, 'admin/functions.html')


def backup_database_view(request):
    backup_dir = Path(settings.BASE_DIR) / "db_backups"

    # Создаем директорию для хранения бэкапов, если её нет
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Формируем имя и путь к файлу бэкапа
    backup_file_name = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_file_path = backup_dir / backup_file_name

    try:
        # Команда для создания бэкапа базы данных
        backup_command = [
            "pg_dump",
            f"--dbname={settings.DATABASES['default']['NAME']}",
            f"--username={settings.DATABASES['default']['USER']}",
            "--host", settings.DATABASES['default']['HOST'],
            "--port", str(settings.DATABASES['default']['PORT']),
            "--file", str(backup_file_path)
        ]

        # Выполняем команду бэкапа базы данных
        subprocess.run(backup_command, check=True, env={"PGPASSWORD": settings.DATABASES['default']['PASSWORD']})

        # Читаем содержимое созданного файла
        with open(backup_file_path, "rb") as f:
            backup_content = f.read()


        response = HttpResponse(
            backup_content,
            content_type="application/octet-stream"
        )
        response["Content-Disposition"] = f'attachment; filename="{backup_file_name}"'
        return response

    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Ошибка создания бэкапа: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"Произошла ошибка: {e}", status=500)

@require_GET
def TON_price_json(request: HttpRequest):
    try:
        tv = TvDatafeed()

        ton_futures_data = tv.get_hist(symbol='TONUSDT', exchange='OKX', interval=Interval.in_daily, n_bars=1000)

        ton_data_json = ton_futures_data.to_json(orient='records', date_format='iso')

        return JsonResponse({'price-data': ton_data_json})
    except Exception as e:
        settings.LOGGER.error(
            "Error occured while sending data "
            f"about Toncoin price: {e} (error)"
        )






