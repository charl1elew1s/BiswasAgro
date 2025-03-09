from django.urls import path
from . import views

# app_name = 'inventory'
app_name = 'inv'


urlpatterns = [
    # handle the `fishbuy` table
    path('fishbuy', views.show_fishbuy_table, name='show_fishbuy_table'),
    path('addup_fishbuy/<int:row_id>', views.add_update_fishbuy, name="addup_fishbuy"),
    path('fishbuy/delete/<int:row_id>', views.fishbuy_delete_row, name='fishbuy_delete_row'),

    # handle the `fishtype` table
    path('fishtype', views.show_fishtype_table, name='show_fishtype_table'),
    path('addup_fishtype/<int:row_id>', views.add_update_fishtype, name="addup_fishtype"),
    path('fishtype/delete/<int:row_id>', views.fishtype_delete_row, name='fishtype_delete_row'),

    # handle the `items` table
    path('items', views.show_items_table, name='show_items_table'),
    path('addup_items/<int:row_id>', views.add_update_items, name="addup_items"),
    path('items/delete/<int:row_id>', views.items_delete_row, name='items_delete_row'),

    # handle the `land` table
    path('land', views.show_land_table, name='show_land_table'),
    path('addup_land/<int:row_id>', views.add_update_land, name="addup_land"),
    path('land/delete/<int:row_id>', views.land_delete_row, name='land_delete_row'),

    # handle the `sectors` table
    path('sectors', views.show_sectors_table, name='show_sectors_table'),
    path('addup_sectors/<int:row_id>', views.add_update_sectors, name="addup_sectors"),
    path('sectors/delete/<int:row_id>', views.sectors_delete_row, name='sectors_delete_row'),

    # handle the `units` table
    path('units', views.show_units_table, name='show_units_table'),
    path('addup_units/<int:row_id>', views.add_update_units, name="addup_units"),
    path('units/delete/<int:row_id>', views.units_delete_row, name='units_delete_row'),

    # handle the `dailyworks` table
    path('dailyworks', views.show_dailyworks_table, name='show_dailyworks_table'),
    path('addup_dailyworks/<int:row_id>', views.add_update_dailyworks, name="addup_dailyworks"),
    path('dailyworks/delete/<int:row_id>', views.dailyworks_delete_row, name='dailyworks_delete_row'),

    # handle the `fooddistribution` table
    path('fooddist', views.show_fooddistribution_table, name='show_fooddistribution_table'),
    path('addup_fooddistribution/<int:row_id>', views.add_update_fooddistribution, name="addup_fooddistribution"),
    path('fooddistribution/delete/<int:row_id>', views.fooddistribution_delete_row, name='fooddistribution_delete_row'),

]