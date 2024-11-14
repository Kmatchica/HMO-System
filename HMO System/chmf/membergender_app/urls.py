from django.urls import path
from . import views

urlpatterns = [
    path('', views.membergendershow, name='membergendershow'),
    path('insert/', views.membergenderinsert, name='membergenderinsert'),
    path('edit/<int:pk>', views.membergenderedit, name='membergenderedit'),
    path('remove/<int:pk>', views.membergenderdelete, name='membergenderdelete'),
]


