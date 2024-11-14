from django.shortcuts import render, redirect
from datetime import datetime
from .models import providerstatus, historyproviderstatus
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q

# Create your views here.
@login_required
def providerstatus_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    providerstatuscode_max = providerstatus.objects.all().aggregate(Max('providerstatuscode'))
                    providerstatuscode_nextvalue = 1 if providerstatuscode_max['providerstatuscode__max'] == None else providerstatuscode_max['providerstatuscode__max'] + 1
                    if providerstatus.objects.annotate(uppercase_statusname=Upper('statusname')).filter(uppercase_statusname=statusname.upper(),status="Inactive"):
                        messages.error(request, "The ProviderStatus Name is already Exist Please View in Inactive List.")  
                    elif providerstatus.objects.annotate(uppercase_statusname=Upper('statusname')).filter(uppercase_statusname=statusname.upper(),status="Active"):
                        messages.error(request, "The ProviderStatus Name is already Exist.")  
                    
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = providerstatus(providerstatuscode=providerstatuscode_nextvalue, statusname=statusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                providerstatushistory_save(data, transactype)
                                return redirect('providerstatus_show')
                            else:
                                Providerstatuscode_max = historyproviderstatus.objects.all().aggregate(Max('recordnohist')) 
                                Providerstatus_nextvalue = 1 if Providerstatuscode_max['recordnohist__max'] == None else Providerstatuscode_max['recordnohist__max']
                                
                                recordnohist_max = historyproviderstatus.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                data = historyproviderstatus(recordno =recordno_nextvalue, providerstatuscode=Providerstatus_nextvalue, statusname=statusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('providerstatus_show')
                        return render(request, 'providerstatus_insert.html')              
                    return render(request, 'providerstatus_insert.html')  
                return render(request, 'providerstatus_insert.html',{'userRoleid': userRoleid})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def providerstatus_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyproviderstatus = historyproviderstatus.objects.get(recordnohist=pk)
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyproviderstatus.transactype = 'Disapprove'
                            Historyproviderstatus.status = 'Disapprove'
                            Historyproviderstatus.save()  
                            return redirect('providerstatus_show')           
                    else:
                        providerstatuscode= Historyproviderstatus.providerstatuscode
                        statusname = Historyproviderstatus.statusname
                        remarks = Historyproviderstatus.remarks
                       
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = providerstatus(providerstatuscode=providerstatuscode,statusname=statusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                        data.save()                       
                        Historyproviderstatus.status = 'Approve'
                        Historyproviderstatus.transactype = 'Approve'
                        Historyproviderstatus.save()                  
                    return redirect('providerstatus_show')               
                return render(request,'providerstatus_approval.html',{'Historyproviderstatus': Historyproviderstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

@login_required   
def providerstatus_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyproviderstatus.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyproviderstatus.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyproviderstatus.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
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
                    Providerstatus = Providerstatus.filter(
                        
                        Q(statusname__icontains=search_query) |
                        Q(remarks__icontains=search_query)
                    )  
                return render(request, 'providerstatus_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Providerstatus': Providerstatus
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

@login_required
def providerstatus_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Providerstatus = providerstatus.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Providerstatus.statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                    Providerstatus.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Providerstatus.transactby = userRoleid
                    Providerstatus.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Providerstatus.transactype = transactype
                            Providerstatus.save()  
                            providerstatushistory_save(Providerstatus,transactype) 
                            return redirect('providerstatus_show')
                        else:
                            recordno = pk
                            providerstatuscode = Providerstatus.providerstatuscode
                            statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyproviderstatus(recordno =recordno, providerstatuscode=providerstatuscode, statusname=statusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                            data.save()                        
                        return redirect('providerstatus_show')         
                    return redirect('providerstatus_show')   
                return render(request,'providerstatus_edit.html',{'Providerstatus': Providerstatus})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def providerstatus_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyproviderstatus = historyproviderstatus.objects.get(recordnohist=pk)
                Providerstatus = providerstatus.objects.get(recordno=Historyproviderstatus.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyproviderstatus.transactype = 'Disapprove'
                            Historyproviderstatus.status = 'Disapprove'
                            Historyproviderstatus.save()
                            return redirect('providerstatus_show')             
                    else:
                        Providerstatus.providerstatuscode = Historyproviderstatus.providerstatuscode
                        Providerstatus.statusname = Historyproviderstatus.statusname
                        Providerstatus.remarks = Historyproviderstatus.remarks
                      
                        Providerstatus.transactby = userRoleid
                        Providerstatus.transactdate = datetime.now()                           
                        Providerstatus.transactype = transactype
                        Providerstatus.status = 'Active'
                        Providerstatus.save() 
                        Historyproviderstatus.status = 'Approve'
                        Historyproviderstatus.transactype = 'Approve'
                        Historyproviderstatus.save()               
                    return redirect('providerstatus_show')
                return render(request,'providerstatus_edited.html',{'Historyproviderstatus': Historyproviderstatus,'Providerstatus': Providerstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def providerstatus_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Providerstatus = providerstatus.objects.get(recordno=pk)

                transactype = 'Terminate'
                Providerstatus.transactby = userRoleid
                Providerstatus.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Providerstatus.transactby = userRoleid
                            Providerstatus.transactdate = datetime.now()
                            Providerstatus.transactype = transactype
                            Providerstatus.status = 'Deactive'
                            Providerstatus.save()
                            providerstatushistory_save(Providerstatus, transactype)
                            return redirect('providerstatus_show') 
                                                                    
                    else:                       
                        Providerstatus.status = 'Deactive'
                        Providerstatus.save()
                        recordno = pk
                        providerstatuscode = Providerstatus.providerstatuscode
                        statusname = Providerstatus.statusname
                        remarks = Providerstatus.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyproviderstatus(recordno=recordno,providerstatuscode=providerstatuscode, statusname=statusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('providerstatus_show')
                    return render(request, 'providerstatus_delete.html', {'Providerstatus': Providerstatus,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def providerstatus_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='providerstatus_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyproviderstatus = historyproviderstatus.objects.get(recordnohist=pk)
                    Providerstatus = providerstatus.objects.get(recordno=Historyproviderstatus.recordno)
                    
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyproviderstatus.transactype = 'Approve'
                                Historyproviderstatus.status = 'Approve'
                                Historyproviderstatus.save()  
                                Providerstatus.transactype = 'edit'
                                Providerstatus.status = 'Active'
                                Providerstatus.save()            
                        else:
                            Historyproviderstatus.transactype = 'Terminate'
                            Historyproviderstatus.status = 'Terminate'
                            Historyproviderstatus.save()  
                            Providerstatus.transactype = 'Terminate'
                            Providerstatus.status = 'Terminate'
                            Providerstatus.save()                
                        return redirect('providerstatus_show')
                    return render(request,'providerstatus_terminate.html',{'Historyproviderstatus': Historyproviderstatus,'Providerstatus': Providerstatus})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def providerstatushistory_save(obj, transactype):
    userstatus = obj
    data = historyproviderstatus(
        recordno=userstatus.recordno,
        providerstatuscode=userstatus.providerstatuscode,
        statusname=userstatus.statusname,
        remarks=userstatus.remarks,
        status=userstatus.status,
        transactby=userstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
