from django import forms
from django.forms import ModelForm
from .models import Fishbuy, Fishtype, Items, Units, Land, Sectors, TblProduct


class FishbuyForm(ModelForm):
    class Meta:
        model = Fishbuy
        fields = ['date', 'fishname', 'buyfrom', 'buyamount', 'fishquantity', 'price',
                  'fishto', 'vouchar', 'comments',]

