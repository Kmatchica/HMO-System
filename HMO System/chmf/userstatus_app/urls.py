from django.urls import path
from . import views

urlpatterns = [
    path('userstatus_insert/', views.userstatus_insert, name='userstatus_insert'),
    path('userstatus_show/', views.userstatus_show, name='userstatus_show'),
    path('edit/<int:pk>', views.userstatus_edit, name='userstatus_edit'),
    path('remove/<int:pk>', views.userstatus_delete, name='userstatus_delete'),
    path('approval/<int:pk>', views.userstatus_approval, name='userstatus_approval'),
    path('edited/<int:pk>', views.userstatus_edited, name='userstatus_edited'),
    path('terminate/<int:pk>', views.userstatus_terminate, name='userstatus_terminate'),
]