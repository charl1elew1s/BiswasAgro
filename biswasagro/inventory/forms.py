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


class FishtypeForm(ModelForm):
    class Meta:
        model = Fishtype
        fields = ['fishname',]


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        fields = ['sector', 'item_name',]


class LandForm(ModelForm):
    class Meta:
        model = Land
        fields = ['mousa', 'dag', 'khotian', 'amount', 'plane_land', 'par_cannel', 'owners', 'comment',]


class SectorsForm(ModelForm):
    class Meta:
        model = Sectors
        fields = ['sector']


class TblProductForm(ModelForm):
    class Meta:
        model = TblProduct
        fields = ['name', 'prix', 'categorie', 'etat',]


class UnitsForm(ModelForm):
    class Meta:
        model = Units
        fields = ['unit']
