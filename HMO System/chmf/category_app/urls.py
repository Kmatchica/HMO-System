from django.urls import path
from . import views

urlpatterns = [
    path('category_insert/', views.category_insert, name='category_insert'),
    path('approval/<int:pk>', views.category_approval, name='category_approval'),
    path('category_show/', views.category_show, name='category_show'),
    path('edit/<int:pk>', views.category_edit, name='category_edit'),
    path('edited/<int:pk>', views.category_edited, name='category_edited'),
    path('remove/<int:pk>', views.category_delete, name='category_delete'),
    path('terminate/<int:pk>', views.category_terminate, name='category_terminate'),
]