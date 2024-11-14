from django.shortcuts import render, redirect
from datetime import datetime
from .models import access, historyaccess
from permission_app.models import permission
from roles_app.models import roles
from modulelist_app.models import moduleslist
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.
########################## new function#####################
from django.db.models import Q


# Create your views here.

def has_permission(user, access_names):
    """Check if the user has the required permissions."""
    if user.is_authenticated:
        userRoleid = user.roleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False

@login_required
def access_insert(request):
    if request.user.is_authenticated:
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                moduless = moduleslist.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                rolesid = roles.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                if request.method == "POST":
                    accessname = request.POST['accessname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    accesscode_max = access.objects.all().aggregate(Max('accesscode'))
                    accesscode_nextvalue = 1 if accesscode_max['accesscode__max'] == None else accesscode_max['accesscode__max'] + 1
                    if access.objects.annotate(uppercase_accessname=Upper('accessname')).filter(uppercase_accessname=accessname.upper()):
                        messages.error(request, "The Access Name is already Exist.") 
                    else:
                        if has_permission(request.user, ['approver', 'Approver']):
                                data = access(accesscode=accesscode_nextvalue,accessname=accessname,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=Status)
                                data.save()
                                acessCode_max = access.objects.all().aggregate(Max('accesscode')) 
                                accessCode_nextvalue = 1 if acessCode_max['accesscode__max'] == None else acessCode_max['accesscode__max']
                                for roleid in rolesid:
                                    for module in moduless:
                                        permission_save(accessCode_nextvalue,module.modulecode, roleid.recordno)
                                acesshistory_save(data, transactype)
                                return redirect('access_show')
                        else:
                                Accesscode_max = historyaccess.objects.all().aggregate(Max('recordnohist')) 
                                Accesscode_nextvalue = 1 if Accesscode_max['recordnohist__max'] == None else Accesscode_max['recordnohist__max'] + 1
                                recordnohist_max = historyaccess.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max'] + 1
                                data = historyaccess(recordno= recordno_nextvalue,accesscode=Accesscode_nextvalue,accessname=accessname,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactype, status=status)
                                data.save()
                        return redirect('access_show')    
                    return render(request, 'access_insert.html')  
                return render(request, 'access_insert.html')  
        return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def access_approval(request,pk):
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
                Dataaccess = historyaccess.objects.get(recordnohist=pk)
                moduless = moduleslist.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                rolesid = roles.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Dataaccess.transactype = 'Disapprove'
                            Dataaccess.status = 'Disapprove'
                            Dataaccess.save()
                    else:
                        accesscode = Dataaccess.accesscode
                        accessname = Dataaccess.accessname
                        remarks = Dataaccess.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = access(accesscode=accesscode,accessname=accessname,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status)
                        data.save()                       
                        Dataaccess.status = 'Approve'
                        Dataaccess.transactype = 'Approve'
                        Dataaccess.save()
                        acessCode_max = access.objects.all().aggregate(Max('accesscode')) 
                        accessCode_nextvalue = 1 if acessCode_max['accesscode__max'] == None else acessCode_max['accesscode__max']
                        for roleid in rolesid:
                            for module in moduless:
                             permission_save(accessCode_nextvalue,module.modulecode, roleid.recordno)
                        acesshistory_save(data, transactype)                  
                    return redirect('access_show')               
                return render(request,'access_approval.html',{'Dataaccess': Dataaccess})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


def permission_save(accessCode, moduleCode,roleCode):
    data = permission(
        roleid = roleCode,
        modulecode = moduleCode,
        accesscode = accessCode,
        holder = 0
    )
    data.save()

@login_required
def access_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                dataaccess = access.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove']).order_by('-transactdate')
                historyupdate = historyaccess.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyaccess.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyaccess.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='access_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                view_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['view', 'View'],status__in=['Active']).values_list('accesscode', flat=True))
                show_view_button = any(permission.holder == 1 for permission in view_permissions)
                edit_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['EDIT', 'Edit'],status__in=['Active']).values_list('accesscode', flat=True))
                show_edit_button = any(permission.holder == 1 for permission in edit_permissions)
                delete_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['DELETE', 'Delete'],status__in=['Active']).values_list('accesscode', flat=True))
                show_delete_button = any(permission.holder == 1 for permission in delete_permissions)
                insert_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['INSERT','Insert', 'ADD', 'Add'],status__in=['Active']).values_list('accesscode', flat=True))
                show_insert_button = any(permission.holder == 1 for permission in insert_permissions)

                # search_query = request.GET.get('search_query')
                # if search_query:dataaccess = dataaccess.filter(Q(accessname__icontains=search_query))   

                return render(request, 'access_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'dataaccess': dataaccess,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate
                # 'search_query': search_query
                
                
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return render(request,'access_show.html' )
                
       
@login_required
def access_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                dataaccess = access.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    dataaccess.accessname = request.POST['accessname'].strip().replace("  ", " ").title()
                    dataaccess.remarks = request.POST['remarks']
                    dataaccess.transactby = userRoleid
                    dataaccess.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='access_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            dataaccess.transactype = transactype
                            dataaccess.save()  
                            acesshistory_save(dataaccess,transactype) 
                            return redirect('access_show')
                        else:
                            recordno = pk
                            accesscode = dataaccess.accesscode
                            accessname = request.POST['accessname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks']
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyaccess(recordno=recordno,accesscode=accesscode,accessname=accessname,remarks=remarks,status=status,transactby=transactby,transactdate=transactdate,transactype=transactypes)
                            data.save() 
                        return redirect('access_show')         
                    return redirect('access_show')   
                return render(request,'access_edit.html',{'dataaccess': dataaccess})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def access_edited(request,pk):
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
                Dataaccess = historyaccess.objects.get(recordnohist=pk)
                dataaccess = access.objects.get(recordno=Dataaccess.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                            Dataaccess.transactype = 'Disapprove'
                            Dataaccess.status = 'Disapprove'
                            Dataaccess.save()             
                    else:
                        dataaccess.accessname = Dataaccess.accessname
                        dataaccess.remarks = Dataaccess.remarks
                        dataaccess.transactby = userRoleid
                        dataaccess.transactdate = datetime.now()                           
                        dataaccess.transactype = transactype
                        dataaccess.status = 'Active'
                        dataaccess.save() 
                        Dataaccess.status = 'Approve'
                        Dataaccess.transactype = 'Approve'
                        Dataaccess.save()               
                    return redirect('access_show')
                return render(request,'access_edited.html',{'Dataaccess': Dataaccess,'dataaccess': dataaccess})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     


@login_required
def access_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                dataaccess = access.objects.get(recordno=pk)
                transactype = 'Terminate'
                dataaccess.transactby = userRoleid
                dataaccess.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='access_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                            if request.method == 'POST':
                                dataaccess.transactby = userRoleid
                                dataaccess.transactdate = datetime.now()
                                dataaccess.transactype = transactype
                                dataaccess.status = 'Deactive'
                                dataaccess.save()
                                acesshistory_save(dataaccess, transactype)
                                return redirect('access_show') 
                            return render(request, 'access_delete.html', {'dataaccess': dataaccess,})                                           
                    else:
                        dataaccess.status = 'Deactive'
                        dataaccess.save()
                        recordno = pk
                        accesscode = dataaccess.accesscode
                        accessname = dataaccess.accessname
                        remarks = dataaccess.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyaccess(recordno=recordno,accesscode=accesscode,accessname=accessname,remarks=remarks,status=status,transactby=transactby,transactdate=transactdate,transactype=transactypes)
                        data.save() 
                        acesshistory_save(data, transactype)
                        return redirect('access_show')
                    
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def access_terminate(request,pk):
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
                Dataaccess = historyaccess.objects.get(recordnohist=pk)
                dataaccess = access.objects.get(recordno=Dataaccess.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Dataaccess.transactype = 'Approve'
                            Dataaccess.status = 'Approve'
                            Dataaccess.save()  
                            dataaccess.transactype = 'edit'
                            dataaccess.status = 'Active'
                            dataaccess.save()            
                    else:
                        Dataaccess.transactype = 'Terminate'
                        Dataaccess.status = 'Terminate'
                        Dataaccess.save()  
                        dataaccess.transactype = 'Terminate'
                        dataaccess.status = 'Terminate'
                        dataaccess.save()                
                    return redirect('access_show')
                return render(request,'access_terminate.html',{'Dataaccess': Dataaccess,'dataaccess': dataaccess})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def access_suspend(request, pk):
     if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                dataaccess = access.objects.get(recordno=pk)
                transactype = 'Suspend'
                dataaccess.transactby = userRoleid
                dataaccess.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='access_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            dataaccess.transactby = userRoleid
                            dataaccess.transactdate = datetime.now()
                            dataaccess.transactype = transactype
                            dataaccess.status = 'Suspend'
                            dataaccess.save()
                            acesshistory_save(dataaccess, transactype)
                            return redirect('access_show')                                             
                    else:
                        dataaccess.status = 'Suspend'
                        dataaccess.save()
                        recordno = pk
                        accesscode = dataaccess.accesscode
                        accessname = dataaccess.accessname
                        remarks = dataaccess.remarks
                        status = 'Suspend'
                        transactypes = 'Suspend'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyaccess(recordno=recordno,accesscode=accesscode,accessname=accessname,remarks=remarks,status=status,transactby=transactby,transactdate=transactdate,transactype=transactypes)
                        data.save() 
                        return redirect('access_show')
                    return render(request, 'access_suspend.html', {'dataaccess': dataaccess,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
     return redirect('login') 

@login_required
def access_suspendapproval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='access_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Dataaccess = historyaccess.objects.get(recordnohist=pk)
                dataaccess = access.objects.get(recordno=Dataaccess.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Dataaccess.transactype = 'Terminate'
                            Dataaccess.status = 'Terminate'
                            Dataaccess.save()  
                            dataaccess.transactype = 'Reactive'
                            dataaccess.status = 'Suspend'
                            dataaccess.save()            
                    else:
                        Dataaccess.transactype = 'Approve'
                        Dataaccess.status = 'Approve'
                        Dataaccess.save()  
                        dataaccess.transactype = 'edit'
                        dataaccess.status = 'Active'
                        dataaccess.save()                
                    return redirect('access_show')
                return render(request,'access_suspendapproval.html',{'Dataaccess': Dataaccess})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  
  

def acesshistory_save(obj, transactype):
    access = obj
    data = historyaccess(
        recordno=access.recordno,
        accesscode=access.accesscode,
        accessname=access.accessname,
        remarks=access.remarks,
        status=access.status,
        transactby=access.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()

