from django.contrib import admin
from .models import (Dailyworks, Fishbuy, Fishtype, Fooddistribution, Items, Units, Land, Mousa, Mousaname, Sectors,
                     Sources, Term)


# Register your models here.
admin.site.register([Dailyworks, Fishbuy, Fishtype, Fooddistribution, Items, Units, Land, Mousa, Mousaname, Sectors,
                     Sources, Term])
