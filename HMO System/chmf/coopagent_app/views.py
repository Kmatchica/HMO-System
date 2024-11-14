from django.shortcuts import render, redirect
from .models import coopagent, historycoopagent
from datetime import datetime 
from django.db.models import Max
from department_app.models import department
from roles_app.models import roles
from permission_app.models import permission
from login_app.models import User
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from datetime import datetime




@login_required
def coopagent_insert(request):
    if request.user.is_authenticated:  
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                roless = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST": 
                    firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                    middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                    lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                    suffix = request.POST['suffix'].title()
                    civilstatuscode = request.POST['civilstatuscode']
                    birthdate= request.POST['birthdate']
                    email = request.POST['email']
                    departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                    roleid = roles.objects.get(roleid=request.POST['roleid'])
                    mobilenumber = request.POST['mobilenumber'].strip().replace("  ", " ").title()
                    address = request.POST['address'].strip().replace("  ", " ").title()
                    locationcode = request.POST['locationcode']
                    remarks = request.POST['remarks'].title()
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    status = 'Active'
                    Status = 'For approval'
                    agentid_max = coopagent.objects.all().aggregate(Max('agentid'))
                    agentid_nextvalue = 1 if agentid_max['agentid__max'] == None else agentid_max['agentid__max'] + 1
                    if coopagent.objects.annotate(uppercase_firstname=Upper('firstname'), uppercase_middlename=Upper('middlename'), uppercase_lastname=Upper('lastname')).filter(uppercase_firstname=firstname.upper(), uppercase_middlename=middlename.upper(), uppercase_lastname=lastname.upper(), birthdate=birthdate):
                        messages.error(request, "The User is already Exist.")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:    
                                data = coopagent(agentid=agentid_nextvalue, firstname=firstname, middlename=middlename, lastname=lastname, suffix=suffix, civilstatuscode=civilstatuscode, birthdate=birthdate, email=email, departmentcode=departmentcode, roleid=roleid, mobilenumber=mobilenumber, address=address,locationcode=locationcode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status)
                                data.save()
                                coopagenthistory_save(data, transactype)
                                return redirect('coopagent_show')
                            else:
                                recordnohist_max = historycoopagent.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                                agentid_max = historycoopagent.objects.all().aggregate(Max('recordnohist')) 
                                Accesscode_nextvalue = 1 if agentid_max['recordnohist__max'] == None else agentid_max['recordnohist__max']+ 1
                                
                                data = historycoopagent(recordno=recordno_nextvalue, agentid=Accesscode_nextvalue, firstname=firstname, middlename=middlename, lastname=lastname, suffix=suffix, civilstatuscode=civilstatuscode, birthdate=birthdate, email=email, departmentcode=departmentcode, roleid=roleid, mobilenumber=mobilenumber, address=address,locationcode=locationcode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactype, status=Status)
                                data.save()
                                return redirect('coopagent_show')
                    return render(request, 'coopagent_insert.html',{'Successful': 'Username already exists','departments':departments, 'roless':roless, 'permissions':permissions})
                return render(request, 'coopagent_insert.html',{'Successful': 'Username already exists','departments':departments, 'roless':roless, 'permissions':permissions})
            else:
             return redirect('home')        
        else:
         return redirect('home')
    return redirect('login')
        
@login_required
def coopagent_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historycoopagent = historycoopagent.objects.get(recordnohist=pk)
                departments = department.objects.exclude(transactype = 'delete')
                roless = roles.objects.exclude(transactype = 'delete')
                transactype = 'add'
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historycoopagent.transactype = 'Disapprove'
                            Historycoopagent.status = 'Disapprove'
                            Historycoopagent.save()             
                    else:
                        agentid = Historycoopagent.agentid
                        firstname = Historycoopagent.firstname
                        middlename = Historycoopagent.middlename
                        lastname = Historycoopagent.lastname
                        suffix = Historycoopagent.suffix
                        civilstatuscode = Historycoopagent.civilstatuscode
                        birthdate= Historycoopagent.birthdate
                        email = Historycoopagent.email
                        departmentcode = Historycoopagent.departmentcode
                        roleid = Historycoopagent.roleid
                        mobilenumber = Historycoopagent.mobilenumber
                        address = Historycoopagent.address
                        locationcode = Historycoopagent.locationcode
                        remarks = Historycoopagent.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = 'add'
                        status='Active'
                        data = coopagent(agentid=agentid, firstname=firstname, middlename=middlename, lastname=lastname, suffix=suffix, civilstatuscode=civilstatuscode, birthdate=birthdate, email=email, departmentcode=departmentcode, roleid=roleid, mobilenumber=mobilenumber, address=address,locationcode=locationcode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status)       
                        data.save()                       
                        Historycoopagent.status = 'Approve'
                        Historycoopagent.transactype = 'Approve'
                        Historycoopagent.save()                  
                    return redirect('coopagent_show')               
                return render(request,'coopagent_approval.html',{'Historycoopagent': Historycoopagent,'departments': departments,'roless': roless})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')        

