from django.shortcuts import render, redirect
from datetime import datetime
from .models import Franchisestatus, historyfranchisestatus
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

def has_permission(user, access_names):
    if user.is_authenticated:
        userRoleid = user.roleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='Franchisestatus_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False


@login_required
def Franchisestatus_insert(request):
    if request.user.is_authenticated:
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid
                    if request.method == "POST":
                        franchisestatusname = request.POST['franchisestatusname'].strip().replace("  ", " ").title()
                        Status = 'Active'
                        status = 'For Approval'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        transactype = 'add'
                        Transactypes = 'Forapproval'                                                 
                        franchisestatusid_max = historyfranchisestatus.objects.all().aggregate(Max('recordnohist'))
                        franchisestatusid_nextvalue = 1 if franchisestatusid_max['recordnohist__max'] == None else franchisestatusid_max['recordnohist__max'] + 1
                        if Franchisestatus.objects.annotate(uppercase_franchisestatusname=Upper('franchisestatusname')).filter(uppercase_franchisestatusname=franchisestatusname.upper()):
                            messages.error(request, "Already Exist.") 
                        else:
                            if has_permission(request.user, ['approver', 'Approver']):
                                    data = Franchisestatus(franchisestatusid=franchisestatusid_nextvalue,
                                                            franchisestatusname=franchisestatusname, 
                                                            transactby=transactby,transactdate=transactdate,
                                                            transactype=transactype,
                                                            status=Status)
                                    data.save()
                                    Franchisestatushistory_save(data, transactype)
                                    return redirect('Franchisestatus_show')
                            else:                            
                                Historyfranchisestatus_max = historyfranchisestatus.objects.all().aggregate(Max('recordnohist')) 
                                Historyfranchisestatus_nextvalue = 1 if Historyfranchisestatus_max['recordnohist__max'] == None else Historyfranchisestatus_max['recordnohist__max']                                
                                data = historyfranchisestatus(recordno=Historyfranchisestatus_nextvalue, 
                                                                franchisestatusid=Historyfranchisestatus_nextvalue, 
                                                                franchisestatusname=franchisestatusname,
                                                                transactby=transactby,
                                                                transactdate=transactdate, 
                                                                transactype=Transactypes,
                                                                status=status)
                                data.save()
                                return redirect('Franchisestatus_show')              
                    return render(request, 'Franchisestatus_insert.html')
        return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def Franchisestatus_approval(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver', 'Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historyfranchisestatus = historyfranchisestatus.objects.get(recordnohist=pk)
            transactype = 'add'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historyfranchisestatus.transactype = 'Disapprove'
                        Historyfranchisestatus.status = 'Disapprove'
                        Historyfranchisestatus.save()  
                        return redirect('Franchisestatus_show')           
                else:
                    franchisestatusid = Historyfranchisestatus.franchisestatusid
                    franchisestatusname = Historyfranchisestatus.franchisestatusname                 
                    transactby = userRoleid
                    transactdate = datetime.now()                           
                    transactype = transactype
                    status='Active'
                    data = Franchisestatus(franchisestatusid=franchisestatusid,franchisestatusname=franchisestatusname,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                    data.save()                       
                    Historyfranchisestatus.status = 'Approve'
                    Historyfranchisestatus.transactype = 'Approve'
                    Historyfranchisestatus.save()                  
                return redirect('Franchisestatus_show')               
            return render(request,'Franchisestatus_approval.html',{'Historyfranchisestatus': Historyfranchisestatus})       
        return redirect('home') 
    return redirect('login')    


@login_required   
def Franchisestatus_show(request):
    if request.user.is_authenticated:   
       if has_permission(request.user, ['LIST', 'List','View', 'SHOW']):
                FranchiseStatus = Franchisestatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyfranchisestatus.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyfranchisestatus.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyfranchisestatus.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='Franchisestatus_app')  
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
                if search_query:FranchiseStatus = FranchiseStatus.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'Franchisestatus_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'FranchiseStatus': FranchiseStatus
                })
       return redirect('home')
    return redirect('login')

@login_required
def Franchisestatus_edit(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['EDIT', 'Edit','UPDATE', 'Update']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            FranchiseStatus = Franchisestatus.objects.get(recordno=pk)
            transactype = 'Edit'
            if request.method == 'POST':
                print(request.POST)
                FranchiseStatus.franchisestatusname = request.POST['franchisestatusname'].strip().replace("  ", " ").title()
                FranchiseStatus.transactby = userRoleid
                FranchiseStatus.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):
                    FranchiseStatus.transactype = transactype
                    FranchiseStatus.save()  
                    Franchisestatushistory_save(FranchiseStatus,transactype) 
                    return redirect('Franchisestatus_show')
                else:
                    recordno = pk
                    franchisestatusid = FranchiseStatus.franchisestatusid
                    franchisestatusname = request.POST['franchisestatusname'].strip().replace("  ", " ").title()
                    status = 'For Update'
                    transactypes = 'Forupdate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historyfranchisestatus(recordno=recordno, franchisestatusid=franchisestatusid,franchisestatusname=franchisestatusname, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                    data.save()                       
                return redirect('Franchisestatus_show')          
            return render(request,'Franchisestatus_edit.html',{'FranchiseStatus': FranchiseStatus}) 
        return redirect('home')       
    return redirect('login')          

