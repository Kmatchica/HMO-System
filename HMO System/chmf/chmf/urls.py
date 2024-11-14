"""
URL configuration for chmf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login_app.urls')),
    path('roles/', include('roles_app.urls')),

  
    path('modulelist/', include('modulelist_app.urls')),
    path('permission/', include('permission_app.urls')),
    path('access/', include('access_app.urls')),

    path('login/', include('django.contrib.auth.urls')),
    path('provider/', include('provider_app.urls')),
    path('specialization/', include('specialization_app.urls')),
    path('category/', include('category_app.urls')),
    path('doctor/', include('doctor_app.urls')),
    path('coopagent/', include('coopagent_app.urls')),
    path('department/', include('department_app.urls')),
    path('userstatus/', include('userstatus_app.urls')),
    path('providerstatus/', include('providerstatus_app.urls')),
    path('payablename/', include('payablename_app.urls')),
    path('providerdoctors/', include('providerdoctors_app.urls')),
    path('doctorstatus/', include('doctorstatus_app.urls')),
    path('medicalprocedures/', include('medicalprocedures_app.urls')),
    path('procedureprovider/', include('procedureprovider_app.urls')),
    path('doctorroomfee/', include('doctorroomfee_app.urls')),
    path('roomtype/', include('roomtype_app.urls')),
    path('natureofmembership/', include('natureofmembership_app.urls')),
    path('MeansofFranchise/', include('MeansofFranchise_app.urls')),
    path('Franchisestatus/', include('Franchisestatus_app.urls')),
    path('clientbranch/', include('clientbranch_app.urls')),
    path('saletype/', include('saletype_app.urls')),
    path('agentstatus/', include('agentstatus_app.urls')),
    path('franchise/', include('franchise_app.urls')),

    path('clientclassification/', include('clientclassification_app.urls')),
    path('clientstatus/', include('clientstatus_app.urls')),
    path('clientsob/', include('clientsob_app.urls')),
    path('clientbranch/', include('clientbranch_app.urls')),
    path('client/', include('client_app.urls')),
    path('sob/', include('sob_app.urls')),
    path('memberstatus/', include('memberstatus_app.urls')),
    path('membergender/', include('membergender_app.urls')),
    path('member/', include('member_app.urls')),
    path('medicalavailmentstatus/', include('medicalavailmentstatus_app.urls')),
    path('medicalavailmenttype/', include('medicalavailmenttype_app.urls')),
    path('medicalapprovalprocedure/', include('medicalapprovalprocedure_app.urls')),
    path('medicaldiagnosis/', include('medicaldiagnosis_app.urls'))

]
