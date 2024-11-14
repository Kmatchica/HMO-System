from django.urls import path
from . import views

urlpatterns = [
    path('procedureprovider_insert/', views.procedureprovider_insert, name='procedureprovider_insert'),
    path('procedureprovider_show/', views.procedureprovider_show, name='procedureprovider_show'),
    path('edit/<int:pk>', views.procedureprovider_edit, name='procedureprovider_edit'),
    path('remove/<int:pk>', views.procedureprovider_delete, name='procedureprovider_delete'),
    path('approval/<int:pk>', views.procedureprovider_approval, name='procedureprovider_approval'),
    path('edited/<int:pk>', views.procedureprovider_edited, name='procedureprovider_edited'),
    path('terminate/<int:pk>', views.procedureprovider_terminate, name='procedureprovider_terminate'),
]