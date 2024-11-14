from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientshow, name='clientshow'),
    path('insert/', views.clientinsert, name='clientinsert'),
    path('edit/<int:pk>', views.clientedit, name='clientedit'),
    path('remove/<int:pk>', views.clientdelete, name='clientdelete'),
]


