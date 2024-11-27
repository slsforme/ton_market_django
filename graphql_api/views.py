from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import (
    HttpRequest, JsonResponse, HttpResponseBadRequest,
    HttpResponseNotFound, Http404, HttpResponse
)
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.db import connection
import psycopg2 as pg


from import_export import resources
from import_export.formats.base_formats import CSV, JSON, XLSX
from import_export.formats.base_formats import DEFAULT_FORMATS
from tablib import Dataset


from .models import (
    Logs, ProductTypes, Products, Requests,
    Roles, SmartContracts, Transactions,
    UserLogs, UserRequests, UserTransactions, Users
)
from .resources import *
import os
from io import StringIO

RESOURCE_MAPPING = {
    "Logs": LogsResource,
    "ProductTypes": ProductTypesResource,
    "Products": ProductsResource,
    "Requests": RequestsResource,
    "Roles": RolesResource,
    "SmartContracts": SmartContractsResource,
    "Transactions": TransactionsResource,
    "UserLogs": UserLogsResource,
    "UserRequests": UserRequestsResource,
    "UserTransactions": UserTransactionsResource,
    "Users": UsersResource,
}

def virtual_views(request):
    try:
        db_config = {
            'dbname': settings.DATABASES['default']['NAME'],
            'user': settings.DATABASES['default']['USER'],
            'password': settings.DATABASES['default']['PASSWORD'],
            'host': settings.DATABASES['default']['HOST'],
            'port': settings.DATABASES['default']['PORT'],
        }
        
        with pg.connect(**db_config) as conn:
            with conn.cursor() as cur_users:
                users_query = "SELECT * FROM users_with_roles_view"
                cur_users.execute(users_query)
                users_with_roles = cur_users.fetchall()
                cur_users.close()

            with conn.cursor() as cur_products:
                products_query = "SELECT * FROM products_with_types_view"
                cur_products.execute(products_query)
                products_with_types = cur_products.fetchall()
                cur_products.close()

        
        return render(request, 'admin/views.html', {
            'users_with_roles': users_with_roles, 
            'products_with_types': products_with_types
        })
    
    except Exception as e:
        print('Ошибка при подключении к базе данных:', e)
        return render(request, 'error_template.html', {'message': str(e)})

@staff_member_required
def functions_admin_view(request):
    return render(request, 'admin/functions.html')


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get("model")
        file_format = request.POST.get("format")

        if not model_name or not file_format:
            return HttpResponse("Модель и формат обязательны.", status=400)

        # Получаем класс модели
        model_class = globals().get(model_name)
        if not model_class:
            return HttpResponse(f"Модель {model_name} не найдена.", status=404)

        # Извлекаем данные
        data = model_class.objects.all()
        
        if file_format == "sql":
            # Генерация SQL для экспорта
            output = StringIO()
            output.write(f"-- Экспорт данных для модели {model_name}\n\n")

            for obj in data:
                fields = [f.name for f in model_class._meta.fields]
                values = [repr(getattr(obj, field)) for field in fields]
                sql_insert = f"INSERT INTO {model_name.lower()} ({', '.join(fields)}) VALUES ({', '.join(values)});\n"
                output.write(sql_insert)

            response = HttpResponse(output.getvalue(), content_type="text/sql")
            response["Content-Disposition"] = f"attachment; filename={model_name}.sql"
            return response

        # Для других форматов (CSV, JSON, XLSX) код остаётся прежним
        if file_format == "csv":
            response = HttpResponse(data.csv, content_type="text/csv")
            response["Content-Disposition"] = f"attachment; filename={model_name}.csv"
        elif file_format == "json":
            response = HttpResponse(data.json, content_type="application/json")
            response["Content-Disposition"] = f"attachment; filename={model_name}.json"
        elif file_format == "xlsx":
            response = HttpResponse(data.xlsx, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response["Content-Disposition"] = f"attachment; filename={model_name}.xlsx"
        else:
            return HttpResponse("Неподдерживаемый формат.", status=400)

        return response

    return HttpResponse("Некорректный запрос.", status=400)

def import_data(request):
    if request.method == "POST" and request.FILES.get("file"):
        model_name = request.POST.get("model")
        import_file = request.FILES["file"]

        if not model_name or not import_file:
            return HttpResponse("Модель и файл обязательны.", status=400)

        model_class = globals().get(model_name)
        if not model_class:
            return HttpResponse(f"Модель {model_name} не найдена.", status=404)

        # Чтение SQL файла
        sql_commands = import_file.read().decode("utf-8").split(";")

        with connection.cursor() as cursor:
            for command in sql_commands:
                command = command.strip()
                if command:
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        return HttpResponse(f"Ошибка выполнения SQL: {str(e)}", status=400)

        return HttpResponse(f"Данные для модели {model_name} успешно импортированы.", status=200)

    return HttpResponse("Некорректный запрос.", status=400)

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

# Получение данных о цене Toncoin
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
