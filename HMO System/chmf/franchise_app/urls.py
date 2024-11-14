from django.urls import path
from . import views

urlpatterns = [
    path('franchise_insert/', views.franchise_insert, name='franchise_insert'),
    path('approval/<int:pk>', views.franchise_approval, name='franchise_approval'),
    path('franchise_show/', views.franchise_show, name='franchise_show'),
    path('edit/<int:pk>', views.franchise_edit, name='franchise_edit'),
    path('edited/<int:pk>', views.franchise_edited, name='franchise_edited'),
    path('remove/<int:pk>', views.franchise_delete, name='franchise_delete'),
    path('terminate/<int:pk>', views.franchise_terminate, name='franchise_terminate'),

]

