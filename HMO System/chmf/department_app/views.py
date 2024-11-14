from django.shortcuts import render, redirect
from datetime import datetime
from .models import department, historydepartment
from django.db.models import Max
from department_app.models import department
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
def department_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    departmentname = request.POST['departmentname'].strip().replace("  ", " ").title()
                    departmentshortname = request.POST['departmentshortname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    departmentcode_max = department.objects.all().aggregate(Max('departmentcode'))
                    departmentcode_nextvalue = 1 if departmentcode_max['departmentcode__max'] == None else departmentcode_max['departmentcode__max'] + 1
                    if department.objects.annotate(uppercase_departmentname=Upper('departmentname')).filter(uppercase_departmentname=departmentname.upper(),status="Inactive"):
                        messages.error(request, "The Departmentname is already Exist Please View in Inactive List.")   
                    elif department.objects.annotate(uppercase_departmentname=Upper('departmentname')).filter(uppercase_departmentname=departmentname.upper(),status="Active"):
                        messages.error(request, "The Departmentname is already Exist.")
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = department(departmentcode=departmentcode_nextvalue, departmentname=departmentname, departmentshortname=departmentshortname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                                data.save()
                                departmenthistory_save(data, transactype)
                                return redirect('department_show')
                            else:
                                Departmentcode_max = historydepartment.objects.all().aggregate(Max('recordnohist')) 
                                Department_nextvalue = 1 if Departmentcode_max['recordnohist__max'] == None else Departmentcode_max['recordnohist__max']+ 1
                                
                                recordnohist_max = historydepartment.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                                data = historydepartment(recordno=recordno_nextvalue,departmentcode=Department_nextvalue, departmentname=departmentname, departmentshortname=departmentshortname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                                data.save()
                                return redirect('department_show')
                        return render(request, 'department_insert.html')              
                    return render(request, 'department_insert.html')  
                return render(request, 'department_insert.html',{'userRoleid': userRoleid})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  

@login_required
def department_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Department = historydepartment.objects.get(recordnohist=pk)
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Department.transactype = 'Disapprove'
                            Department.status = 'Disapprove'
                            Department.save()             
                    else:
                        departmentcode = Department.departmentcode
                        departmentname = Department.departmentname
                        departmentshortname= Department.departmentshortname
                        remarks = Department.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='active'
                        data = department(departmentcode=departmentcode, departmentname=departmentname, departmentshortname=departmentshortname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                        data.save()                       
                        Department.status = 'Approve'
                        Department.transactype = 'Approve'
                        Department.save()                  
                    return redirect('department_show')               
                return render(request,'department_approval.html',{'Department': Department})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

@login_required   
def department_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Department = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historydepartment.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historydepartment.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historydepartment.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='department_app')  
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
                 # filter_status = request.GET.get('filter_status')
                search_query = request.GET.get('search_query')
                if search_query:Department = Department.filter(Q(departmentname__icontains=search_query))                                                                           
                return render(request, 'department_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'Department': Department,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate
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
def department_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Department = department.objects.get(recordno=pk)
                transactype = 'Edit'
                status='Active'
                if request.method == 'POST':
                    print(request.POST)
                    Department.departmentname = request.POST['departmentname'].strip().replace("  ", " ").title()
                    Department.departmentshortname = request.POST['departmentshortname'].strip().replace("  ", " ").title()
                    Department.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Department.transactby = userRoleid
                    Department.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='department_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Department.transactype = transactype
                            Department.save()  
                            departmenthistory_save(Department,transactype) 
                            return redirect('department_show')
                        else:
                            recordno = pk
                            departmentcode = Department.departmentcode
                            departmentname = request.POST['departmentname'].strip().replace("  ", " ").title()
                            departmentshortname = request.POST['departmentshortname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historydepartment(recordno=recordno,departmentcode=departmentcode, departmentname=departmentname, departmentshortname=departmentshortname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                            data.save()                       
                        
                           
                        return redirect('department_show')         
                    return redirect('department_show')   
                return render(request,'department_edit.html',{'Department': Department})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def access_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydepartment = historydepartment.objects.get(recordnohist=pk)
                Department = department.objects.get(recordno=Historydepartment.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydepartment.transactype = 'Disapprove'
                            Historydepartment.status = 'Disapprove'
                            Historydepartment.save()             
                    else:
                        Department.departmentcode = Historydepartment.departmentcode
                        Department.departmentname = Historydepartment.departmentname
                        Department.departmentshortname = Historydepartment.departmentshortname
                        Department.remarks = Historydepartment.remarks
                       
                        Department.transactby = userRoleid
                        Department.transactdate = datetime.now()                           
                        Department.transactype = transactype
                        Department.status = 'Active'
                        Department.save() 
                        Historydepartment.status = 'Approve'
                        Historydepartment.transactype = 'Approve'
                        Historydepartment.save()               
                    return redirect('department_show')
                return render(request,'department_edited.html',{'Historydepartment': Historydepartment,'Department': Department})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def department_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Department = department.objects.get(recordno=pk)

                transactype = 'Terminate'
                Department.transactby = userRoleid
                Department.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='department_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Department.transactby = userRoleid
                            Department.transactdate = datetime.now()
                            Department.transactype = transactype
                            Department.status = 'Deactive'
                            Department.save()
                            departmenthistory_save(Department, transactype)
                            return redirect('department_show')                                             
                    else:                       
                        Department.status = 'Deactive'
                        Department.save()
                        recordno = pk
                        departmentcode = Department.departmentcode
                        departmentname = Department.departmentname
                        departmentshortname = Department.departmentshortname
                        remarks = Department.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historydepartment(recordno=recordno,departmentcode=departmentcode, departmentname=departmentname, departmentshortname=departmentshortname , remarks=remarks,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('department_show')
                    return render(request, 'department_delete.html', {'Department': Department,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def department_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='department_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydepartment = historydepartment.objects.get(recordnohist=pk)
                Department = department.objects.get(recordno=Historydepartment.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historydepartment.transactype = 'Approve'
                            Historydepartment.status = 'Approve'
                            Historydepartment.save()  
                            Department.transactype = 'edit'
                            Department.status = 'Active'
                            Department.save()            
                    else:
                        Historydepartment.transactype = 'Terminate'
                        Historydepartment.status = 'Terminate'
                        Historydepartment.save()  
                        Department.transactype = 'Terminate'
                        Department.status = 'Terminate'
                        Department.save()                
                    return redirect('department_show')
                return render(request,'department_terminate.html',{'Historydepartment': Historydepartment,'Department': Department})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

def departmenthistory_save(obj, transactype):
    department = obj
    data = historydepartment(
        recordno=department.recordno,
        departmentcode=department.departmentcode,
        departmentname=department.departmentname,
        departmentshortname=department.departmentshortname,
        remarks=department.remarks,
        transactby=0,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
