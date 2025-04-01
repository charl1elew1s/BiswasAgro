import re
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date, datetime
from collections import defaultdict
from costs.models import Cost, Earning
from inventory.models import Fishbuy
from .forms import DateSelectorForm, YearMonthForm, YearForm, ToFromDateSelectorForm
from common.utils import get_dates_in_month, get_now
from common.column_mappers import *

# expected: 2025-04 [April 2025]
# m.group(1) -> year
# m.group(2) -> month (zero padded)
MONTHLY_RE = re.compile(r"(\d{4})-(\d{2})")

# expected: 23-04-2025 [April 23 2025]
# m.group(1) -> day (zero padded)
# m.group(2) -> month (zero padded)
# m.group(3) -> year
DAILY_RE = re.compile(r"(\d{2})-(\d{2})-(\d{4})")

MONTH_NAMES = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}
DISPLAY_FMT = '%d-%m-%Y'
DB_FMT = '%Y-%m-%d'


def reports_landing(request):
    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    return render(request, 'reports_landing.html', {})


def daily(request, str_date):
    """Generate the daily report, it should include, costs, fishbuy and earnings"""

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    right_now = get_now(to_str=False)

    month_word = None
    day_word = None
    if request.method == 'GET':
        if str_date == 'now':
            # this means to use right now as the timestamp
            month_word = right_now.strftime('%B')
            month_numb_str = right_now.strftime('%m')
            year_str = right_now.strftime('%Y')
            day_str = right_now.strftime('%d')
        else:
            # we need to parse the passed in str_date to know which date we're actually interested in
            m = DAILY_RE.search(str_date)
            if m:
                day_str = m.group(1)
                month_numb_str = m.group(2)
                year_str = m.group(3)
                # get the day_word and month_word by creating a datetime object and then changing its format
                dt = datetime.strptime(str_date, '%d-%m-%Y')
                month_word = dt.strftime('%B')
                day_word = dt.strftime('%a')
            else:
                # a bad string was passed to us so just use "now" as a fall-back
                day_word = right_now.strftime('%a')
                day_str = right_now.strftime('%d')
                month_word = right_now.strftime('%B')
                month_numb_str = right_now.strftime('%m')
                year_str = right_now.strftime('%Y')

        # we need year-month-day for initializing a date field
        date_str = f"{year_str}-{month_numb_str}-{day_str}"

        initial_data = {'date': date_str}  # allow the form constructor parse the string
        form = DateSelectorForm(initial=initial_data, data=initial_data)
    else:
        # POST
        form = DateSelectorForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'daily_report.html'
        return render(request, template_name, context)

    # from here we know we have a valid form (date)
    cleaned_data = form.cleaned_data
    form_date = cleaned_data['date']  # datetime.date object

    # CL: ++
    print(f"form is valid, cleaned_data: {cleaned_data}")
    # CL: --

    year_str = form_date.strftime('%Y')
    month_numb_str = form_date.strftime('%m')
    day_str = form_date.strftime('%d')

    if not month_word:
        month_word = form_date.strftime('%B')

    if not day_word:
        day_word = form_date.strftime('%a')

    date_query_str = f"{year_str}-{month_numb_str}-{day_str}"

    #
    # Costs (from cost table and fishbuy table)
    #

    # get the data from cost table
    rows_from_cost = list(Cost.objects.filter(date=date_query_str))
    context['rows_from_cost'] = rows_from_cost
    context['num_rows_from_cost'] = len(rows_from_cost)
    context['num_rows_from_cost_plus_1'] = len(rows_from_cost) + 1

    cost_total = 0.00
    for row in rows_from_cost:
        # reformat the cost values by converting them to strings with commas (for display in the template)
        cost_total += row.cost
        row.cost = f"{row.cost:,.2f}"  # we convert to a string just for display
    context['cost_total'] = f"{cost_total:,.2f}"

    # get the data from the fishbuy table
    rows_from_fishbuy = list(Fishbuy.objects.filter(date=date_query_str))
    context['rows_from_fishbuy'] = rows_from_fishbuy
    context['num_rows_from_fishbuy'] = len(rows_from_fishbuy)
    context['num_rows_from_fishbuy_plus_1'] = len(rows_from_fishbuy) + 1

    fishbuy_total = 0.0
    for row in rows_from_fishbuy:
        # reformat the price values by converting them to strings with commas (for display in the template)
        fishbuy_total += row.price
        row.price = f"{row.price:,.2f}"  # we convert to a string just for display
    context['fishbuy_total'] = f"{fishbuy_total:,.2f}"

    income_grand_total = cost_total + fishbuy_total
    context['income_grand_total'] = f"{income_grand_total:,.2f}"

    #
    # Earnings (from earnings table)
    #
    rows_from_earning = list(Earning.objects.filter(date=date_query_str))
    context['rows_from_earning'] = rows_from_earning
    context['num_rows_from_earning'] = len(rows_from_earning)
    context['num_rows_from_earning_plus_1'] = len(rows_from_earning) + 1

    earning_total = 0.0
    # we need to do the mappings lookups and reformat the price values for display
    sector_mapping = get_mapping(request, SECTOR_MAPPING)
    item_mapping = get_mapping(request, ITEMS_MAPPING)
    source_mapping = get_mapping(request, SOURCE_MAPPING)
    for row in rows_from_earning:
        # reformat the price values by converting them to strings with commas (for display in the template)
        earning_total += row.price
        row.sector = sector_mapping[row.sector]
        row.item = item_mapping[row.item]
        row.source = source_mapping[row.source]
        row.price = f"{row.price:,.2f}"
    context['earning_total'] = f"{earning_total:,.2f}"

    context['form'] = form
    context['right_now'] = get_now(to_str=True)
    context['month_word'] = month_word
    context['year'] = int(year_str)
    context['month'] = month_numb_str
    context['day_str'] = day_str
    context['day_word'] = day_word

    template_name = 'daily_report.html'
    return render(request, template_name, context)


