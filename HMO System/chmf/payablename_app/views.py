from django.shortcuts import render, redirect
from datetime import datetime
from .models import payableName, historypayableName
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from provider_app.models import provider
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q

# Create your views here.
@login_required
def payablename_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST":
                    providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                    payablename = request.POST['payablename'].strip().replace("  ", " ").title()
                    tin = request.POST['tin'].strip().replace("  ", " ").title()
                    daystype = request.POST['daystype']
                    numberofdays = request.POST['numberofdays']
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    payablenameid_max = payableName.objects.all().aggregate(Max('payablenameid'))
                    payablenameid_nextvalue = 1 if payablenameid_max['payablenameid__max'] == None else payablenameid_max['payablenameid__max'] + 1
                    if payableName.objects.annotate(uppercase_payablename=Upper('payablename')).filter(uppercase_payablename=payablename.upper(),status="Inactive"):
                        messages.error(request, "The PayableName Name is already Exist Please View in Inactive List.")  
                    elif payableName.objects.annotate(uppercase_payablename=Upper('payablename')).filter(uppercase_payablename=payablename.upper(),status="Active"):
                        messages.error(request, "The PayableName Name is already Exist.")  
                   
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = payableName(tin=tin,remarks=remarks,payablenameid=payablenameid_nextvalue, providercode=providercode,payablename=payablename,daystype=daystype,numberofdays=numberofdays, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                payableNamehistory_save(data, transactype)
                                return redirect('payablename_show')
                            else:
                                Payablename_max = historypayableName.objects.all().aggregate(Max('recordnohist')) 
                                Payablename_nextvalue = 1 if Payablename_max['recordnohist__max'] == None else Payablename_max['recordnohist__max']
                                
                                recordnohist_max = historypayableName.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                
                                data = historypayableName(tin=tin,recordno=recordno_nextvalue, payablenameid=Payablename_nextvalue, providercode=providercode,payablename=payablename,daystype=daystype,numberofdays=numberofdays, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('payablename_show')
                        return render(request, 'payablename_insert.html')              
                    return render(request, 'payablename_insert.html',{'Provider': Provider})  
                return render(request, 'payablename_insert.html',{'Provider': Provider})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def payablename_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                HistorypayableName = historypayableName.objects.get(recordnohist=pk)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            HistorypayableName.transactype = 'Disapprove'
                            HistorypayableName.status = 'Disapprove'
                            HistorypayableName.save()  
                            return redirect('payablename_show')           
                    else:
                        payablenameid = HistorypayableName.payablenameid
                        providercode = HistorypayableName.providercode
                        payablename =HistorypayableName.payablename
                        tin =HistorypayableName.tin
                        daystype = HistorypayableName.daystype
                        numberofdays = HistorypayableName.numberofdays
                        remarks = HistorypayableName.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = payableName(tin=tin,payablenameid=payablenameid, providercode=providercode,payablename=payablename,daystype=daystype,numberofdays=numberofdays, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)    
                        data.save()                       
                        HistorypayableName.status = 'Approve'
                        HistorypayableName.transactype = 'Approve'
                        HistorypayableName.save()                  
                    return redirect('payablename_show')               
                return render(request,'payablename_approval.html',{'HistorypayableName': HistorypayableName,'Provider': Provider})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def payablename_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                PayableName = payableName.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historypayableName.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historypayableName.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historypayableName.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
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
                if search_query:PayableName = PayableName.filter( Q(payablename__icontains=search_query) )                                                                            
                return render(request, 'payablename_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'PayableName': PayableName
                
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
def payablename_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                PayableName = payableName.objects.get(recordno=pk)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    PayableName.providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                    PayableName.payablename = request.POST['payablename'].strip().replace("  ", " ").title()
                    PayableName.tin = request.POST['tin'].strip().replace("  ", " ").title()
                    PayableName.daystype = request.POST['daystype']
                    PayableName.numberofdays = request.POST['numberofdays']
                    PayableName.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    PayableName.transactby = userRoleid
                    PayableName.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            PayableName.transactype = transactype
                            PayableName.save()  
                            payableNamehistory_save(PayableName,transactype) 
                            return redirect('payablename_show')
                        else:
                            recordno = pk
                            payablenameid = PayableName.payablenameid
                            providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                            payablename = request.POST['payablename'].strip().replace("  ", " ").title()
                            tin = request.POST['tin'].strip().replace("  ", " ").title()
                            daystype = request.POST['daystype']
                            numberofdays = request.POST['numberofdays']
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historypayableName(tin=tin,recordno=recordno, payablenameid=payablenameid, providercode=providercode,payablename=payablename,daystype=daystype,numberofdays=numberofdays, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                            data.save()                       
                        
                           
                        return redirect('payablename_show')         
                    return redirect('payablename_show')   
                return render(request,'payablename_edit.html',{'PayableName': PayableName,'Provider': Provider})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def payablename_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historypayablename = historypayableName.objects.get(recordnohist=pk)
                PayableName = payableName.objects.get(recordno=Historypayablename.recordno)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historypayablename.transactype = 'Disapprove'
                            Historypayablename.status = 'Disapprove'
                            Historypayablename.save()
                            return redirect('payablename_show')             
                    else:
                        PayableName.payablenameid = Historypayablename.payablenameid
                        PayableName.providercode = Historypayablename.providercode
                        PayableName.payablename = Historypayablename.payablename
                        PayableName.tin = Historypayablename.tin
                        PayableName.daystype = Historypayablename.daystype
                        PayableName.numberofdays = Historypayablename.numberofdays
                        PayableName.remarks = Historypayablename.remarks
                      
                        PayableName.transactby = userRoleid
                        PayableName.transactdate = datetime.now()                           
                        PayableName.transactype = transactype
                        PayableName.status = 'Active'
                        PayableName.save() 
                        Historypayablename.status = 'Approve'
                        Historypayablename.transactype = 'Approve'
                        Historypayablename.save()               
                    return redirect('payablename_show')
                return render(request,'payablename_edited.html',{'Historypayablename': Historypayablename,'PayableName': PayableName,'Provider': Provider})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def payablename_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                PayableName = payableName.objects.get(recordno=pk)

                transactype = 'Terminate'
                PayableName.transactby = userRoleid
                PayableName.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            PayableName.transactby = userRoleid
                            PayableName.transactdate = datetime.now()
                            PayableName.transactype = transactype
                            PayableName.status = 'Deactive'
                            PayableName.save()
                            payableNamehistory_save(PayableName, transactype)
                            return redirect('payablename_show') 
                                                                    
                    else:                       
                        PayableName.status = 'Deactive'
                        PayableName.save()
                        recordno = pk
                        payablenameid = PayableName.payablenameid
                        providercode = PayableName.providercode  
                        payablename = PayableName.payablename
                        tin = PayableName.tin
                        daystype = PayableName.daystype
                        numberofdays = PayableName.numberofdays
                        remarks = PayableName.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historypayableName(tin=tin,recordno=recordno, payablenameid=payablenameid, providercode=providercode,payablename=payablename,daystype=daystype,numberofdays=numberofdays, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('payablename_show')
                    return render(request, 'payablename_delete.html', {'PayableName': PayableName,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def payablename_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='payablename_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historypayablename = historypayableName.objects.get(recordnohist=pk)
                    Payablename = payableName.objects.get(recordno=Historypayablename.recordno)
                    Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historypayablename.transactype = 'Approve'
                                Historypayablename.status = 'Approve'
                                Historypayablename.save()  
                                Payablename.transactype = 'edit'
                                Payablename.status = 'Active'
                                Payablename.save()            
                        else:
                            Historypayablename.transactype = 'Terminate'
                            Historypayablename.status = 'Terminate'
                            Historypayablename.save()  
                            Payablename.transactype = 'Terminate'
                            Payablename.status = 'Terminate'
                            Payablename.save()                
                        return redirect('payablename_show')
                    return render(request,'payablename_terminate.html',{'Historypayablename': Historypayablename,'Payablename': Payablename,'Provider': Provider})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def payableNamehistory_save(obj, transactype):
    payableName = obj
    data = historypayableName(
        recordno=payableName.recordno,
        payablenameid=payableName.payablenameid,
        providercode=payableName.providercode,
        payablename=payableName.payablename,
        tin=payableName.tin,
        daystype=payableName.daystype,
        numberofdays=payableName.numberofdays,
        remarks=payableName.remarks,
        status=payableName.status,
        transactby=payableName.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
