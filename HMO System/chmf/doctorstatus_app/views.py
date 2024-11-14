from django.shortcuts import render, redirect
from datetime import datetime
from .models import doctorstatus, historydoctorstatus
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
def doctorstatus_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    doctorstatuscode_max = doctorstatus.objects.all().aggregate(Max('doctorstatuscode'))
                    doctorstatuscode_nextvalue = 1 if doctorstatuscode_max['doctorstatuscode__max'] == None else doctorstatuscode_max['doctorstatuscode__max'] + 1
                    if doctorstatus.objects.annotate(uppercase_statusname=Upper('statusname')).filter(uppercase_statusname=statusname.upper()):
                        messages.error(request, "The Record is already Exist .")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = doctorstatus(doctorstatuscode=doctorstatuscode_nextvalue,statusname=statusname,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                doctorstatushistory_save(data, transactype)
                                return redirect('doctorstatus_show')
                            else:
                                doctorstatus_max = historydoctorstatus.objects.all().aggregate(Max('recordnohist')) 
                                doctorstatus_nextvalue = 1 if doctorstatus_max['recordnohist__max'] == None else doctorstatus_max['recordnohist__max']                                
                                Historydoctorstatus_max = historydoctorstatus.objects.all().aggregate(Max('recordnohist')) 
                                Historydoctorstatus_nextvalue = 1 if Historydoctorstatus_max['recordnohist__max'] == None else Historydoctorstatus_max['recordnohist__max']                                
                                data = historydoctorstatus(recordno=Historydoctorstatus_nextvalue, doctorstatuscode=doctorstatus_nextvalue,statusname=statusname,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('doctorstatus_show')
                        return render(request, 'doctorstatus_show.html')              
                    return render(request, 'doctorstatus_insert.html') 
                return render(request, 'doctorstatus_insert.html')
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def doctorstatus_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctorstatus = historydoctorstatus.objects.get(recordnohist=pk)
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctorstatus.transactype = 'Disapprove'
                            Historydoctorstatus.status = 'Disapprove'
                            Historydoctorstatus.save()  
                            return redirect('doctorstatus_show')           
                    else:
                        doctorstatuscode = Historydoctorstatus.doctorstatuscode
                        statusname = Historydoctorstatus.statusname                   
                        remarks = Historydoctorstatus.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = doctorstatus(doctorstatuscode=doctorstatuscode,statusname=statusname,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historydoctorstatus.status = 'Approve'
                        Historydoctorstatus.transactype = 'Approve'
                        Historydoctorstatus.save()                  
                    return redirect('doctorstatus_show')               
                return render(request,'doctorstatus_approval.html',{'Historydoctorstatus': Historydoctorstatus,'Doctorstatus': Doctorstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def doctorstatus_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historydoctorstatus.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historydoctorstatus.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historydoctorstatus.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
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
                if search_query:Doctorstatus = Doctorstatus.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'doctorstatus_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Doctorstatus': Doctorstatus
                
                
                ###############filter for search ###############
                # 'filter_status': filter_status,
                # 'search_query': search_query
                ###############filter for search ###############
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

@login_required
def doctorstatus_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Doctorstatus = doctorstatus.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Doctorstatus.statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                    Doctorstatus.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Doctorstatus.transactby = userRoleid
                    Doctorstatus.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Doctorstatus.transactype = transactype
                            Doctorstatus.save()  
                            doctorstatushistory_save(Doctorstatus,transactype) 
                            return redirect('doctorstatus_show')
                        else:
                            recordno = pk
                            doctorstatuscode = Doctorstatus.doctorstatuscode
                            statusname = request.POST['statusname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historydoctorstatus(recordno=recordno, doctorstatuscode=doctorstatuscode,statusname=statusname,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                           
                        return redirect('doctorstatus_show')         
                    return redirect('doctorstatus_show')   
                return render(request,'doctorstatus_edit.html',{'Doctorstatus': Doctorstatus})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def doctorstatus_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctorstatus = historydoctorstatus.objects.get(recordnohist=pk)
                Doctorstatus = doctorstatus.objects.get(recordno=Historydoctorstatus.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctorstatus.transactype = 'Disapprove'
                            Historydoctorstatus.status = 'Disapprove'
                            Historydoctorstatus.save()
                            return redirect('doctorstatus_show')             
                    else:
                        Doctorstatus.doctorstatuscode = Historydoctorstatus.doctorstatuscode
                        Doctorstatus.statusname = Historydoctorstatus.statusname                   
                        Doctorstatus.remarks = Historydoctorstatus.remarks
                        Doctorstatus.transactby = userRoleid
                        Doctorstatus.transactdate = datetime.now()                           
                        Doctorstatus.transactype = transactype
                        Doctorstatus.status = 'Active'
                        Doctorstatus.save() 
                        Historydoctorstatus.status = 'Approve'
                        Historydoctorstatus.transactype = 'Approve'
                        Historydoctorstatus.save()               
                    return redirect('doctorstatus_show')
                return render(request,'doctorstatus_edited.html',{'Historydoctorstatus': Historydoctorstatus,'Doctorstatus': Doctorstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def doctorstatus_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Doctorstatus = doctorstatus.objects.get(recordno=pk)

                transactype = 'Terminate'
                Doctorstatus.transactby = userRoleid
                Doctorstatus.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Doctorstatus.transactby = userRoleid
                            Doctorstatus.transactdate = datetime.now()
                            Doctorstatus.transactype = transactype
                            Doctorstatus.status = 'Deactive'
                            Doctorstatus.save()
                            doctorstatushistory_save(Doctorstatus, transactype)
                            return redirect('doctorstatus_show') 
                                                                    
                    else:                       
                        Doctorstatus.status = 'Deactive'
                        Doctorstatus.save()
                        recordno = pk
                        doctorstatuscode = Doctorstatus.doctorstatuscode
                        statusname = Doctorstatus.statusname                   
                        
                        remarks = Doctorstatus.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historydoctorstatus(recordno=recordno, doctorstatuscode=doctorstatuscode,statusname=statusname,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('doctorstatus_show')
                    return render(request, 'doctorstatus_delete.html', {'Doctorstatus': Doctorstatus,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def doctorstatus_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='doctorstatus_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historydoctorstatus = historydoctorstatus.objects.get(recordnohist=pk)
                    Doctorstatus = doctorstatus.objects.get(recordno=Historydoctorstatus.recordno)
                   
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historydoctorstatus.transactype = 'Approve'
                                Historydoctorstatus.status = 'Approve'
                                Historydoctorstatus.save()  
                                Doctorstatus.transactype = 'edit'
                                Doctorstatus.status = 'Active'
                                Doctorstatus.save()            
                        else:
                            Historydoctorstatus.transactype = 'Terminate'
                            Historydoctorstatus.status = 'Terminate'
                            Historydoctorstatus.save()  
                            Doctorstatus.transactype = 'Terminate'
                            Doctorstatus.status = 'Terminate'
                            Doctorstatus.save()                
                        return redirect('doctorstatus_show')
                    return render(request,'doctorstatus_terminate.html',{'Historydoctorstatus': Historydoctorstatus,'Doctorstatus': Doctorstatus})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def doctorstatushistory_save(obj, transactype):
    doctorstatus = obj
    data = historydoctorstatus(
        recordno=doctorstatus.recordno,
        doctorstatuscode = doctorstatus.doctorstatuscode,
        statusname = doctorstatus.statusname,                   
        remarks = doctorstatus.remarks,
        status=doctorstatus.status,
        transactby=doctorstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
