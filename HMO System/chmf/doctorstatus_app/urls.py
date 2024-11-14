from django.urls import path
from . import views

urlpatterns = [
    path('doctorstatus_insert/', views.doctorstatus_insert, name='doctorstatus_insert'),
    path('doctorstatus_show/', views.doctorstatus_show, name='doctorstatus_show'),
    path('edit/<int:pk>', views.doctorstatus_edit, name='doctorstatus_edit'),
    path('remove/<int:pk>', views.doctorstatus_delete, name='doctorstatus_delete'),
    path('approval/<int:pk>', views.doctorstatus_approval, name='doctorstatus_approval'),
    path('edited/<int:pk>', views.doctorstatus_edited, name='doctorstatus_edited'),
    path('terminate/<int:pk>', views.doctorstatus_terminate, name='doctorstatus_terminate'),
]