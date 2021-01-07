from django.urls import path
from . import views

#path('url', '<view name>', name=<''url name>)
urlpatterns = [
    path('<int:pk>', views.ProfileView.as_view(), name='xd'),
    path('registry', views.user_create_view, name='registry'),
]