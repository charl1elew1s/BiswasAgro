from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from common.utils import *
from common.column_mappers import *

# define the order of the User Roles from the least access to most, we use this when creating a new
# user. The preferred role level is the one that has the least amount of access.
ROLE_LEVELS = ['User', 'Operator', 'Manager', 'Admin']


#
# Login
#
def login(request):

    if 'user' in request.session:
        # this means there is a user logged in
        # render the home page
        return render(request, 'home.html', {})

    context = dict()
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            userinfo = Usersinfo.objects.filter(username=cleaned_data.get('username'))
            user = None
            if userinfo.exists():
                user = userinfo[0]
                # add the user to the session and render the home page
                # we need to know what the user's role is
                request.session['user'] = {'id': user.id,
                                           'username': user.username,
                                           'role': user.role}
                return render(request, 'home.html', {})

        else:  # form is invalid for ANY reason
            context['form'] = form  # re-render form with errors
            return render(request, 'login.html', context)

    context['form'] = form
    return render(request, 'login.html', context)


def logout(request):
    if 'user' in request.session:
        del request.session['user']
        remove_all_mappings(request)
    return redirect('home')


#
# Register a new user
#
def register(request):

    if request.method == 'GET':
        form = RegistrationForm()
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            hashed_password = make_password(password)
            user.password = hashed_password
            user.mobile = cleaned_data.get('mobile')

            db_known_roles = get_mapping(request, ROLE_MAPPING).values()
            # we will default to giving a new user the lowest level of access to the system, this value
            # could be changed by an Admin or Manager later
            # we loop over the ROLE_LEVELS until we find one that is defined in the database, if none was found
            # this means the database values were changed or removed, so we give an ID with the highest value, but
            # we set the is_active flag to 0 meaning the user is inactive and can not access the site until the
            # role is fixed by an Admin
            this_users_role = 'Unknown'
            for role_name in ROLE_LEVELS:
                if this_users_role != 'Unknown':
                    break
                for r_name in db_known_roles:
                    if role_name == r_name:
                        # we found a match
                        user.role = role_name
                        user.isactive = 1  # default to making the new user active
                        this_users_role = role_name
                        break
            if this_users_role == 'Unknown':
                # this is an exceptional case and should never happen if the database is set up correctly
                # in this case (we didn't find any roles which were listed in the ROLE_LEVELS list) we
                # assign a Role of "Unknown" and we set the isActive flag to inactive so that the user can not
                # log in until an Admin fixes this situation (by changing the role to an valid value).
                user.role = this_users_role
                user.isactive = 0  # make this user inactive

            user.save()

            # see if we were able to create the user, if so we'll redirect to the login page if not
            # we render the registration form again
            if user:
                # present the login form and indicate that the account was created
                context = dict()
                form = LoginForm()
                context['new_user'] = username
                context['form'] = form
                return render(request, 'login.html', context)

    context = dict()
    context['form'] = form
    return render(request, 'register.html', context)


#
# roles Table
#
def show_roles_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'bisauth', 'roles', Roles)


def roles_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Roles, row_id)


def add_update_roles(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    context = dict()
    return add_update_table(request, 'bisauth', 'roles',
                            Roles, RolesForm, row_id, set(), context)


#
# usersinfo Table
#
def show_usersinfo_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'bisauth', 'usersinfo', Usersinfo, show_usersinfo_mapper)


def usersinfo_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Usersinfo, row_id)


def add_update_usersinfo(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    skip_set = {'password', 'created_at', 'updated_at'}
    context = dict()
    context['is_active'] = IS_ACTIVE  # a dict
    context['roles'] = get_mapping(request, ROLE_MAPPING)  # a dict

    return add_update_table(request, 'bisauth', 'usersinfo',
                            Usersinfo, UsersInfoForm, row_id, skip_set, context)


#
# salary table
#
def show_salary_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'bisauth', 'salary', Salary, show_salary_mapper)


def salary_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Salary, row_id)


def add_update_salary(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    skip_set = {'logs'}
    context = dict()

    status_map = get_mapping(request, STATUS_MAPPING)
    context['status'] = status_map

    # we'll use the hardcoded values for the 'purpose' field
    context['purposes'] = SALARY_PURPOSE

    return add_update_table(request, 'bisauth', 'salary',
                            Salary, SalaryForm, row_id, skip_set, context, addup_salary_mapper)


#
# staff table
#
def show_staff_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'bisauth', 'staff', Staff)


def staff_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Staff, row_id)


def add_update_staff(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    skip_set = {'staffno', 'log'}
    context = dict()
    return add_update_table(request, 'bisauth', 'staff',
                            Staff, StaffForm, row_id, skip_set, context)


#
# staffs table
#
def show_staffs_table(request):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return show_table(request, 'bisauth', 'staffs', Staffs)


def staffs_delete_row(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    return delete_tabel_row(request, Staffs, row_id)


def add_update_staffs(request, row_id):
    is_in = 'user' in request.session
    if not is_in:
        return redirect('bisauth:login')

    skip_set = set()
    context = dict()
    return add_update_table(request, 'bisauth', 'staffs',
                            Staffs, StaffsForm, row_id, skip_set, context)
