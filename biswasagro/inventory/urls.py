from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('fishbuy', views.enter_fishbuy, name='enter_fishbuy')
]