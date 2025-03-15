from django.urls import path
from . import views

app_name = 'bisauth'

urlpatterns = [
    # handle login and register
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # handle the `roles` table
    path('roles', views.show_roles_table, name='show_roles_table'),
    path('addup_roles/<int:row_id>', views.add_update_roles, name="addup_roles"),
    path('roles/delete/<int:row_id>', views.roles_delete_row, name='roles_delete_row'),

    # handle the `usersinfo` table
    path('usersinfo', views.show_usersinfo_table, name='show_usersinfo_table'),
    path('addup_usersinfo/<int:row_id>', views.add_update_usersinfo, name="addup_usersinfo"),
    path('usersinfo/delete/<int:row_id>', views.usersinfo_delete_row, name='usersinfo_delete_row'),

    # handle the `salary` table
    path('salary', views.show_salary_table, name='show_salary_table'),
    path('addup_salary/<int:row_id>', views.add_update_salary, name="addup_salary"),
    path('salary/delete/<int:row_id>', views.salary_delete_row, name='salary_delete_row'),

    # handle the `staff` table
    path('staff', views.show_staff_table, name='show_staff_table'),
    path('addup_staff/<int:row_id>', views.add_update_staff, name="addup_staff"),
    path('staff/delete/<int:row_id>', views.staff_delete_row, name='staff_delete_row'),

    # handle the `staffs` table
    path('staffs', views.show_staffs_table, name='show_staffs_table'),
    path('addup_staffs/<int:row_id>', views.add_update_staffs, name="addup_staffs"),
    path('staffs/delete/<int:row_id>', views.staffs_delete_row, name='staffs_delete_row'),

]
