from locale import currency
from django import forms
from .models import CurrencyModel

class DatesQueryForm(forms.Form):
    date_start = forms.DateField(required=True)
    date_end = forms.DateField(required=True)
    currency = forms.ChoiceField(choices=CurrencyModel.currency_choices(), required=True)
