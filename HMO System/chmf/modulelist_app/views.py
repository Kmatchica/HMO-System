from django.shortcuts import render, redirect
from .models import moduleslist, historymoduleslist
from access_app.models import access
from permission_app.models import permission
from roles_app.models import roles
from django.db.models import Max
from datetime import datetime 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from permission_app.models import permission
from access_app.models import access
from modulelist_app.models import moduleslist
from django.contrib import messages
from django.db.models.functions import Upper
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages

# Create your views here.
########################## new function#####################
from django.db.models import Q

@login_required
def modulelist_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
                Access = access.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                Roles = roles.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                if request.method == "POST":
                    modulename = request.POST['modulename'].strip().replace("  ", " ").title()
                    moduleshortname = request.POST['moduleshortname'].strip().replace("  ", " ").title()
                    moduleappname = request.POST['moduleappname']
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    modulecode_max = moduleslist.objects.all().aggregate(Max('modulecode'))
                    modulecode_nextvalue = 1 if modulecode_max['modulecode__max'] == None else modulecode_max['modulecode__max'] + 1
                    if moduleslist.objects.annotate(uppercase_moduleappname=Upper('moduleappname')).filter(uppercase_moduleappname=moduleappname.upper()):
                        messages.error(request, "The Module is already Exist Please View in Inactive List.")  
                    
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = moduleslist(modulecode=modulecode_nextvalue, modulename=modulename, moduleshortname=moduleshortname,moduleappname= moduleappname,remarks= remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=Status)
                                data.save()                   
                                modulelisthistory_save(data, transactype)
                                moduleCode_max = moduleslist.objects.all().aggregate(Max('modulecode')) 
                                moduleCode_nextvalue = 1 if moduleCode_max['modulecode__max'] == None else moduleCode_max['modulecode__max']
                                for Roles in Roles:
                                    for dataaccess in Access:
                                        permission_save(moduleCode_nextvalue, dataaccess.accesscode, Roles.recordno)
                                return redirect('modulelist_show')
                            else:
                                modulecode_max = historymoduleslist.objects.all().aggregate(Max('recordnohist')) 
                                modulecode_nextvalue = 1 if modulecode_max['recordnohist__max'] == None else modulecode_max['recordnohist__max']+1                                
                                recordnohist_max = historymoduleslist.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+1 
                                data = historymoduleslist(recordno= recordno_nextvalue,modulecode=modulecode_nextvalue, modulename=modulename, moduleshortname=moduleshortname,moduleappname= moduleappname,remarks= remarks,transactby=transactby,transactdate=transactdate,transactype=Transactype,status=status)
                                data.save()
                                return redirect('modulelist_show')
                        return redirect('modulelist_show')             
                    return render(request, 'modulelist_insert.html',{'installed_apps': installed_apps})  
                return render(request, 'modulelist_insert.html',{'installed_apps': installed_apps})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def modulelist_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historymoduleslist = historymoduleslist.objects.get(recordnohist=pk)
                installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
                Access = access.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                Roles = roles.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historymoduleslist.transactype = 'Disapprove'
                            Historymoduleslist.status = 'Disapprove'
                            Historymoduleslist.save()             
                    else:
                        modulecode = Historymoduleslist.modulecode
                        modulename = Historymoduleslist.modulename
                        moduleshortname = Historymoduleslist.moduleshortname
                        moduleappname = Historymoduleslist.moduleappname
                        remarks = Historymoduleslist.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='active'
                        data = moduleslist(modulecode=modulecode, modulename=modulename, moduleshortname=moduleshortname,moduleappname= moduleappname,remarks= remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status)
                        data.save()                        
                        Historymoduleslist.status = 'Approve'
                        Historymoduleslist.transactype = 'Approve'
                        Historymoduleslist.save()
                        moduleCode_max = moduleslist.objects.all().aggregate(Max('modulecode')) 
                        moduleCode_nextvalue = 1 if moduleCode_max['modulecode__max'] == None else moduleCode_max['modulecode__max']
                        for Roles in Roles:
                            for dataaccess in Access:
                                 permission_save(moduleCode_nextvalue, dataaccess.accesscode, Roles.recordno)
                        return redirect('modulelist_show')                 
                    return redirect('modulelist_show')               
                return render(request,'modulelist_approval.html',{'installed_apps': installed_apps,'Historymoduleslist': Historymoduleslist})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

def permission_save( moduleCode,accessCode,roleCode):
    data = permission(
        roleid = roleCode,
        modulecode = moduleCode,
        accesscode = accessCode,
        holder = 0
    )
    data.save()