def monthly(request, str_date):
    """Generate the monthly report of costs and expenses"""

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    # we always want to report on when the report was made: "now"
    right_now = get_now(to_str=False)
    # datetime.now(ZoneInfo("Europe/London"))

    month_word = None
    if request.method == 'GET':
        if str_date == 'now':
            # this means to use right now as the timestamp
            month_word = right_now.strftime('%B')
            month_numb_str = right_now.strftime('%m')
            year_str = right_now.strftime('%Y')
        else:
            # we need to parse the passed in str_date to know which month we're actually interested in
            m = MONTHLY_RE.search(str_date)
            if m:
                year_str = m.group(1)
                month_numb_str = m.group(2)
                # get the month_word by creating a datetime object and then changing its format
                dt = datetime.strptime(str_date, '%Y-%m')
                month_word = dt.strftime('%B')
            else:
                # a bad string was passed to us so just use "now" as a fall-back
                month_word = right_now.strftime('%B')
                month_numb_str = right_now.strftime('%m')
                year_str = right_now.strftime('%Y')

        initial_data = {'year': year_str, 'month': month_numb_str}
        form = YearMonthForm(initial=initial_data, data=initial_data)

    else:
        form = YearMonthForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'monthly_report.html'
        return render(request, template_name, context)

    # the rest of this code executes on a valid form submission (or initialization)
    context['form'] = form
    cleaned_data = form.cleaned_data

    year_str = cleaned_data['year']
    month_numb_str = cleaned_data['month']

    # set month_word if it's not already set (in the case of a POST request it won't be set)
    if not month_word or month_word == '':
        # we just want to know the name of the Month so any day will do
        date_obj = date(int(year_str), int(month_numb_str), 1)
        month_word = date_obj.strftime('%B')

    date_query_str = f"{year_str}-{month_numb_str}"

    # dict -> k:{str} - date in the format: dd-mm-yyyy
    #         v:{list] - 2 value list [costs , earnings] either could be zero, hence the default values of 0.0
    value_dict = defaultdict(lambda: [0.0, 0.0])

    # get the date and cost values from the costs table for the month in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_cost = list(Cost.objects.filter(date__startswith=date_query_str, status=1).values('date', 'cost'))
    rows_from_cost = list(Cost.objects.filter(date__startswith=date_query_str).values('date', 'cost'))

    # start building the value_dict for these values
    for row in rows_from_cost:
        date_val = row['date']
        cost_val = row['cost']
        # we don't yet have any earnings for this date so don't touch the default value of 0.0
        value_dict[date_val][0] += cost_val

    # get the costs (price) from the fishbuy table for the month in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=date_query_str, status=1).values('date', 'price'))
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=date_query_str).values('date', 'price'))

    # if any value is for an existing month add the value from the fisthbuy table
    for row in rows_from_fishbuy:
        date_val = row['date']
        price_val = row['price']
        value_dict[date_val][0] += price_val

    # now get the earnings values from the earning table
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_earning = list(Earning.objects.filter(date__startswith=date_query_str, status=1).values('date', 'price'))
    rows_from_earning = list(Earning.objects.filter(date__startswith=date_query_str).values('date', 'price'))

    # now update the earning values in the value_dict for any date found
    for row in rows_from_earning:
        date_val = row['date']
        price_val = row['price']
        value_dict[date_val][1] += price_val

    # get the totals for both cost and earning
    total_costs = f"{sum([v[0] for k, v in value_dict.items()]):,.2f}"
    total_earnings = f"{sum([v[1] for k, v in value_dict.items()]):,.2f}"

    # convert all the values to a displayable format
    report_value_dict = dict()
    if len(value_dict) > 0:
        # since there are at least some values for this month we need to report on every day of the month

        # get all the days in the given month (these values are already in sorted order)
        all_days_for_month = get_dates_in_month(int(year_str), int(month_numb_str))

        for date_obj in all_days_for_month:
            date_value = value_dict[date_obj]
            # convert the date to the correct display format
            date_str = date_obj.strftime(DISPLAY_FMT)
            cost_val = f"{value_dict[date_obj][0]:,.2f}"
            earning_val = f"{value_dict[date_obj][1]:,.2f}"
            report_value_dict[date_str] = [cost_val, earning_val]

    now_yr = right_now.strftime('%Y')
    context['year_select'] = [y for y in range(int(now_yr) - 6, int(now_yr) + 1)]  # last 6 years
    context['month_select'] = MONTH_NAMES
    context['right_now'] = get_now(to_str=True)
    context['month_word'] = month_word
    context['year'] = int(year_str)
    context['month'] = month_numb_str
    context['value_dict'] = report_value_dict
    context['total_costs'] = total_costs
    context['total_earnings'] = total_earnings
    template_name = 'monthly_report.html'
    return render(request, template_name, context)


