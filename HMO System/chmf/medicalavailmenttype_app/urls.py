from django.urls import path
from . import views

urlpatterns = [
    path('', views.availmenttypeshow, name='availmenttypeshow'),
    path('insert/', views.availmenttypeinsert, name='availmenttypeinsert'),
    path('edit/<int:pk>', views.availmenttypeedit, name='availmenttypeedit'),
    path('remove/<int:pk>', views.availmenttypedelete, name='availmenttypedelete'),
]


