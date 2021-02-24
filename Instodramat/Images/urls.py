from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_image_view, name='add_photo'),
    path('preview/<int:photo_id>/', views.image_preview, name='preview'),
    path('preview/<int:photo_id>/like/', views.like_photo_ajax, name='like_photo_ajax'),
    path('preview/<int:photo_id>/like_list/', views.get_likes_list_ajax, name='like_list_ajax'),
    path('preview/<int:photo_id>/remove', views.remove_photo, name='remove'),
    path('preview/<int:photo_id>/edit/', views.edit_photo, name='photo_edit'),
]