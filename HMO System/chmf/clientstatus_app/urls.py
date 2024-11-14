from django.urls import path
from . import views

urlpatterns = [
    path('', views.statusshow, name='statusshow'),
    path('insert/', views.statusinsert, name='statusinsert'),
    path('edit/<int:pk>', views.statusedit, name='statusedit'),
    path('remove/<int:pk>', views.statusdelete, name='statusdelete'),
]


