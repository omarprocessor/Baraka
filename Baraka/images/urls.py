from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image_and_analyze, name='upload_image_and_analyze'),
    path('by-name/<str:filename>/', views.get_analysis_by_name, name='get_analysis_by_name'),
    path('by-id/<int:image_id>/', views.get_analysis_by_id, name='get_analysis_by_id'),
    path('all/', views.list_all_images, name='list_all_images'),
]
