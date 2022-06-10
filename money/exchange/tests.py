import datetime

from django.test import TestCase

from django.test import TestCase
from .models import CurrencyModel
from .usecase import RateUseCase
from datetime import date 

class AnimalTestCase(TestCase):

    def setUp(self):
        CurrencyModel.objects.create(currency_code="USD")
        CurrencyModel.objects.create(currency_code="BRL")
        CurrencyModel.objects.create(currency_code="EUR")
        CurrencyModel.objects.create(currency_code="JPY")


    def test_get_data(self):
        start = date(2020, 4, 4)
        end = date(2020, 4, 9)
        rate = RateUseCase(start, end, "BRL")
        rate.execute()
    

    def test_date_five_days(self):
        start = date(2020, 4, 4)
        end = date(2020, 4, 10)
        rate = RateUseCase(start, end, "BRL")
        try:
            rate.execute()
        except Exception as e:
            self.assertEqual(str(e), "O intervalo de dias não deve ser maior que 5 dias")


    def test_date_start_less_end(self):
        start = date(2020, 4, 4)
        end = date(2020, 4, 1)
        rate = RateUseCase(start, end, "BRL")
        try:
            rate.execute()
        except Exception as e:
            self.assertEqual(str(e), "Data Inicial é maior que Data Final")


    def test_invalid_currency(self):
        start = date(2020, 4, 4)
        end = date(2020, 4, 9)
        rate = RateUseCase(start, end, "AAA")
        try:
            rate.execute()
        except Exception as e:
            self.assertEqual(str(e), "Moeda AAA não suportada")

