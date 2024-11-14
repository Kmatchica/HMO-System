from django.urls import path
from . import views

urlpatterns = [
    path('payablename_insert/', views.payablename_insert, name='payablename_insert'),
    path('payablename_show/', views.payablename_show, name='payablename_show'),
    path('edit/<int:pk>', views.payablename_edit, name='payablename_edit'),
    path('remove/<int:pk>', views.payablename_delete, name='payablename_delete'),
    path('approval/<int:pk>', views.payablename_approval, name='payablename_approval'),
    path('edited/<int:pk>', views.payablename_edited, name='payablename_edited'),
    path('terminate/<int:pk>', views.payablename_terminate, name='payablename_terminate'),
]