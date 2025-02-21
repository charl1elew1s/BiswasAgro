from django.shortcuts import redirect
from .models import Fishbuy, Fishtype, Items, Land, Sectors, TblProduct, Units
from .forms import FishbuyForm, FishtypeForm, ItemsForm, LandForm, SectorsForm, TblProductForm, UnitsForm
from common.utils import delete_tabel_row, show_table, add_update_table


#
# Fishbuy table
#
def show_fishbuy_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'fishbuy', Fishbuy)


def add_update_fishbuy(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'inv', 'fishbuy', Fishbuy, FishbuyForm, row_id, {'logs'})


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

    return add_update_table(request, 'inv', 'fishtype', Fishtype, FishtypeForm, row_id, {'logs'})


def fishtype_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Fishtype, row_id)


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

    return add_update_table(request, 'inv', 'items', Items, ItemsForm, row_id, {'logs'})


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

    return add_update_table(request, 'inv', 'land', Land, LandForm, row_id, {'logs'})


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

    return add_update_table(request, 'inv', 'sectors', Sectors, SectorsForm, row_id, {'logs'})


def sectors_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Sectors, row_id)


#
# Tblproduct table
#
def show_tblproduct_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'inv', 'tblproduct', TblProduct)


def add_update_tblproduct(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return add_update_table(request, 'inv', 'tblproduct', TblProduct, TblProductForm, row_id, {'logs'})


def tblproduct_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(TblProduct, row_id)


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

    return add_update_table(request, 'inv', 'units', Units, UnitsForm, row_id, {'logs'})


def units_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(Units, row_id)
