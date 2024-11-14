from django.urls import path
from . import views

urlpatterns = [
    path('memberstatusshow/', views.memberstatusshow, name='memberstatusshow'),
    path('memberstatusinsert/', views.memberstatusinsert, name='memberstatusinsert'),
    path('memberstatusedit/<int:pk>', views.memberstatusedit, name='memberstatusedit'),
    path('memberstatusremove/<int:pk>', views.memberstatusdelete, name='memberstatusdelete'),
]


