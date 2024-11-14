from django.shortcuts import render, redirect
from datetime import datetime
from .models import userstatus, historyuserstatus
from django.db.models import Max
from department_app.models import department
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper



# Create your views here.
@login_required
def userstatus_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    userstatusname = request.POST['userstatusname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    userstatuscode_max = userstatus.objects.all().aggregate(Max('userstatuscode'))
                    userstatuscode_nextvalue = 1 if userstatuscode_max['userstatuscode__max'] == None else userstatuscode_max['userstatuscode__max'] + 1
                    if userstatus.objects.annotate(uppercase_userstatusname=Upper('userstatusname')).filter(uppercase_userstatusname=userstatusname.upper(),status="Inactive"):
                        messages.error(request, "The Userstatus Name is already Exist Please View in Inactive List.")
                    elif userstatus.objects.annotate(uppercase_userstatusname=Upper('userstatusname')).filter(uppercase_userstatusname=userstatusname.upper(),status="Active"):
                        messages.error(request, "The Userstatus Name is already Exist.")  
                     
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = userstatus(userstatuscode=userstatuscode_nextvalue, userstatusname=userstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                userstatushistory_save(data, transactype)
                                return redirect('userstatus_show')
                            else:
                                Userstatuscode_max = historyuserstatus.objects.all().aggregate(Max('recordnohist')) 
                                Userstatus_nextvalue = 1 if Userstatuscode_max['recordnohist__max'] == None else Userstatuscode_max['recordnohist__max']
                                
                                recordnohist_max = historyuserstatus.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                data = historyuserstatus(recordno =recordno_nextvalue, userstatuscode=Userstatus_nextvalue, userstatusname=userstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('userstatus_show')
                        return render(request, 'userstatus_insert.html')              
                    return render(request, 'userstatus_insert.html')  
                return render(request, 'userstatus_insert.html',{'userRoleid': userRoleid})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def userstatus_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyuserstatus = historyuserstatus.objects.get(recordnohist=pk)
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyuserstatus.transactype = 'Disapprove'
                            Historyuserstatus.status = 'Disapprove'
                            Historyuserstatus.save()  
                            return redirect('userstatus_show')           
                    else:
                        userstatuscode= Historyuserstatus.userstatuscode
                        userstatusname = Historyuserstatus.userstatusname
                        remarks = Historyuserstatus.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='active'
                        data = userstatus(userstatuscode=userstatuscode,userstatusname=userstatusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                        data.save()                       
                        Historyuserstatus.status = 'Approve'
                        Historyuserstatus.transactype = 'Approve'
                        Historyuserstatus.save()                  
                    return redirect('userstatus_show')               
                return render(request,'userstatus_approval.html',{'Historyuserstatus': Historyuserstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

@login_required   
def userstatus_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Userstatus = userstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyuserstatus.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyuserstatus.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyuserstatus.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
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
                return render(request, 'userstatus_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Userstatus': Userstatus
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

@login_required
def userstatus_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Userstatus = userstatus.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Userstatus.userstatusname = request.POST['userstatusname'].strip().replace("  ", " ").title()
                    Userstatus.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Userstatus.transactby = userRoleid
                    Userstatus.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Userstatus.transactype = transactype
                            Userstatus.save()  
                            userstatushistory_save(Userstatus,transactype) 
                            return redirect('userstatus_show')
                        else:
                            recordno = pk
                            userstatuscode = Userstatus.userstatuscode
                            userstatusname = request.POST['userstatusname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyuserstatus(recordno =recordno, userstatuscode=userstatuscode, userstatusname=userstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                            data.save()                       
                        
                           
                        return redirect('userstatus_show')         
                    return redirect('userstatus_show')   
                return render(request,'userstatus_edit.html',{'Userstatus': Userstatus})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def userstatus_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyuserstatus = historyuserstatus.objects.get(recordnohist=pk)
                Userstatus = userstatus.objects.get(recordno=Historyuserstatus.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyuserstatus.transactype = 'Disapprove'
                            Historyuserstatus.status = 'Disapprove'
                            Historyuserstatus.save()
                            return redirect('userstatus_show')             
                    else:
                        Userstatus.userstatuscode = Historyuserstatus.userstatuscode
                        Userstatus.userstatusname = Historyuserstatus.userstatusname
                        Userstatus.remarks = Historyuserstatus.remarks
                      
                        Userstatus.transactby = userRoleid
                        Userstatus.transactdate = datetime.now()                           
                        Userstatus.transactype = transactype
                        Userstatus.status = 'Active'
                        Userstatus.save() 
                        Historyuserstatus.status = 'Approve'
                        Historyuserstatus.transactype = 'Approve'
                        Historyuserstatus.save()               
                    return redirect('userstatus_show')
                return render(request,'userstatus_edited.html',{'Historyuserstatus': Historyuserstatus,'Userstatus': Userstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def userstatus_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Userstatus = userstatus.objects.get(recordno=pk)

                transactype = 'Terminate'
                Userstatus.transactby = userRoleid
                Userstatus.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Userstatus.transactby = userRoleid
                            Userstatus.transactdate = datetime.now()
                            Userstatus.transactype = transactype
                            Userstatus.status = 'Deactive'
                            Userstatus.save()
                            userstatushistory_save(Userstatus, transactype)
                            return redirect('userstatus_show') 
                                                                    
                    else:                       
                        Userstatus.status = 'Deactive'
                        Userstatus.save()
                        recordno = pk
                        userstatuscode = Userstatus.userstatuscode
                        userstatusname = Userstatus.userstatusname
                        remarks = Userstatus.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyuserstatus(recordno=recordno,userstatuscode=userstatuscode, userstatusname=userstatusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('userstatus_show')
                    return render(request, 'userstatus_delete.html', {'Userstatus': Userstatus,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def userstatus_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='userstatus_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyuserstatus = historyuserstatus.objects.get(recordnohist=pk)
                    Userstatus = userstatus.objects.get(recordno=Historyuserstatus.recordno)
                    
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyuserstatus.transactype = 'Approve'
                                Historyuserstatus.status = 'Approve'
                                Historyuserstatus.save()  
                                Userstatus.transactype = 'edit'
                                Userstatus.status = 'Active'
                                Userstatus.save()            
                        else:
                            Historyuserstatus.transactype = 'Terminate'
                            Historyuserstatus.status = 'Terminate'
                            Historyuserstatus.save()  
                            Userstatus.transactype = 'Terminate'
                            Userstatus.status = 'Terminate'
                            Userstatus.save()                
                        return redirect('userstatus_show')
                    return render(request,'userstatus_terminate.html',{'Historyuserstatus': Historyuserstatus,'Userstatus': Userstatus})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def userstatushistory_save(obj, transactype):
    userstatus = obj
    data = historyuserstatus(
        recordno=userstatus.recordno,
        userstatuscode=userstatus.userstatuscode,
        userstatusname=userstatus.userstatusname,
        remarks=userstatus.remarks,
        status=userstatus.status,
        transactby=userstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
