from django.urls import path
from . import views

#path('url', '<view name>', name=<''url name>)
urlpatterns = [
    path('', views.test, name='xd')
]