def annual(request, str_date):
    """Generate the annual report of costs and expenses"""

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    # we always want to report on when the report was made: "now"
    right_now = get_now(to_str=False)

    if request.method == 'GET':
        if str_date == 'now':
            # this means to use right now as the timestamp
            year_str = right_now.strftime('%Y')
        else:
            year_str = str_date

        initial_data = {'year': year_str}
        form = YearForm(initial=initial_data, data=initial_data)

    else:
        form = YearForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'monthly_report.html'
        return render(request, template_name, context)

    # the rest of this code executes on a valid form submission (or initialization)
    cleaned_data = form.cleaned_data
    year_str = cleaned_data['year']

    # dict -> k:{str} - month number (zero padded)
    #         v:{list] - 2 value list [costs , earnings] either could be zero, hence the default values of 0.0
    value_dict = defaultdict(lambda: [0.0, 0.0])

    # get the date and cost values from the cost table for the month in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_cost = list(Cost.objects.filter(date__startswith=year_str, status=1).values('date', 'cost'))
    rows_from_cost = list(Cost.objects.filter(date__startswith=year_str).values('date', 'cost'))

    # start building the value_dict for these values
    for row in rows_from_cost:
        date_val = row['date']
        cost_val = row['cost']

        month_num = date_val.strftime('%m')

        # we don't yet have any earnings for this date so don't touch the default value of 0.0
        value_dict[month_num][0] += cost_val

    # get the costs (price) from the fishbuy table for the month in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=year_str, status=1).values('date', 'price'))
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=year_str).values('date', 'price'))

    # if any value is for an existing month add the value from the fisthbuy table
    for row in rows_from_fishbuy:
        date_val = row['date']
        price_val = row['price']

        month_num = date_val.strftime('%m')
        value_dict[month_num][0] += price_val

    # now get the earnings values from the earning table
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_earning = list(Earning.objects.filter(date__startswith=year_str, status=1).values('date', 'price'))
    rows_from_earning = list(Earning.objects.filter(date__startswith=year_str).values('date', 'price'))

    # now update the earning values in the value_dict for any date found
    for row in rows_from_earning:
        date_val = row['date']
        price_val = row['price']

        month_num = date_val.strftime('%m')
        value_dict[month_num][1] += price_val

    # get the totals for both cost and earning
    total_costs = f"{sum([v[0] for v in value_dict.values()]):,.2f}"
    total_earnings = f"{sum([v[1] for v in value_dict.values()]):,.2f}"

    # CL: ++
    # convert all the values to a displayable format and add the month name to the value list
    # dict -> k:{str} - YYYY-MM (2025-04) str_date format for the monthly URL
    #         v:{list} - [{str}-month name, {str}-cost value, {str}-earning value]
    report_value_dict = dict()
    if len(value_dict) > 0:

        # report on all months in this year
        for month_num in MONTH_NAMES:
            cost_val = f"{value_dict[month_num][0]:,.2f}"
            earning_val = f"{value_dict[month_num][1]:,.2f}"
            url_key = f"{year_str}-{month_num}"
            month_name = MONTH_NAMES[month_num]
            report_value_dict[url_key] = [month_name, cost_val, earning_val]

    context['form'] = form
    context['value_dict'] = report_value_dict
    context['year'] = int(year_str)
    context['right_now'] = get_now(to_str=True)
    now_yr = right_now.strftime('%Y')
    context['year_select'] = [y for y in range(int(now_yr) - 6, int(now_yr) + 1)]  # last 6 years
    context['total_costs'] = total_costs
    context['total_earnings'] = total_earnings

    template_name = 'annual_report.html'
    return render(request, template_name, context)


