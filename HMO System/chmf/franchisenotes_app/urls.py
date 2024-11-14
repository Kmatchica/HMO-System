from django.urls import path
from . import views

urlpatterns = [
    path('franchisenotes_insert/', views.franchisenotes_insert, name='franchisenotes_insert'),
    path('franchisenotes_show/', views.franchisenotes_show, name='franchisenotes_show'),
    path('edit/<int:pk>', views.franchisenotes_edit, name='franchisenotes_edit'),
    path('remove/<int:pk>', views.franchisenotes_delete, name='franchisenotes_delete'),
    path('approval/<int:pk>', views.franchisenotes_approval, name='franchisenotes_approval'),
    path('edited/<int:pk>', views.franchisenotes_edited, name='franchisenotes_edited'),
    path('terminate/<int:pk>', views.franchisenotes_terminate, name='franchisenotes_terminate'),
]