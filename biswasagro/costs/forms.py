from django import forms
from django.forms import ModelForm
from .models import Cost, Costitems, Costpurpose, Earning, Investment, Loandetails, LoanTransactions, LoanProvidersInfo


class CostForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Cost
        fields = ['date', 'costcategory', 'costitems', 'buyamount', 'unit', 'cost', 'status',
                  'buyer', 'buyvoucher', 'comment',]

        labels = {
            'date': 'Date',
            'costcategory': 'Expense Account',
            'costitems': 'Product Name',
            'buyamount': 'Quantity',
            'unit': 'Unit',
            'cost': 'Cost amount',
            'buyer': 'Spender',
            'status': 'Status',
            'buyvoucher': 'Voucher',
            'comment': 'Additional Comments',
        }


class CostItemsForm(ModelForm):
    class Meta:
        model = Costitems
        fields = ['sector', 'costitems',]

        labels = {
            'sector': 'Sector',
            'costitems': 'Product'  #'Cost Items',
        }

        error_messages = {
            'costitems': {
                'unique': 'Product with this name already exists.',
            },
        }


class CostPurposeForm(ModelForm):
    class Meta:
        model = Costpurpose
        fields = ['costpurpose',]

        labels = {
            'costpurpose': 'Cost Purpose',
        }
        error_messages = {
            'costpurpose': {
                'unique': 'Cost Purpose with this name already exists.',
            },
        }


class EarningForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = Earning
        fields = ['date', 'sector', 'item', 'source', 'quantity_per_unit', 'quantity',
                  'unit', 'price', 'status', 'memo', 'comment',]

        labels = {
            'date': 'Date',
            'sector': 'Sector',
            'item': 'Item',
            'source': 'Source',
            'quantity_per_unit': 'Quantity per Unit',
            'quantity': 'Quantity',
            'unit': 'Unit',
            'price': 'Price',
            'status': 'Status',
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

        labels = {
            'date': 'Date',
            'name': 'Name',
            'amount': 'Amount',
            'comments': 'Comments',
        }


class LoanDetailsForm(ModelForm):
    class Meta:
        model = Loandetails
        fields = ['investerid', 'amount', 'interestpermonth', 'conditions']

        labels = {
            'investerid': 'Investor ID',
            'amount': 'Amount',
            'interestpermonth': 'Interest per Month',
            'conditions': 'Conditions'
        }


class LoanProvidersInfoForm(ModelForm):
    class Meta:
        model = LoanProvidersInfo
        fields = ['name', 'address', 'mobile', 'refference']

        widgets = {
            'mobile': forms.TextInput(attrs={'maxlength': 20})
        }

        labels = {
            'name': 'Name',
            'address': 'Address',
            'mobile': 'Mobile',
            'refference': 'Reference'
        }


class LoanTransactionsForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # Use an HTML5 date picker
    )

    class Meta:
        model = LoanTransactions
        fields = ['loanid', 'investerid', 'date', 'payment', 'voucherno',]

        labels = {
            'loanid': 'Loan ID',
            'investerid': 'Investor ID',
            'date': 'Date',
            'payment': 'Payment',
            'voucherno': 'Voucher No.'
        }
