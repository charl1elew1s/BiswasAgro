from django.urls import path
from . import views

app_name = 'costs'

urlpatterns = [
    path('cost', views.enter_cost, name='enter_cost')
]
