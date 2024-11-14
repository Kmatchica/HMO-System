from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:pk>', views.permission_edit, name='permission_edit'),
]