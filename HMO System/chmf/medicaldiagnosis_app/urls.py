from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagnosisshow, name='diagnosisshow'),
    path('diagnosisinsert/', views.diagnosisinsert, name='diagnosisinsert'),
    path('diagnosisedit/<int:pk>', views.diagnosisedit, name='diagnosisedit'),
    path('diagnosisremove/<int:pk>', views.diagnosisdelete, name='diagnosisdelete'),
]


