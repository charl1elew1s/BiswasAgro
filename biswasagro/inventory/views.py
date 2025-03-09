from django.shortcuts import redirect
from .models import (Fishbuy, Fishtype, Items, Land, Sectors, Units, Dailyworks, Fooddistribution)
from .forms import (FishbuyForm, FishtypeForm, ItemsForm, LandForm, SectorsForm, UnitsForm, DailyworksForm,
                    FoodDistributionForm)
from common.utils import (delete_tabel_row, show_table, add_update_table)
# from common.column_mappers import (SECTOR_MAPPING, ITEMS_MAPPING, UNIT_MAPPING, FISHTYPE_MAPPING,
#                                    SOURCE_MAPPING, STATUS_MAPPING)
# from common.column_mappers import (get_mapping, show_dailyworks_mapper, show_fishbuy_mapper, addup_fishbuy_mapper,
#                                    show_fooddistribution_mapper)
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

    return delete_tabel_row(Fishbuy, row_id)


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

    return delete_tabel_row(Fishtype, row_id)


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

    return delete_tabel_row(Fooddistribution, row_id)


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

    return delete_tabel_row(Items, row_id)


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

    return delete_tabel_row(Land, row_id)


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

    return delete_tabel_row(Sectors, row_id)


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

    return delete_tabel_row(Units, row_id)


#
# Dailyworks table
#
def show_dailyworks_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'dailyworks', Dailyworks, show_dailyworks_mapper)
    # return show_table(request, 'inv', 'dailyworks', Dailyworks)


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

    return delete_tabel_row(Dailyworks, row_id)
