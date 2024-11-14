from django.urls import path
from . import views

urlpatterns = [
    path('specialization_insert/', views.specialization_insert, name='specialization_insert'),
    path('specialization_show/', views.specialization_show, name='specialization_show'),
    path('edit/<int:pk>', views.specialization_edit, name='specialization_edit'),
    path('remove/<int:pk>', views.specialization_delete, name='specialization_delete'),
    path('approval/<int:pk>', views.specialization_approval, name='specialization_approval'),
    path('edited/<int:pk>', views.specialization_edited, name='specialization_edited'),
    path('terminate/<int:pk>', views.specialization_terminate, name='specialization_terminate'),
]