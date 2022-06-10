from datetime import timedelta
import requests
import json
import asyncio


class ApiVatComply:
    URI = "https://api.vatcomply.com/rates"

    def __init__(self, dates) -> None:
        self._dates = dates

    @asyncio.coroutine
    def _get_rate_by_date(self, date, loop):
        query = {'date': date.strftime('%Y-%m-%d'), 'base': 'USD'}

        # Cria um Future para realizar as requisições em paralelo. 
        future = loop.run_in_executor(None, requests.get, self.URI, query)
        yield from future
        return future.result().json()

        
    def get_rates(self):
        """
            Returna um dicionario, 
                key: data
                value: armazena um dict com os codigo e valor de cada moeda
        """
        dates = {}
        try:
             loop = asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()

        # O method gather agrupa o futures(coroutine) gerados pelo yield.
        # Com os futures agrupados, executamos todas as futures juntos,
        # realizando as multiplas requisicoes em paralelo.
        resp = loop.run_until_complete(
            asyncio.gather(
                *[self._get_rate_by_date(date, loop) for date in self._dates]
            )
        )
        for r in resp:
            dates[r["date"]] = r["rates"]
        return dates
