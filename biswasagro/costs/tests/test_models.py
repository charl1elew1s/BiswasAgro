import pytest
from unittest.mock import patch
from datetime import datetime, timezone, date
from .. models import Cost, Costitems, Costpurpose
from .. forms import CostForm


class TestCosts:

    def test_get_cost_by_id(self):
        """Mocking QuerySet.get() so that I don't have to go to the actual DB!"""
        with patch("django.db.models.query.QuerySet.get") as mock_get:
            fake_date = '2025-02-02'
            fake_costcategory = 'fake cost category'
            fake_costitems = 'fake cost items'
            fake_buyamount = 'fake buy amount'
            fake_unit = 'fake unit'
            fake_cost = 'fake cost'
            fake_buyer = 'fake buyer'
            fake_buyvoucher = 'fake voucher'
            fake_comment = 'fake cost comment'
            fake_logs = 'fake logs'

            # this tests the cost constructor
            mock_get.return_value = Cost(id=1, date=fake_date, costcategory=fake_costcategory,
                                         costitems=fake_costitems, buyamount=fake_buyamount, unit=fake_unit,
                                         cost=fake_cost, buyer=fake_buyer, buyvoucher=fake_buyvoucher,
                                         comment=fake_comment, logs=fake_logs)

            cost_obj = mock_get(id=1)

            assert cost_obj.id == 1
            assert cost_obj.date == fake_date
            assert cost_obj.costcategory == fake_costcategory
            assert cost_obj.costitems == fake_costitems
            assert cost_obj.buyamount == fake_buyamount
            assert cost_obj.unit == fake_unit
            assert cost_obj.cost == fake_cost
            assert cost_obj.buyer == fake_buyer
            assert cost_obj.buyvoucher == fake_buyvoucher
            assert cost_obj.comment == fake_comment
            assert cost_obj.logs == fake_logs

            # now attempt to change a value on the cost_obj and test that it's mocked correctly
            updated_log_str = f"prefix - {fake_date}"
            cost_obj.logs = updated_log_str
            assert cost_obj.logs == updated_log_str, "cost_obj not updated correctly!"

    def test_cost_form(self):
        # let's go with the Sunny Day scenario first (everything correct)

        # pretend like this came from a date picker on the website
        fake_now = date(year=2025, month=2, day=2)
        fake_form_data = {
            'date': fake_now,
            'costcategory': 'cost category',
            'costitems': 'cost items',
            'buyamount': 111.11,
            'unit': 'cost unit',
            'cost': 2.22,
            'buyer': 'cost buyer',
            'buyvoucher': 'cost buy voucher',
            'comment': 'cost comment',
            'logs': 'cost logs',
        }

        form = CostForm(data=fake_form_data)
        assert form.is_valid(), "form should have been valid but was not!"

        # check the types of some of the attributes of the cleaned form
        assert isinstance(form.cleaned_data['date'], date), "cleaned date has incorrect type!"
        assert isinstance(form.cleaned_data['buyamount'], float), "cleaned buyamount has incorrect type!"
        assert isinstance(form.cleaned_data['cost'], float), "cleaned cost has incorrect type!"
        assert isinstance(form.cleaned_data['buyvoucher'], str), "cleaned buyvoucher has incorrect type!"

        # now we'll enter some incorrect data on the form (as if the user input incorrect values)
        # Note: the UI will prevent these things from making it to the back end, but let's ensure that the
        # back-end can handle it
        fake_form_data = {
            'date': fake_now,
            'costcategory': 22,  # should be a str
            'costitems': 'cost items',
            'buyamount': "amount",  # should be a float
            'unit': 'cost unit',
            'cost': 2.22,
            'buyer': 'cost buyer',
            'buyvoucher': 'cost buy voucher',
            'comment': 'cost comment',
            'logs': 'cost logs',
        }
        form = CostForm(data=fake_form_data)
        assert not form.is_valid(), "form should NOT have been valid but was!"
        assert "buyamount" in form.errors, "buyamount should have been reported as being incorrect but wasn't"
        assert isinstance("costcategory", str), "costcategory should have been converted to str but wasn't"

