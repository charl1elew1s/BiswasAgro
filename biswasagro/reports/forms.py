from django import forms
from django.forms import Form
from datetime import date

# Human-readable format for Dates
DISPLAY_FMT = '%d-%m-%Y'


class DateSelectorForm(Form):
    # Use an HTML5 date picker
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={'type': 'date'}))


class YearMonthForm(Form):
    year = forms.CharField(label="Year", required=True)
    month = forms.CharField(label='Month', required=True)


class YearForm(Form):
    year = forms.CharField(label="Year", required=True)


class ToFromDateSelectorForm(Form):
    # Use an HTML5 date pickers
    fr_date = forms.DateField(label="Date From", widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To", widget=forms.DateInput(attrs={'type': 'date'}))
