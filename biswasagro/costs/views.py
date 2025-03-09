from django.shortcuts import redirect, reverse
from .models import Cost, Costitems, Costpurpose, Earning, Investment, Loandetails
from .forms import CostForm, CostItemsForm, CostPurposeForm, EarningForm, InvestmentForm, LoanDetailsForm
from common.utils import *
from common.column_mappers import *


#
# Cost Table (aka: Casual Expenses)
#
def show_cost_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'cost', Cost, show_cost_mapper)


def cost_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Cost, row_id)


def add_update_cost(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    #
    # populate specific template context values for this view
    #
    context = dict()

    # for expense_accounts, product_names, and units, we're only interested in the values and not the id's

    # get the expense accounts from the Sectors table and put the values in a set to get rid of potential duplicates
    expense_accounts = set(get_mapping(request, SECTOR_MAPPING).values())
    context['expense_accounts'] = expense_accounts

    # get product names (from Costitems table) and put the values in a set to get rid of potential duplicates
    product_names = set(get_mapping(request, COSTITEM_MAPPING).values())
    context['product_names'] = product_names

    # get units (from Units table) and put the values in a set to get rid of potential duplicates
    units = set(get_mapping(request, UNIT_MAPPING).values())
    context['units'] = units

    status_map = get_mapping(request, STATUS_MAPPING)
    context['status'] = status_map

    return add_update_table(request, 'costs', 'cost',
                            Cost, CostForm, row_id, {'logs', 'costitems_id'}, context, addup_cost_mapper)


#
# Cost Items Table
#
def show_costitems_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'costitems', Costitems, show_costitems_mapper)


def costitems_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Costitems, row_id)


def add_update_costitems(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    # get the sector name from the sector id stored in the costitems table
    # dict -> k:{}
    secid_to_secname = {sec.id: sec.sector for sec in Sectors.objects.all()}  # dictionary comprehension
    context['secid_to_sec'] = secid_to_secname

    return add_update_table(request, 'costs', 'costitems',
                            Costitems, CostItemsForm, row_id, {'logs'}, context, addup_costitems_mapper)


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

    context = dict()
    return add_update_table(request, 'costs', 'costpurpose',
                            Costpurpose, CostPurposeForm, row_id, set(), context)


#
# Earning Table
#
def show_earning_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'earning', Earning, show_earning_mapper)


def earning_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Earning, row_id)


def add_update_earning(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    # status pull-down
    context['status'] = get_mapping(request, STATUS_MAPPING)

    # sectors pull-down
    context['sectors'] = get_mapping(request, SECTOR_MAPPING)

    # items pull-down
    context['items'] = get_mapping(request, ITEMS_MAPPING)

    # sources pull-down
    context['sources'] = get_mapping(request, SOURCE_MAPPING)

    # units pull-down
    context['units'] = get_mapping(request, UNIT_MAPPING)

    return add_update_table(request, 'costs', 'earning',
                            Earning, EarningForm, row_id, {'logs'}, context, addup_earning_mapper)


#
# Investment Table
#
def show_investment_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'investment', Investment, show_investment_mapper)


def investment_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Investment, row_id)


def add_update_investment(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'costs', 'investment',
                            Investment, InvestmentForm, row_id, {'logs'}, context)


#
# Loandetails Table
#
def show_loandetails_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'costs', 'loandetails', Loandetails)#, show_investment_mapper)


def loandetails_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Loandetails, row_id)


def add_update_loandetails(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'costs', 'loandetails',
                            Loandetails, LoanDetailsForm, row_id, {'loanid', 'logs'}, context)
