from django.urls import path
from . import views

urlpatterns = [
    path('doctorroomfee_insert/', views.doctorroomfee_insert, name='doctorroomfee_insert'),
    path('doctorroomfee_show/', views.doctorroomfee_show, name='doctorroomfee_show'),
    path('edit/<int:pk>', views.doctorroomfee_edit, name='doctorroomfee_edit'),
    path('remove/<int:pk>', views.doctorroomfee_delete, name='doctorroomfee_delete'),
    path('approval/<int:pk>', views.doctorroomfee_approval, name='doctorroomfee_approval'),
    path('edited/<int:pk>', views.doctorroomfee_edited, name='doctorroomfee_edited'),
    path('terminate/<int:pk>', views.doctorroomfee_terminate, name='doctorroomfee_terminate'),
]