def fish_count_details(request):
    """
    Generate the fish details report based on data in the fishbuy table, group by region and sort by date.
    """

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    # get details from the fishbuy table
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_fishbuy = list(Fishbuy.objects.filter(status=1).order_by('date'))
    rows_from_fishbuy = list(Fishbuy.objects.all().order_by('date'))

    # accumulate values for each area
    # Note: all of the records in rows_from_fishbuy have already been sorted by date by ORM, by the order_by() clause
    # dict -> k:{str} - "fishto" value (Area or interest)
    #         v:{list} - list of Fishbuy Model Objects with values from the database
    value_dict = defaultdict(list)
    for row in rows_from_fishbuy:
        area = row.fishto
        row.date = row.date.strftime(DISPLAY_FMT)
        value_dict[area].append(row)

    value_d = dict()
    for k, v in value_dict.items():
        value_d[k] = v

    context = dict()
    context['right_now'] = get_now(to_str=True)
    context['value_dict'] = value_d
    template_name = 'fish_details.html'
    return render(request, template_name, context)


def financial_accounting(request, str_date):
    """
    Generate the financial accounting report.
    """

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    right_now = get_now(to_str=False)

    if request.method == 'GET':
        if str_date == 'now':
            # this means to use dates from the "beginning of this fiscal year" to now. The
            # "beginning of a fiscal year" is April 1st so we need to determine if it's past April 1, if it is
            # then the fiscal year was this year, if right_now is before April 1 then we need to recognize that
            # the fiscal year started last calendar year.
            mon_num = right_now.month
            if mon_num > 3:
                yr_num = right_now.year
            else:
                yr_num = right_now.year - 1  # use last year

            fr_date_str = f"{yr_num}-04-01"
            to_date_str = right_now.strftime('%Y-%m-%d')
        else:
            fr_date_str, to_date_str = str_date.split('_')

        initial_data = {'fr_date': fr_date_str, 'to_date': to_date_str}
        form = ToFromDateSelectorForm(initial=initial_data, data=initial_data)

    else:
        form = ToFromDateSelectorForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'finacc_report.html'
        return render(request, template_name, context)

    # from here we know we have a valid form (date)
    cleaned_data = form.cleaned_data

    # CL: ++
    print(f"fr_date: {cleaned_data['fr_date']}")
    print(f"to_date: {cleaned_data['to_date']}")
    # CL: --

    context['form'] = form
    context['right_now'] = get_now(to_str=True)
    template_name = 'finacc_report.html'
    return render(request, template_name, context)


