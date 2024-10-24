from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import ( 
    HttpRequest, JsonResponse, HttpResponseBadRequest,
    HttpResponseNotFound, Http404
)
from django.core.exceptions import (
    ObjectDoesNotExist, 
)
from django.core.cache import cache

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




