from django.shortcuts import render, redirect
from datetime import datetime
from .models import procedureprovider, historyprocedureprovider
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q
from medicalprocedures_app.models import medicalprocedures
from provider_app.models import provider
from medicalprocedures_app.models import medicalprocedures
# Create your views here.
@login_required
def procedureprovider_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST":
                    procedurecode = medicalprocedures.objects.get(procedurecode=request.POST['procedurecode'])
                    providercode = provider.objects.get(providercode=request.POST['providercode'])
                    amount = request.POST['amount'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    procedureprovidercode_max = historyprocedureprovider.objects.all().aggregate(Max('recordnohist')) 
                    procedureprovidercode_nextvalue = 1 if procedureprovidercode_max['recordnohist__max'] == None else procedureprovidercode_max['recordnohist__max']+1
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid  
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            data = procedureprovider(procedureprovidercode=procedureprovidercode_nextvalue,procedurecode=procedurecode,providercode=providercode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                            data.save()
                            procedureproviderhistory_save(data, transactype)
                            return redirect('procedureprovider_show')
                        else:
                            procedureprovider_max = historyprocedureprovider.objects.all().aggregate(Max('recordnohist')) 
                            procedureprovider_nextvalue = 1 if procedureprovider_max['recordnohist__max'] == None else procedureprovider_max['recordnohist__max']  +1                              
                            data = historyprocedureprovider(recordno=procedureprovider_nextvalue, procedureprovidercode=procedureprovider_nextvalue,procedurecode=procedurecode,providercode=providercode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                            data.save()
                            return redirect('procedureprovider_show')
                    return render(request, 'procedureprovider_show.html')                  
                return render(request, 'procedureprovider_insert.html',{'Provider':Provider,'Medicalprocedures':Medicalprocedures})
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def procedureprovider_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyprocedureprovider = historyprocedureprovider.objects.get(recordnohist=pk)
                Procedureprovider = procedureprovider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyprocedureprovider.transactype = 'Disapprove'
                            Historyprocedureprovider.status = 'Disapprove'
                            Historyprocedureprovider.save()  
                            return redirect('procedureprovider_show')           
                    else:
                        procedureprovidercode = Historyprocedureprovider.procedureprovidercode
                        procedurecode = Historyprocedureprovider.procedurecode
                        providercode = Historyprocedureprovider.providercode 
                        amount = Historyprocedureprovider.amount                 
                        remarks = Historyprocedureprovider.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = procedureprovider(procedureprovidercode=procedureprovidercode,procedurecode=procedurecode,providercode=providercode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historyprocedureprovider.status = 'Approve'
                        Historyprocedureprovider.transactype = 'Approve'
                        Historyprocedureprovider.save()                  
                    return redirect('procedureprovider_show')               
                return render(request,'procedureprovider_approval.html',{'Historyprocedureprovider': Historyprocedureprovider,'Procedureprovider': Procedureprovider,'Provider': Provider,'Medicalprocedures': Medicalprocedures})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def procedureprovider_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Procedureprovider = procedureprovider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyprocedureprovider.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyprocedureprovider.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyprocedureprovider.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
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
                if search_query:Procedureprovider = Procedureprovider.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'procedureprovider_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Procedureprovider': Procedureprovider
                
                
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
def procedureprovider_edit(request,pk):
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
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Procedureprovider = procedureprovider.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Procedureprovider.procedurecode = medicalprocedures.objects.get(procedurecode=request.POST['procedurecode'])
                    Procedureprovider.providercode = provider.objects.get(providercode=request.POST['providercode'])
                    Procedureprovider.amount = request.POST['amount'].strip().replace("  ", " ").title()
                    Procedureprovider.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Procedureprovider.transactby = userRoleid
                    Procedureprovider.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Procedureprovider.transactype = transactype
                            Procedureprovider.save()  
                            procedureproviderhistory_save(Procedureprovider,transactype) 
                            return redirect('procedureprovider_show')
                        else:
                            recordno = pk
                            procedureprovidercode = Procedureprovider.procedureprovidercode
                            procedurecode = medicalprocedures.objects.get(procedurecode=request.POST['procedurecode'])
                            providercode = provider.objects.get(providercode=request.POST['providercode'])
                            amount = request.POST['amount'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyprocedureprovider(recordno=recordno, procedureprovidercode=procedureprovidercode, procedurecode=procedurecode, providercode=providercode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                           
                        return redirect('procedureprovider_show')         
                    return redirect('procedureprovider_show')   
                return render(request,'procedureprovider_edit.html',{'Procedureprovider': Procedureprovider,'Provider': Provider,'Medicalprocedures': Medicalprocedures})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def procedureprovider_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyprocedureprovider = historyprocedureprovider.objects.get(recordnohist=pk)
                Procedureprovider = procedureprovider.objects.get(recordno=Historyprocedureprovider.recordno)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyprocedureprovider.transactype = 'Disapprove'
                            Historyprocedureprovider.status = 'Disapprove'
                            Historyprocedureprovider.save()
                            return redirect('procedureprovider_show')             
                    else:
                        Procedureprovider.procedureprovidercode = Historyprocedureprovider.procedureprovidercode
                        Procedureprovider.procedurecode = Historyprocedureprovider.procedurecode  
                        Procedureprovider.providercode = Historyprocedureprovider.providercode 
                        Procedureprovider.amount = Historyprocedureprovider.amount                     
                        Procedureprovider.remarks = Historyprocedureprovider.remarks
                        Procedureprovider.transactby = userRoleid
                        Procedureprovider.transactdate = datetime.now()                           
                        Procedureprovider.transactype = transactype
                        Procedureprovider.status = 'Active'
                        Procedureprovider.save() 
                        Historyprocedureprovider.status = 'Approve'
                        Historyprocedureprovider.transactype = 'Approve'
                        Historyprocedureprovider.save()               
                    return redirect('procedureprovider_show')
                return render(request,'procedureprovider_edited.html',{'Historyprocedureprovider': Historyprocedureprovider,'Procedureprovider': Procedureprovider,'Medicalprocedures': Medicalprocedures,'Provider': Provider})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def procedureprovider_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Procedureprovider = procedureprovider.objects.get(recordno=pk)

                transactype = 'Terminate'
                Procedureprovider.transactby = userRoleid
                Procedureprovider.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Procedureprovider.transactby = userRoleid
                            Procedureprovider.transactdate = datetime.now()
                            Procedureprovider.transactype = transactype
                            Procedureprovider.status = 'Deactive'
                            Procedureprovider.save()
                            procedureproviderhistory_save(Procedureprovider, transactype)
                            return redirect('procedureprovider_show') 
                                                                    
                    else:                       
                        Procedureprovider.status = 'Deactive'
                        Procedureprovider.save()
                        recordno = pk
                        procedureprovidercode = Procedureprovider.procedureprovidercode
                        procedurecode = Procedureprovider.procedurecode  
                        providercode = Procedureprovider.providercode
                        amount = Procedureprovider.amount                
                        
                        remarks = Procedureprovider.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyprocedureprovider(recordno=recordno, procedureprovidercode=procedureprovidercode,procedurecode=procedurecode,providercode=providercode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('procedureprovider_show')
                    return render(request, 'procedureprovider_delete.html', {'Procedureprovider': Procedureprovider,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def procedureprovider_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='procedureprovider_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyprocedureprovider = historyprocedureprovider.objects.get(recordnohist=pk)
                    Procedureprovider = procedureprovider.objects.get(recordno=Historyprocedureprovider.recordno)
                    Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    Medicalprocedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyprocedureprovider.transactype = 'Approve'
                                Historyprocedureprovider.status = 'Approve'
                                Historyprocedureprovider.save()  
                                Procedureprovider.transactype = 'edit'
                                Procedureprovider.status = 'Active'
                                Procedureprovider.save()            
                        else:
                            Historyprocedureprovider.transactype = 'Terminate'
                            Historyprocedureprovider.status = 'Terminate'
                            Historyprocedureprovider.save()  
                            Procedureprovider.transactype = 'Terminate'
                            Procedureprovider.status = 'Terminate'
                            Procedureprovider.save()                
                        return redirect('procedureprovider_show')
                    return render(request,'procedureprovider_terminate.html',{'Historyprocedureprovider': Historyprocedureprovider,'Procedureprovider': Procedureprovider,'Medicalprocedures': Medicalprocedures,'Provider': Provider})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def procedureproviderhistory_save(obj, transactype):
    procedureprovider = obj
    data = historyprocedureprovider(
        recordno=procedureprovider.recordno,
        procedureprovidercode = procedureprovider.procedureprovidercode,
        procedurecode = procedureprovider.procedurecode,
        providercode = procedureprovider.providercode,   
        amount = procedureprovider.amount,                
        remarks = procedureprovider.remarks,
        status=procedureprovider.status,
        transactby=procedureprovider.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