@login_required
def Franchisestatus_edited(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historyfranchisestatus = historyfranchisestatus.objects.get(recordnohist=pk)
            FranchiseStatus = Franchisestatus.objects.get(recordno=Historyfranchisestatus.recordno)
            transactype = 'edit'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historyfranchisestatus.transactype = 'Disapprove'
                        Historyfranchisestatus.status = 'Disapprove'
                        Historyfranchisestatus.save()
                        return redirect('Franchisestatus_show')             
                else:
                    FranchiseStatus.franchisestatusid = Historyfranchisestatus.franchisestatusid
                    FranchiseStatus.franchisestatusname = Historyfranchisestatus.franchisestatusname                  
                    FranchiseStatus.transactby = userRoleid
                    FranchiseStatus.transactdate = datetime.now()                           
                    FranchiseStatus.transactype = transactype
                    FranchiseStatus.status = 'Active'
                    FranchiseStatus.save() 
                    Historyfranchisestatus.status = 'Approve'
                    Historyfranchisestatus.transactype = 'Approve'
                    Historyfranchisestatus.save()               
                return redirect('Franchisestatus_show')
            return render(request,'Franchisestatus_edited.html',{'Historyfranchisestatus': Historyfranchisestatus,'FranchiseStatus': FranchiseStatus})       
        return redirect('home')
    return redirect('login')     

@login_required
def Franchisestatus_delete(request, pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['Delete','delete']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            FranchiseStatus = Franchisestatus.objects.get(recordno=pk)
            transactype = 'Terminate'
            FranchiseStatus.transactby = userRoleid
            FranchiseStatus.transactdate = datetime.now()       
            if has_permission(request.user, ['approver','Approver']):
                if request.method == 'POST':
                    FranchiseStatus.transactby = userRoleid
                    FranchiseStatus.transactdate = datetime.now()
                    FranchiseStatus.transactype = transactype
                    FranchiseStatus.status = 'Deactive'
                    FranchiseStatus.save()
                    Franchisestatushistory_save(FranchiseStatus, transactype)
                    return redirect('Franchisestatus_show') 
                return render(request, 'Franchisestatus_delete.html', {'FranchiseStatus': FranchiseStatus})                                             
            else:                       
                FranchiseStatus.status = 'Deactive'
                FranchiseStatus.save()
                recordno = pk
                franchisestatusid = FranchiseStatus.franchisestatusid
                franchisestatusname = FranchiseStatus.franchisestatusname  
                
                status = 'For Terminate'
                transactypes = 'Forterminate'
                transactby = userRoleid
                transactdate = datetime.now()
                data = historyfranchisestatus(recordno=recordno, franchisestatusid=franchisestatusid,franchisestatusname=franchisestatusname, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                data.save() 
                return redirect('Franchisestatus_show')
        return redirect('home')
    return redirect('login') 

@login_required
def Franchisestatus_terminate(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historyfranchisestatus = historyfranchisestatus.objects.get(recordnohist=pk)
            FranchiseStatus = Franchisestatus.objects.get(recordno=Historyfranchisestatus.recordno)
            if request.method == 'POST':
                if 'Disapprove' in request.POST:
                    Historyfranchisestatus.transactype = 'Approve'
                    Historyfranchisestatus.status = 'Approve'
                    Historyfranchisestatus.save()  
                    FranchiseStatus.transactype = 'edit'
                    FranchiseStatus.status = 'Active'
                    FranchiseStatus.save()            
                else:
                    Historyfranchisestatus.transactype = 'Terminate'
                    Historyfranchisestatus.status = 'Terminate'
                    Historyfranchisestatus.save()  
                    FranchiseStatus.transactype = 'Terminate'
                    FranchiseStatus.status = 'Terminate'
                    FranchiseStatus.save()                
                return redirect('Franchisestatus_show')
            return render(request,'Franchisestatus_terminate.html',{'Historyfranchisestatus': Historyfranchisestatus,'FranchiseStatus': FranchiseStatus})       
        return redirect('home')
    return redirect('login')  

def Franchisestatushistory_save(obj, transactype):
    Franchisestatus = obj
    data = historyfranchisestatus(
        recordno=Franchisestatus.recordno,
        franchisestatusid = Franchisestatus.franchisestatusid,
        franchisestatusname = Franchisestatus.franchisestatusname,              
        status=Franchisestatus.status,
        transactby=Franchisestatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
