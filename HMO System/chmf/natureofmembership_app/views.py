from django.shortcuts import render, redirect
from datetime import datetime
from .models import NatureOfMembership, historynatureofmembership
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
        modulelist = moduleslist.objects.filter(moduleappname='natureofmembership_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False



@login_required
def natureofmembership_insert(request):
    if request.user.is_authenticated:
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid
                    if request.method == "POST":
                        natureofmembership = request.POST['natureofmembership']
                        Status = 'Active'
                        status = 'For Approval'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        transactype = 'add'
                        Transactypes = 'Forapproval'                                                 
                        natureofmembershipid_max = historynatureofmembership.objects.all().aggregate(Max('recordnohist'))
                        natureofmembershipid_nextvalue = 1 if natureofmembershipid_max['recordnohist__max'] == None else natureofmembershipid_max['recordnohist__max'] + 1
                        if has_permission(request.user, ['approver', 'Approver']):
                                data = NatureOfMembership(natureofmembershipid=natureofmembershipid_nextvalue,
                                                          natureofmembership=natureofmembership, 
                                                          transactby=transactby,transactdate=transactdate,
                                                          transactype=transactype,
                                                          status=Status)
                                data.save()
                                natureofmembershiphistory_save(data, transactype)
                                return redirect('natureofmembership_show')
                        else:                            
                            Historynatureofmembership_max = historynatureofmembership.objects.all().aggregate(Max('recordnohist')) 
                            Historynatureofmembership_nextvalue = 1 if Historynatureofmembership_max['recordnohist__max'] == None else Historynatureofmembership_max['recordnohist__max']                                
                            data = historynatureofmembership(recordno=Historynatureofmembership_nextvalue, 
                                                             natureofmembershipid=Historynatureofmembership_nextvalue, 
                                                             natureofmembership=natureofmembership,
                                                             transactby=transactby,
                                                             transactdate=transactdate, 
                                                             transactype=Transactypes,
                                                             status=status)
                            data.save()
                            return redirect('natureofmembership_show')              
                    return render(request, 'natureofmembership_insert.html')
        return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def natureofmembership_approval(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver', 'Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historynatureofmembership = historynatureofmembership.objects.get(recordnohist=pk)
            transactype = 'add'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historynatureofmembership.transactype = 'Disapprove'
                        Historynatureofmembership.status = 'Disapprove'
                        Historynatureofmembership.save()  
                        return redirect('natureofmembership_show')           
                else:
                    natureofmembershipid = Historynatureofmembership.natureofmembershipid
                    natureofmembership = Historynatureofmembership.natureofmembership                 
                    transactby = userRoleid
                    transactdate = datetime.now()                           
                    transactype = transactype
                    status='Active'
                    data = NatureOfMembership(natureofmembershipid=natureofmembershipid,natureofmembership=natureofmembership,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                    data.save()                       
                    Historynatureofmembership.status = 'Approve'
                    Historynatureofmembership.transactype = 'Approve'
                    Historynatureofmembership.save()                  
                return redirect('natureofmembership_show')               
            return render(request,'natureofmembership_approval.html',{'Historynatureofmembership': Historynatureofmembership})       
        return redirect('home') 
    return redirect('login')    


@login_required   
def natureofmembership_show(request):
    if request.user.is_authenticated:   
       if has_permission(request.user, ['LIST', 'List','View', 'SHOW']):
                Natureofmembership = NatureOfMembership.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historynatureofmembership.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historynatureofmembership.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historynatureofmembership.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='natureofmembership_app')  
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
                if search_query:Natureofmembership = Natureofmembership.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'natureofmembership_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Natureofmembership': Natureofmembership
                })
       return redirect('home')
    return redirect('login')

@login_required
def natureofmembership_edit(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['EDIT', 'Edit','UPDATE', 'Update']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Natureofmembership = NatureOfMembership.objects.get(recordno=pk)
            transactype = 'Edit'
            if request.method == 'POST':
                print(request.POST)
                Natureofmembership.natureofmembership = request.POST['natureofmembership'].strip().replace("  ", " ").title()
                Natureofmembership.transactby = userRoleid
                Natureofmembership.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):
                    Natureofmembership.transactype = transactype
                    Natureofmembership.save()  
                    natureofmembershiphistory_save(Natureofmembership,transactype) 
                    return redirect('natureofmembership_show')
                else:
                    recordno = pk
                    natureofmembershipid = Natureofmembership.natureofmembershipid
                    natureofmembership = request.POST['natureofmembership'].strip().replace("  ", " ").title()
                    status = 'For Update'
                    transactypes = 'Forupdate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historynatureofmembership(recordno=recordno, natureofmembershipid=natureofmembershipid,natureofmembership=natureofmembership, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                    data.save()                       
                return redirect('natureofmembership_show')          
            return render(request,'natureofmembership_edit.html',{'Natureofmembership': Natureofmembership}) 
        return redirect('home')       
    return redirect('login')          

