import re
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from costs.models import Cost, Earning
from bisauth.models import Salary
from inventory.models import Fishbuy, Mousa, Land
from .forms import DateSelectorForm, YearMonthForm, YearForm, ToFromDateSelectorForm
from common.utils import get_dates_in_month, get_now
from common.column_mappers import *

# add font for Bengali characters
plt.rcParams['font.family'] = ['DejaVu Sans', 'Noto Serif Bengali']

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

# Human-readable format for Dates
DISPLAY_FMT = '%d-%m-%Y'

# Database (ISO 8601) format required for lookups on the database
DB_FMT = '%Y-%m-%d'

PLOT_BAR_COLOR = '#b0a787'
PLOT_BODY_COLOR = '#d9d9d9'


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

    year_str = form_date.strftime('%Y')
    month_numb_str = form_date.strftime('%m')
    day_str = form_date.strftime('%d')

    if not month_word:
        month_word = form_date.strftime('%B')

    if not day_word:
        day_word = form_date.strftime('%a')

    date_query_str = f"{year_str}-{month_numb_str}-{day_str}"

    #
    # Debits (from cost, fishbuy, mousa, and salary tables)
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

    # get the data from the salary table
    rows_from_salary = list(Salary.objects.filter(date=date_query_str))
    context['rows_from_salary'] = rows_from_salary
    context['num_rows_from_salary'] = len(rows_from_salary)
    context['num_rows_from_salary_plus_1'] = len(rows_from_salary) + 1

    salary_total = 0.0
    for row in rows_from_salary:
        # reformat the total values by converting them to strings with commas (for display in the template)
        salary_total += row.total
        row.total = f"{row.total:,.2f}"  # we convert to a string just for display
    context['salary_total'] = f"{salary_total:,.2f}"

    # get the data from the mousa table
    rows_from_mousa = list(Mousa.objects.filter(date=date_query_str))
    context['rows_from_mousa'] = rows_from_mousa
    context['num_rows_from_mousa'] = len(rows_from_mousa)
    context['num_rows_from_mousa_plus_1'] = len(rows_from_mousa) + 1

    mousa_total = 0.0
    for row  in rows_from_mousa:
        # reformat the amount values by converting them to strings with commas (for display in the template)
        mousa_total += row.amount
        row.amount = f"{row.amount:,.2f}"
    context['mousa_total'] = mousa_total

    costs_grand_total = cost_total + fishbuy_total + salary_total + mousa_total
    context['costs_grand_total'] = f"{costs_grand_total:,.2f}"

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

    # get values from the salary table (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_salary = Salary.objects.filter(date__startswith=date_query_str, status=1).values('date', 'total')
    rows_from_salary = list(Salary.objects.filter(date__startswith=date_query_str).values('date', 'total'))

    # add values from salary table
    for row in rows_from_salary:
        date_val = row['date']
        total_val = row['total']

        value_dict[date_val][0] += total_val

    # include values from the mousa table (if any)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_mousa = list(Mousa.objects.filter(date__startswith=date_query_str, status=1).values('date', 'amount'))
    rows_from_mousa = list(Mousa.objects.filter(date__startswith=date_query_str).values('date', 'amount'))

    # if any value is for an existing year, add the value from the mousa table
    for row in rows_from_mousa:
        date_val = row['date']
        amount_val = row['amount']

        value_dict[date_val][0] += amount_val

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

    # get the date and cost values from the cost table for the year in question (there may be none)
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

    # get the costs (price) from the fishbuy table for the year in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=year_str, status=1).values('date', 'price'))
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__startswith=year_str).values('date', 'price'))

    # if any value is for an existing year, add the value from the fisthbuy table
    for row in rows_from_fishbuy:
        date_val = row['date']
        price_val = row['price']

        month_num = date_val.strftime('%m')
        value_dict[month_num][0] += price_val

    # get the salaries from the salary table for the year in question (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_salary = Salary.objects.filter(date__startswith=year_str, status=1).values('date', 'total')
    rows_from_salary = list(Salary.objects.filter(date__startswith=year_str).values('date', 'total'))

    # if any value is for an existing year, add the value from the salary table
    for row in rows_from_salary:
        date_val = row['date']
        total_val = row['total']

        month_num = date_val.strftime('%m')
        value_dict[month_num][0] += total_val

    # get the amounts from the mousa table (there may be none)
    # CL: use the first query if we need to filter out and only include 'Paid' status values
    # rows_from_mousa = list(Mousa.objects.filter(date__startswith=year_str, status=1).values('date', 'amount'))
    rows_from_mousa = list(Mousa.objects.filter(date__startswith=year_str).values('date', 'amount'))

    # if any value is for an existing year, add the value from the mousa table
    for row in rows_from_mousa:
        date_val = row['date']
        amount_val = row['amount']

        month_num = date_val.strftime('%m')
        value_dict[month_num][0] += amount_val

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
    # dict -> k:{str} - "fishto" value (Area of interest)
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


