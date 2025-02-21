"""Shared utilities"""
from django.http import JsonResponse
from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from bisauth.models import TblRoles
from datetime import datetime, timezone


DATE_FMT = '%Y-%m-%d'
LOGS_FMT = '%Y-%m-%d %H:%M:%S'

TBL_2_NAME = {
    'cost': 'Cost',
    'costitems': 'Cost Items',
    'costpurpose': 'Cost Purpose',
    'earning': 'Earning',
    'fishbuy': 'Fish Buy',
    'fishtype': 'Fish Type',
    'investment': 'Investment',
    'items': 'Items',
    'land': 'Land',
    'sectors': 'Sectors',
    'tblproduct': 'Product',
    'units': 'Units',
    'tblroles': 'Roles',
    'tblusers': 'Users',
}


def add_fields_to_session(request, model_obj):
    # dict: -> k:{str} - name of the field
    #          v:{type} - current value of the field (type depends on the type of field)
    orig = dict()
    # store the class type in orig so that we know we're comparing the right objects when the time comes
    orig['model_name'] = model_obj.__class__._meta.model_name
    for field in model_obj._meta.fields:
        field_value = getattr(model_obj, field.name)
        if isinstance(field_value, date) or isinstance(field_value, datetime):
            field_value = field_value.strftime(LOGS_FMT)
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
        # this is the case where we don't have any diffs so the field_data is just for the model_obj
        # we hit this case for a new entry in the table
        for field in model_obj._meta.fields:
            if field.name in skip_cases:
                continue
            column_name = field.name
            model_obj_value = getattr(model_obj, field.name)
            col_dict = {'col_name': column_name,
                        'orig_value': model_obj_value,
                        'new_value': ''}
            field_data.append(col_dict)

    # we no longer need the original values so let's remove them from the session
    if 'orig' in request.session:
        del request.session['orig']

    # return the set of original values for cases where changes were made
    return field_data


def delete_tabel_row(table_model_obj, row_id):
    try:
        model_obj = table_model_obj.objects.get(id=row_id)
        model_obj.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        response_json = {'success': False,
                         'error': e}
        return JsonResponse(response_json)


def show_table(request, app_name: str, table_name: str, table_model_obj: Model):
    context = dict()
    context['addModal'] = True  # for edit/delete

    # for add entry which is in the pagination_control template
    context['add_url'] = f'{app_name}:addup_{table_name}'

    # display the contents of the table (we'll always use a Paginator just in case the table is large)
    # we'll order by date in reverse order by id the newest first
    paginator = Paginator(table_model_obj.objects.all().order_by('-id'), 15)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)

    # put the page_objs into the context for rendering
    context['page_objs'] = page_objs

    template_name = f"{table_name}_landing.html"
    if table_name == 'tblusers' or request.session['user']['role'] == 'User':
        # prevent the "Add" button on the user page
        context['skipAddButton'] = True

    return render(request, template_name, context)


def add_update_table(request, app_name: str, table_name: str,
                     table_model_obj: Model, table_form_obj: ModelForm, row_id: int, skip_cases: set):
    new_entry = True
    context = dict()

    if request.method == 'GET':
        if row_id == 0:
            # this indicates that we want to add a new record (no id == 0)
            form = table_form_obj()
        else:
            # we need to go get the instance of this form (with prepopulated values)
            new_entry = False
            model_obj = get_object_or_404(table_model_obj, pk=row_id)  # get the object we want to edit
            form = table_form_obj(instance=model_obj)  # prepopulate the form with the data from the db

            # save the original fields and their values in the session so that we can report
            # on which were changed during the edit process (when this method is called via a POST request)
            add_fields_to_session(request, model_obj)

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
            # field_data = find_update_diffs(request, model_instance, skip_cases)
            field_data = find_update_diffs(request, model_instance)
            if row_id > 0:
                context['new_entry'] = False
            else:
                context['new_entry'] = True

            # update the logs field
            # we need the username which is in the session
            logged_in_username = request.session['user']['username']

            update_time = datetime.now(tz=timezone.utc).strftime(LOGS_FMT)
            model_instance.logs = f"{logged_in_username} {update_time}"
            model_instance.updated_at = update_time

            # get the created at time from the value stored in the session
            orig_created_at = get_field_data(field_data, 'created_at')
            if orig_created_at:
                model_instance.created_at = orig_created_at

            password_hash = get_field_data(field_data, 'password')
            model_instance.password = password_hash

            model_instance.save()

            # remove the skip_cases plus 'id'
            skip_cases.add('id')
            post_skip_data = []
            for field_dict in field_data:
                if field_dict['col_name'] in skip_cases:
                    continue
                post_skip_data.append(field_dict)
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
            return render(request, add_update_template_name, {'form': form})

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
    """Returns a dictionary with a mapping of role_id to role_name of all the values in the tbl_role table"""
    # dict -> k:{int} - roleID from database
    #         v:{str} - role name (e.g. Admin, Manager, etc)
    roleid_2_name = dict()
    qs = TblRoles.objects.all()
    for role_obj in qs:
        roleid_2_name[role_obj.id] = role_obj.role
    return roleid_2_name


def get_field_data(field_data, key):
    if field_data:
        for col_dict in field_data:
            if col_dict.get('col_name') == key:
                return col_dict.get('orig_value')
    else:
        return None
