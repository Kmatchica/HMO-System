from django.urls import path
from . import views

urlpatterns = [
    path('Franchisestatus_insert/', views.Franchisestatus_insert, name='Franchisestatus_insert'),
    path('Franchisestatus_show/', views.Franchisestatus_show, name='Franchisestatus_show'),
    path('edit/<int:pk>', views.Franchisestatus_edit, name='Franchisestatus_edit'),
    path('remove/<int:pk>', views.Franchisestatus_delete, name='Franchisestatus_delete'),
    path('approval/<int:pk>', views.Franchisestatus_approval, name='Franchisestatus_approval'),
    path('edited/<int:pk>', views.Franchisestatus_edited, name='Franchisestatus_edited'),
    path('terminate/<int:pk>', views.Franchisestatus_terminate, name='Franchisestatus_terminate'),
]