@login_required   
def coopagent_show(request):
     if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','Show', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                historyupdate = historycoopagent.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historycoopagent.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historycoopagent.objects.filter(transactype__in=['Forapproval'])
                Coopagents = coopagent.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                edit_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['EDIT', 'Edit']).values_list('accesscode', flat=True))
                show_edit_button = any(permission.holder == 1 for permission in edit_permissions)
                delete_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['DELETE', 'Delete']).values_list('accesscode', flat=True))
                show_delete_button = any(permission.holder == 1 for permission in delete_permissions)
                insert_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['INSERT','Insert', 'ADD', 'Add']).values_list('accesscode', flat=True))
                show_insert_button = any(permission.holder == 1 for permission in insert_permissions)
                return render(request, 'coopagent_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'Coopagents': Coopagents,
                'Departments': Departments,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Roles': Roles
                })                
            else:
             return redirect('home')                
        else:
         return redirect('home')
     return redirect('login')
       
@login_required       
def coopagent_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Coopagent = coopagent.objects.get(recordno=pk)
                Departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'Edit'
                status='Active'
                if request.method == 'POST':
                    print(request.POST)
                    Coopagent.firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                    Coopagent.middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                    Coopagent.lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                    Coopagent.suffix = request.POST['suffix'].strip().replace("  ", " ").title()
                    Coopagent.civilstatuscode = request.POST['civilstatuscode']
                    Coopagent.birthdate = datetime.strptime(request.POST['birthdate'], '%Y-%m-%d')
                    Coopagent.email = request.POST['email']
                    Coopagent.departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                    Coopagent.roleid = roles.objects.get(roleid=request.POST['roleid'])
                    Coopagent.mobilenumber = request.POST['mobilenumber']
                    Coopagent.address = request.POST['address'].strip().replace("  ", " ").title()
                    Coopagent.locationcode = request.POST['locationcode']
                    Coopagent.remarks = request.POST['remarks']
                    Coopagent.transactby = userRoleid
                    Coopagent.transactdate = datetime.now()
                    Coopagent.transactype = 'edit'     
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Coopagent.transactype = transactype
                            Coopagent.save()  
                            coopagenthistory_save(Coopagent,transactype) 
                            return redirect('coopagent_show')
                        else:
                            recordno = pk
                            agentid=Coopagent.agentid
                            firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                            middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                            lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                            suffix = request.POST['suffix'].title()
                            civilstatuscode = request.POST['civilstatuscode']
                            birthdate= request.POST['birthdate']
                            email = request.POST['email']
                            departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                            roleid = roles.objects.get(roleid=request.POST['roleid'])
                            mobilenumber = request.POST['mobilenumber'].strip().replace("  ", " ").title()
                            address = request.POST['address'].strip().replace("  ", " ").title()
                            locationcode = request.POST['locationcode']
                            remarks = request.POST['remarks'].title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historycoopagent(recordno=recordno, agentid=agentid, firstname=firstname, middlename=middlename, lastname=lastname, suffix=suffix, civilstatuscode=civilstatuscode, birthdate=birthdate, email=email, departmentcode=departmentcode, roleid=roleid, mobilenumber=mobilenumber, address=address,locationcode=locationcode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes, status=status)      
                            data.save() 
                        return redirect('coopagent_show')         
                    return redirect('coopagent_show')   
                return render(request,'coopagent_edit.html',{'Coopagent': Coopagent,'Departments': Departments,'Roles': Roles})       
            else:
                return redirect('home')
        else:
            return redirect('home') 
    return redirect('login')     