@login_required
def natureofmembership_edited(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historynatureofmembership = historynatureofmembership.objects.get(recordnohist=pk)
            Natureofmembership = NatureOfMembership.objects.get(recordno=Historynatureofmembership.recordno)
            transactype = 'edit'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historynatureofmembership.transactype = 'Disapprove'
                        Historynatureofmembership.status = 'Disapprove'
                        Historynatureofmembership.save()
                        return redirect('natureofmembership_show')             
                else:
                    Natureofmembership.natureofmembershipid = Historynatureofmembership.natureofmembershipid
                    Natureofmembership.natureofmembership = Historynatureofmembership.natureofmembership                  
                    Natureofmembership.transactby = userRoleid
                    Natureofmembership.transactdate = datetime.now()                           
                    Natureofmembership.transactype = transactype
                    Natureofmembership.status = 'Active'
                    Natureofmembership.save() 
                    Historynatureofmembership.status = 'Approve'
                    Historynatureofmembership.transactype = 'Approve'
                    Historynatureofmembership.save()               
                return redirect('natureofmembership_show')
            return render(request,'natureofmembership_edited.html',{'Historynatureofmembership': Historynatureofmembership,'Natureofmembership': Natureofmembership})       
        return redirect('home')
    return redirect('login')     

@login_required
def natureofmembership_delete(request, pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['Delete','delete']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Natureofmembership = NatureOfMembership.objects.get(recordno=pk)
            transactype = 'Terminate'
            Natureofmembership.transactby = userRoleid
            Natureofmembership.transactdate = datetime.now()       
            if has_permission(request.user, ['approver','Approver']):
                if request.method == 'POST':
                    Natureofmembership.transactby = userRoleid
                    Natureofmembership.transactdate = datetime.now()
                    Natureofmembership.transactype = transactype
                    Natureofmembership.status = 'Deactive'
                    Natureofmembership.save()
                    natureofmembershiphistory_save(Natureofmembership, transactype)
                    return redirect('natureofmembership_show') 
                return render(request, 'natureofmembership_delete.html', {'Natureofmembership': Natureofmembership})                                             
            else:                       
                Natureofmembership.status = 'Deactive'
                Natureofmembership.save()
                recordno = pk
                natureofmembershipid = Natureofmembership.natureofmembershipid
                natureofmembership = Natureofmembership.natureofmembership  
                
                status = 'For Terminate'
                transactypes = 'Forterminate'
                transactby = userRoleid
                transactdate = datetime.now()
                data = historynatureofmembership(recordno=recordno, natureofmembershipid=natureofmembershipid,natureofmembership=natureofmembership, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                data.save() 
                return redirect('natureofmembership_show')
        return redirect('home')
    return redirect('login') 

@login_required
def natureofmembership_terminate(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historynatureofmembership = historynatureofmembership.objects.get(recordnohist=pk)
            Natureofmembership = NatureOfMembership.objects.get(recordno=Historynatureofmembership.recordno)
            if request.method == 'POST':
                if 'Disapprove' in request.POST:
                    Historynatureofmembership.transactype = 'Approve'
                    Historynatureofmembership.status = 'Approve'
                    Historynatureofmembership.save()  
                    Natureofmembership.transactype = 'edit'
                    Natureofmembership.status = 'Active'
                    Natureofmembership.save()            
                else:
                    Historynatureofmembership.transactype = 'Terminate'
                    Historynatureofmembership.status = 'Terminate'
                    Historynatureofmembership.save()  
                    Natureofmembership.transactype = 'Terminate'
                    Natureofmembership.status = 'Terminate'
                    Natureofmembership.save()                
                return redirect('natureofmembership_show')
            return render(request,'natureofmembership_terminate.html',{'Historynatureofmembership': Historynatureofmembership,'Natureofmembership': Natureofmembership})       
        return redirect('home')
    return redirect('login')  

def natureofmembershiphistory_save(obj, transactype):
    natureofmembership = obj
    data = historynatureofmembership(
        recordno=natureofmembership.recordno,
        natureofmembershipid = natureofmembership.natureofmembershipid,
        natureofmembership = natureofmembership.natureofmembership,              
        status=natureofmembership.status,
        transactby=natureofmembership.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
