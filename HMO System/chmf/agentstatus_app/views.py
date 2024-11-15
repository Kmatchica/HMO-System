from django.shortcuts import render, redirect
from datetime import datetime
from .models import agentstatus, historyagentstatus
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q
from django.apps import apps
from utils.utils import has_permission, get_app_config

['List','Edit', ]


@login_required
def agentstatus_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        app_name = get_app_config()
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT'], app_name):
            if request.method == "POST":
                agentstatusname = request.POST['agentstatusname'].strip().replace("  ", " ").title()
                remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                Status = 'Active'
                status = 'For Approval'
                transactby = userRoleid
                transactdate = datetime.now()
                transactype = 'add'
                Transactypes = 'Forapproval'
                agentstatuscode_max = historyagentstatus.objects.all().aggregate(Max('recordnohist')) 
                agentstatus_nextvalue = 1 if agentstatuscode_max['recordnohist__max'] == None else agentstatuscode_max['recordnohist__max']+ 1 
                if agentstatus.objects.annotate(uppercase_agentstatusname=Upper('agentstatusname')).filter(uppercase_agentstatusname=agentstatusname.upper(),status="Inactive"):
                    messages.error(request, "The Agentstatus Name is already Exist Please View in Inactive List.")  
                elif agentstatus.objects.annotate(uppercase_agentstatusname=Upper('agentstatusname')).filter(uppercase_agentstatusname=agentstatusname.upper(),status="Active"):
                    messages.error(request, "The Agentstatus Name is already Exist.")  
                else:
                    if has_permission(request.user, ['Approver','approver']):
                        data = agentstatus(agentstatusid=agentstatus_nextvalue, agentstatusname=agentstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                        data.save()
                        agentstatushistory_save(data, transactype)
                        return redirect('agentstatus_show')
                    else:
                        agentstatuscode_max = historyagentstatus.objects.all().aggregate(Max('recordnohist')) 
                        agentstatus_nextvalue = 1 if agentstatuscode_max['recordnohist__max'] == None else agentstatuscode_max['recordnohist__max']+ 1
                        recordnohist_max = historyagentstatus.objects.all().aggregate(Max('recordnohist')) 
                        recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+1
                        data = historyagentstatus(recordno=recordno_nextvalue, agentstatusid=agentstatus_nextvalue, agentstatusname=agentstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                        data.save()
                        return redirect('agentstatus_show')             
                return render(request, 'agentstatus_insert.html')  
            return render(request, 'agentstatus_insert.html',{'userRoleid': userRoleid})  
        return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def agentstatus_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver','Approver']):   
            Historyagentstatus = historyagentstatus.objects.get(recordnohist=pk)
            transactype = 'add'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historyagentstatus.transactype = 'Disapprove'
                        Historyagentstatus.status = 'Disapprove'
                        Historyagentstatus.save()  
                        return redirect('agentstatus_show')           
                else:
                    agentstatusid= Historyagentstatus.agentstatusid
                    agentstatusname = Historyagentstatus.agentstatusname
                    remarks = Historyagentstatus.remarks
                    transactby = userRoleid
                    transactdate = datetime.now()                           
                    transactype = transactype
                    status='Active'
                    data = agentstatus(agentstatusid=agentstatusid,agentstatusname=agentstatusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                    data.save()                       
                    Historyagentstatus.status = 'Approve'
                    Historyagentstatus.transactype = 'Approve'
                    Historyagentstatus.save()                  
                return redirect('agentstatus_show')               
            return render(request,'agentstatus_approval.html',{'Historyagentstatus': Historyagentstatus})       
        return redirect('home')
    return redirect('login')    

@login_required   
def agentstatus_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['LIST', 'List','View', 'SHOW'], 'agentstatus_app'):    
            Agentstatus = agentstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
            historyupdate = historyagentstatus.objects.filter(transactype__in=['Forupdate'])
            historyterminate = historyagentstatus.objects.filter(transactype__in=['Forterminate'])
            historyapproval= historyagentstatus.objects.filter(transactype__in=['Forapproval'])
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='agentstatus_app')  
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
                Agentstatus = Agentstatus.filter(
                    
                    Q(statusname__icontains=search_query) |
                    Q(remarks__icontains=search_query)
                )  
            return render(request, 'agentstatus_show.html', {
            'show_edit_button': show_edit_button,
            'show_delete_button': show_delete_button,
            'show_insert_button': show_insert_button,
            'show_view_button': show_view_button,
            'historyapproval': historyapproval,
            'historyupdate': historyupdate,
            'historyterminate': historyterminate,
            'Agentstatus': Agentstatus
            })
        else:
            return redirect('home')
    return redirect('login')

@login_required
def agentstatus_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['EDIT', 'Edit','UPDATE', 'Update']): 
            Agentstatus = agentstatus.objects.get(recordno=pk)
            transactype = 'Edit'
            if request.method == 'POST':
                print(request.POST)
                Agentstatus.agentstatusname = request.POST['agentstatusname'].strip().replace("  ", " ").title()
                Agentstatus.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                Agentstatus.transactby = userRoleid
                Agentstatus.transactdate = datetime.now()       
                if has_permission(request.user, ['approver','Approver']): 
                    Agentstatus.transactype = transactype
                    Agentstatus.save()  
                    agentstatushistory_save(Agentstatus,transactype) 
                    return redirect('agentstatus_show')
                else:
                    recordno = pk
                    agentstatusid = Agentstatus.agentstatusid
                    agentstatusname = request.POST['agentstatusname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    status = 'For Update'
                    transactypes = 'Forupdate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historyagentstatus(recordno=recordno, agentstatusid=agentstatusid, agentstatusname=agentstatusname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                    data.save()                        
                return redirect('agentstatus_show')           
            return render(request,'agentstatus_edit.html',{'Agentstatus': Agentstatus})       
        return redirect('home')
    return redirect('login')          

@login_required
def agentstatus_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver','Approver']):  
                Historyagentstatus = historyagentstatus.objects.get(recordnohist=pk)
                Agentstatus = agentstatus.objects.get(recordno=Historyagentstatus.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        Historyagentstatus.transactype = 'Disapprove'
                        Historyagentstatus.status = 'Disapprove'
                        Historyagentstatus.save()
                        return redirect('agentstatus_show')             
                    else:
                        Agentstatus.agentstatusid = Historyagentstatus.agentstatusid
                        Agentstatus.agentstatusname = Historyagentstatus.agentstatusname
                        Agentstatus.remarks = Historyagentstatus.remarks
                      
                        Agentstatus.transactby = userRoleid
                        Agentstatus.transactdate = datetime.now()                           
                        Agentstatus.transactype = transactype
                        Agentstatus.status = 'Active'
                        Agentstatus.save() 
                        Historyagentstatus.status = 'Approve'
                        Historyagentstatus.transactype = 'Approve'
                        Historyagentstatus.save()               
                    return redirect('agentstatus_show')
                return render(request,'agentstatus_edited.html',{'Historyagentstatus': Historyagentstatus,'Agentstatus': Agentstatus})              
        return redirect('home') 
    return redirect('login')     

@login_required
def agentstatus_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['DELETE', 'Delete','Remove', 'REMOVE']):  
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Agentstatus = agentstatus.objects.get(recordno=pk)
                transactype = 'Terminate'
                Agentstatus.transactby = userRoleid
                Agentstatus.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):  
                    if request.method == 'POST':
                        Agentstatus.transactby = userRoleid
                        Agentstatus.transactdate = datetime.now()
                        Agentstatus.transactype = transactype
                        Agentstatus.status = 'Deactive'
                        Agentstatus.save()
                        agentstatushistory_save(Agentstatus, transactype)
                        return redirect('agentstatus_show')                                             
                else:                       
                        Agentstatus.status = 'Deactive'
                        Agentstatus.save()
                        recordno = pk
                        agentstatusid = Agentstatus.agentstatusid
                        agentstatusname = Agentstatus.agentstatusname
                        remarks = Agentstatus.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyagentstatus(recordno=recordno,agentstatusid=agentstatusid, agentstatusname=agentstatusname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('agentstatus_show')
                return render(request, 'agentstatus_delete.html', {'Agentstatus': Agentstatus})
        return redirect('home')  
    return redirect('login') 

@login_required
def agentstatus_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            if has_permission(request.user, ['approver','Approver']):  
                Historyagentstatus = historyagentstatus.objects.get(recordnohist=pk)
                Agentstatus = agentstatus.objects.get(recordno=Historyagentstatus.recordno)
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        Historyagentstatus.transactype = 'Approve'
                        Historyagentstatus.status = 'Approve'
                        Historyagentstatus.save()  
                        Agentstatus.transactype = 'edit'
                        Agentstatus.status = 'Active'
                        Agentstatus.save()
                        return redirect('agentstatus_show')            
                    else:
                        Historyagentstatus.transactype = 'Terminate'
                        Historyagentstatus.status = 'Terminate'
                        Historyagentstatus.save()  
                        Agentstatus.transactype = 'Terminate'
                        Agentstatus.status = 'Terminate'
                        Agentstatus.save()                
                        return redirect('agentstatus_show')
                return render(request,'agentstatus_terminate.html',{'Historyagentstatus': Historyagentstatus,'Agentstatus': Agentstatus})       
            return redirect('home') 
    return redirect('login')  

def agentstatushistory_save(obj, transactype):
    agentstatus = obj
    data = historyagentstatus(
        recordno=agentstatus.recordno,
        agentstatusid=agentstatus.agentstatusid,
        agentstatusname=agentstatus.agentstatusname,
        remarks=agentstatus.remarks,
        status=agentstatus.status,
        transactby=agentstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
