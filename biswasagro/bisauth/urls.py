from django.urls import path
from . import views

app_name = 'bisauth'

urlpatterns = [
    # handle login and register
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # handle the `tbl_roles` table
    path('tblroles', views.show_tblroles_table, name='show_tblroles_table'),
    path('addup_tblroles/<int:row_id>', views.add_update_tblroles, name="addup_tblroles"),
    path('tblroles/delete/<int:row_id>', views.tblroles_delete_row, name='tblroles_delete_row'),

    # handle the `tbl_users` table
    path('tblusers', views.show_tblusers_table, name='show_tblusers_table'),
    path('addup_tblusers/<int:row_id>', views.add_update_tblusers, name="addup_tblusers"),
    path('tblusers/delete/<int:row_id>', views.tblusers_delete_row, name='tblusers_delete_row'),
]
