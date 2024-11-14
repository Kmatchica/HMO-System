from django.urls import path
from . import views

urlpatterns = [
    path('coopagent_insert/', views.coopagent_insert, name='coopagent_insert'),
    path('approval/<int:pk>', views.coopagent_approval, name='coopagent_approval'),
    path('coopagent_show/', views.coopagent_show, name='coopagent_show'),
    path('edit/<int:pk>', views.coopagent_edit, name='coopagent_edit'),
    path('edited/<int:pk>', views.coopagent_edited, name='coopagent_edited'),
    path('remove/<int:pk>', views.coopagent_delete, name='coopagent_delete'),
    path('terminate/<int:pk>', views.coopagent_terminate, name='coopagent_terminate'),

]

