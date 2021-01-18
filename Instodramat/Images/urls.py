from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_image_view, name='add'),
    path('preview/<int:photo_id>/', views.image_preview, name='preview')
]