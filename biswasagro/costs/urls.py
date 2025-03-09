from django.urls import path
from . import views

app_name = 'costs'

urlpatterns = [
    # handle the `cost` table
    path('cost', views.show_cost_table, name='show_cost_table'),
    path('cost/delete/<int:row_id>', views.cost_delete_row, name='cost_delete_row'),
    path('addup_cost/<int:row_id>', views.add_update_cost, name="addup_cost"),

    # handle the `costitems` table
    path('costitems', views.show_costitems_table, name='show_costitems_table'),
    path('costitems/delete/<int:row_id>', views.costitems_delete_row, name='costitems_delete_row'),
    path('addup_costitems/<int:row_id>', views.add_update_costitems, name="addup_costitems"),

    # handle the `costpurpose` table
    path('costpurpose', views.show_costpurpose_table, name='show_costpurpose_table'),
    path('costpurpose/delete/<int:row_id>', views.costpurpose_delete_row, name='costpurpose_delete_row'),
    path('addup_costpurpose/<int:row_id>', views.add_update_costpurpose, name="addup_costpurpose"),

    # handle the `earning` table
    path('earning', views.show_earning_table, name='show_earning_table'),
    path('earning/delete/<int:row_id>', views.earning_delete_row, name='earning_delete_row'),
    path('addup_earning/<int:row_id>', views.add_update_earning, name="addup_earning"),

    # handle the `investment` table
    path('investment', views.show_investment_table, name='show_investment_table'),
    path('investment/delete/<int:row_id>', views.investment_delete_row, name='investment_delete_row'),
    path('addup_investment/<int:row_id>', views.add_update_investment, name="addup_investment"),

    # handle the `loandetails` table
    path('loandetails', views.show_loandetails_table, name='show_loandetails_table'),
    path('loandetails/delete/<int:row_id>', views.loandetails_delete_row, name='loandetails_delete_row'),
    path('addup_loandetails/<int:row_id>', views.add_update_loandetails, name="addup_loandetails"),

]
