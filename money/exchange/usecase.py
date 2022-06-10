
import datetime
from locale import currency
from .models import CurrencyModel, CurrencyRateModel
from .api_rates import ApiVatComply
from django.db import IntegrityError


class RateUseCase:

    def __init__(self, date_start, date_end, currency_target):
        self.date_start = date_start 
        self.date_end = date_end
        self.currency_target = currency_target
    
    def _rangedates(self, total_days):
        dates = []
        for n in range(total_days):
            d = self.date_start + datetime.timedelta(n)
            # Desconsidera sabado e domingo
            if d.weekday() not in [5, 6]:
                dates.append(self.date_start + datetime.timedelta(n))
        return dates
    
    def _get_data_external(self, dates_to_find):
        base_currency = CurrencyModel(currency_code=CurrencyModel.USD)
        data = ApiVatComply(dates_to_find)
        dict_data = data.get_rates()

        # Armazena as novas datas no banco de dados.
        for date, rates in dict_data.items():
            for target in CurrencyModel.filter_currency:
                target_obj = CurrencyModel(currency_code=target)

                rate = CurrencyRateModel(
                    currency_code_base=base_currency,
                    currency_code_target=target_obj,
                    date=datetime.datetime.strptime(date, "%Y-%m-%d"),
                    value=rates[target]
                )

                try:
                    rate.save()
                except IntegrityError:
                        # A informacao já existe no banco
                        pass


    def _get_data(self, total_days):
        qs = (
            CurrencyRateModel
            .objects
            .filter(
                currency_code_base=CurrencyModel.USD,
                currency_code_target=self.currency_target,
                date__gte=self.date_start,
                date__lte=self.date_end)
            .values("date", "value")
        )
        # Utilizar o len aqui não terá problema
        # pois o numero de registro sempre será pequeno.
        # Se a condicao for falsa, entao nao temos todos os registros
        # no banco.
        if len(qs) == total_days:
            return qs.values_list("date", "value")

        # Vamos pegar apenas as datas que o banco nao possui.
        dates_found = qs.values_list('date', flat=True)
        all_dates = self._rangedates(total_days)
        dates_to_find = list(set(all_dates) - set(dates_found)) 

        self._get_data_external(dates_to_find)

        qs_new_date = (
            CurrencyRateModel
            .objects
            .filter(
                currency_code_base=CurrencyModel.USD,
                currency_code_target=self.currency_target,
                date__in=dates_to_find)
            .values("date", "value")
        )

        qs = qs | qs_new_date
        return qs.values_list("date", "value")

    def execute(self):
        days = 5
        if self.date_start > self.date_end:
            raise Exception("Data Inicial é maior que Data Final")

        total_days = (self.date_end - self.date_start).days
        if total_days > days:
            raise Exception(f"O intervalo de dias não deve ser maior que {days} dias")
        
        if self.date_end > datetime.date.today():
            raise Exception("A data final deve ser menor ou igual que a data de hoje")

        if self.currency_target not in CurrencyModel.filter_currency:
            raise Exception(f"Moeda {self.currency_target} não suportada")

        return self._get_data(total_days)


class CurrencyUseCase:

    @staticmethod
    def get_all_currencies():
        return (
            CurrencyModel
            .objects
            .all()
            .values_list("currency_code", flat=True)
            .exclude(currency_code="USD")
        )
        
    