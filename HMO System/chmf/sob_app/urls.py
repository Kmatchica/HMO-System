from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.sob_insert, name='sob-insert'),
    path('', views.sob_show, name='sob-show'),
    path('edit/<int:pk>', views.sob_edit, name='sob-edit'),
    path('remove/<int:pk>', views.sob_remove, name='sob-remove'),
]