from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.roomtype_insert, name='roomtype-insert'),
    path('', views.roomtype_show, name='roomtype-show'),
    path('edit/<int:pk>', views.roomtype_edit, name='roomtype-edit'),
    path('remove/<int:pk>', views.roomtype_remove, name='roomtype-remove'),
]