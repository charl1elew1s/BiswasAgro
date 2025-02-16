from django import forms
from django.forms import ModelForm
from .models import Cost, Costitems, Costpurpose, Earning, Investment


class CostForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Cost
        fields = ['date', 'costcategory', 'costitems', 'buyamount', 'unit', 'cost',
                  'buyer', 'buyvoucher', 'comment',]


class CostItemsForm(ModelForm):
    class Meta:
        model = Costitems
        fields = ['costitems',]


class CostPurposeForm(ModelForm):
    class Meta:
        model = Costpurpose
        fields = ['costpurpose',]


class EarningForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Earning
        fields = ['date', 'sector', 'item', 'source', 'quantity_per_unit', 'quantity',
                  'unit', 'price', 'memo', 'comment',]


class InvestmentForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Investment
        fields = ['date', 'name', 'amount', 'comments',]
