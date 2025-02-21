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

        labels = {
            'date': 'Date',
            'costcategory': 'Cost Category',
            'costitems': 'Cost Items',
            'buyamount': 'Buy Amount',
            'unit': 'Unit',
            'cost': 'Cost',
            'buyer': 'Buyer',
            'buyvoucher': 'Buy Voucher',
            'comment': 'Additional Comments',
        }


class CostItemsForm(ModelForm):
    class Meta:
        model = Costitems
        fields = ['costitems',]

        labels = {
            'costitems': 'Cost Items',
        }


class CostPurposeForm(ModelForm):
    class Meta:
        model = Costpurpose
        fields = ['costpurpose',]

        labels = {
            'costpurpose': 'Cost Purpose',
        }


class EarningForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Earning
        fields = ['date', 'sector', 'item', 'source', 'quantity_per_unit', 'quantity',
                  'unit', 'price', 'memo', 'comment',]

        labels = {
            'date': 'Date',
            'sector': 'Sector',
            'item': 'Item',
            'source': 'Source',
            'quantity_per_unit': 'Quantity per Unit',
            'quantity': 'Quantity',
            'unit': 'Unit',
            'price': 'Price',
            'memo': 'Memo',
            'comment': 'Additional Comments',
        }


class InvestmentForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Investment
        fields = ['date', 'name', 'amount', 'comments',]
