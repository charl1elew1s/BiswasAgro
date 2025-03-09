"""Shared utilities"""
from django.core.exceptions import FieldDoesNotExist
from django.http import JsonResponse
from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from bisauth.models import Roles
from decimal import Decimal
from datetime import datetime, timezone
from inventory.models import Sectors

DATE_FMT = '%Y-%m-%d'
LOGS_FMT = '%Y-%m-%d %H:%M:%S'

TBL_2_NAME = {
    'cost': 'Casual Expenses',
    'costitems': 'Products',
    'costpurpose': 'Cost Purpose',
    'dailyworks': 'Daily Works',
    'earning': 'Earning',
    'fishbuy': 'Fish Buy',
    'fishtype': 'Fish Type',
    'fooddistribution': 'Food Distribution',
    'investment': 'Investment',
    'items': 'Items',
    'land': 'Land',
    'loandetails': 'Loan Details',
    'loan_providers_info': 'Loan Providers',
    'mousa': 'Mousa',
    'mousaname': 'Mousa Names',
    'salary': 'Salary',
    'sectors': 'Sectors',
    'staff': 'Staff',
    'staffs': 'Staffs',
    'units': 'Units',
    'roles': 'Roles',
    'usersinfo': 'Users',
    'term': 'Term'
}

# these are the primary keys for a given table (the default primary key field name is 'id' so we only put tables
# in this dictionary that DO NOT have 'id' as it's primary key)
TABLE_PK_FIELDS = {
    'loandetails': 'loanid',
    'loan_providers_info': 'investerid',
    'staff': 'staffNo',
}

STATUS_LIST = [(1, 'Paid'), (2, 'Due')]


def add_fields_to_session(request, model_obj):
    # dict: -> k:{str} - name of the field
    #          v:{type} - current value of the field (type depends on the type of field)
    orig = dict()
    # store the class type in orig so that we know we're comparing the right objects when the time comes
    orig['model_name'] = model_obj.__class__._meta.model_name
    for field in model_obj._meta.fields:
        field_value = getattr(model_obj, field.name)
        if isinstance(field_value, date) or isinstance(field_value, datetime):
            field_value = field_value.strftime(DATE_FMT)
        if isinstance(field_value, Decimal):
            field_value = str(field_value)  # convert Decimals to strings for serialization
        orig[field.name] = field_value
    request.session['orig'] = orig


def find_update_diffs(request, model_obj, skip_cases=set()):
    """
    return a list of dictionaries which have the following structure
         { 'col_name': {str},
           'orig_value' : {str},
           'new_value' : {str} [Note: this could be an empty string]
    """
    field_data = []

    # if orig is in the session make sure the model_name is the same as "our" model_name if it isn't, it's
    # a leftover remnant that needs to be removed
    if 'orig' in request.session:
        orig_dict = request.session['orig']
        our_model_name = model_obj.__class__._meta.model_name
        if 'model_name' not in orig_dict or orig_dict['model_name'] != our_model_name:
            del request.session['orig']

    if 'orig' in request.session:
        orig_dict = request.session['orig']
        for field in model_obj._meta.fields:
            if field.name in skip_cases:
                continue
            column_name = field.name
            model_obj_value = getattr(model_obj, field.name)
            if isinstance(model_obj_value, date) or isinstance(model_obj_value, datetime):
                model_obj_value = model_obj_value.strftime(DATE_FMT)
            if isinstance(model_obj_value, Decimal):
                # for this model_obj value we converted the value into a string before we serialized it in
                # the session so now we need to convert the string back into a Decimal
                orig_field_value = Decimal(orig_dict[column_name])
            else:
                orig_field_value = orig_dict[column_name]
            if model_obj_value == orig_field_value:
                # no change for this field
                orig_value = model_obj_value
                new_value = ''
            else:
                # this field was updated
                orig_value = orig_field_value
                new_value = model_obj_value
            col_dict = {'col_name': column_name,
                        'orig_value': orig_value,
                        'new_value': new_value}
            field_data.append(col_dict)
    else:
        # This is the case where we don't have any diffs so the field_data is just for the model_obj.
        # We hit this case for a new entry in the table
        for field in model_obj._meta.fields:
            if field.name in skip_cases:
                continue
            column_name = field.name
            model_obj_value = getattr(model_obj, field.name)
            if isinstance(model_obj_value, date) or isinstance(model_obj_value, datetime):
                model_obj_value = model_obj_value.strftime(DATE_FMT)
            col_dict = {'col_name': column_name,
                        'orig_value': model_obj_value,
                        'new_value': ''}
            field_data.append(col_dict)

    # we no longer need the original values so let's remove them from the session
    if 'orig' in request.session:
        del request.session['orig']

    # return the list of col_dict objects for each field of the model_obj
    # CL: ++
    # print("\nfield_data values:\n")
    # for field_dict in field_data:
    #     print(f"  field_dict: {field_dict}")
    # print("\n")
    # CL: --
    return field_data


def delete_tabel_row(table_model_obj, row_id):
    try:
        pk_name = table_model_obj._meta.pk.name
        kwargs = {pk_name: row_id}
        model_obj = table_model_obj.objects.get(**kwargs)
        model_obj.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        response_json = {'success': False,
                         'error': e}
        return JsonResponse(response_json)


