from django.urls import path
from . import views

urlpatterns = [
    path('provider_insert/', views.provider_insert, name='provider_insert'),
    path('provider_show/', views.provider_show, name='provider_show'),
    path('edit/<int:pk>', views.provider_edit, name='provider_edit'),
    path('remove/<int:pk>', views.provider_delete, name='provider_delete'),
    path('approval/<int:pk>', views.provider_approval, name='provider_approval'),
    path('edited/<int:pk>', views.provider_edited, name='provider_edited'),
    path('terminate/<int:pk>', views.provider_terminate, name='provider_terminate'),
]


    