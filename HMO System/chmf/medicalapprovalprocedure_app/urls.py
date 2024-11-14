from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicalapprovalprocedureshow, name='approvalprocedureshow'),
    path('insert/', views.medicalapprovalprocedureinsert, name='approvalprocedureinsert'),
    path('edit/<int:pk>', views.medicalapprovalprocedureedit, name='approvalprocedureedit'),
    path('remove/<int:pk>', views.medicalapprovalproceduredelete, name='approvalproceduredelete'),
]


