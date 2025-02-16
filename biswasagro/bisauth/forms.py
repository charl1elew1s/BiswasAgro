from django import forms
from django.forms import ModelForm
from .models import TblUsers, TblRoles


class TblUsersForm(ModelForm):
    class Meta:
        model = TblUsers
        fields = ['name', 'username', 'email', 'password', 'mobile', 'roleid', 'isActive',
                  'created_at', 'updated_at',]


class TblRolesForm(ModelForm):
    class Meta:
        model = TblRoles
        fields = ['role']

