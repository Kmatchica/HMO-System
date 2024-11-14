from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views




urlpatterns = [
    path('login/', views.login_user, name='login_user'),#index
    path('logout/', views.logout_user, name='logout_user'),
    path('home/',views.home, name='home'),
    path('login_insert/', views.login_insert, name='login_insert'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/login/change-password/done/'), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
    path('edit/<int:pk>',views.login_edit, name='login_edit'),
    path('login_show/',views.login_show, name='login_show'),
    path('approval/<int:pk>/',views.login_approval, name='login_approval'),
    path('edited/<int:pk>', views.login_edited, name='login_edited'),
    path('remove/<int:pk>', views.login_delete, name='login_delete'),
    path('terminate/<int:pk>', views.login_terminate, name='login_terminate'),
    ]


