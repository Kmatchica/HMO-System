from django.urls import path
from . import views

urlpatterns = [
    path('medicalprocedures_insert/', views.medicalprocedures_insert, name='medicalprocedures_insert'),
    path('medicalprocedures_show/', views.medicalprocedures_show, name='medicalprocedures_show'),
    path('edit/<int:pk>', views.medicalprocedures_edit, name='medicalprocedures_edit'),
    path('remove/<int:pk>', views.medicalprocedures_delete, name='medicalprocedures_delete'),
    path('approval/<int:pk>', views.medicalprocedures_approval, name='medicalprocedures_approval'),
    path('edited/<int:pk>', views.medicalprocedures_edited, name='medicalprocedures_edited'),
    path('terminate/<int:pk>', views.medicalprocedures_terminate, name='medicalprocedures_terminate'),
]