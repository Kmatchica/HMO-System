from django.urls import path
from . import views

urlpatterns = [
    path('', views.branchshow, name='branchshow'),
    path('insert/', views.branchinsert, name='branchinsert'),
    path('edit/<int:pk>', views.branchedit, name='branchedit'),
    path('remove/<int:pk>', views.branchdelete, name='branchdelete'),
]


