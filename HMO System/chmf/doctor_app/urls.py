from django.urls import path
from . import views

urlpatterns = [
    path('doctor_insert/', views.doctor_insert, name='doctor_insert'),
    path('approval/<int:pk>', views.doctor_approval, name='doctor_approval'),
    path('doctor_show/', views.doctor_show, name='doctor_show'),
    path('edit/<int:pk>', views.doctor_edit, name='doctor_edit'),
    path('edited/<int:pk>', views.doctor_edited, name='doctor_edited'),
    path('remove/<int:pk>', views.doctor_delete, name='doctor_delete'),
    path('terminate/<int:pk>', views.doctor_terminate, name='doctor_terminate'),
]