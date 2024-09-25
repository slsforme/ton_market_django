from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpRequest, JsonResponse

from tvDatafeed import TvDatafeed, Interval


@require_GET
def TON_price_json(request):
    tv = TvDatafeed()

    ton_futures_data = tv.get_hist(symbol='TONUSDT', exchange='OKX', interval=Interval.in_daily, n_bars=1000)

    ton_data_json = ton_futures_data.to_json(orient='records', date_format='iso')

    return JsonResponse({'price-data': ton_data_json})


@require_GET
def TON_capitalization_json(request):
    tv = TvDatafeed()

    ton_futures_data = tv.get_hist(symbol='TON', exchange='CRYPTOCAP', interval=Interval.in_daily, n_bars=1000)

    ton_data_json = ton_futures_data.to_json(orient='records', date_format='iso')

    return JsonResponse({'price-data': ton_data_json})

    


