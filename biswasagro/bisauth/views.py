from .models import TblRoles, TblUsers
from .forms import TblRolesForm, TblUsersForm
from common.utils import delete_tabel_row, show_table, add_update_table

LOGS_FMT = '%Y-%m-%d %H:%M:%S'


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
    return add_update_table(request, 'bisauth', 'tblusers',
                            TblUsers, TblUsersForm, row_id, set())
