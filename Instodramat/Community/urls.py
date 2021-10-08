from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_webpage_view, name='main_page'),
    path('community', views.latest_photos_all_view, name='community'),
]