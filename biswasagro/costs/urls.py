from django.urls import path
from . import views

app_name = 'costs'

urlpatterns = [
    path('cost', views.show_cost_table, name='show_cost_table'),
    path('addup_cost/<int:row_id>', views.add_update_cost, name="addup_cost"),
    path('delete/<int:row_id>', views.cost_delete_row, name='cost_delete_row'),
]
