from django.urls import path
from . import views

urlpatterns = [
    path('department_insert/', views.department_insert, name='department_insert'),
    path('approval/<int:pk>', views.department_approval, name='access_approval'),
    path('department_show/', views.department_show, name='department_show'),
    path('edit/<int:pk>', views.department_edit, name='department_edit'),
    path('edited/<int:pk>', views.access_edited, name='access_edited'),
    path('remove/<int:pk>', views.department_delete, name='departmentdelete'),
    path('terminate/<int:pk>', views.department_terminate, name='department_terminate'),
    
]