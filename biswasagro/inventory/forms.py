from django import forms
from django.forms import ModelForm
from .models import Fishbuy, Fishtype, Items, Units, Land, Sectors, TblProduct


class FishbuyForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Fishbuy
        fields = ['date', 'fishname', 'buyfrom', 'buyamount', 'fishquantity', 'price',
                  'fishto', 'vouchar', 'comments',]

        labels = {
            'date': 'Date of Purchase',
            'fishname': 'Fish Name',
            'buyfrom': 'Bought From',
            'buyamount': 'Buy Amount',
            'fishquantity': 'Fish Quantity',
            'price': 'Price per unit',
            'fishto': 'Fish To',
            'vouchar': 'Voucher Name',
            'comments': 'Additional Comments',
        }


class FishtypeForm(ModelForm):
    class Meta:
        model = Fishtype
        fields = ['fishname',]

        labels = {
            'fishname': 'Fish Name'
        }


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        fields = ['sector', 'item_name',]


class LandForm(ModelForm):
    class Meta:
        model = Land
        fields = ['mousa', 'dag', 'khotian', 'amount', 'plane_land', 'par_cannel', 'owners', 'comment',]

        labels = {
            'comment': 'Additional Comments',
        }


class SectorsForm(ModelForm):
    class Meta:
        model = Sectors
        fields = ['sector']


class TblProductForm(ModelForm):
    class Meta:
        model = TblProduct
        fields = ['name', 'prix', 'categorie', 'etat',]

        labels = {
            'categorie': 'Category',
        }

class UnitsForm(ModelForm):
    class Meta:
        model = Units
        fields = ['unit']
