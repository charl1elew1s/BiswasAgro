from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('landing', views.reports_landing, name='landing'),
    path('daily/<str:str_date>', views.daily, name='daily'),
    path('monthly/<str:str_date>', views.monthly, name='monthly'),
    path('annual/<str:str_date>', views.annual, name='annual'),
    path('finacc', views.financial_accounting, name='finacc'),
    path('fish_details', views.fish_count_details, name='fish_cnt_details'),
    path('land_report/<str:source>', views.land_report, name='land_report'),
    path('disp_fish', views.display_fish_chart, name='disp_fish'),
    path('gen_fish/<str:str_date>', views.generate_fish_chart, name='gen_fish'),
    path('disp_earning', views.display_earnings, name='disp_earn'),
    path('gen_earn_plt/<str:plt_source>', views.gen_earn_plt, name='gen_earn_plt'),
]
