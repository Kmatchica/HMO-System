from django.shortcuts import render, redirect
from .models import permission
from access_app.models import access
from modulelist_app.models import moduleslist
from django.contrib.auth.decorators import login_required
# Create your views here.


         
@login_required
def permission_edit(request,pk):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='permission_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
                if holder_values[0] == 1:
                    permissions = permission.objects.filter(roleid=pk)
                    moduless = moduleslist.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    dataaccess = access.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    if request.method == 'POST':
                        for key, value in request.POST.items():
                            if key.startswith('permission_checkbox_'):
                                recordno = key.split('_')[-1]
                                try:
                                    per = permission.objects.get(recordno=recordno)
                                    per.holder = value
                                    per.save()
                                except permission.DoesNotExist:
                                    pass   
                        return redirect('/roles/roles_show/')
                    context = {'moduless': moduless, 'dataaccess': dataaccess, 'permissions': permissions}
                    return render(request, 'permission_edit.html', context)
                else:
                 return redirect('home')
        return redirect('home') 
    return redirect('login') 

