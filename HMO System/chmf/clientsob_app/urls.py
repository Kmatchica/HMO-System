from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientsobshow, name='clientsobshow'),
    path('insert/', views.clientsobinsert, name='clientsobinsert'),
    path('edit/<int:pk>', views.clientsobedit, name='clientsobedit'),
    path('remove/<int:pk>', views.clientsobdelete, name='clientsobdelete'),
]


