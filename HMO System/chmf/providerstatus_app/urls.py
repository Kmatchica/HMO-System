from django.urls import path
from . import views

urlpatterns = [
    path('providerstatus_insert/', views.providerstatus_insert, name='providerstatus_insert'),
    path('providerstatus_show/', views.providerstatus_show, name='providerstatus_show'),
    path('edit/<int:pk>', views.providerstatus_edit, name='providerstatus_edit'),
    path('remove/<int:pk>', views.providerstatus_delete, name='providerstatus_delete'),
    path('approval/<int:pk>', views.providerstatus_approval, name='providerstatus_approval'),
    path('edited/<int:pk>', views.providerstatus_edited, name='providerstatus_edited'),
    path('terminate/<int:pk>', views.providerstatus_terminate, name='providerstatus_terminate'),
]