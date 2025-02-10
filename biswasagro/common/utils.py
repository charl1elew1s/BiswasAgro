"""Shared utilities"""
from datetime import date, datetime

DATE_FMT = '%Y-%m-%d'


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
