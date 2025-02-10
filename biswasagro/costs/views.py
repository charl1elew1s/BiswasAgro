import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.timezone import now
from .forms import CostForm
from .models import Cost, Costitems, Costpurpose
from common.utils import add_fields_to_session, find_update_diffs

LOGS_FMT = '%Y-%m-%d %H:%M:%S'


def show_cost_table(request):
    context = dict()
    context['addModal'] = True  # for edit/delete
    context['add_url'] = 'costs:addup_cost'  # for add entry which is in the pagination_control template

    # display the contents of the table (we'll always use a Paginator just in case the table is large)
    # we'll order by date in reverse chronological order (latest first)
    paginator = Paginator(Cost.objects.all().order_by('-date'), 15)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)

    # put the page_objs into the context for rendering
    context['page_objs'] = page_objs

    return render(request, 'cost_landing.html', context)


def cost_delete_row(request, row_id):
    try:
        cost_obj = Cost.objects.get(id=row_id)
        cost_obj.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        response_json = {'success': False,
                         'error': e}
        return JsonResponse(response_json)


def add_update_cost(request, row_id):
    new_entry = True
    context = dict()

    # CL: ++
    print(f"CL comment - add_update_cost() was called with row_id={row_id} using method={request.method}")
    # CL: --

    if request.method == 'GET':
        if row_id == 0:
            # this indicates that we want to add a new record (no id == 0)
            form = CostForm()
        else:
            # we need to go get the instance of this form (with prepopulated values)
            new_entry = False
            cost_obj = get_object_or_404(Cost, pk=row_id)  # get the object we want to edit
            form = CostForm(instance=cost_obj)  # prepopulate the form with the data from the db

            # save the original fields and their values in the session so that we can report
            # on which were changed during the edit process (when this method is called via a POST request)
            add_fields_to_session(request, cost_obj)

    elif request.method == 'POST':
        # if row_id is 0, it's a new record, so we just create a new form
        if row_id == 0:
            form = CostForm(request.POST)
        else:
            # for an existing record, we need to update the instance of the form
            new_entry = False
            cost_obj = get_object_or_404(Cost, pk=row_id)  # get the object to update
            form = CostForm(request.POST, instance=cost_obj)

        if form.is_valid():
            # we need the Cost Model object, but we don't want to *yet* commit changes to the database
            # we'll do that after we update the logs field
            cost_instance = form.save(commit=False)

            # pass find_update_diffs the cases that we don't want to include in the resultant list
            skip_cases = {'logs'}
            field_data = find_update_diffs(request, cost_instance, skip_cases)
            context['field_data'] = field_data
            # we don't want to display the logs entry in the confirmation since the user did not update that
            # field so we remove it from the field_data
            # del field_data['logs']
            if row_id > 0:
                context['new_entry'] = False
            else:
                context['new_entry'] = True

            # update the logs field
            logged_in_username = 'longo'  # CL: pretend like I figured out how to get this!!
            update_time = now().strftime(LOGS_FMT)
            cost_instance.logs = f"{logged_in_username} {update_time}"
            cost_instance.save()

            field_values = form.cleaned_data
            if new_entry:
                context['heading'] = 'Record added to the Cost table'
            else:
                context['heading'] = 'Entry updated in the Cost table'
            context['field_values'] = field_values
            relative_url = reverse('costs:show_cost_table')
            full_url = request.build_absolute_uri(relative_url)
            context['next_url'] = full_url
            return render(request, 'add_update_confirmation.html', context)

        else:
            print('form is NOT valid!')
            return render(request, 'add_update_cost.html', {'form': form})

    context['form'] = form
    context['row_id'] = row_id
    if new_entry:
        context['heading'] = 'Add New Cost Entry'
    else:
        context['heading'] = 'Update Cost Entry'

    return render(request, 'add_update_cost.html', context)
