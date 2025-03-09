"""
These are functions used to map table columns to values taken from other table/cols.
"""
from datetime import date
from costs.models import Costitems
from inventory.models import Sectors, Items, Sources, Units, Fishtype
from common.utils import DATE_FMT

STATUS_MAP = {1: 'Paid', 2: 'Due'}

STATUS_MAPPING = 'status_mapping'
SECTOR_MAPPING = 'sector_mapping'
COSTITEM_MAPPING = 'costitem_mapping'
ITEMS_MAPPING = 'items_mapping'
SOURCE_MAPPING = 'source_mapping'
UNIT_MAPPING = 'unit_mapping'
FISHTYPE_MAPPING = 'fishtype_mapping'


def get_mapping(request, mapping_type):
    """
    We want to cache the mappings and centralize the storing and retrieving of these mappings from the
    session. Because the dictionaries are stored in the session, a potential problem could arise when the dictionary
    keys and values are serialized to be stored, Django converts the dictionaries to json which requires the keys to
    be strings so when we return a dictionary we must convert the keys back to ints, we do this using a dictionary
    comprehension.
    """
    the_mapping = request.session.get(mapping_type)
    if not the_mapping:
        the_mapping = dict()
        if mapping_type == STATUS_MAPPING:
            the_mapping = STATUS_MAP
        elif mapping_type == SECTOR_MAPPING:
            for sec in Sectors.objects.all():
                the_mapping[sec.id] = sec.sector.strip()
        elif mapping_type == COSTITEM_MAPPING:
            for citm in Costitems.objects.all():
                the_mapping[citm.id] = citm.costitems.strip()
        elif mapping_type == ITEMS_MAPPING:
            for itm in Items.objects.all():
                the_mapping[itm.id] = itm.item_name.strip()
        elif mapping_type == SOURCE_MAPPING:
            for src in Sources.objects.all():
                the_mapping[src.id] = src.source.strip()
        elif mapping_type == UNIT_MAPPING:
            for unt in Units.objects.all():
                the_mapping[unt.id] = unt.unit.strip()
        elif mapping_type == FISHTYPE_MAPPING:
            for ftype in Fishtype.objects.all():
                the_mapping[ftype.id] = ftype.fishname.strip()

        request.session[mapping_type] = the_mapping

    # in every one of these mappings we are storing a database id (an int) as the key and a string as the value,
    # because of this we know converting the keys to ints is OK.
    return {int(k): v for k, v in the_mapping.items()}


def remove_all_mappings(request):
    if request.session.get(SECTOR_MAPPING):
        del request.session[SECTOR_MAPPING]
    if request.session.get(ITEMS_MAPPING):
        del request.session[ITEMS_MAPPING]
    if request.session.get(SOURCE_MAPPING):
        del request.session[SOURCE_MAPPING]
    if request.session.get(UNIT_MAPPING):
        del request.session[UNIT_MAPPING]


def get_mapped_value(mapper, field_data):
    """change the passed-in field_data in-place (as a side effect)"""
    field_data['orig_value'] = mapper[int(field_data['orig_value'])]
    if field_data['new_value'] != '':
        field_data['new_value'] = mapper[int(field_data['new_value'])]


#
# Cost table mappers
#
def show_cost_mapper(request, page_objs):
    # change the status to Paid or Due appropriately
    for page_obj in page_objs:
        page_obj.status = STATUS_MAP[int(page_obj.status)]
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)


def addup_cost_mapper(request, field_data_list):
    # get the mapping status_id -> status
    status_mapping = get_mapping(request, STATUS_MAPPING)

    for field_data in field_data_list:
        col_name = field_data['col_name']
        if col_name == 'Status':
            get_mapped_value(status_mapping, field_data)


#
# Costitems table mappers
#
def show_costitems_mapper(request, page_objs):
    sector_mapping = get_mapping(request, SECTOR_MAPPING)
    for page_obj in page_objs:
        page_obj.sector = sector_mapping.get(page_obj.sector, '--')


def addup_costitems_mapper(request, field_data_list):
    # get the mappings sector_id -> sector
    sector_mapping = get_mapping(request, SECTOR_MAPPING)

    # we're just relying on the side effect of changing the passed in list in-place
    for field_data in field_data_list:
        if field_data['col_name'] == 'Sector':
            get_mapped_value(sector_mapping, field_data)


#
# Earnings table mappers
#
def show_earning_mapper(request, page_objs):
    # get the mappings sector_id -> sector
    sector_mapping = get_mapping(request, SECTOR_MAPPING)

    # get mappings items_id -> items_name
    items_mapping = get_mapping(request, ITEMS_MAPPING)

    # get mappings source_id -> source
    source_mapping = get_mapping(request, SOURCE_MAPPING)

    # get mappings unit_id -> unit
    unit_mapping = get_mapping(request, UNIT_MAPPING)

    for page_obj in page_objs:
        page_obj.status = STATUS_MAP[int(page_obj.status)]
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)
        page_obj.sector = sector_mapping[page_obj.sector]
        page_obj.item = items_mapping[page_obj.item]
        page_obj.source = source_mapping[page_obj.source]
        page_obj.unit = unit_mapping[page_obj.unit]


def addup_earning_mapper(request, field_data_lst):

    # get the mapping status_id -> status
    status_mapping = get_mapping(request, STATUS_MAPPING)

    # get the mappings sector_id -> sector
    sector_mapping = get_mapping(request, SECTOR_MAPPING)

    # get mappings items_id -> items_name
    items_mapping = get_mapping(request, ITEMS_MAPPING)

    # get mappings source_id -> source
    source_mapping = get_mapping(request, SOURCE_MAPPING)

    # get mappings unit_id -> unit
    unit_mapping = get_mapping(request, UNIT_MAPPING)

    for field_data in field_data_lst:
        col_name = field_data['col_name']
        mapper = None
        if col_name == 'Sector':
            mapper = sector_mapping
        elif col_name == 'Status':
            mapper = status_mapping
        elif col_name == 'Item':
            mapper = items_mapping
        elif col_name == 'Source':
            mapper = source_mapping
        elif col_name == 'Unit':
            mapper = unit_mapping

        # now just change the field values using the mapper
        if mapper:
            get_mapped_value(mapper, field_data)


#
# Daily Works table mappers
#
def show_dailyworks_mapper(request, page_objs):
    for page_obj in page_objs:
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)


#
# Fishbuy table mappers
#
def show_fishbuy_mapper(request, page_objs):
    for page_obj in page_objs:
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)
        page_obj.status = STATUS_MAP[int(page_obj.status)]


def addup_fishbuy_mapper(request, field_data_lst):
    # get the mapping status_id -> status
    status_mapping = get_mapping(request, STATUS_MAPPING)

    for field_data in field_data_lst:
        col_name = field_data['col_name']
        mapper = None
        if col_name == 'Status':
            mapper = status_mapping

        # now just change the field values using the mapper
        if mapper:
            get_mapped_value(mapper, field_data)


#
# Food Distribution mappers
#
def show_fooddistribution_mapper(request, page_objs):
    for page_obj in page_objs:
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)


#
# Investment mappers
#
def show_investment_mapper(request, page_objs):
    for page_obj in page_objs:
        if isinstance(page_obj.date, date):
            page_obj.date = page_obj.date.strftime(DATE_FMT)
