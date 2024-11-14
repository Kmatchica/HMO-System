from django.urls import path
from . import views

urlpatterns = [
    path('roles_insert/', views.roles_insert, name='roles_insert'),
    path('roles_show/', views.roles_show, name='roles_show'),
    path('edit/<int:pk>', views.roles_edit, name='roles_edit'),
    path('remove/<int:pk>', views.roles_delete, name='roles_delete'),
    path('approval/<int:pk>', views.roles_approval, name='roles_approval'),
    path('edited/<int:pk>', views.roles_edited, name='roles_edited'),
    path('terminate/<int:pk>', views.roles_terminate, name='roles_terminate'),
]