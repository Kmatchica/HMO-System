from django.urls import path
from . import views

urlpatterns = [
    path('access_insert/', views.access_insert, name='access_insert'),
    path('access_show/', views.access_show, name='access_show'),
    path('edit/<int:pk>', views.access_edit, name='access_edit'),
    path('edited/<int:pk>', views.access_edited, name='access_edited'),
    path('remove/<int:pk>', views.access_delete, name='access_delete'),
    path('approval/<int:pk>', views.access_approval, name='access_approval'),
    path('terminate/<int:pk>', views.access_terminate, name='access_terminate'),
]


