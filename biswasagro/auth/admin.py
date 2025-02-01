from django.contrib import admin
from .models import TblRoles, TblUsers

# Register your models here.
admin.site.register([TblRoles, TblUsers])
