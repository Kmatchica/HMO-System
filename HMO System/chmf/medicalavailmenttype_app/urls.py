from django.urls import path
from . import views

urlpatterns = [
    path('', views.availmenttypeshow, name='availmenttypeshow'),
    path('availmenttypeinsert/', views.availmenttypeinsert, name='availmenttypeinsert'),
    path('availmenttypeedit/<int:pk>', views.availmenttypeedit, name='availmenttypeedit'),
    path('availmenttyperemove/<int:pk>', views.availmenttypedelete, name='availmenttypedelete'),
]