def show_table(request, app_name: str, table_name: str, table_model_obj: Model, page_mapper=None):
    context = dict()
    context['addModal'] = True  # for edit/delete

    # for add entry which is in the pagination_control template
    context['add_url'] = f'{app_name}:addup_{table_name}'

    # display the contents of the table (we'll always use a Paginator just in case the table is large)
    # we'll present in reverse order by the primary key, this will give the newest first
    # we get the name of the primary key from the table_model class (table_model_obj). We need to do this because
    # not all tables have a primary key of 'id'
    pk_fieldname = table_model_obj._meta.pk.name
    sorted_pk_fieldname = f'-{pk_fieldname}'
    paginator = Paginator(table_model_obj.objects.all().order_by(sorted_pk_fieldname), 15)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)

    # put the page_objs into the context for rendering, but if any of the columns need look-ups use the passed
    # in <table specific> page_mapper function to do the looks for us
    if page_mapper:
        page_mapper(request, page_objs)
    context['page_objs'] = page_objs

    template_name = f"{table_name}_landing.html"
    if table_name == 'usersinfo' or request.session['user']['role'] == 'User':
        # prevent the "Add" button on the user page
        context['skipAddButton'] = True

    return render(request, template_name, context)


def add_update_table(request, app_name: str, table_name: str,
                     table_model_obj: Model, table_form_obj: ModelForm,
                     row_id: int, skip_cases: set, context: dict, col_mapper=None):

    # remove the skip_cases plus 'id' (we never want to include the 'id')
    skip_cases.add('id')
    new_entry = True
    if request.method == 'GET':
        if row_id == 0:
            # this indicates that we want to add a new record (no id == 0)
            form = table_form_obj()
            # we want to get rid of any "orig" data in the session since we know we want a new entry here
            if 'orig' in request.session:
                del request.session['orig']
        else:
            # we need to go get the instance of this form (with prepopulated values)
            new_entry = False
            model_obj = get_object_or_404(table_model_obj, pk=row_id)  # get the object we want to edit
            form = table_form_obj(instance=model_obj)  # prepopulate the form with the data from the db

            # save the original fields and their values in the session so that we can report
            # on which were changed during the edit process (when this method is called via a POST request)
            add_fields_to_session(request, model_obj)
            # CL: ++
            #  : let's see the values in the session 'orig'
            # print(f"request.session['orig']: {request.session['orig']}")
            # CL: --

    elif request.method == 'POST':
        # if row_id is 0, it's a new record, so we just create a new form
        if row_id == 0:
            form = table_form_obj(request.POST)
        else:
            # for an existing record, we need to update the instance of the form
            new_entry = False
            model_obj = get_object_or_404(table_model_obj, pk=row_id)  # get the object to update
            form = table_form_obj(request.POST, instance=model_obj)

        if form.is_valid():
            # we need the Model object, but we don't want to *yet* commit changes to the database
            # we'll do that after we update the logs field
            model_instance = form.save(commit=False)

            # pass find_update_diffs the cases that we don't want to include in the resultant list
            field_data = find_update_diffs(request, model_instance, skip_cases)
            if row_id > 0:
                context['new_entry'] = False
            else:
                context['new_entry'] = True

            # update the logs field
            # first see if there is a logs field and if so what it's max length is (they are all different)
            try:
                log_field = table_model_obj._meta.get_field('logs')
                if log_field:
                    max_length = -1
                    if hasattr(log_field, 'max_length'):
                        max_length = log_field.max_length

                    # we need the username which is in the session
                    logged_in_username = request.session['user']['username']
                    update_time = datetime.now(tz=timezone.utc).strftime(LOGS_FMT)
                    full_log_field = f"{logged_in_username} {update_time}"
                    truncated_log = full_log_field[:max_length]
                    model_instance.logs = truncated_log
            except FieldDoesNotExist as fde:
                # nothing to do here we were just checking if the field was there
                pass

            # hash the password field if it exists on the Model Object
            try:
                password_field = table_model_obj._meta.get_field('password')
                if password_field:
                    password_hash = get_field_data(field_data, 'password')
                    model_instance.password = password_hash
            except FieldDoesNotExist as fde:
                # nothing to do here
                pass

            model_instance.save()

            post_skip_data = []
            form_labels = form.Meta.labels
            for field_dict in field_data:
                # remap the column name with values that came from the labels dict in the form
                # (to make them more human readable)
                field_dict['col_name'] = form_labels[field_dict['col_name']]
                post_skip_data.append(field_dict)

            # CL: ++
            # print("\npost_skip_data:\n")
            # for field_dict in post_skip_data:
            #     print(f"  field_dict: {field_dict}")
            # CL: --

            if col_mapper:
                col_mapper(request, post_skip_data)

            context['field_data'] = post_skip_data

            field_values = form.cleaned_data
            table_heading = TBL_2_NAME[table_name]
            if new_entry:
                context['heading'] = f'Record added to the {table_heading} table'
            else:
                context['heading'] = f'Entry updated in the {table_heading} table'
            context['field_values'] = field_values
            url_str = f"{app_name}:show_{table_name}_table"
            relative_url = reverse(url_str)
            full_url = request.build_absolute_uri(relative_url)
            context['next_url'] = full_url

            return render(request, 'add_update_confirmation.html', context)

        else:
            print('form is NOT valid!')
            add_update_template_name = f"add_update_{table_name}.html"
            context['form'] = form
            context['row_id'] = row_id
            return render(request, add_update_template_name, context)

    context['form'] = form
    context['row_id'] = row_id
    table_heading = TBL_2_NAME[table_name]
    if new_entry:
        context['heading'] = f'Add New {table_heading} Entry'
    else:
        context['heading'] = f'Update {table_heading} Entry'

    add_update_template_name = f"add_update_{table_name}.html"
    return render(request, add_update_template_name, context)


def get_user_roles():
    """Returns a list of all the values in the role table"""
    role_names = []
    qs = Roles.objects.all()
    for role_obj in qs:
        role_names.append(role_obj.role)
    return role_names


def get_field_data(field_data, key):
    if field_data:
        for col_dict in field_data:
            if col_dict.get('col_name') == key:
                return col_dict.get('orig_value')
    else:
        return None


