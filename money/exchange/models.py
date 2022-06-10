from locale import currency
from django.db import models

class CurrencyModel(models.Model):
    USD = "USD"
    BRL = "BRL"
    EUR = "EUR"
    JPY = "JPY"

    filter_currency = [
        BRL,
        EUR,
        JPY
    ]

    @staticmethod
    def currency_choices():
        return [(code, code) for code in CurrencyModel.filter_currency]

    currency_code = models.CharField(max_length=3, primary_key=True)
 

class CurrencyRateModel(models.Model):
    currency_code_base = models.ForeignKey(CurrencyModel, related_name="currency_base", on_delete=models.CASCADE)
    currency_code_target = models.ForeignKey(CurrencyModel, related_name="currency_target", on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=16)

    class Meta:
        unique_together = ('currency_code_base', 'currency_code_target', 'date')