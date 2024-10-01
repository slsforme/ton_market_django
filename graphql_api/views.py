from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import ( 
    HttpRequest, JsonResponse, HttpResponseBadRequest,
    HttpResponseNotFound, Http404
)
from django.core.exceptions import (
    ObjectDoesNotExist, 
)

from tvDatafeed import TvDatafeed, Interval
import json
import hashlib
from .models import Roles, Users


from TON_market_backend import settings


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

class Users(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    uuid = models.UUIDField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=65)
    address = models.CharField(unique=True, max_length=60)
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id')

    class Meta:
        managed = False
        db_table = 'users'




@require_POST
def register_user(request: HttpRequest):
    try:
        login = request.POST.get('login')
        if Users.objects.filter(login=login):
            return Http404("Пользователь с таким логином уже зарегестрирован")
        password = request.POST.get('password')  # хэширование на сторроне фронта
        role_id = request.POST.get('role_id')
        address = request.POST.get('address')
        if Users.objects.filter(address=address):
            return Http404("Пользователь с таким адресом кошелька уже зарегестрирован")
        try:
            db_role_id =  Roles.objects.filter(id=role_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Такой роли не существует")
        
        user = Users(
            login=login,
            password=password,
            role_id=db_role_id,
            address=address
        )

        user.save()


    except Exception as e:
        settings.LOGGER.error(
            "Error occured while creating user "
            f": {e} (error)"
        )

@require_POST
def auth_user(request: HttpRequest):
    try:
        login = request.POST.get('login')
        password = request.POST.get('password') 
        address = request.POST.get('address') 

        try:
            user = Users.objects.filter(login=login,
                                        password=password,
                                        address=address)
            return HttpRequest("Авторизация прошла успешно", status=200)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Неправильно введены данные")

        
    except Exception as e:
        settings.LOGGER.error(
            "Error occured while authorization "
            f": {e} (error)"
        )


