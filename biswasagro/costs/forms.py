from django import forms
from django.forms import ModelForm
from .models import Cost, Costitems, Costpurpose


class CostForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )
    class Meta:
        model = Cost
        fields = ['date', 'costcategory', 'costitems', 'buyamount', 'unit', 'cost',
                  'buyer', 'buyvoucher', 'comment',]
