from django.urls import path
from . import views

urlpatterns = [
    path('natureofmembership_insert/', views.natureofmembership_insert, name='natureofmembership_insert'),
    path('natureofmembership_show/', views.natureofmembership_show, name='natureofmembership_show'),
    path('edit/<int:pk>', views.natureofmembership_edit, name='natureofmembership_edit'),
    path('remove/<int:pk>', views.natureofmembership_delete, name='natureofmembership_delete'),
    path('approval/<int:pk>', views.natureofmembership_approval, name='natureofmembership_approval'),
    path('edited/<int:pk>', views.natureofmembership_edited, name='natureofmembership_edited'),
    path('terminate/<int:pk>', views.natureofmembership_terminate, name='natureofmembership_terminate'),
]