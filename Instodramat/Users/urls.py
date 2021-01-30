from django.urls import path
from . import views


#path('url', '<view name>', name=<''url name>)
urlpatterns = [
    path('<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('registry/', views.user_create_view, name='registry'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('<int:pk>/follow/', views.follow_ajax, name='follow_ajax'),
    path('<int:pk>/follow_list/', views.follow_list_ajax, name='follow_list_ajax'),
    path('<int:pk>/followers_list/', views.followers_list_ajax, name='followers_list_ajax'),
]