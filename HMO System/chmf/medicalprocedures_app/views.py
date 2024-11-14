from django.shortcuts import render, redirect
from datetime import datetime
from .models import medicalprocedures, historymedicalprocedures
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
def medicalprocedures_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    procedureabbreviation = request.POST['procedureabbreviation'].strip().replace("  ", " ").title()
                    procedurename = request.POST['procedurename'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    procedurecode_max = medicalprocedures.objects.all().aggregate(Max('procedurecode'))
                    procedurecode_nextvalue = 1 if procedurecode_max['procedurecode__max'] == None else procedurecode_max['procedurecode__max'] + 1
                    if medicalprocedures.objects.annotate(uppercase_procedureabbreviation=Upper('procedureabbreviation'),uppercase_procedurename=Upper('procedurename')).filter(uppercase_procedureabbreviation=procedureabbreviation.upper(),uppercase_procedurename=procedurename.upper()):
                        messages.error(request, "The Record is already Exist .")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = medicalprocedures(procedurecode=procedurecode_nextvalue,procedureabbreviation=procedureabbreviation,procedurename=procedurename,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                medicalprocedureshistory_save(data, transactype)
                                return redirect('medicalprocedures_show')
                            else:
                                medicalprocedures_max = historymedicalprocedures.objects.all().aggregate(Max('recordnohist')) 
                                medicalprocedures_nextvalue = 1 if medicalprocedures_max['recordnohist__max'] == None else medicalprocedures_max['recordnohist__max']                                
                                Historymedicalprocedures_max = historymedicalprocedures.objects.all().aggregate(Max('recordnohist')) 
                                Historymedicalprocedures_nextvalue = 1 if Historymedicalprocedures_max['recordnohist__max'] == None else Historymedicalprocedures_max['recordnohist__max']                                
                                data = historymedicalprocedures(recordno=Historymedicalprocedures_nextvalue, procedurecode=medicalprocedures_nextvalue,procedureabbreviation=procedureabbreviation,procedurename=procedurename,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('medicalprocedures_show')
                        return render(request, 'medicalprocedures_show.html')              
                    return render(request, 'medicalprocedures_insert.html') 
                return render(request, 'medicalprocedures_insert.html')
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def medicalprocedures_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historymedicalprocedures = historymedicalprocedures.objects.get(recordnohist=pk)
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historymedicalprocedures.transactype = 'Disapprove'
                            Historymedicalprocedures.status = 'Disapprove'
                            Historymedicalprocedures.save()  
                            return redirect('medicalprocedures_show')           
                    else:
                        procedurecode = Historymedicalprocedures.procedurecode
                        procedureabbreviation = Historymedicalprocedures.procedureabbreviation
                        procedurename = Historymedicalprocedures.procedurename                   
                        remarks = Historymedicalprocedures.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = medicalprocedures(procedurecode=procedurecode,procedureabbreviation=procedureabbreviation,procedurename=procedurename,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historymedicalprocedures.status = 'Approve'
                        Historymedicalprocedures.transactype = 'Approve'
                        Historymedicalprocedures.save()                  
                    return redirect('medicalprocedures_show')               
                return render(request,'medicalprocedures_approval.html',{'Historymedicalprocedures': Historymedicalprocedures,'Medicalprocedures': Medicalprocedures})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def medicalprocedures_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historymedicalprocedures.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historymedicalprocedures.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historymedicalprocedures.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
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
                if search_query:Medicalprocedures = Medicalprocedures.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'medicalprocedures_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Medicalprocedures': Medicalprocedures
                
                
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
def medicalprocedures_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Medicalprocedures = medicalprocedures.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Medicalprocedures.procedureabbreviation = request.POST['procedureabbreviation'].strip().replace("  ", " ").title()
                    Medicalprocedures.procedurename = request.POST['procedurename'].strip().replace("  ", " ").title()
                    Medicalprocedures.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Medicalprocedures.transactby = userRoleid
                    Medicalprocedures.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Medicalprocedures.transactype = transactype
                            Medicalprocedures.save()  
                            medicalprocedureshistory_save(Medicalprocedures,transactype) 
                            return redirect('medicalprocedures_show')
                        else:
                            recordno = pk
                            procedurecode = Medicalprocedures.procedurecode
                            procedureabbreviation = request.POST['procedureabbreviation'].strip().replace("  ", " ").title()
                            procedurename = request.POST['procedurename'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historymedicalprocedures(recordno=recordno, procedurecode=procedurecode,procedureabbreviation=procedureabbreviation,procedurename=procedurename,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                           
                        return redirect('medicalprocedures_show')         
                    return redirect('medicalprocedures_show')   
                return render(request,'medicalprocedures_edit.html',{'Medicalprocedures': Medicalprocedures})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def medicalprocedures_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historymedicalprocedures = historymedicalprocedures.objects.get(recordnohist=pk)
                Medicalprocedures = medicalprocedures.objects.get(recordno=Historymedicalprocedures.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historymedicalprocedures.transactype = 'Disapprove'
                            Historymedicalprocedures.status = 'Disapprove'
                            Historymedicalprocedures.save()
                            return redirect('medicalprocedures_show')             
                    else:
                        Medicalprocedures.procedurecode = Historymedicalprocedures.procedurecode
                        Medicalprocedures.procedureabbreviation = Historymedicalprocedures.procedureabbreviation  
                        Medicalprocedures.procedurename = Historymedicalprocedures.procedurename                   
                        Medicalprocedures.remarks = Historymedicalprocedures.remarks
                        Medicalprocedures.transactby = userRoleid
                        Medicalprocedures.transactdate = datetime.now()                           
                        Medicalprocedures.transactype = transactype
                        Medicalprocedures.status = 'Active'
                        Medicalprocedures.save() 
                        Historymedicalprocedures.status = 'Approve'
                        Historymedicalprocedures.transactype = 'Approve'
                        Historymedicalprocedures.save()               
                    return redirect('medicalprocedures_show')
                return render(request,'medicalprocedures_edited.html',{'Historymedicalprocedures': Historymedicalprocedures,'Medicalprocedures': Medicalprocedures})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def medicalprocedures_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Medicalprocedures = medicalprocedures.objects.get(recordno=pk)

                transactype = 'Terminate'
                Medicalprocedures.transactby = userRoleid
                Medicalprocedures.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Medicalprocedures.transactby = userRoleid
                            Medicalprocedures.transactdate = datetime.now()
                            Medicalprocedures.transactype = transactype
                            Medicalprocedures.status = 'Deactive'
                            Medicalprocedures.save()
                            medicalprocedureshistory_save(Medicalprocedures, transactype)
                            return redirect('medicalprocedures_show') 
                                                                    
                    else:                       
                        Medicalprocedures.status = 'Deactive'
                        Medicalprocedures.save()
                        recordno = pk
                        procedurecode = Medicalprocedures.procedurecode
                        procedureabbreviation = Medicalprocedures.procedureabbreviation  
                        procedurename = Medicalprocedures.procedurename
                                         
                        
                        remarks = Medicalprocedures.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historymedicalprocedures(recordno=recordno, procedurecode=procedurecode,procedureabbreviation=procedureabbreviation,procedurename=procedurename,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('medicalprocedures_show')
                    return render(request, 'medicalprocedures_delete.html', {'Medicalprocedures': Medicalprocedures,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def medicalprocedures_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='medicalprocedures_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historymedicalprocedures = historymedicalprocedures.objects.get(recordnohist=pk)
                    Medicalprocedures = medicalprocedures.objects.get(recordno=Historymedicalprocedures.recordno)
                   
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historymedicalprocedures.transactype = 'Approve'
                                Historymedicalprocedures.status = 'Approve'
                                Historymedicalprocedures.save()  
                                Medicalprocedures.transactype = 'edit'
                                Medicalprocedures.status = 'Active'
                                Medicalprocedures.save()            
                        else:
                            Historymedicalprocedures.transactype = 'Terminate'
                            Historymedicalprocedures.status = 'Terminate'
                            Historymedicalprocedures.save()  
                            Medicalprocedures.transactype = 'Terminate'
                            Medicalprocedures.status = 'Terminate'
                            Medicalprocedures.save()                
                        return redirect('medicalprocedures_show')
                    return render(request,'medicalprocedures_terminate.html',{'Historymedicalprocedures': Historymedicalprocedures,'Medicalprocedures': Medicalprocedures})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def medicalprocedureshistory_save(obj, transactype):
    medicalprocedures = obj
    data = historymedicalprocedures(
        recordno=medicalprocedures.recordno,
        procedurecode = medicalprocedures.procedurecode,
        procedureabbreviation = medicalprocedures.procedureabbreviation,
        procedurename = medicalprocedures.procedurename,                   
        remarks = medicalprocedures.remarks,
        status=medicalprocedures.status,
        transactby=medicalprocedures.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
