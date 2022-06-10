from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal
from datetime import datetime


class NumberJSONEncoder(DjangoJSONEncoder):
    
    def default(self, d):
        # O tipo Decimal, por padrao, e convertido para
        # string no parse do JSON. Convertando para float.
        if isinstance(d, Decimal):
            return float(d)
        elif isinstance(d, date):
            time = datetime.min.time()
            d = datetime.combine(d, time)
            return d.timestamp() * 1000
        return super().default(d)