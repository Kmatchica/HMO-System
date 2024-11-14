from django.shortcuts import render, redirect
from .models import specialization, historyspecialization
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from datetime import datetime 
from django.db.models import Max
from modulelist_app.models import moduleslist
from permission_app.models import permission
from access_app.models import access
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.



@login_required
def specialization_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    specializationname = request.POST['specializationname'].strip().replace("  ", " ").title()
                    specializationshortname = request.POST['specializationshortname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    specializationcode_max = specialization.objects.all().aggregate(Max('specializationcode'))
                    specializationcode_nextvalue = 1 if specializationcode_max['specializationcode__max'] == None else specializationcode_max['specializationcode__max'] + 1
                    if specialization.objects.annotate(uppercase_specializationname=Upper('specializationname')).filter(uppercase_specializationname=specializationname.upper(),status="Inactive"):
                        messages.error(request, "The Specialization Name Name is already Exist Please View in Inactive List.")  
                    elif specialization.objects.annotate(uppercase_specializationname=Upper('specializationname')).filter(uppercase_specializationname=specializationname.upper(),status="Active"):
                        messages.error(request, "The Specialization Name Name is already Exist.")  
                    
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = specialization(specializationcode=specializationcode_nextvalue,specializationname=specializationname, specializationshortname=specializationshortname, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status )
                                data.save()
                                specializationhistory_save(data, transactype)
                                return redirect('specialization_show')
                            else:
                                Specializationcode_max = historyspecialization.objects.all().aggregate(Max('recordnohist')) 
                                Specialization_nextvalue = 1 if Specializationcode_max['recordnohist__max'] == None else Specializationcode_max['recordnohist__max']
                                recordnohist_max = historyspecialization.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                data = historyspecialization(recordno =recordno_nextvalue,specializationcode=Specialization_nextvalue,specializationname=specializationname, specializationshortname=specializationshortname, remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactypes,status=status )                                
                                data.save()
                                return redirect('specialization_show')
                        return render(request, 'specialization_insert.html')              
                    return render(request, 'specialization_insert.html')  
                return render(request, 'specialization_insert.html',{'userRoleid': userRoleid})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')      

@login_required
def specialization_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyspecialization = historyspecialization.objects.get(recordnohist=pk)  
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyspecialization.transactype = 'Disapprove'
                            Historyspecialization.status = 'Disapprove'
                            Historyspecialization.save()  
                            return redirect('specialization_show')           
                    else:
                        specializationcode = Historyspecialization.specializationcode
                        specializationname = Historyspecialization.specializationname
                        specializationshortname = Historyspecialization.specializationshortname
                        remarks = Historyspecialization.remarks
                        
                       
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = specialization(specializationcode=specializationcode, specializationname=specializationname ,specializationshortname=specializationshortname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                        data.save()                       
                        Historyspecialization.status = 'Approve'
                        Historyspecialization.transactype = 'Approve'
                        Historyspecialization.save()                  
                    return redirect('specialization_show')               
                return render(request,'specialization_approval.html',{'Historyspecialization': Historyspecialization})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required
def specialization_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Specialization = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyspecialization.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyspecialization.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyspecialization.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
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
                return render(request, 'specialization_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Specialization': Specialization
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')


@login_required
def specialization_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Specialization = specialization.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Specialization.specializationname = request.POST['specializationname']
                    Specialization.specializationshortname = request.POST['specializationshortname']
                    Specialization.remarks = request.POST['remarks'] 
                    Specialization.transactby = userRoleid
                    Specialization.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Specialization.transactype = transactype
                            Specialization.save()  
                            specializationhistory_save(Specialization,transactype) 
                            return redirect('specialization_show')
                        else:
                            recordno = pk
                            specializationcode = Specialization.specializationcode
                            specializationname = request.POST['specializationname'].strip().replace("  ", " ").title()
                            specializationshortname = request.POST['specializationshortname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title() 
                            
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyspecialization(recordno=recordno, specializationcode=specializationcode, specializationname=specializationname,specializationshortname=specializationshortname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                            data.save()                       
                        
                           
                        return redirect('specialization_show')         
                    return redirect('specialization_show')   
                return render(request,'specialization_edit.html',{'Specialization': Specialization})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          


@login_required
def specialization_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyspecialization = historyspecialization.objects.get(recordnohist=pk)
                Specialization = specialization.objects.get(recordno=Historyspecialization.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyspecialization.transactype = 'Disapprove'
                            Historyspecialization.status = 'Disapprove'
                            Historyspecialization.save()
                            return redirect('specialization_show')             
                    else:
                        Specialization.specializationcode = Historyspecialization.specializationcode
                        Specialization.specializationname = Historyspecialization.specializationname
                        Specialization.specializationshortname = Historyspecialization.specializationshortname
                        Specialization.remarks = Historyspecialization.remarks
                        
                      
                        Specialization.transactby = userRoleid
                        Specialization.transactdate = datetime.now()                           
                        Specialization.transactype = transactype
                        Specialization.status = 'Active'
                        Specialization.save() 
                        Historyspecialization.status = 'Approve'
                        Historyspecialization.transactype = 'Approve'
                        Historyspecialization.save()               
                    return redirect('specialization_show')
                return render(request,'specialization_edited.html',{'Historyspecialization': Historyspecialization,'Specialization': Specialization})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def specialization_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Specialization = specialization.objects.get(recordno=pk)
                transactype = 'Terminate'
                Specialization.transactby = userRoleid
                Specialization.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Specialization.transactby = userRoleid
                            Specialization.transactdate = datetime.now()
                            Specialization.transactype = transactype
                            Specialization.status = 'Deactive'
                            Specialization.save()
                            specializationhistory_save(Specialization, transactype)
                            return redirect('specialization_show') 
                                                                    
                    else:                       
                        Specialization.status = 'Deactive'
                        Specialization.save()
                        recordno = pk
                        specializationcode = Specialization.specializationcode
                        specializationname = Specialization.specializationname
                        specializationshortname = Specialization.specializationshortname
                        remarks = Specialization.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyspecialization(recordno=recordno, specializationcode=specializationcode, specializationname=specializationname,specializationshortname=specializationshortname, remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)  
                        data.save() 
                        return redirect('specialization_show')
                    return render(request, 'specialization_delete.html', {'Specialization': Specialization,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def specialization_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='specialization_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyspecialization = historyspecialization.objects.get(recordnohist=pk)
                    Specialization = specialization.objects.get(recordno=Historyspecialization.recordno)
                    
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyspecialization.transactype = 'Approve'
                                Historyspecialization.status = 'Approve'
                                Historyspecialization.save()  
                                Specialization.transactype = 'edit'
                                Specialization.status = 'Active'
                                Specialization.save()            
                        else:
                            Historyspecialization.transactype = 'Terminate'
                            Historyspecialization.status = 'Terminate'
                            Historyspecialization.save()  
                            Specialization.transactype = 'Terminate'
                            Specialization.status = 'Terminate'
                            Specialization.save()                
                        return redirect('specialization_show')
                    return render(request,'specialization_terminate.html',{'Historyspecialization': Historyspecialization,'Specialization': Specialization})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def specializationhistory_save(obj, transactype):
    specialization = obj
    data = historyspecialization(

        recordno=specialization.recordno,
        
        specializationcode = specialization.specializationcode,
        specializationname = specialization.specializationname,
        specializationshortname = specialization.specializationshortname,
        
        remarks=specialization.remarks,
        status=specialization.status,
        transactby=specialization.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
