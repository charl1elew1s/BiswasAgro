from django.contrib import admin
from .models import Fishbuy, Fishtype, Items, Units, Land, Sectors, TblProduct

# Register your models here.
admin.site.register([Fishbuy, Fishtype, Items, Units, Land, Sectors, TblProduct])
