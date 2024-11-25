from django.urls import path
from . import views

urlpatterns = [
    path('', views.approvalshow, name='approvalshow'),
    path('insert/', views.approvalinsert, name='approvalinsert'),
    path('edit/<int:pk>', views.approvaledit, name='approvaledit'),
    path('remove/<int:pk>', views.approvaldelete, name='approvaldelete'),
]