def financial_accounting(request):
    """
    Generate the financial accounting report.
    """

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()
    right_now = get_now(to_str=False)

    # For "previous" and "current" reporting (the top of the report) we need to know what is "current" and was
    # "previous" and that depends on the beginning of the current fiscal year. Because fiscal years start on April
    # 1st we first need to know if it's before or after April 1 so that we can determine which fiscal year we are
    # presently in.
    #
    # This is regardless of the "Date From" and "Date To" values coming from the search boxes,
    # those dates are used for the bottom table of the report
    mon_num = right_now.month

    # We will need to calculate the previous_(start/end) and current_(start/end) based on where "right_now" falls
    # with respect to fiscal years.
    previous_start_dt = None
    previous_end_dt = None
    current_start_dt = None
    current_end_dt = None
    if mon_num > 3:
        # the start of the current fiscal year was April 1 THIS year
        current_start_dt = datetime.strptime(f'{right_now.year}-04-01', DB_FMT)
    else:
        # the start of the current fiscal year was last April 1
        last_year = right_now.year - 1
        current_start_dt = datetime.strptime(f'{last_year}-04-01', DB_FMT)

    # the previous_(start/end) and the current_end are relative to the current_start
    current_end_dt = current_start_dt + relativedelta(years=1) - relativedelta(days=1)
    previous_start_dt = current_start_dt - relativedelta(years=1)
    previous_end_dt = previous_start_dt + relativedelta(years=1) - relativedelta(days=1)

    previous_credits, previous_debits = get_yearly_total(previous_start_dt, previous_end_dt)
    current_credits, current_debits = get_yearly_total(current_start_dt, current_end_dt)
    context['previous_start_str'] = previous_start_dt.strftime(DISPLAY_FMT)
    context['previous_end_str'] = previous_end_dt.strftime(DISPLAY_FMT)
    context['previous_credits'] = f"{previous_credits:,.2f}"
    context['previous_debits'] = f"{previous_debits:,.2f}"

    context['current_start_str'] = current_start_dt.strftime(DISPLAY_FMT)
    context['current_end_str'] = current_end_dt.strftime(DISPLAY_FMT)
    context['current_credits'] = f"{current_credits:,.2f}"
    context['current_debits'] = f"{current_debits:,.2f}"

    final_balance = current_credits - current_debits
    context['final_balance'] = f"{final_balance:,.2f}"

    if request.method == 'GET':
        # This means we landed here off the reports landing page and no date range was selected
        # we will start off using the monthly totals, so we'll arbitrarily choose the start time to be the
        # beginning of this month and the end time to be today, the user can change this time span using
        # the From Date, To Date form at the top of the page
        fr_date_str = f"{right_now.year}-{right_now.month:02d}-01"
        to_date_str = f"{right_now.year}-{right_now.month:02d}-{right_now.day:02d}"

        initial_data = {'fr_date': fr_date_str, 'to_date': to_date_str}
        form = ToFromDateSelectorForm(initial=initial_data, data=initial_data)

    else:
        form = ToFromDateSelectorForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        template_name = 'finacc_report.html'
        return render(request, template_name, context)

    # from here we know we have a valid form
    cleaned_data = form.cleaned_data
    start_dt = cleaned_data['fr_date']
    end_dt = cleaned_data['to_date']

    # Get the values for the date span table (at the bottom of the page)
    # as we're accumulating data for each day we will only update the debit and credit for that day and then
    # after all dates in the span were visited we will order the data by date and calculate the total_debit and
    # total_credit entries in the list because they are an accumulation from the beginning of the time span.
    # dict -> k:{date} - datetime.date value from the database `date`
    #         v:{list} - [debit, credit, total_debit, total_credit]
    span_data = dict()

    # get contributions from the cost table
    rows_from_cost = list(Cost.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                          .values('date', 'cost'))

    for row in rows_from_cost:
        date_val = row['date']
        debit_val = row['cost']
        value_list = span_data.get(date_val, [0.0, 0.0, 0.0, 0.0])
        value_list[0] += debit_val
        span_data[date_val] = value_list

    # add contributions from the fishbuy table
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                             .values('date', 'price'))

    for row in rows_from_fishbuy:
        date_val = row['date']
        debit_val = row['price']
        value_list = span_data.get(date_val, [0.0, 0.0, 0.0, 0.0])
        value_list[0] += debit_val
        span_data[date_val] = value_list

    # add contributions from the salary table
    rows_from_salary = list(Salary.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                            .values('date', 'total'))

    for row in rows_from_salary:
        date_val = row['date']
        debit_val = row['total']
        value_list = span_data.get(date_val, [0.0, 0.0, 0.0, 0.0])
        value_list[0] += debit_val
        span_data[date_val] = value_list

    # add contributions from the mousa table
    rows_from_mousa = list(Mousa.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                           .values('date', 'amount'))

    for row in rows_from_mousa:
        date_val = row['date']
        debit_val = row['amount']
        value_list = span_data.get(date_val, [0.0, 0.0, 0.0, 0.0])
        value_list[0] += debit_val
        span_data[date_val] = value_list

    # add the credits from the earning table
    rows_from_earning = list(Earning.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                             .values('date', 'price'))

    for row in rows_from_earning:
        date_val = row['date']
        credit_val = row['price']
        value_list = span_data.get(date_val, [0.0, 0.0, 0.0, 0.0])
        value_list[1] += credit_val
        span_data[date_val] = value_list

    dates_in_order = sorted(span_data.keys())
    # list -> [(date_str, debit_str, credit_str, total_debit_str, total_credit_str),...]
    #   these values are strings because they are in displayable format with commas separating the thousands place
    summary_data = []
    for n in range(len(dates_in_order)):
        date_key = dates_in_order[n]
        date_str = date_key.strftime(DISPLAY_FMT)
        span_data_entry = span_data[date_key]
        debit_val = span_data_entry[0]
        debit_str = f"{debit_val:,.2f}"
        credit_val = span_data_entry[1]
        credit_str = f"{credit_val:,.2f}"
        if n == 0:
            total_debit_str = debit_str
            total_credit_str = credit_str
        else:
            total_debit_val = float(summary_data[n-1][3].replace(',', '')) + debit_val
            total_debit_str = f"{total_debit_val:,.2f}"
            total_credit_val = float(summary_data[n-1][4].replace(',', '')) + credit_val
            total_credit_str = f"{total_credit_val:,.2f}"

        summary_data.append((date_str, debit_str, credit_str, total_debit_str, total_credit_str))

    context['form'] = form
    context['summary_data'] = summary_data
    context['right_now'] = get_now(to_str=True)
    context['fr_date'] = cleaned_data['fr_date'].strftime(DISPLAY_FMT)
    context['to_date'] = cleaned_data['to_date'].strftime(DISPLAY_FMT)
    template_name = 'finacc_report.html'
    return render(request, template_name, context)


