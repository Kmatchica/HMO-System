from django.urls import path
from . import views

urlpatterns = [
    path('agentstatus_insert/', views.agentstatus_insert, name='agentstatus_insert'),
    path('agentstatus_show/', views.agentstatus_show, name='agentstatus_show'),
    path('edit/<int:pk>', views.agentstatus_edit, name='agentstatus_edit'),
    path('remove/<int:pk>', views.agentstatus_delete, name='agentstatus_delete'),
    path('approval/<int:pk>', views.agentstatus_approval, name='agentstatus_approval'),
    path('edited/<int:pk>', views.agentstatus_edited, name='agentstatus_edited'),
    path('terminate/<int:pk>', views.agentstatus_terminate, name='agentstatus_terminate'),
]