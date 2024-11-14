from django.urls import path
from . import views

urlpatterns = [
    path('providerdoctors_insert/', views.providerdoctors_insert, name='providerdoctors_insert'),
    path('providerdoctors_show/', views.providerdoctors_show, name='providerdoctors_show'),
    path('edit/<int:pk>', views.providerdoctors_edit, name='providerdoctors_edit'),
    path('remove/<int:pk>', views.providerdoctors_delete, name='providerdoctors_delete'),
    path('approval/<int:pk>', views.providerdoctors_approval, name='providerdoctors_approval'),
    path('edited/<int:pk>', views.providerdoctors_edited, name='providerdoctors_edited'),
    path('terminate/<int:pk>', views.providerdoctors_terminate, name='providerdoctors_terminate'),
]