def get_yearly_total(start_dt, end_dt):
    """Return a tuple: (yearly_credits, yearly_debits)"""

    # debits come from cost::cost, fishbuy::price, salary::total, and mousa::amount
    # credits come from earnings::price

    total_debits = 0.0

    # add contributions from the cost table
    rows_from_cost = list(Cost.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                          .values('cost'))
    total_debits += sum([r['cost'] for r in rows_from_cost])

    # add contributions from the fishbuy table
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                             .values('price'))
    total_debits += sum([r['price'] for r in rows_from_fishbuy])

    # add contributions from the salary table
    rows_from_salary = list(Salary.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                            .values('total'))
    total_debits += sum([r['total'] for r in rows_from_salary])

    # add contributions from the mousa table
    rows_from_mousa = list(Mousa.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                           .values('amount'))
    total_debits += sum([r['amount'] for r in rows_from_mousa])

    # add the credits from the earning table
    total_credits = 0.0
    rows_from_earning = list(Earning.objects.filter(date__range=(start_dt.strftime(DB_FMT), end_dt.strftime(DB_FMT)))
                             .values('price'))
    total_credits += sum([r['price'] for r in rows_from_earning])

    return total_credits, total_debits


def land_report(request, source):
    """Generate the Land summary report for the given enclosure (source)"""

    if 'user' not in request.session:
        # no reports allowed if you're not logged in!
        return redirect('bisauth:login')

    context = dict()

    # we'll use our source mapper for the gher field of the land table, in this case we're doing a reverse lookup
    # we have the source, but we want the index (for the query on the database)
    source_idx = -1  # impossible value
    source_mapper = get_mapping(request, SOURCE_MAPPING)
    for id, source_val in source_mapper.items():
        if source_val == source:
            source_idx = id
            # we found what we were looking for, no need to keep looking
            break

    rows_from_land = list(Land.objects.filter(gher=source_idx))
    context['num_of_rows_from_land'] = len(rows_from_land)

    # list of dictionaries of data to display in the template
    #  they have this structure:
    # {
    #   'id': {int}
    #   'enclosure': {str} - this is the source passed to this function
    #   'mousa': {str} mousa field value
    #   'stain': {str} dag field value
    #   'ledger': {str} khotian field value
    #   'quantity': {float} amount field value
    #   'flat': {float} plan_lan field value
    #   'cannal': {float} par_cannel field value
    #   'take': {str} calculated value (based on currency exchange rate) converted to string for formatting
    #   'owners': {str} owners field value
    #   'comment': {str} comment field value
    # }
    #
    display_values = []
    total_take = 0.0
    for row in rows_from_land:
        td = dict()
        td['id'] = row.id
        td['enclosure'] = source
        td['mousa'] = row.mousa
        td['stain'] = row.dag
        td['ledger'] = row.khotian
        td['quantity'] = row.amount
        td['flat'] = row.plane_land
        td['cannal'] = row.par_cannel
        take_value = row.amount * (14_000.0/42.0)
        td['take'] = f"{take_value:,.2f}"
        td['owners'] = row.owners
        td['comment'] = row.comment
        total_take += take_value
        display_values.append(td)

    context['source'] = source
    context['right_now'] = get_now(to_str=True)
    context['display_values'] = display_values
    context['total_take'] = f"{total_take:,.2f}"
    template_name = 'land_report.html'
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
    rows_from_fishbuy = list(Fishbuy.objects.filter(date__range=(fr_date_str, to_date_str))
                             .values('fishquantity', 'fishto'))

    # dict -> k:{str} - source (fishto value)
    #         v:{int} - accumulation of fishquantitiy values
    value_dict = dict()
    for row in rows_from_fishbuy:
        source = row['fishto']
        count = row['fishquantity']
        value_dict[source] = value_dict.get(source, 0) + count

    # build the lists for plotting
    sources = []
    quantities = []
    for src, qty in value_dict.items():
        sources.append(src)
        quantities.append(qty)

    # generate the plot in-memory
    fig, ax = plt.subplots()

    # set colors
    fig.patch.set_facecolor(PLOT_BODY_COLOR)
    ax.set_facecolor(PLOT_BODY_COLOR)

    ax.bar(sources, quantities, color=PLOT_BAR_COLOR)
    ax.set_xlabel('Sources')
    ax.set_ylabel('Quantity')
    ax.grid(axis='y')

    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)

    plt.close(fig)  # free up memory
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def display_earnings(request):
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
        template_name = 'earning_charts.html'
        return render(request, template_name, context)

    # from here we know we have a valid form
    cleaned_data = form.cleaned_data

    fr_date = cleaned_data['fr_date']
    to_date = cleaned_data['to_date']

    rows_from_earning = list(Earning.objects.filter(date__range=(fr_date.strftime(DB_FMT), to_date.strftime(DB_FMT))))

    # Build the data structure that has all the data for all plots.
    # dict -> k:{int} - id for source (pk of sources table)
    #         v:{dict} - k:{int} - id for item (pk of the items table)
    #                    v:{int} - accumulated price amount for this source and item
    #
    earning_data = dict()
    for row in rows_from_earning:
        source_id = row.source
        source_dict = earning_data.get(source_id, dict())
        item_id = row.item
        price_val = source_dict.get(item_id, 0) + row.price
        source_dict[item_id] = price_val
        earning_data[source_id] = source_dict

    # we've accumulated all the data for all plots, we'll delegate the job of generating the plots and putting
    # that data into the session to another function.
    save_earning_plts_in_session(request, earning_data)

    # set flags in the context so that we know if each source has data or not for the given timespan
    # dict -> k:{str} source name
    #         v:{bool} - True if there is data for this source for this timespan False otherwise
    # initialise all sources with False, and then we'll see which have data and which do not
    source_mapping = get_mapping(request, SOURCE_MAPPING)
    has_data_dict = {src: False for src in source_mapping.values()}

    # check the earning_data for data for each source
    for source_id, source_name in source_mapping.items():
        if source_id in earning_data:
            has_data_dict[source_name] = True

    context['form'] = form
    context['has_data_dict'] = has_data_dict
    context['fr_date_str'] = fr_date.strftime(DISPLAY_FMT)
    context['to_date_str'] = to_date.strftime(DISPLAY_FMT)
    context['right_now'] = get_now(to_str=True)

    template_name = 'earning_charts.html'
    return render(request, template_name, context)


