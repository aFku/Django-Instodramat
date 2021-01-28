from django.urls import path
from . import views


#path('url', '<view name>', name=<''url name>)
urlpatterns = [
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('registry', views.user_create_view, name='registry'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/follow', views.follow_ajax, name='follow_ajax')
]