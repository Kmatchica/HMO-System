from django.shortcuts import render, redirect
from .models import provider, historyprovider
from category_app.models import category
from providerstatus_app.models import providerstatus
from datetime import datetime 
from django.db.models import Max
from datetime import datetime
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.
from django.db.models import Q


@login_required
def provider_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Category = category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove']) 
                if request.method == "POST":
                    categorycode = category.objects.get(categorycode=request.POST['categorycode'])
                    providername = request.POST['providername'].strip().replace("  ", " ").title()
                    tin = request.POST['tin']
                    address = request.POST['address'].strip().replace("  ", " ").title()
                    emailaddress = request.POST['emailaddress']
                    contactperson = request.POST['contactperson'].strip().replace("  ", " ").title()
                    landline = request.POST['landline']
                    mobilenumber = request.POST['mobilenumber']
                    providerstatuscode = providerstatus.objects.get(providerstatuscode=request.POST['providerstatuscode'])
                    accreditdate= request.POST['accreditdate']
                    suspensiondate= request.POST['suspensiondate']
                    disaccreditdate= request.POST['disaccreditdate']
                    reaccreditdate= request.POST['reaccreditdate']
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    locationcode_max = provider.objects.all().aggregate(Max('locationcode'))
                    locationcode_nextvalue = 1 if locationcode_max['locationcode__max'] == None else locationcode_max['locationcode__max'] + 1
                    providercode_max = provider.objects.all().aggregate(Max('providercode'))
                    providercode_nextvalue = 1 if providercode_max['providercode__max'] == None else providercode_max['providercode__max'] + 1
                    if provider.objects.annotate(uppercase_providername=Upper('providername')).filter(uppercase_providername=providername.upper(),status="Inactive"):
                        messages.error(request, "The Provider Name is already Exist Please View in Inactive List.")   
                    elif provider.objects.annotate(uppercase_providername=Upper('providername')).filter(uppercase_providername=providername.upper(),status="Active"):
                        messages.error(request, "The Provider Name is already Exist.")
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = provider(providerstatuscode=providerstatuscode,accreditdate=accreditdate,suspensiondate=suspensiondate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,providercode=providercode_nextvalue, categorycode=categorycode, providername=providername, tin=tin, address=address, locationcode=locationcode_nextvalue, emailaddress=emailaddress, contactperson=contactperson, landline=landline, mobilenumber=mobilenumber, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status)
                                data.save()
                                providerhistory_save(data, transactype)
                                return redirect('provider_show')
                            else:
                                Providercode_max = historyprovider.objects.all().aggregate(Max('recordnohist')) 
                                Providercode_nextvalue = 1 if Providercode_max['recordnohist__max'] == None else Providercode_max['recordnohist__max']                                
                                recordnohist_max = historyprovider.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                data = historyprovider(providerstatuscode=providerstatuscode,accreditdate=accreditdate,suspensiondate=suspensiondate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=recordno_nextvalue,providercode=Providercode_nextvalue, categorycode=categorycode, providername=providername, tin=tin, address=address, locationcode=locationcode_nextvalue, emailaddress=emailaddress, contactperson=contactperson, landline=landline, mobilenumber=mobilenumber, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactypes,status=status)
                                data.save()
                                return redirect('provider_show')
                        return redirect('provider_show')            
                    return render(request, 'provider_insert.html',{'userRoleid': userRoleid,'Category': Category,'Providerstatus': Providerstatus})  
                return render(request, 'provider_insert.html',{'userRoleid': userRoleid,'Category': Category,'Providerstatus': Providerstatus})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def provider_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyprovider = historyprovider.objects.get(recordnohist=pk)
                Category = category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyprovider.transactype = 'Disapprove'
                            Historyprovider.status = 'Disapprove'
                            Historyprovider.save()             
                    else:

                        locationcode= Historyprovider.locationcode
                        providercode = Historyprovider.providercode
                        categorycode = Historyprovider.categorycode
                        providername = Historyprovider.providername
                        tin = Historyprovider.tin
                        address = Historyprovider.address
                        emailaddress = Historyprovider.emailaddress
                        contactperson = Historyprovider.contactperson
                        landline = Historyprovider.landline
                        mobilenumber = Historyprovider.mobilenumber
                        providerstatuscode = Historyprovider.providerstatuscode
                        accreditdate= Historyprovider.accreditdate
                        suspensiondate= Historyprovider.suspensiondate
                        disaccreditdate= Historyprovider.disaccreditdate
                        reaccreditdate= Historyprovider.reaccreditdate
                        remarks = Historyprovider.remarks
                        
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='active'
                        data = provider(providerstatuscode=providerstatuscode,accreditdate=accreditdate,suspensiondate=suspensiondate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,providercode=providercode, categorycode=categorycode, providername=providername, tin=tin, address=address, locationcode=locationcode, emailaddress=emailaddress, contactperson=contactperson, landline=landline, mobilenumber=mobilenumber, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=status)
                        data.save()                       
                        Historyprovider.status = 'Approve'
                        Historyprovider.transactype = 'Approve'
                        Historyprovider.save()                  
                    return redirect('provider_show')               
                return render(request,'provider_approval.html',{'Historyprovider': Historyprovider,'Category': Category,'Providerstatus': Providerstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

@login_required
def provider_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'],status__in=['Active'])      
                historyupdate = historyprovider.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyprovider.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyprovider.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
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
                if search_query:Provider = Provider.filter( Q(providername__icontains=search_query) )                                                                            
                return render(request, 'provider_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,

                'Provider': Provider
                
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
def provider_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Category = category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Provider = provider.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)                    
                    Provider.categorycode = category.objects.get(categorycode=request.POST['categorycode'])
                    Provider.providername = request.POST['providername'].strip().replace("  ", " ").title()
                    Provider.tin = request.POST['tin']
                    Provider.address = request.POST['address'].strip().replace("  ", " ").title()
                    Provider.emailaddress = request.POST['emailaddress']
                    Provider.contactperson = request.POST['contactperson'].strip().replace("  ", " ").title()
                    Provider.landline = request.POST['landline']
                    Provider.mobilenumber = request.POST['mobilenumber']
                    Provider.providerstatuscode = providerstatus.objects.get(providerstatuscode=request.POST['providerstatuscode'])
                    Provider.accreditdate= request.POST['accreditdate']
                    Provider.suspensiondate= request.POST['suspensiondate']
                    Provider.disaccreditdate= request.POST['disaccreditdate']
                    Provider.reaccreditdate= request.POST['reaccreditdate']
                    Provider.remarks = request.POST['remarks']
                    Provider.transactby = userRoleid
                    Provider.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Provider.transactype = transactype
                            Provider.save()  
                            providerhistory_save(Provider,transactype) 
                            return redirect('provider_show')
                        else:
                            recordno = pk
                            providercode = Provider.providercode
                            categorycode = category.objects.get(categorycode=request.POST['categorycode'])
                            providername = request.POST['providername']
                            tin = request.POST['tin']
                            address = request.POST['address']
                            locationcode = Provider.locationcode
                            emailaddress = request.POST['emailaddress']
                            contactperson = request.POST['contactperson']
                            landline = request.POST['landline']
                            mobilenumber = request.POST['mobilenumber']
                            providerstatuscode = providerstatus.objects.get(providerstatuscode=request.POST['providerstatuscode'])
                            accreditdate= request.POST['accreditdate']
                            suspensiondate= request.POST['suspensiondate']
                            disaccreditdate= request.POST['disaccreditdate']
                            reaccreditdate= request.POST['reaccreditdate']
                            remarks = request.POST['remarks']
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyprovider(providerstatuscode=providerstatuscode,accreditdate=accreditdate,suspensiondate=suspensiondate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=recordno,providercode=providercode, categorycode=categorycode, providername=providername, tin=tin, address=address, locationcode=locationcode, emailaddress=emailaddress, contactperson=contactperson, landline=landline, mobilenumber=mobilenumber, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status) 
                            data.save()                       
                        return redirect('provider_show')         
                    return redirect('provider_show')   
                return render(request,'provider_edit.html',{'Category':Category, 'Provider':Provider, 'Providerstatus':Providerstatus})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def provider_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyprovider = historyprovider.objects.get(recordnohist=pk)
                Provider = provider.objects.get(recordno=Historyprovider.recordno)
                Category = category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
               
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyprovider.transactype = 'Disapprove'
                            Historyprovider.status = 'Disapprove'
                            Historyprovider.save()             
                    else:
                        Provider.providercode = Historyprovider.providercode
                        Provider.categorycode = Historyprovider.categorycode
                        Provider.providername = Historyprovider.providername
                        Provider.tin = Historyprovider.tin
                        Provider.address = Historyprovider.address
                        Provider.locationcode = Historyprovider.locationcode
                        Provider.emailaddress = Historyprovider.emailaddress
                        Provider.contactperson = Historyprovider.contactperson
                        Provider.landline = Historyprovider.landline
                        Provider.mobilenumber = Historyprovider.mobilenumber
                        Provider.providerstatuscode = Historyprovider.providerstatuscode
                        Provider.accreditdate= Historyprovider.accreditdate
                        Provider.suspensiondate= Historyprovider.suspensiondate
                        Provider.disaccreditdate= Historyprovider.disaccreditdate
                        Provider.reaccreditdate= Historyprovider.reaccreditdate
                        Provider.remarks = Historyprovider.remarks   
                        Provider.transactby = userRoleid
                        Provider.transactdate = datetime.now()                           
                        Provider.transactype = transactype
                        Provider.status = 'Active'
                        Provider.save() 
                        Historyprovider.status = 'Approve'
                        Historyprovider.transactype = 'Approve'
                        Historyprovider.save()               
                    return redirect('provider_show')
                return render(request,'provider_edited.html',{'Historyprovider': Historyprovider,'Provider': Provider,'Category': Category, 'Providerstatus':Providerstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     
@login_required
def provider_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Provider = provider.objects.get(recordno=pk)
                transactype = 'Terminate'
                Provider.transactby = userRoleid
                Provider.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Provider.transactby = userRoleid
                            Provider.transactdate = datetime.now()
                            Provider.transactype = transactype
                            Provider.status = 'Deactive'
                            Provider.save()
                            providerhistory_save(Provider, transactype)
                            return redirect('provider_show')                                             
                    else:                       
                        Provider.status = 'Deactive'
                        Provider.save()
                        recordno = pk
                        providercode = Provider.providercode
                        categorycode = Provider.categorycode
                        providername = Provider.providername
                        tin = Provider.tin
                        address = Provider.address
                        locationcode = Provider.locationcode
                        emailaddress = Provider.emailaddress
                        contactperson = Provider.contactperson
                        landline = Provider.landline
                        mobilenumber = Provider.mobilenumber
                        providerstatuscode = Provider.providerstatuscode
                        accreditdate= Provider.accreditdate
                        suspensiondate= Provider.suspensiondate
                        disaccreditdate= Provider.disaccreditdate
                        reaccreditdate= Provider.reaccreditdate
                        remarks = Provider.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyprovider(providerstatuscode=providerstatuscode,accreditdate=accreditdate,suspensiondate=suspensiondate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=recordno,providercode=providercode, categorycode=categorycode, providername=providername, tin=tin, address=address, locationcode=locationcode, emailaddress=emailaddress, contactperson=contactperson, landline=landline, mobilenumber=mobilenumber, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status) 
                        data.save()  
                        
                        return redirect('provider_show')
                    return render(request, 'provider_delete.html', {'Provider': Provider})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def provider_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='provider_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyprovider = historyprovider.objects.get(recordnohist=pk)
                Provider = provider.objects.get(recordno=Historyprovider.recordno)
          
                Category= category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                Providerstatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historyprovider.transactype = 'Approve'
                            Historyprovider.status = 'Approve'
                            Historyprovider.save()  
                            Provider.transactype = 'edit'
                            Provider.status = 'Active'
                            Provider.save()            
                    else:
                        Historyprovider.transactype = 'Terminate'
                        Historyprovider.status = 'Terminate'
                        Historyprovider.save()  
                        Provider.transactype = 'Terminate'
                        Provider.status = 'Terminate'
                        Provider.save()                
                    return redirect('provider_show')
                return render(request,'provider_terminate.html',{'Historyprovider': Historyprovider,'Provider': Provider,'Providerstatus': Providerstatus,'Category': Category})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

def providerhistory_save(obj, transactype):
    provider = obj
    data = historyprovider(
        recordno=provider.recordno,
        providercode=provider.providercode,
        categorycode=provider.categorycode,
        providername=provider.providername,
        tin=provider.tin,
        address=provider.address,
        locationcode=provider.locationcode,
        emailaddress=provider.emailaddress,
        contactperson=provider.contactperson,
        landline=provider.landline,
        mobilenumber=provider.mobilenumber,
        providerstatuscode = provider.providerstatuscode,
        accreditdate= provider.accreditdate,
        suspensiondate= provider.suspensiondate,
        disaccreditdate= provider.disaccreditdate,
        reaccreditdate= provider.reaccreditdate,
        remarks=provider.remarks,
        status=provider.status,
        transactby=provider.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
