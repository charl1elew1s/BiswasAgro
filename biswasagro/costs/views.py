from django.shortcuts import redirect, reverse
from .models import Cost, Costitems, Costpurpose, Earning, Investment
from .forms import CostForm, CostItemsForm, CostPurposeForm, EarningForm, InvestmentForm
from common.utils import delete_tabel_row, show_table, add_update_table


#
# Cost Table
#
def show_cost_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'cost', Cost)


def cost_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Cost, row_id)


def add_update_cost(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'costs', 'cost',
                            Cost, CostForm, row_id, {'logs'})


#
# Cost Items Table
#
def show_costitems_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'costitems', Costitems)


def costitems_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Costitems, row_id)


def add_update_costitems(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'costs', 'costitems',
                            Costitems, CostItemsForm, row_id, {'logs'})


#
# Cost Purpose Table
#
def show_costpurpose_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'costpurpose', Costpurpose)


def costpurpose_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Costpurpose, row_id)


def add_update_costpurpose(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'costs', 'costpurpose',
                            Costpurpose, CostPurposeForm, row_id, set())


#
# Earning Table
#
def show_earning_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'earning', Earning)


def earning_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Earning, row_id)


def add_update_earning(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'costs', 'earning',
                            Earning, EarningForm, row_id, {'logs'})


#
# Investment Table
#
def show_investment_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'investment', Investment)


def investment_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Investment, row_id)


def add_update_investment(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'costs', 'investment',
                            Investment, InvestmentForm, row_id, {'logs'})
