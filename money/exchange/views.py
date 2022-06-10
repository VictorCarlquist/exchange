from http import HTTPStatus
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from .utils import NumberJSONEncoder
from .usecase import RateUseCase, CurrencyUseCase
from .forms import DatesQueryForm


def index(request):
    context = {
        "currencies": CurrencyUseCase.get_all_currencies()
    }
    return render(request, 'exchange/index.html', context)


def get_exchange_value(request):
    if request.method == 'GET':
        form = DatesQueryForm(request.GET)
        if not form.is_valid():
            erro = form.errors.as_text()
            return HttpResponseBadRequest(erro)

        date_start = form.cleaned_data['date_start']
        date_end = form.cleaned_data['date_end']
        currency = form.cleaned_data['currency']

        rate_usecase = RateUseCase(date_start, date_end, currency)
        try:
            data = rate_usecase.execute()
            data = list(data)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        return JsonResponse(list(data), safe=False, encoder=NumberJSONEncoder)

    return JsonResponse({})