def display_fish_chart(request):

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    right_now = get_now(to_str=False)

    if request.method == 'GET':
        # when we're called as a GET request we just set the fr_date to the first day of the current year
        # and the to_date to today
        fr_date_str = right_now.strftime('%Y-01-01')  # use the first day of THIS year
        to_date_str = right_now.strftime('%Y-%m-%d')

        initial_data = {'fr_date': fr_date_str, 'to_date': to_date_str}
        form = ToFromDateSelectorForm(initial=initial_data, data=initial_data)
    else:
        form = ToFromDateSelectorForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'fish_chart.html'
        return render(request, template_name, context)

    # from here we know we have a valid form (date)
    cleaned_data = form.cleaned_data

    fr_date = cleaned_data['fr_date']
    to_date = cleaned_data['to_date']

    context['form'] = form
    context['fr_date_str'] = fr_date.strftime(DISPLAY_FMT)
    context['to_date_str'] = to_date.strftime(DISPLAY_FMT)
    context['db_date'] = f"{fr_date.strftime(DB_FMT)}_{to_date.strftime(DB_FMT)}"
    context['right_now'] = get_now(to_str=True)
    template_name = 'fish_chart.html'
    return render(request, template_name, context)


def generate_fish_chart(request, str_date):
    """Generates the Fish Count plot and returns an image (using content_type='image/png')"""
    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    fr_date_str, to_date_str = str_date.split('_')

    # first we get the data to plot (all the data comes from the fishbuy table)
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__range=(fr_date_str, to_date_str)).values('fishquantity', 'fishto'))

    # dict -> k:{str} - source (fishto value)
    #         v:{int} - accumulation of fishquantitiy values
    value_dict = dict()
    for row in rows_from_fishbuy:
        source = row['fishto']
        count = row['fishquantity']
        curr_val = value_dict.get(source, 0) + count
        value_dict[source] = curr_val

    # build the lists for plotting
    quantities = []
    sources = []
    for src, qty in value_dict.items():
        quantities.append(qty)
        sources.append(src)

    # generate the plot in-memory
    fig, ax = plt.subplots()
    ax.bar(sources, quantities, color='#D2E9EA')
    ax.set_xlabel('Sources')
    ax.set_ylabel('Quantity')
    ax.grid(axis='y')

    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)

    plt.close(fig)  # free up memory
    return HttpResponse(buffer.getvalue(), content_type='image/png')
