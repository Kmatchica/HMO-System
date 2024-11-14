from django.urls import path
from . import views

urlpatterns = [
    path('modulelist_insert/', views.modulelist_insert, name='modulelist_insert'),
    path('approval/<int:pk>', views.modulelist_approval, name='modulelist_approval'),
    path('modulelist_show/', views.modulelist_show, name='modulelist_show'),
    path('edit/<int:pk>', views.modulelist_edit, name='modulelist_edit'),
    path('edited/<int:pk>', views.modulelist_edited, name='modulelist_edited'),
    path('remove/<int:pk>', views.modulelist_delete, name='modulelist_delete'),
    path('terminate/<int:pk>', views.modulelist_terminate, name='modulelist_terminate'),
    
]

