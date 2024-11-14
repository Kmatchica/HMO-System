from django.shortcuts import render, redirect
from datetime import datetime
from .models import franchisenotes, historyfranchisenotes
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q
from franchise_app.models import franchise
# Create your views here.
@login_required
def franchisenotes_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                if request.method == "POST":
                    franchisecode = franchise.objects.get(franchisecode=request.POST['franchisecode'])
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    franchisecode_max = historyfranchisenotes.objects.all().aggregate(Max('recordnohist'))
                    franchisecode_nextvalue = 1 if franchisecode_max['franchisecode__max'] == None else franchisecode_max['franchisecode__max'] + 1
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid  
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            data = franchisenotes(franchisenoteid=franchisecode_nextvalue,franchisecode=franchisecode,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=Status)
                            data.save()
                            franchisenoteshistory_save(data, transactype)
                            return redirect('franchisenotes_show')
                        else:                            
                            Historyfranchisenotes_max = historyfranchisenotes.objects.all().aggregate(Max('recordnohist')) 
                            Historyfranchisenotes_nextvalue = 1 if Historyfranchisenotes_max['recordnohist__max'] == None else Historyfranchisenotes_max['recordnohist__max']                                
                            data = historyfranchisenotes(recordno=Historyfranchisenotes_nextvalue, franchisenoteid=Historyfranchisenotes_nextvalue,franchisecode=franchisecode,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=Transactypes,status=status)
                            data.save()
                            return redirect('franchisenotes_show')
                    return render(request, 'franchisenotes_show.html')              
                    
                return render(request, 'franchisenotes_insert.html')
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def franchisenotes_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyfranchisenotes = historyfranchisenotes.objects.get(recordnohist=pk)
                Franchisenotes = franchisenotes.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Franchise = franchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyfranchisenotes.transactype = 'Disapprove'
                            Historyfranchisenotes.status = 'Disapprove'
                            Historyfranchisenotes.save()  
                            return redirect('franchisenotes_show')           
                    else:
                        franchisenoteid = Historyfranchisenotes.franchisenoteid
                        franchisecode = Historyfranchisenotes.franchisecode                  
                        remarks = Historyfranchisenotes.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = franchisenotes(franchisenoteid=franchisenoteid,franchisecode=franchisecode,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                        data.save()                       
                        Historyfranchisenotes.status = 'Approve'
                        Historyfranchisenotes.transactype = 'Approve'
                        Historyfranchisenotes.save()                  
                    return redirect('franchisenotes_show')               
                return render(request,'franchisenotes_approval.html',{'Historyfranchisenotes': Historyfranchisenotes,'Franchisenotes': Franchisenotes,'Franchise': Franchise})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required   
def franchisenotes_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Franchisenotes = franchisenotes.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historyfranchisenotes.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyfranchisenotes.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyfranchisenotes.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
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
                if search_query:Franchisenotes = Franchisenotes.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'franchisenotes_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Franchisenotes': Franchisenotes
                
                
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
def franchisenotes_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Franchisenotes = franchisenotes.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Franchisenotes.franchisecode = franchise.objects.get(franchisecode=request.POST['franchisecode'])
                    Franchisenotes.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Franchisenotes.transactby = userRoleid
                    Franchisenotes.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Franchisenotes.transactype = transactype
                            Franchisenotes.save()  
                            franchisenoteshistory_save(Franchisenotes,transactype) 
                            return redirect('franchisenotes_show')
                        else:
                            recordno = pk
                            franchisenoteid = Franchisenotes.franchisenoteid
                            franchisecode = franchise.objects.get(franchisecode=request.POST['franchisecode'])
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historyfranchisenotes(recordno=recordno, franchisenoteid=franchisenoteid,franchisecode=franchisecode,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                            data.save()                       
                        return redirect('franchisenotes_show')         
                    return redirect('franchisenotes_show')   
                return render(request,'franchisenotes_edit.html',{'Franchisenotes': Franchisenotes})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')          

@login_required
def franchisenotes_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historyfranchisenotes = historyfranchisenotes.objects.get(recordnohist=pk)
                Franchisenotes = franchisenotes.objects.get(recordno=Historyfranchisenotes.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historyfranchisenotes.transactype = 'Disapprove'
                            Historyfranchisenotes.status = 'Disapprove'
                            Historyfranchisenotes.save()
                            return redirect('franchisenotes_show')             
                    else:
                        Franchisenotes.franchisenoteid = Historyfranchisenotes.franchisenoteid
                        Franchisenotes.franchisecode = Historyfranchisenotes.franchisecode                   
                        Franchisenotes.remarks = Historyfranchisenotes.remarks
                        Franchisenotes.transactby = userRoleid
                        Franchisenotes.transactdate = datetime.now()                           
                        Franchisenotes.transactype = transactype
                        Franchisenotes.status = 'Active'
                        Franchisenotes.save() 
                        Historyfranchisenotes.status = 'Approve'
                        Historyfranchisenotes.transactype = 'Approve'
                        Historyfranchisenotes.save()               
                    return redirect('franchisenotes_show')
                return render(request,'franchisenotes_edited.html',{'Historyfranchisenotes': Historyfranchisenotes,'Franchisenotes': Franchisenotes})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def franchisenotes_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Franchisenotes = franchisenotes.objects.get(recordno=pk)
                transactype = 'Terminate'
                Franchisenotes.transactby = userRoleid
                Franchisenotes.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver'],status__in=['Active']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Franchisenotes.transactby = userRoleid
                            Franchisenotes.transactdate = datetime.now()
                            Franchisenotes.transactype = transactype
                            Franchisenotes.status = 'Deactive'
                            Franchisenotes.save()
                            franchisenoteshistory_save(Franchisenotes, transactype)
                            return redirect('franchisenotes_show') 
                                                                    
                    else:                       
                        Franchisenotes.status = 'Deactive'
                        Franchisenotes.save()
                        recordno = pk
                        franchisenoteid = Franchisenotes.franchisenoteid
                        franchisecode = Franchisenotes.franchisecode  
                        remarks = Franchisenotes.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historyfranchisenotes(recordno=recordno, franchisenoteid=franchisenoteid,franchisecode=franchisecode,remarks=remarks, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                        data.save() 
                        return redirect('franchisenotes_show')
                    return render(request, 'franchisenotes_delete.html', {'Franchisenotes': Franchisenotes})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def franchisenotes_terminate(request,pk):
    if request.user.is_authenticated:
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            permissions = permission.objects.filter(roleid=userRoleid)
            modulelist = moduleslist.objects.filter(moduleappname='franchisenotes_app')  
            modulecodes = [module.modulecode for module in modulelist]
            permissions = permissions.filter(modulecode__in=modulecodes)
            accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
            permissions = permissions.filter(accesscode__in=accesscodes)
            holder_values = [permission.holder for permission in permissions]
            if holder_values:
                if holder_values[0] == 1: 
                    Historyfranchisenotes = historyfranchisenotes.objects.get(recordnohist=pk)
                    Franchisenotes = franchisenotes.objects.get(recordno=Historyfranchisenotes.recordno)
                   
                    if request.method == 'POST':
                        if 'Disapprove' in request.POST:
                            if 'Disapprove' in request.POST:
                                Historyfranchisenotes.transactype = 'Approve'
                                Historyfranchisenotes.status = 'Approve'
                                Historyfranchisenotes.save()  
                                Franchisenotes.transactype = 'edit'
                                Franchisenotes.status = 'Active'
                                Franchisenotes.save()            
                        else:
                            Historyfranchisenotes.transactype = 'Terminate'
                            Historyfranchisenotes.status = 'Terminate'
                            Historyfranchisenotes.save()  
                            Franchisenotes.transactype = 'Terminate'
                            Franchisenotes.status = 'Terminate'
                            Franchisenotes.save()                
                        return redirect('franchisenotes_show')
                    return render(request,'franchisenotes_terminate.html',{'Historyfranchisenotes': Historyfranchisenotes,'Franchisenotes': Franchisenotes})       
                else:
                 return redirect('home')
            else:
             return redirect('home') 
    return redirect('login')  

def franchisenoteshistory_save(obj, transactype):
    franchisenotes = obj
    data = historyfranchisenotes(
        recordno=franchisenotes.recordno,
        franchisenoteid = franchisenotes.franchisenoteid,
        franchisecode = franchisenotes.franchisecode,              
        remarks = franchisenotes.remarks,
        status=franchisenotes.status,
        transactby=franchisenotes.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
