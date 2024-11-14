from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientclassificationshow, name='clientclassificationshow'),
    path('insert/', views.clientclassificationinsert, name='clientclassificationinsert'),
    path('edit/<int:pk>', views.clientclassificationedit, name='clientclassificationedit'),
    path('remove/<int:pk>', views.clientclassificationdelete, name='clientclassificationdelete'),
]


