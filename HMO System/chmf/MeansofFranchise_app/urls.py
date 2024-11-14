from django.urls import path
from . import views

urlpatterns = [
    path('MeansofFranchise_insert/', views.MeansofFranchise_insert, name='MeansofFranchise_insert'),
    path('MeansofFranchise_show/', views.MeansofFranchise_show, name='MeansofFranchise_show'),
    path('edit/<int:pk>', views.MeansofFranchise_edit, name='MeansofFranchise_edit'),
    path('remove/<int:pk>', views.MeansofFranchise_delete, name='MeansofFranchise_delete'),
    path('approval/<int:pk>', views.MeansofFranchise_approval, name='MeansofFranchise_approval'),
    path('edited/<int:pk>', views.MeansofFranchise_edited, name='MeansofFranchise_edited'),
    path('terminate/<int:pk>', views.MeansofFranchise_terminate, name='MeansofFranchise_terminate'),
]