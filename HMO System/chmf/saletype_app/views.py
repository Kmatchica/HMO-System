from django.shortcuts import render, redirect
from datetime import datetime
from .models import saletype, historysaletype
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
    """Check if the user has the required permissions."""
    if user.is_authenticated:
        userRoleid = user.roleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='saletype_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False

@login_required
def saletype_insert(request):
    if request.user.is_authenticated:
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                if request.method == "POST":
                    salestypename = request.POST['salestypename'].strip().replace("  ", " ").title()
                    salestypeshortname = request.POST['salestypeshortname'].strip().replace("  ", " ").title()
                    commissionpercent = request.POST['commissionpercent']
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    salestypeid_max = historysaletype.objects.all().aggregate(Max('recordnohist')) 
                    salestypeid_nextvalue = 1 if salestypeid_max['recordnohist__max'] == None else salestypeid_max['recordnohist__max'] + 1          
                    if saletype.objects.annotate(uppercase_salestypename=Upper('salestypename')).filter(uppercase_salestypename=salestypename.upper()):
                        messages.error(request, "The Sale Type Name is already Exist.") 
                    else:
                        if has_permission(request.user, ['approver', 'Approver']):
                                data = saletype(salestypeid=salestypeid_nextvalue,salestypename=salestypename,salestypeshortname=salestypeshortname,commissionpercent=commissionpercent,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=Status)
                                data.save()
                                saletypehistory_save(data, transactype)
                                return redirect('saletype_show')
                        else:
                                salestypeid_max = historysaletype.objects.all().aggregate(Max('recordnohist')) 
                                salestypeid_nextvalue = 1 if salestypeid_max['recordnohist__max'] == None else salestypeid_max['recordnohist__max'] + 1
                                recordnohist_max = historysaletype.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max'] + 1
                                data = historysaletype(recordno= recordno_nextvalue,
                                                       salestypeid=salestypeid_nextvalue,
                                                       salestypename=salestypename,
                                                       salestypeshortname=salestypeshortname,
                                                       commissionpercent=commissionpercent,
                                                       remarks=remarks,
                                                       transactby=transactby,
                                                       transactdate=transactdate,
                                                       transactype=Transactype, 
                                                       status=status)
                                data.save()
                        return redirect('saletype_show')    
                    return render(request, 'saletype_insert.html')  
                return render(request, 'saletype_insert.html')  
        return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def saletype_approval(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver', 'Approver']): 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Historysaletype = historysaletype.objects.get(recordnohist=pk)
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historysaletype.transactype = 'Disapprove'
                            Historysaletype.status = 'Disapprove'
                            Historysaletype.save()
                    else:
                        salestypeid = Historysaletype.salestypeid
                        salestypename = Historysaletype.salestypename
                        salestypeshortname = Historysaletype.salestypeshortname
                        commissionpercent = Historysaletype.commissionpercent
                        remarks = Historysaletype.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = saletype(salestypeid=salestypeid,
                                      salestypename=salestypename,
                                      salestypeshortname=salestypeshortname,
                                      commissionpercent=commissionpercent,
                                      remarks=remarks,
                                      transactby=transactby,
                                      transactdate=transactdate,
                                      transactype=transactype, 
                                      status=status)
                        data.save()                       
                        Historysaletype.status = 'Approve'
                        Historysaletype.transactype = 'Approve'
                        Historysaletype.save()
                        saletypehistory_save(data, transactype)                  
                    return redirect('saletype_show')               
                return render(request,'saletype_approval.html',{'Historysaletype': Historysaletype})       
        return redirect('home') 
    return redirect('login')    


@login_required
def saletype_show(request):
    if request.user.is_authenticated:   
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                Saletype = saletype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove']).order_by('-transactdate')
                historyupdate = historysaletype.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historysaletype.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historysaletype.objects.filter(transactype__in=['Forapproval'])
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

                return render(request, 'saletype_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'Saletype': Saletype,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate})
        return redirect('home') 
    return redirect('home') 
                
       
@login_required
def saletype_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                Saletype = saletype.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Saletype.salestypename = request.POST['salestypename'].strip().replace("  ", " ").title()
                    Saletype.salestypeshortname = request.POST['salestypeshortname'].strip().replace("  ", " ").title()
                    Saletype.commissionpercent = request.POST['commissionpercent']
                    Saletype.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Saletype.transactby = userRoleid
                    Saletype.transactdate = datetime.now()       
                    if has_permission(request.user, ['approver', 'Approver']):
                        Saletype.transactype = transactype
                        Saletype.save()  
                        saletypehistory_save(Saletype,transactype) 
                        return redirect('saletype_show')
                    else:
                        recordno = pk
                        salestypeid = Saletype.salestypeid
                        salestypename = request.POST['salestypename'].strip().replace("  ", " ").title()
                        salestypeshortname = request.POST['salestypeshortname'].strip().replace("  ", " ").title()
                        commissionpercent = request.POST['commissionpercent']
                        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                        status = 'For Update'
                        transactypes = 'Forupdate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historysaletype(recordno=recordno,
                                               salestypeid=salestypeid,
                                               salestypename=salestypename,
                                               salestypeshortname=salestypeshortname,
                                               commissionpercent=commissionpercent,
                                               remarks=remarks,
                                               status=status,
                                               transactby=transactby,
                                               transactdate=transactdate,
                                               transactype=transactypes)
                        data.save() 
                        return redirect('saletype_show')           
                return render(request,'saletype_edit.html',{'Saletype': Saletype})       
        return redirect('home')
    return redirect('login')  

@login_required
def saletype_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver', 'Approver']):
                Historysaletype = historysaletype.objects.get(recordnohist=pk)
                Saletype = saletype.objects.get(recordno=Historysaletype.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                            Saletype.transactype = 'Disapprove'
                            Saletype.status = 'Disapprove'
                            Saletype.save()             
                    else:
                        Saletype.salestypename = Historysaletype.salestypename
                        Saletype.salestypeshortname = Historysaletype.salestypeshortname
                        Saletype.commissionpercent = Historysaletype.commissionpercent
                        Saletype.remarks = Historysaletype.remarks
                        Saletype.transactby = userRoleid
                        Saletype.transactdate = datetime.now()                           
                        Saletype.transactype = transactype
                        Saletype.status = 'Active'
                        Saletype.save() 
                        Historysaletype.status = 'Approve'
                        Historysaletype.transactype = 'Approve'
                        Historysaletype.save()               
                    return redirect('saletype_show')
                return render(request,'saletype_edited.html',{'Historysaletype': Historysaletype,'Saletype': Saletype})         
        return redirect('home')   
    return redirect('login')     


@login_required
def saletype_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['DELETE', 'Delete','Remove', 'REMOVE']):
                Saletype = saletype.objects.get(recordno=pk)
                transactype = 'Terminate'
                Saletype.transactby = userRoleid
                Saletype.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):
                    if request.method == 'POST':
                        Saletype.transactby = userRoleid
                        Saletype.transactdate = datetime.now()
                        Saletype.transactype = transactype
                        Saletype.status = 'Deactive'
                        Saletype.save()
                        saletypehistory_save(Saletype, transactype)
                        return redirect('saletype_show') 
                    return render(request, 'saletype_delete.html', {'Saletype': Saletype})                                           
                else:
                        Saletype.status = 'Deactive'
                        Saletype.save()
                        recordno = pk
                        salestypeid = Saletype.salestypeid
                        salestypename = Saletype.salestypename
                        salestypeshortname = Saletype.salestypeshortname
                        commissionpercent = Saletype.commissionpercent
                        remarks = Saletype.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historysaletype(recordno=recordno,salestypeid=salestypeid,salestypename=salestypename,salestypeshortname=salestypeshortname,commissionpercent=commissionpercent,remarks=remarks,status=status,transactby=transactby,transactdate=transactdate,transactype=transactypes)
                        data.save() 
                        saletypehistory_save(data, transactype)
                        return redirect('saletype_show')                   
    return redirect('login') 

