from django.contrib import admin
from .models import Cost, Costitems, Costpurpose, Earning, Investment

# Register your models here.
admin.site.register([Cost, Costitems, Costpurpose, Earning, Investment])
