from django.shortcuts import render, redirect
from datetime import datetime
from .models import doctorroomfee, historydoctorroomfee
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q
from doctor_app.models import doctor
from doctorroomfee_app.models import doctorroomfee
from roomtype_app.models import roomtype
# Create your views here.
@login_required
def doctorroomfee_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST":
                    doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                    roomcode = roomtype.objects.get(roomcode=request.POST['roomcode'])
                    amount = request.POST['amount'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    doctorroomfeecode_max = historydoctorroomfee.objects.all().aggregate(Max('recordnohist')) 
                    doctorroomfeecode_nextvalue = 1 if doctorroomfeecode_max['recordnohist__max'] == None else doctorroomfeecode_max['recordnohist__max']+1
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid  
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            data = doctorroomfee(doctorroomfeecode=doctorroomfeecode_nextvalue,doctorcode=doctorcode,roomcode=roomcode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                            data.save()
                            doctorroomfeehistory_save(data, transactype)
                            return redirect('doctorroomfee_show')
                        else:
                            doctorroomfee_max = historydoctorroomfee.objects.all().aggregate(Max('recordnohist')) 
                            doctorroomfee_nextvalue = 1 if doctorroomfee_max['recordnohist__max'] == None else doctorroomfee_max['recordnohist__max']  +1                              
                            data = historydoctorroomfee(recordno=doctorroomfee_nextvalue, doctorroomfeecode=doctorroomfee_nextvalue,doctorcode=doctorcode,roomcode=roomcode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                            data.save()
                            return redirect('doctorroomfee_show')
                    return render(request, 'doctorroomfee_show.html')                  
                return render(request, 'doctorroomfee_insert.html',{'Roomtype':Roomtype,'Doctor':Doctor})
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def doctorroomfee_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctorroomfee = historydoctorroomfee.objects.get(recordnohist=pk)
                Doctorroomfee = doctorroomfee.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctorroomfee.transactype = 'Disapprove'
                            Historydoctorroomfee.status = 'Disapprove'
                            Historydoctorroomfee.save()  
                            return redirect('doctorroomfee_show')           
                    else:
                        doctorroomfeecode = Historydoctorroomfee.doctorroomfeecode
                        doctorcode = Historydoctorroomfee.doctorcode
                        roomcode = Historydoctorroomfee.roomcode 
                        amount = Historydoctorroomfee.amount                 
                        remarks = Historydoctorroomfee.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = doctorroomfee(doctorroomfeecode=doctorroomfeecode,doctorcode=doctorcode,roomcode=roomcode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historydoctorroomfee.status = 'Approve'
                        Historydoctorroomfee.transactype = 'Approve'
                        Historydoctorroomfee.save()                  
                    return redirect('doctorroomfee_show')               
                return render(request,'doctorroomfee_approval.html',{'Historydoctorroomfee': Historydoctorroomfee,'Doctorroomfee': Doctorroomfee,'Doctor': Doctor,'Roomtype': Roomtype})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def doctorroomfee_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Doctorroomfee = doctorroomfee.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historydoctorroomfee.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historydoctorroomfee.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historydoctorroomfee.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
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
                return render(request, 'doctorroomfee_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Doctor': Doctor,
                'Roomtype': Roomtype,
                'Doctorroomfee': Doctorroomfee
                
                
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
def doctorroomfee_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctorroomfee = doctorroomfee.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Doctorroomfee.doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                    Doctorroomfee.roomcode = roomtype.objects.get(roomcode=request.POST['roomcode'])
                    Doctorroomfee.amount = request.POST['amount'].strip().replace("  ", " ").title()
                    Doctorroomfee.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Doctorroomfee.transactby = userRoleid
                    Doctorroomfee.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Doctorroomfee.transactype = transactype
                            Doctorroomfee.save()  
                            doctorroomfeehistory_save(Doctorroomfee,transactype) 
                            return redirect('doctorroomfee_show')
                        else:
                            recordno = pk
                            doctorroomfeecode = Doctorroomfee.doctorroomfeecode
                            doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
                            roomcode = roomtype.objects.get(roomcode=request.POST['roomcode'])
                            amount = request.POST['amount'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historydoctorroomfee(recordno=recordno, doctorroomfeecode=doctorroomfeecode, doctorcode=doctorcode, roomcode=roomcode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                           
                        return redirect('doctorroomfee_show')         
                    return redirect('doctorroomfee_show')   
                return render(request,'doctorroomfee_edit.html',{'Doctor': Doctor,'Roomtype': Roomtype,'Doctorroomfee': Doctorroomfee})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def doctorroomfee_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctorroomfee = historydoctorroomfee.objects.get(recordnohist=pk)
                Doctorroomfee = doctorroomfee.objects.get(recordno=Historydoctorroomfee.recordno)
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctorroomfee.transactype = 'Disapprove'
                            Historydoctorroomfee.status = 'Disapprove'
                            Historydoctorroomfee.save()
                            return redirect('doctorroomfee_show')             
                    else:
                        Doctorroomfee.doctorroomfeecode = Historydoctorroomfee.doctorroomfeecode
                        Doctorroomfee.doctorcode = Historydoctorroomfee.doctorcode  
                        Doctorroomfee.roomcode = Historydoctorroomfee.roomcode 
                        Doctorroomfee.amount = Historydoctorroomfee.amount                     
                        Doctorroomfee.remarks = Historydoctorroomfee.remarks
                        Doctorroomfee.transactby = userRoleid
                        Doctorroomfee.transactdate = datetime.now()                           
                        Doctorroomfee.transactype = transactype
                        Doctorroomfee.status = 'Active'
                        Doctorroomfee.save() 
                        Historydoctorroomfee.status = 'Approve'
                        Historydoctorroomfee.transactype = 'Approve'
                        Historydoctorroomfee.save()               
                    return redirect('doctorroomfee_show')
                return render(request,'doctorroomfee_edited.html',{'Historydoctorroomfee': Historydoctorroomfee,'Doctorroomfee': Doctorroomfee,'Doctor': Doctor,'Roomtype': Roomtype})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def doctorroomfee_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Doctorroomfee = doctorroomfee.objects.get(recordno=pk)

                transactype = 'Terminate'
                Doctorroomfee.transactby = userRoleid
                Doctorroomfee.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Doctorroomfee.transactby = userRoleid
                            Doctorroomfee.transactdate = datetime.now()
                            Doctorroomfee.transactype = transactype
                            Doctorroomfee.status = 'Deactive'
                            Doctorroomfee.save()
                            doctorroomfeehistory_save(Doctorroomfee, transactype)
                            return redirect('doctorroomfee_show') 
                                                                    
                    else:                       
                        Doctorroomfee.status = 'Deactive'
                        Doctorroomfee.save()
                        recordno = pk
                        doctorroomfeecode = Doctorroomfee.doctorroomfeecode
                        doctorcode = Doctorroomfee.doctorcode  
                        roomcode = Doctorroomfee.roomcode
                        amount = Doctorroomfee.amount                
                        remarks = Doctorroomfee.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historydoctorroomfee(recordno=recordno, doctorroomfeecode=doctorroomfeecode,doctorcode=doctorcode,roomcode=roomcode,amount=amount,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('doctorroomfee_show')
                    return render(request, 'doctorroomfee_delete.html', {'Doctorroomfee': Doctorroomfee,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def doctorroomfee_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='doctorroomfee_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historydoctorroomfee = historydoctorroomfee.objects.get(recordnohist=pk)
                    Doctorroomfee = doctorroomfee.objects.get(recordno=Historydoctorroomfee.recordno)
                    Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    Roomtype = roomtype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historydoctorroomfee.transactype = 'Approve'
                                Historydoctorroomfee.status = 'Approve'
                                Historydoctorroomfee.save()  
                                Doctorroomfee.transactype = 'edit'
                                Doctorroomfee.status = 'Active'
                                Doctorroomfee.save()            
                        else:
                            Historydoctorroomfee.transactype = 'Terminate'
                            Historydoctorroomfee.status = 'Terminate'
                            Historydoctorroomfee.save()  
                            Doctorroomfee.transactype = 'Terminate'
                            Doctorroomfee.status = 'Terminate'
                            Doctorroomfee.save()                
                        return redirect('doctorroomfee_show')
                    return render(request,'doctorroomfee_terminate.html',{'Roomtype': Roomtype,'Doctor': Doctor,'Doctorroomfee': Doctorroomfee,'Historydoctorroomfee': Historydoctorroomfee})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def doctorroomfeehistory_save(obj, transactype):
    doctorroomfee = obj
    data = historydoctorroomfee(
        recordno=doctorroomfee.recordno,
        doctorroomfeecode = doctorroomfee.doctorroomfeecode,
        doctorcode = doctorroomfee.doctorcode,
        roomcode = doctorroomfee.roomcode,   
        amount = doctorroomfee.amount,                
        remarks = doctorroomfee.remarks,
        status=doctorroomfee.status,
        transactby=doctorroomfee.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
