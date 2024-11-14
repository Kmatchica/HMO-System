from django.shortcuts import render, redirect
from .models import roles,historyroles
from access_app.models import access
from modulelist_app.models import moduleslist
from permission_app.models import permission
from roles_app.models import roles
from datetime import datetime 
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.
from django.db.models import Q
@login_required
def roles_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                moduless = moduleslist.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                dataaccess = access.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                rolecode_max = roles.objects.all().aggregate(Max('recordno')) 
                if request.method == "POST":
                    rolename = request.POST['rolename']
                    roledisplayname = request.POST['roledisplayname']
                    roledescription = request.POST['roledescription']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    roleid_max = roles.objects.all().aggregate(Max('roleid'))
                    roleid_nextvalue = 1 if roleid_max['roleid__max'] == None else roleid_max['roleid__max'] + 1 
                    if roles.objects.annotate(uppercase_rolename=Upper('rolename')).filter(uppercase_rolename=rolename.upper(),status="Inactive"):
                        messages.error(request, "The Role name is already Exist Please View in Inactive List.")   
                    elif roles.objects.annotate(uppercase_rolename=Upper('rolename')).filter(uppercase_rolename=rolename.upper(),status="Active"):
                        messages.error(request, "The Role name is already Exist.")   
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                roleid_max = historyroles.objects.all().aggregate(Max('recordnohist')) 
                                roleid_nextvalue = 1 if roleid_max['recordnohist__max'] == None else roleid_max['recordnohist__max']+ 1
                                data = roles(roleid=roleid_nextvalue,rolename=rolename, roledisplayname=roledisplayname, roledescription=roledescription,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status)
                                data.save()
                                rolecode_max = historyroles.objects.all().aggregate(Max('recordnohist'))
                                rolecode_nextvalue = 1 if rolecode_max['recordnohist__max'] == None else rolecode_max['recordnohist__max']+ 1
                                for module in moduless:
                                     for codeaccess in dataaccess:
                                        permission_save(rolecode_nextvalue, module.modulecode, codeaccess.accesscode)
                                roleshistory_save(data, transactype)
                                return redirect('roles_show')
                            else:
                                roleid_max = historyroles.objects.all().aggregate(Max('recordnohist')) 
                                roleid_nextvalue = 1 if roleid_max['recordnohist__max'] == None else roleid_max['recordnohist__max']+ 1                                
                                recordnohist_max = historyroles.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                                data = historyroles(recordno=recordno_nextvalue,roleid=roleid_nextvalue,rolename=rolename, roledisplayname=roledisplayname, roledescription=roledescription,transactby=transactby,transactdate=transactdate,transactype=Transactypes,status=status)                                
                                data.save()
                                return redirect('roles_show')
                        return render(request, 'roles_insert.html')              
                    return render(request, 'roles_insert.html')  
                return render(request, 'roles_insert.html',{'userRoleid': userRoleid,'moduless': moduless,'dataaccess': dataaccess})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def roles_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyroles = historyroles.objects.get(recordnohist=pk)
                moduless = moduleslist.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                dataaccess = access.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                rolecode_max = roles.objects.all().aggregate(Max('recordno'))
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyroles.transactype = 'Disapprove'
                            Historyroles.status = 'Disapprove'
                            Historyroles.save()             
                    else:
                        roleid = Historyroles.roleid
                        rolename = Historyroles.rolename
                        roledisplayname = Historyroles.roledisplayname
                        roledescription = Historyroles.roledescription
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = roles(roleid=roleid,rolename=rolename, roledisplayname=roledisplayname, roledescription=roledescription,transactby=transactby,transactdate=transactdate,transactype=transactype,status=status)
                        data.save()                       
                        Historyroles.status = 'Approve'
                        Historyroles.transactype = 'Approve'
                        Historyroles.save()
                        rolecode_nextvalue = 1 if rolecode_max['recordno__max'] == None else rolecode_max['recordno__max']+ 1
                        for module in moduless:
                            for codeaccess in dataaccess:
                                permission_save(rolecode_nextvalue, module.modulecode, codeaccess.accesscode)
                        roleshistory_save(data, transactype)                  
                    return redirect('roles_show')               
                return render(request,'roles_approval.html',{'Historyroles': Historyroles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')                  

def permission_save(roleCodes, moduleCode, accessCode):
    data = permission(
        roleid = roleCodes,
        modulecode = moduleCode,
        accesscode = accessCode,
        holder = 0
    )
    data.save()

@login_required
def roles_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyroles.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyroles.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyroles.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
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
                # Search the dataaccess queryset based on the search query
                search_query = request.GET.get('search_query')
                if search_query:
                    Roles = Roles.filter(
                        
                        Q(rolename__icontains=search_query) 
                        # Q(remarks__icontains=search_query)
                    )
                return render(request, 'roles_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Roles': Roles           
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

@login_required
def roles_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Roles = roles.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Roles.rolename = request.POST['rolename']
                    Roles.roledisplayname = request.POST['roledisplayname']
                    Roles.roledescription = request.POST['roledescription']
                    Roles.transactby = userRoleid
                    Roles.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Roles.transactype = transactype
                            Roles.save()  
                            roleshistory_save(Roles,transactype) 
                            return redirect('roles_show')
                        else:
                            recordno = pk
                            roleid = Roles.roleid
                            rolename = Roles.rolename
                            roledisplayname = Roles.roledisplayname
                            roledescription = Roles.roledescription
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyroles(recordno=recordno,roleid=roleid,rolename=rolename, roledisplayname=roledisplayname, roledescription=roledescription,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status)
                            data.save()                       
                        return redirect('roles_show')         
                    return redirect('roles_show')   
                return render(request,'roles_edit.html',{'Roles': Roles})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     
    
@login_required
def roles_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyroles = historyroles.objects.get(recordnohist=pk)
                Roles = roles.objects.get(recordno=Historyroles.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyroles.transactype = 'Disapprove'
                            Historyroles.status = 'Disapprove'
                            Historyroles.save()             
                    else:
                        Roles.roleid=Historyroles.roleid
                        Roles.rolename = Historyroles.rolename
                        Roles.roledisplayname = Historyroles.roledisplayname
                        Roles.roledescription = Historyroles.roledescription
                       
                        Roles.transactby = userRoleid
                        Roles.transactdate = datetime.now()                           
                        Roles.transactype = transactype
                        Roles.status = 'Active'
                        Roles.save() 
                        Historyroles.status = 'Approve'
                        Historyroles.transactype = 'Approve'
                        Historyroles.save()               
                    return redirect('roles_show')
                return render(request,'roles_edited.html',{'Historyroles': Historyroles,'Roles': Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login') 

@login_required   
def roles_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Roles = roles.objects.get(recordno=pk)
                transactype = 'Terminate'
                Roles.transactby = userRoleid
                Roles.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Roles.transactby = userRoleid
                            Roles.transactdate = datetime.now()
                            Roles.transactype = transactype
                            Roles.status = 'Deactive'
                            Roles.save()
                            roleshistory_save(Roles, transactype)
                            permissions = permission.objects.filter(roleid=pk)
                            permissions.update(holder=0)
                            return redirect('roles_show')                                             
                    else:                       
                        Roles.status = 'Deactive'
                        Roles.save()
                        recordno = pk
                        roleid=Roles.roleid
                        rolename = Roles.rolename
                        roledisplayname = Roles.roledisplayname
                        roledescription = Roles.roledescription
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyroles(recordno=recordno,roleid=roleid,rolename=rolename, roledisplayname=roledisplayname, roledescription=roledescription,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status)     
                        data.save() 
                        return redirect('roles_show')
                    return render(request, 'roles_delete.html', {'Roles': Roles,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def roles_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='roles_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyroles= historyroles.objects.get(recordnohist=pk)
                Roles = roles.objects.get(recordno=Historyroles.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historyroles.transactype = 'Approve'
                            Historyroles.status = 'Approve'
                            Historyroles.save()  
                            Roles.transactype = 'edit'
                            Roles.status = 'Active'
                            Roles.save()            
                    else:
                        Historyroles.transactype = 'Terminate'
                        Historyroles.status = 'Terminate'
                        Historyroles.save()  
                        Roles.transactype = 'Terminate'
                        Roles.status = 'Terminate'
                        Roles.save()
                        permissions = permission.objects.filter(roleid=Roles.roleid)
                        permissions.update(holder=0)               
                    return redirect('roles_show')
                return render(request,'roles_terminate.html',{'Historyroles': Historyroles,'Roles': Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

def roleshistory_save(obj, transactype):
    roles = obj
    data = historyroles(
        recordno=roles.recordno,
        roleid=roles.roleid,
        rolename=roles.rolename,
        roledisplayname=roles.roledisplayname,
        roledescription=roles.roledescription,
        transactby=roles.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()