@login_required
def coopagent_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'Edit'
                Historycoopagent = historycoopagent.objects.get(recordnohist=pk)
                Coopagent = coopagent.objects.get(recordno=Historycoopagent.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historycoopagent.transactype = 'Disapprove'
                            Historycoopagent.status = 'Disapprove'
                            Historycoopagent.save()             
                    else:
                        Coopagent.firstname = Historycoopagent.firstname
                        Coopagent.middlename = Historycoopagent.middlename
                        Coopagent.lastname =  Historycoopagent.lastname
                        Coopagent.suffix = Historycoopagent.suffix
                        Coopagent.civilstatuscode =  Historycoopagent.civilstatuscode
                        Coopagent.birthdate = Historycoopagent.birthdate
                        Coopagent.email = Historycoopagent.email
                        Coopagent.departmentcode = Historycoopagent.departmentcode
                        Coopagent.roleid = Historycoopagent.roleid
                        Coopagent.mobilenumber = Historycoopagent.mobilenumber
                        Coopagent.address = Historycoopagent.address
                        Coopagent.locationcode = Historycoopagent.locationcode
                        Coopagent.remarks = Historycoopagent.remarks
                        Coopagent.status = 'Active'
                        Coopagent.transactby = userRoleid
                        Coopagent.transactdate = datetime.now()                           
                        Coopagent.transactype = transactype
                        Coopagent.save() 
                        Historycoopagent.status = 'Approve'
                        Historycoopagent.transactype = 'Approve'
                        Historycoopagent.save()               
                    return redirect('coopagent_show')
                return render(request,'coopagent_edited.html',{'Historycoopagent': Historycoopagent,'Coopagent': Coopagent,'Departments': Departments,'Roles': Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login') 
            
@login_required
def coopagent_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Coopagent = coopagent.objects.get(recordno=pk)
                transactype = 'Terminate'
                Coopagent.transactby = userRoleid
                Coopagent.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Coopagent.transactby = userRoleid
                            Coopagent.transactdate = datetime.now()
                            Coopagent.transactype = transactype
                            Coopagent.status = 'Deactive'
                            Coopagent.save()
                            coopagenthistory_save(Coopagent, transactype)
                            return redirect('coopagent_show')                                             
                    else:
                        Coopagent.status = 'Deactive'
                        Coopagent.save()
                        recordno = pk
                        agentid = Coopagent.agentid
                        firstname = Coopagent.firstname
                        middlename = Coopagent.middlename
                        lastname =  Coopagent.lastname
                        suffix = Coopagent.suffix
                        civilstatuscode =  Coopagent.civilstatuscode
                        birthdate = Coopagent.birthdate
                        email = Coopagent.email
                        departmentcode = Coopagent.departmentcode
                        roleid = Coopagent.roleid
                        mobilenumber = Coopagent.mobilenumber
                        address = Coopagent.address
                        locationcode = Coopagent.locationcode
                        remarks = Coopagent.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historycoopagent(recordno=recordno, agentid=agentid, firstname=firstname, middlename=middlename, lastname=lastname, suffix=suffix, civilstatuscode=civilstatuscode, birthdate=birthdate, email=email, departmentcode=departmentcode, roleid=roleid, mobilenumber=mobilenumber, address=address,locationcode=locationcode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes, status=status)
                        data.save() 
                
                        return redirect('coopagent_show')
                    return render(request, 'coopagent_delete.html', {'Coopagent': Coopagent,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def coopagent_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='coopagent_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historycoopagent = historycoopagent.objects.get(recordnohist=pk)
                Coopagent = coopagent.objects.get(recordno=Historycoopagent.recordno)
                Departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historycoopagent.transactype = 'Approve'
                            Historycoopagent.status = 'Approve'
                            Historycoopagent.save()  
                            Coopagent.transactype = 'edit'
                            Coopagent.status = 'Active'
                            Coopagent.save()            
                    else:
                        Historycoopagent.transactype = 'Terminate'
                        Historycoopagent.status = 'Terminate'
                        Historycoopagent.save()  
                        Coopagent.transactype = 'Terminate'
                        Coopagent.status = 'Terminate'
                        Coopagent.save()                
                    return redirect('coopagent_show')
                return render(request,'coopagent_terminate.html',{'Historycoopagent': Historycoopagent,'Departments': Departments,'Roles': Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login') 

def coopagenthistory_save(obj, transactype):
    
    coopagent = obj
    data = historycoopagent(
        recordno=coopagent.recordno,
        agentid=coopagent.agentid,
        firstname=coopagent.firstname,
        middlename=coopagent.middlename,
        lastname=coopagent.lastname,
        suffix=coopagent.suffix,
        civilstatuscode=coopagent.civilstatuscode,
        birthdate=coopagent.birthdate,
        email=coopagent.email,
        departmentcode=coopagent.departmentcode,
        roleid=coopagent.roleid,
        mobilenumber=coopagent.mobilenumber,
        address=coopagent.address,
        locationcode=coopagent.locationcode,
        remarks=coopagent.remarks,
        status=coopagent.status,
        transactby=coopagent.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
