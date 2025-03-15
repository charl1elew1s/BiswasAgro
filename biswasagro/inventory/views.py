from django.shortcuts import redirect
from .models import *
from .forms import *
from common.utils import *
from common.column_mappers import *


#
# Fishbuy table
#
def show_fishbuy_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'fishbuy', Fishbuy, show_fishbuy_mapper)


def add_update_fishbuy(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    # get the set of fishnames
    context['fish_names'] = set(get_mapping(request, FISHTYPE_MAPPING).values())

    # get the sources
    context['sources'] = set(get_mapping(request, SOURCE_MAPPING).values())

    status_map = get_mapping(request, STATUS_MAPPING)
    context['status'] = status_map

    return add_update_table(request, 'inv', 'fishbuy', Fishbuy, FishbuyForm,
                            row_id, {'logs'}, context, addup_fishbuy_mapper)


def fishbuy_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Fishbuy, row_id)


#
# Fishtype table
#
def show_fishtype_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'fishtype', Fishtype)


def add_update_fishtype(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'fishtype', Fishtype, FishtypeForm,
                            row_id, {'logs'}, context)


def fishtype_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Fishtype, row_id)


#
# Fooddistribution table
#
def show_fooddistribution_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'fooddistribution', Fooddistribution,
                      show_fooddistribution_mapper)


def add_update_fooddistribution(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'fooddistribution', Fooddistribution,
                            FoodDistributionForm, row_id, {'logs'}, context)


def fooddistribution_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Fooddistribution, row_id)


#
# Items table
#
def show_items_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'items', Items)


def add_update_items(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    context['sectors'] = set(get_mapping(request, SECTOR_MAPPING).values())

    return add_update_table(request, 'inv', 'items', Items, ItemsForm,
                            row_id, {'logs'}, context)


def items_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Items, row_id)


#
# Land table
#
def show_land_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'land', Land)


def add_update_land(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'land', Land, LandForm,
                            row_id, {'logs'}, context)


def land_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Land, row_id)


#
# Mousa table
#
def show_mousa_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'mousa', Mousa, show_mousa_mapper)


def add_update_mousa(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    # get the set of mousa names
    context['mousa_names'] = set(get_mapping(request, MOUSANAME_MAPPING).values())

    # get the set of dag values (remove empty strings)
    context['dag_vals'] = [v.strip() for v in set(get_mapping(request, DAG_MAPPING).values()) if v.strip() != '']

    # get the terms
    context['terms'] = set(get_mapping(request, TERM_MAPPING).values())

    # get the status mappings
    context['status_dict'] = get_mapping(request, STATUS_MAPPING)

    return add_update_table(request, 'inv', 'mousa', Mousa, MousaForm,
                            row_id, {'log'}, context, addup_mousa_mapper)


def mousa_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Mousa, row_id)


#
# Mousa Name table
#
def show_mousaname_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'mousaname', Mousaname)


def add_update_mousaname(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'mousaname', Mousaname, MousaNameForm,
                            row_id, set(), context)


def mousaname_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Mousaname, row_id)


#
# Sectors table
#
def show_sectors_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'sectors', Sectors)


def add_update_sectors(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'sectors', Sectors, SectorsForm,
                            row_id, {'logs'}, context)


def sectors_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Sectors, row_id)


#
# Units table
#
def show_units_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'units', Units)


def add_update_units(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'units', Units, UnitsForm,
                            row_id, {'logs'}, context)


def units_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Units, row_id)


#
# Dailyworks table
#
def show_dailyworks_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'dailyworks', Dailyworks, show_dailyworks_mapper)


def add_update_dailyworks(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()

    # get the work type from the Sectors mapping
    context['work_types'] = set(get_mapping(request, SECTOR_MAPPING).values())

    # get the item_names from the Items mapping
    context['item_names'] = set(get_mapping(request, ITEMS_MAPPING).values())

    # get the units from the Units mapping
    context['units'] = set(get_mapping(request, UNIT_MAPPING).values())

    return add_update_table(request, 'inv', 'dailyworks', Dailyworks, DailyworksForm,
                            row_id, {'logs'}, context)


def dailyworks_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Dailyworks, row_id)


#
# Sources table
#
def show_sources_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'sources', Sources)


def add_update_sources(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'sources', Sources, SourcesForm,
                            row_id, {'logs'}, context)


def sources_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Sources, row_id)


#
# Units table
#
def show_units_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'units', Units)


def add_update_units(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'inv', 'units', Units, UnitsForm,
                            row_id, {'logs'}, context)


def units_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Units, row_id)


#
# Term table
#
def show_term_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'term', Term)


def add_update_term(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    skip_set = set()
    return add_update_table(request, 'inv', 'term', Term, TermForm,
                            row_id, skip_set, context)


def term_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Term, row_id)
