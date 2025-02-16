"""Shared utilities"""
from django.http import JsonResponse
from datetime import date, datetime
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Model
from django.forms import ModelForm
from django.urls import reverse
from django.utils.timezone import now


DATE_FMT = '%Y-%m-%d'
LOGS_FMT = '%Y-%m-%d %H:%M:%S'


def add_fields_to_session(request, model_obj):
    # dict: -> k:{str} - name of the field
    #          v:{type} - current value of the field (type depends on the type of field)
    orig = dict()
    for field in model_obj._meta.fields:
        field_value = getattr(model_obj, field.name)
        if isinstance(field_value, date) or isinstance(field_value, datetime):
            field_value = field_value.strftime(DATE_FMT)
        orig[field.name] = field_value
    request.session['orig'] = orig


def find_update_diffs(request, model_obj, skip_cases=set()):
    """
    return a list of dictionaries which have the following structure
         { 'col_name': {str},
           'orig_value' : {str},
           'new_value' : {str} [Note: this could be an empty string]
    """
    # we always skip the 'id' field so add that to the passed in skip_cases set
    skip_cases.add('id')
    # get original values from the session
    field_data = []
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
    if table_name == 'tblusers':
        # prevent the "Add" button on the user page
        context['skipButton'] = True

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
            field_data = find_update_diffs(request, model_instance, skip_cases)
            context['field_data'] = field_data
            # we don't want to display the logs entry in the confirmation since the user did not update that
            # field so we remove it from the field_data
            # del field_data['logs']
            if row_id > 0:
                context['new_entry'] = False
            else:
                context['new_entry'] = True

            # update the logs field
            logged_in_username = 'user'  # CL: pretend like I figured out how to get this!!
            update_time = now().strftime(LOGS_FMT)
            model_instance.logs = f"{logged_in_username} {update_time}"
            model_instance.save()

            field_values = form.cleaned_data
            if new_entry:
                context['heading'] = f'Record added to the {table_name} table'
            else:
                context['heading'] = f'Entry updated in the {table_name} table'
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
    if new_entry:
        context['heading'] = f'Add New {table_name} Entry'
    else:
        context['heading'] = f'Update {table_name} Entry'

    add_update_template_name = f"add_update_{table_name}.html"

    return render(request, add_update_template_name, context)
