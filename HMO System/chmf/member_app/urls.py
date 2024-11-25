from django.urls import path
from . import views

urlpatterns = [
    path('', views.membershow, name='membershow'),
    path('insert/', views.memberinsert, name='memberinsert'),
    path('edit/<int:pk>', views.memberedit, name='memberedit'),
    path('remove/<int:pk>', views.memberdelete, name='memberdelete'),
    path('get-client-branches/', views.get_client_branches, name='get_client_branches'),
]


