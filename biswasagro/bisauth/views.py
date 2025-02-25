from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timezone
from .models import TblRoles, TblUsers
from .forms import TblRolesForm, TblUsersForm, RegistrationForm, LoginForm
from common.utils import delete_tabel_row, show_table, add_update_table, LOGS_FMT, get_user_roles
from bisauth.models import TblUsers, TblRoles

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

            tbl_user = TblUsers.objects.filter(username=cleaned_data.get('username'))
            user = None
            if tbl_user.exists():
                user = tbl_user[0]
                # add the user to the session and render the home page
                # we need to know what the user's role is
                roleid_2_name = get_user_roles()
                role_name = roleid_2_name[user.roleid]
                request.session['user'] = {'id': user.id,
                                           'username': user.username,
                                           'role': role_name}
                return render(request, 'home.html', {})

        else:  # form is invalid for ANY reason
            context['form'] = form  # re-render form with errors
            return render(request, 'login.html', context)

    context['form'] = form
    return render(request, 'login.html', context)


def logout(request):
    if 'user' in request.session:
        del request.session['user']
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

            roleid_2_name = get_user_roles()
            # we will default to giving a new user the lowest level of access to the system, this value
            # could be changed by an Admin or Manager later
            # we loop over the ROLE_LEVELS until we find one that is defined in the database, if none was found
            # this means the database values were changed or removed, so we give an ID with the highest value, but
            # we set the is_active flag to 0 meaning the user is inactive and can not access the site until the
            # role is fixed by an Admin
            init_id = -1  # this is an impossible role_id
            for role_name in ROLE_LEVELS:
                if init_id > 0:
                    break
                for r_id, r_name in roleid_2_name.items():
                    if role_name == r_name:
                        # we found a match
                        init_id = r_id
                        user.roleid = init_id
                        user.is_active = 1  # default to making the new user active
                        break
            if init_id == -1:
                # this is an exceptional case and should never happen if the database is set up correctly
                # in this case (we didn't find any roles which were listed in the ROLE_LEVELS list) we
                # assign an id of the highest value found in the database and make the user inactive
                sorted_roles = sorted(roleid_2_name.items(), key=lambda item: item[0], reverse=True)
                user.roleid = sorted_roles[0][0]
                user.is_active = 0  # make this user inactive

            user.created_at = datetime.now(tz=timezone.utc)
            user.updated_at = datetime.now(tz=timezone.utc)
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
# Tblroles Table
#
def show_tblroles_table(request):
    return show_table(request, 'bisauth', 'tblroles', TblRoles)


def tblroles_delete_row(request, row_id):
    return delete_tabel_row(TblRoles, row_id)


def add_update_tblroles(request, row_id):
    return add_update_table(request, 'bisauth', 'tblroles',
                            TblRoles, TblRolesForm, row_id, set())


#
# Tblusers Table
#
def show_tblusers_table(request):
    return show_table(request, 'bisauth', 'tblusers', TblUsers)


def tblusers_delete_row(request, row_id):
    return delete_tabel_row(TblUsers, row_id)


def add_update_tblusers(request, row_id):
    skip_set = {'password', 'created_at', 'updated_at'}
    return add_update_table(request, 'bisauth', 'tblusers',
                            TblUsers, TblUsersForm, row_id, skip_set)