@login_required    
def modulelist_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                historyupdate = historymoduleslist.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historymoduleslist.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historymoduleslist.objects.filter(transactype__in=['Forapproval'])
                Modulelist = moduleslist.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='access_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                view_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['View', 'View']).values_list('accesscode', flat=True))
                show_view_button = any(permission.holder == 1 for permission in view_permissions)
                edit_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['EDIT', 'Edit']).values_list('accesscode', flat=True))
                show_edit_button = any(permission.holder == 1 for permission in edit_permissions)
                delete_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['DELETE', 'Delete']).values_list('accesscode', flat=True))
                show_delete_button = any(permission.holder == 1 for permission in delete_permissions)
                insert_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['INSERT','Insert', 'ADD', 'Add']).values_list('accesscode', flat=True))
                show_insert_button = any(permission.holder == 1 for permission in insert_permissions)                                
                history_button = historymoduleslist.objects.filter(transactype='forapproval')
                show_approval_button = history_button.filter(status='forapproval').exists() 
                # filter_status = request.GET.get('filter_status')
                search_query = request.GET.get('search_query')  
                # Search the dataaccess queryset based on the search query
                if search_query:Modulelist = Modulelist.filter(Q(modulename__icontains=search_query))                          
                return render(request, 'modulelist_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_approval_button': show_approval_button,
                'show_view_button': show_view_button,
                'Modulelist': Modulelist,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate
                ###############filter for search ###############
                # 'filter_status': filter_status,
                # 'search_query': search_query
                ###############filter for search ###############
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return render(request,'modulelist_show.html' )

@login_required         
def modulelist_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Moduleslist = moduleslist.objects.get(recordno=pk)
                installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
                transactype = 'edit'
                if request.method == 'POST':
                    print(request.POST)                 
                    Moduleslist.modulename = request.POST['modulename']
                    Moduleslist.moduleshortname = request.POST['moduleshortname']
                    Moduleslist.moduleappname = request.POST['moduleappname']
                    Moduleslist.remarks = request.POST['remarks']                         
                    Moduleslist.transactype = 'edit'
                    Moduleslist.transactby = userRoleid
                    Moduleslist.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Moduleslist.transactype = transactype
                            Moduleslist.save()  
                            modulelisthistory_save(Moduleslist,transactype) 
                            return redirect('modulelist_show')
                        else:
                            recordno = pk
                            modulecode = Moduleslist.modulecode
                            modulename = Moduleslist.modulename
                            moduleshortname = Moduleslist.moduleshortname
                            moduleappname = Moduleslist.moduleappname
                            remarks = Moduleslist.remarks
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historymoduleslist(recordno=recordno,modulecode=modulecode, modulename=modulename, moduleshortname=moduleshortname,moduleappname= moduleappname,remarks= remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes, status=status)
                            data.save()
                        return redirect('modulelist_show')         
                    return redirect('modulelist_show')   
                return render(request,'modulelist_edit.html',{'installed_apps': installed_apps,'Moduleslist': Moduleslist})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def modulelist_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historymoduleslist = historymoduleslist.objects.get(recordnohist=pk)
                Moduleslist = moduleslist.objects.get(recordno=Historymoduleslist.recordno)
                transactype = 'edit'
                installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historymoduleslist.transactype = 'Disapprove'
                            Historymoduleslist.status = 'Disapprove'
                            Historymoduleslist.save()             
                    else:
                        
                        Moduleslist.modulename = Historymoduleslist.modulename
                        Moduleslist.moduleshortname = Historymoduleslist.moduleshortname
                        Moduleslist.moduleappname = Historymoduleslist.moduleappname
                        Moduleslist.remarks = Historymoduleslist.remarks
                        Moduleslist.transactby = userRoleid
                        Moduleslist.transactdate = datetime.now()                           
                        Moduleslist.transactype = transactype
                        Moduleslist.status = 'Active'
                        Moduleslist.save() 
                        Historymoduleslist.status = 'Approve'
                        Historymoduleslist.transactype = 'Approve'
                        Historymoduleslist.save()               
                    return redirect('modulelist_show')
                return render(request,'modulelist_edited.html',{'Moduleslist': Moduleslist,'installed_apps': installed_apps,'Historymoduleslist': Historymoduleslist})       
            else:
             return redirect('home')
        else:
         return redirect('home') 

@login_required
def modulelist_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Moduleslist = moduleslist.objects.get(recordno=pk)
                transactype = 'Terminate'
                Moduleslist.transactby = userRoleid
                Moduleslist.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Moduleslist.transactby = userRoleid
                            Moduleslist.transactdate = datetime.now()
                            Moduleslist.transactype = transactype
                            Moduleslist.status = 'Deactive'
                            Moduleslist.save()
                            return redirect('modulelist_show')                                             
                    else:
                        
                        Moduleslist.status = 'Deactive'
                        Moduleslist.save()
                        recordno = pk
                        modulecode = Moduleslist.modulecode
                        modulename = Moduleslist.modulename
                        moduleshortname = Moduleslist.moduleshortname
                        moduleappname = Moduleslist.moduleappname
                        remarks = Moduleslist.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historymoduleslist(recordno=recordno,modulecode=modulecode, modulename=modulename, moduleshortname=moduleshortname,moduleappname= moduleappname,remarks= remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes, status=status)
                        data.save()
                        modulelisthistory_save(data, transactype)
                        return redirect('modulelist_show')
                    return render(request, 'modulelist_delete.html', {'Moduleslist': Moduleslist,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def modulelist_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='modulelist_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historymoduleslist = historymoduleslist.objects.get(recordnohist=pk)
                Moduleslist = moduleslist.objects.get(recordno=Historymoduleslist.recordno)
                installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historymoduleslist.transactype = 'Approve'
                            Historymoduleslist.status = 'Approve'
                            Historymoduleslist.save()  
                            Moduleslist.transactype = 'edit'
                            Moduleslist.status = 'Active'
                            Moduleslist.save()            
                    else:
                        Historymoduleslist.transactype = 'Terminate'
                        Historymoduleslist.status = 'Terminate'
                        Historymoduleslist.save()  
                        Moduleslist.transactype = 'Terminate'
                        Moduleslist.status = 'Terminate'
                        Moduleslist.save()                
                    return redirect('modulelist_show')
                return render(request,'modulelist_terminate.html',{'Historymoduleslist': Historymoduleslist,'installed_apps': installed_apps})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  


def modulelisthistory_save(obj, transactype):
    moduleslist = obj
    data = historymoduleslist(
        recordno=moduleslist.recordno,
        modulecode=moduleslist.modulecode,
        modulename=moduleslist.modulename,
        moduleshortname=moduleslist.moduleshortname,
        moduleappname=moduleslist.moduleappname,
        status=moduleslist.status,
        transactby=moduleslist.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()