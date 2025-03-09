from django import forms
from django.forms import ModelForm
from .models import (Dailyworks, Fishbuy, Fishtype, Fooddistribution, Items, Units, Land,
                     Sectors, Mousa, Mousaname, Sources, Term)


class DailyworksForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Dailyworks
        fields = ['date', 'worktype', 'item', 'amount', 'unit', 'personel', 'comment']

        labels = {
            'date': 'Date',
            'worktype': "Work Type",
            'item': 'Item',
            'amount': 'Amount',
            'unit': 'Unit',
            'personel': 'Personnel',
            'comment': 'Additional Comments'
        }


class FishbuyForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Fishbuy
        fields = ['date', 'fishname', 'buyfrom', 'buyamount', 'fishquantity', 'price',
                  'status', 'fishto', 'vouchar', 'comments',]

        labels = {
            'date': 'Date of Purchase',
            'fishname': 'Fish Name',
            'buyfrom': 'Bought From',
            'buyamount': 'Buy Amount',
            'fishquantity': 'Fish Quantity',
            'price': 'Price per unit',
            'status': 'Status',
            'fishto': 'Fish To',
            'vouchar': 'Voucher',
            'comments': 'Additional Comments',
        }


class FishtypeForm(ModelForm):
    class Meta:
        model = Fishtype
        fields = ['fishname',]

        labels = {
            'fishname': 'Fish Name'
        }
        error_messages = {
            'fishname': {
                'unique': 'Fish Name with this name already exists.',
            },
        }


class FoodDistributionForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Fooddistribution
        fields = ['date', 'gher', 'item', 'amount', 'unit',]

        labels = {
            'date': 'Date',
            'gher': 'Gher',
            'item': 'Item',
            'amount': 'Amount',
            'unit': 'Unit'
        }


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        fields = ['sector', 'item_name',]

        labels = {
            'sector': 'Sector',
            'item_name': 'Item Name'
        }
        error_messages = {
            'item_name': {
                'unique': 'Item Name with this name already exists.',
            },
        }


class LandForm(ModelForm):
    class Meta:
        model = Land
        fields = ['gher', 'mousa', 'dag', 'khotian', 'amount', 'plane_land', 'par_cannel',
                  'owners', 'comment',]

        labels = {
            'gher': 'Gher',
            'mousa': 'Mousa',
            'dag': 'Dag',
            'khotian': 'Khotian',
            'amount': 'Amount',
            'plane_land': 'Plane Land',
            'par_cannel': 'Par Cannel',
            'owners': 'Owners',
            'comment': 'Additional Comments',
        }


class SectorsForm(ModelForm):
    class Meta:
        model = Sectors
        fields = ['sector']

        labels = {
            'sector': 'Sector',
        }
        error_messages = {
            'sector': {
                'unique': 'Sector with that name already exists.',
            },
        }


class UnitsForm(ModelForm):
    class Meta:
        model = Units
        fields = ['unit']

        labels = {
            'unit': 'Unit'
        }


class MousaForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Mousa
        fields = ['mousa', 'dag', 'owner', 'date', 'amount', 'term', 'vc_numnber', 'status', ]

        labels = {
            'mousa': 'Mousa',
            'dag': 'Dag',
            'owner': 'Owner',
            'date': 'Date',
            'amount': 'Amount',
            'term': 'Term',
            'vc_numnber': 'VC Number',
            'status': 'Status'
        }


class MousaName(ModelForm):
    class Meta:
        model = Mousaname
        fields = ['name']

        labels = {
            'name': 'Name'
        }
        error_messages = {
            'name': {
                'unique': 'Name already exists.',
            },
        }


class SourcesForm(ModelForm):
    class Meta:
        model = Sources
        fields = ['source']

        labels = {
            'source': 'Source'
        }


class TermForm(ModelForm):
    class Meta:
        model = Term
        fields = ['term']

        labels = {
            'term': 'Term'
        }
        error_messages = {
            'term': {
                'unique': 'Term with that name already exists.',
            },
        }
