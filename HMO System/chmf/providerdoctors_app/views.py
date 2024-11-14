from django.shortcuts import render, redirect
from datetime import datetime
from .models import providerdoctors, historyproviderdoctors
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from provider_app.models import provider
from doctor_app.models import doctor
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q

# Create your views here.
@login_required
def providerdoctors_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST":
                    doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                    providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                    room = request.POST['room'].strip().replace("  ", " ").title()
                    scheduleday = request.POST['scheduleday'].strip().replace("  ", " ").title()
                    scheduletime = request.POST['scheduletime'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    if providerdoctors.objects.annotate(uppercase_room=Upper('room'),uppercase_scheduleday=Upper('scheduleday'),uppercase_scheduletime=Upper('scheduletime')).filter(uppercase_room=room.upper(),uppercase_scheduleday=scheduleday.upper(),uppercase_scheduletime=scheduletime.upper(),doctorcode=doctorcode,providercode=providercode):
                        messages.error(request, "The Record is already Exist .")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = providerdoctors(doctorcode=doctorcode,providercode=providercode,room=room,scheduleday=scheduleday,scheduletime=scheduletime,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status)
                                data.save()
                                providerdoctorshistory_save(data, transactype)
                                return redirect('providerdoctors_show')
                            else:
                                Historyproviderdoctors_max = historyproviderdoctors.objects.all().aggregate(Max('recordnohist')) 
                                Historyproviderdoctors_nextvalue = 1 if Historyproviderdoctors_max['recordnohist__max'] == None else Historyproviderdoctors_max['recordnohist__max']
                                
                                
                                data = historyproviderdoctors(recordno=Historyproviderdoctors_nextvalue, doctorcode=doctorcode,providercode=providercode,room=room,scheduleday=scheduleday,scheduletime=scheduletime,remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('providerdoctors_show')
                        return render(request, 'providerdoctors_insert.html')              
                    return render(request, 'providerdoctors_insert.html',{'Provider': Provider,'Doctor': Doctor})  
                return render(request, 'providerdoctors_insert.html',{'Provider': Provider,'Doctor': Doctor})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def providerdoctors_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyproviderdoctors = historyproviderdoctors.objects.get(recordnohist=pk)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyproviderdoctors.transactype = 'Disapprove'
                            Historyproviderdoctors.status = 'Disapprove'
                            Historyproviderdoctors.save()  
                            return redirect('providerdoctors_show')           
                    else:
                        doctorcode = Historyproviderdoctors.doctorcode
                        providercode = Historyproviderdoctors.providercode                   
                        room = Historyproviderdoctors.room
                        scheduleday = Historyproviderdoctors.scheduleday
                        scheduletime = Historyproviderdoctors.scheduletime
                        remarks = Historyproviderdoctors.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = providerdoctors(doctorcode=doctorcode,providercode=providercode,room=room,scheduleday=scheduleday,scheduletime=scheduletime,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historyproviderdoctors.status = 'Approve'
                        Historyproviderdoctors.transactype = 'Approve'
                        Historyproviderdoctors.save()                  
                    return redirect('providerdoctors_show')               
                return render(request,'providerdoctors_approval.html',{'Historyproviderdoctors': Historyproviderdoctors,'Provider': Provider,'Doctor': Doctor})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

@login_required   
def providerdoctors_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Providerdoctors = providerdoctors.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyproviderdoctors.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyproviderdoctors.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyproviderdoctors.objects.filter(transactype__in=['Forapproval'])
                
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])                
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
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
                if search_query:Providerdoctors = Providerdoctors.filter(Q(room__icontains=search_query) |Q(scheduleday__icontains=search_query) |Q(scheduletime__icontains=search_query) |Q(remarks__icontains=search_query) )                                                                            
                return render(request, 'providerdoctors_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Providerdoctors': Providerdoctors,
                'Provider': Provider,
                'Doctor': Doctor,
                ###############filter for search ###############
                # 'filter_status': filter_status,
                ###############filter for search ###############
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

@login_required
def providerdoctors_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Providerdoctors = providerdoctors.objects.get(recordno=pk)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Providerdoctors.doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                    Providerdoctors.providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                    Providerdoctors.room = request.POST['room'].strip().replace("  ", " ").title()
                    Providerdoctors.scheduleday = request.POST['scheduleday'].strip().replace("  ", " ").title()
                    Providerdoctors.scheduletime = request.POST['scheduletime'].strip().replace("  ", " ").title()
                    Providerdoctors.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Providerdoctors.transactby = userRoleid
                    Providerdoctors.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Providerdoctors.transactype = transactype
                            Providerdoctors.save()  
                            providerdoctorshistory_save(Providerdoctors,transactype) 
                            return redirect('providerdoctors_show')
                        else:
                            recordno = pk
                            doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                            providercode = provider.objects.get(providercode=request.POST['providercode'])                   
                            room = request.POST['room'].strip().replace("  ", " ").title()
                            scheduleday = request.POST['scheduleday'].strip().replace("  ", " ").title()
                            scheduletime = request.POST['scheduletime'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyproviderdoctors(recordno=recordno, doctorcode=doctorcode,providercode=providercode,room=room,scheduleday=scheduleday,scheduletime=scheduletime,remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                           
                        return redirect('providerdoctors_show')         
                    return redirect('providerdoctors_show')   
                return render(request,'providerdoctors_edit.html',{'Provider': Provider,'Doctor': Doctor,'Providerdoctors': Providerdoctors})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def providerdoctors_edited(request,pk):
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
                Historyproviderdoctors = historyproviderdoctors.objects.get(recordnohist=pk)
                Providerdoctors = providerdoctors.objects.get(recordno=Historyproviderdoctors.recordno)
                Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyproviderdoctors.transactype = 'Disapprove'
                            Historyproviderdoctors.status = 'Disapprove'
                            Historyproviderdoctors.save()
                            return redirect('providerdoctors_show')             
                    else:
                        Providerdoctors.doctorcode = Historyproviderdoctors.doctorcode
                        Providerdoctors.providercode = Historyproviderdoctors.providercode                   
                        Providerdoctors.room = Historyproviderdoctors.room
                        Providerdoctors.scheduleday = Historyproviderdoctors.scheduleday
                        Providerdoctors.scheduletime = Historyproviderdoctors.scheduletime
                        Providerdoctors.remarks = Historyproviderdoctors.remarks
                      
                        Providerdoctors.transactby = userRoleid
                        Providerdoctors.transactdate = datetime.now()                           
                        Providerdoctors.transactype = transactype
                        Providerdoctors.status = 'Active'
                        Providerdoctors.save() 
                        Historyproviderdoctors.status = 'Approve'
                        Historyproviderdoctors.transactype = 'Approve'
                        Historyproviderdoctors.save()               
                    return redirect('providerdoctors_show')
                return render(request,'providerdoctors_edited.html',{'Historyproviderdoctors': Historyproviderdoctors,'Providerdoctors': Providerdoctors,'Provider': Provider,'Doctor': Doctor})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def providerdoctors_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Providerdoctors = providerdoctors.objects.get(recordno=pk)

                transactype = 'Terminate'
                Providerdoctors.transactby = userRoleid
                Providerdoctors.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Providerdoctors.transactby = userRoleid
                            Providerdoctors.transactdate = datetime.now()
                            Providerdoctors.transactype = transactype
                            Providerdoctors.status = 'Deactive'
                            Providerdoctors.save()
                            providerdoctorshistory_save(Providerdoctors, transactype)
                            return redirect('providerdoctors_show') 
                                                                    
                    else:                       
                        Providerdoctors.status = 'Deactive'
                        Providerdoctors.save()
                        recordno = pk
                        doctorcode = Providerdoctors.doctorcode
                        providercode = Providerdoctors.providercode                   
                        room = Providerdoctors.room
                        scheduleday = Providerdoctors.scheduleday
                        scheduletime = Providerdoctors.scheduletime
                        remarks = Providerdoctors.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyproviderdoctors(recordno=recordno, doctorcode=doctorcode,providercode=providercode,room=room,scheduleday=scheduleday,scheduletime=scheduletime,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('providerdoctors_show')
                    return render(request, 'providerdoctors_delete.html', {'Providerdoctors': Providerdoctors,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def providerdoctors_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='providerdoctors_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyproviderdoctors = historyproviderdoctors.objects.get(recordnohist=pk)
                    Providerdoctors = providerdoctors.objects.get(recordno=Historyproviderdoctors.recordno)
                    Provider = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyproviderdoctors.transactype = 'Approve'
                                Historyproviderdoctors.status = 'Approve'
                                Historyproviderdoctors.save()  
                                Providerdoctors.transactype = 'edit'
                                Providerdoctors.status = 'Active'
                                Providerdoctors.save()            
                        else:
                            Historyproviderdoctors.transactype = 'Terminate'
                            Historyproviderdoctors.status = 'Terminate'
                            Historyproviderdoctors.save()  
                            Providerdoctors.transactype = 'Terminate'
                            Providerdoctors.status = 'Terminate'
                            Providerdoctors.save()                
                        return redirect('providerdoctors_show')
                    return render(request,'providerdoctors_terminate.html',{'Historyproviderdoctors': Historyproviderdoctors,'Providerdoctors': Providerdoctors,'Provider': Provider,'Doctor': Doctor})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def providerdoctorshistory_save(obj, transactype):
    providerdoctors = obj
    data = historyproviderdoctors(
        recordno=providerdoctors.recordno,
        doctorcode = providerdoctors.doctorcode,
        providercode = providerdoctors.providercode,                   
        room = providerdoctors.room,
        scheduleday = providerdoctors.scheduleday,
        scheduletime = providerdoctors.scheduletime,
        remarks = providerdoctors.remarks,
        status=providerdoctors.status,
        transactby=providerdoctors.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