def gen_earn_plt(request, plt_source):
    plt_data = request.session.get('plt_data', {})
    plot_bytes_base64 = plt_data.get(plt_source, None)
    if plot_bytes_base64:
        # decode the base64 string back into bytes, this is really a png format datastream.
        plot_bytes = base64.b64decode(plot_bytes_base64)
        return HttpResponse(plot_bytes, content_type='image_png')
    else:
        return HttpResponse('Plot data not found', status=404)


def save_earning_plts_in_session(request, earning_data):
    """
    For each source including in the earning_data generate a plot and put the plot data in the session under a
    key that specifies the source name
    """
    source_mapping = get_mapping(request, SOURCE_MAPPING)
    items_mapping = get_mapping(request, ITEMS_MAPPING)

    # dict -> k:{str} - source name: North, South, ...
    #         v:{data} - the png bytes (base64 encoded) of the generated plot. We must use: content_type='image/png'
    plt_data = dict()
    for source_id, src_data in earning_data.items():
        source_name = source_mapping[source_id]  # use this name as the key into the session data
        items = []
        prices = []
        for item_id, price in src_data.items():
            item_val = items_mapping.get(item_id, None)  # bad data check
            if item_val:
                items.append(item_val)
                prices.append(price)

        # generate the plot in-memory
        fig, ax = plt.subplots()

        # set colors
        fig.patch.set_facecolor(PLOT_BODY_COLOR)
        ax.set_facecolor(PLOT_BODY_COLOR)
        ax.bar(items, prices, color=PLOT_BAR_COLOR)

        ax.set_title(source_name)
        ax.set_xlabel('Items', labelpad=10)
        ax.set_ylabel('Price')
        ax.grid(axis='y')
        ax.xaxis.set_tick_params(labelrotation=45, labelsize=10, pad=10)
        plt.tight_layout()

        buffer = io.BytesIO()
        canvas = FigureCanvas(fig)

        # have matplotlib render the figure into a png file and store it in the buffer object
        # (in-memory instead of writing to the filesystem into a file)
        canvas.print_png(buffer)

        plt.close(fig)  # free up memory

        # Put the bytes of the plot into the plt_data dict that we'll store in the session for later retrieval.
        # We have to encode the bytes into a base64 string so that it can be serialized properly when
        # storing it in the session.
        # Note: we must ensure that we decode this string when we pull it out of the session.
        plt_data[source_name] = base64.b64encode(buffer.getvalue()).decode('utf-8')

    request.session['plt_data'] = plt_data
