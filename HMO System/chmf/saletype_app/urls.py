from django.urls import path
from . import views

urlpatterns = [
    path('saletype_insert/', views.saletype_insert, name='saletype_insert'),
    path('saletype_show/', views.saletype_show, name='saletype_show'),
    path('edit/<int:pk>', views.saletype_edit, name='saletype_edit'),
    path('remove/<int:pk>', views.saletype_delete, name='saletype_delete'),
    path('approval/<int:pk>', views.saletype_approval, name='saletype_approval'),
    path('edited/<int:pk>', views.saletype_edited, name='saletype_edited'),
    path('terminate/<int:pk>', views.saletype_terminate, name='saletype_terminate'),
]