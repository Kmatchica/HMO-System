from django.urls import path
from . import views

urlpatterns = [
    path('', views.memberstatusshow, name='memberstatusshow'),
    path('insert/', views.memberstatusinsert, name='memberstatusinsert'),
    path('edit/<int:pk>', views.memberstatusedit, name='memberstatusedit'),
    path('remove/<int:pk>', views.memberstatusdelete, name='memberstatusdelete'),
]


