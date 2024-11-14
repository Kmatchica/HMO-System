from django.urls import path
from . import views

urlpatterns = [
    path('', views.availmentstatusshow, name='availmentstatusshow'),
    path('availmentstatusinsert/', views.availmentstatusinsert, name='availmentstatusinsert'),
    path('availmentstatusedit/<int:pk>', views.availmentstatusedit, name='availmentstatusedit'),
    path('availmentstatusremove/<int:pk>', views.availmentstatusdelete, name='availmentstatusdelete'),
]