@login_required
def saletype_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver', 'Approver']): 
                Historysaletype = historysaletype.objects.get(recordnohist=pk)
                Saletype = saletype.objects.get(recordno=Historysaletype.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historysaletype.transactype = 'Approve'
                            Historysaletype.status = 'Approve'
                            Historysaletype.save()  
                            Saletype.transactype = 'edit'
                            Saletype.status = 'Active'
                            Saletype.save()            
                    else:
                        Historysaletype.transactype = 'Terminate'
                        Historysaletype.status = 'Terminate'
                        Historysaletype.save()  
                        Saletype.transactype = 'Terminate'
                        Saletype.status = 'Terminate'
                        Saletype.save()                
                    return redirect('saletype_show')
                return render(request,'saletype_terminate.html',{'Saletype': Saletype,'Historysaletype': Historysaletype})       
        else:
         return redirect('home')
    return redirect('login')  

 

def saletypehistory_save(obj, transactype):
    saletype = obj
    data = historysaletype(
        recordno=saletype.recordno,
        salestypeid=saletype.salestypeid,
        salestypename=saletype.salestypename,
        salestypeshortname=saletype.salestypeshortname,
        commissionpercent=saletype.commissionpercent,
        remarks=saletype.remarks,
        status=saletype.status,
        transactby=saletype.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()

