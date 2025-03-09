from django.contrib import admin
from .models import Roles, Usersinfo, Staff, Staffs, Salary

# Register your models here.
admin.site.register([Roles, Usersinfo, Staff, Staffs, Salary])
