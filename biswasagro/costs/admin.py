from django.contrib import admin
from .models import Cost, Costitems, Costpurpose, Earning, Investment, Loandetails, LoanProvidersInfo, LoanTransactions

# Register your models here.
admin.site.register([Cost, Costitems, Costpurpose, Earning, Investment, Loandetails,
                     LoanProvidersInfo, LoanTransactions])
