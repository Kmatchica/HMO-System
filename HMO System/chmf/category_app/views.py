# Create your views here.
from django.shortcuts import render, redirect
from .models import category, historycategory
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
########################## new function#####################
from django.db.models import Q

@login_required
def category_insert(request):
    if request.user.is_authenticated:  
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                if request.method == "POST":
                    providercategoryname = request.POST['providercategoryname'].strip().replace("  ", " ").title()
                    providercategoryshortname = request.POST['providercategoryshortname'].strip().replace("  ", " ").title()
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    ordernumber = request.POST['ordernumber']
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    status = 'Active'
                    Status = 'For approval'
                    categorycode_max = category.objects.all().aggregate(Max('categorycode'))
                    categorycode_nextvalue = 1 if categorycode_max['categorycode__max'] == None else categorycode_max['categorycode__max'] + 1
                    if category.objects.annotate(uppercase_providercategoryname=Upper('providercategoryname'), uppercase_providercategoryshortname=Upper('providercategoryshortname')).filter(uppercase_providercategoryname=providercategoryname.upper(), uppercase_providercategoryshortname=providercategoryshortname.upper(), status="Inactive"):
                        messages.error(request, "The Category Name is already Exist Please View in Inactive List.")  
                    elif category.objects.annotate(uppercase_providercategoryname=Upper('providercategoryname'), uppercase_providercategoryshortname=Upper('providercategoryshortname')).filter(uppercase_providercategoryname=providercategoryname.upper(), uppercase_providercategoryshortname=providercategoryshortname.upper(),status="Active"):
                        messages.error(request, "The Category Name is already Exist.")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1: 
                                data = category(categorycode=categorycode_nextvalue, providercategoryname=providercategoryname, providercategoryshortname=providercategoryshortname, remarks=remarks, ordernumber=ordernumber,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)
                                data.save()
                                categoryhistory_save(data, transactype)
                                return redirect('category_show')
                            else:
                                Categorycode_max = historycategory.objects.all().aggregate(Max('recordnohist')) 
                                CategoryCode_nextvalue = 1 if Categorycode_max['recordnohist__max'] == None else Categorycode_max['recordnohist__max']+ 1
                                recordnohist_max = historycategory.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                                data = historycategory(recordno=recordno_nextvalue, categorycode=CategoryCode_nextvalue, providercategoryname=providercategoryname, providercategoryshortname=providercategoryshortname, remarks=remarks, ordernumber=ordernumber,transactby=transactby,transactdate=transactdate, transactype=Transactype,status=Status)
                                data.save()
                                return redirect('category_show')
                        return redirect('home')    
                    return render(request, 'category_insert.html')
                else:
                 return render(request, 'category_insert.html')
            else:
             return redirect('home')  
        else:
         return redirect('home')                        
    return redirect('login')                  
    
@login_required
def category_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historycategory = historycategory.objects.get(recordnohist=pk)
                
                transactype = 'add'
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historycategory.transactype = 'Disapprove'
                            Historycategory.status = 'Disapprove'
                            Historycategory.save()             
                    else:
                        categorycode = Historycategory.categorycode
                        providercategoryname = Historycategory.providercategoryname
                        providercategoryshortname = Historycategory.providercategoryshortname
                        remarks = Historycategory.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = category(categorycode=categorycode,providercategoryname=providercategoryname,providercategoryshortname=providercategoryshortname,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status)
                        data.save()                       
                        Historycategory.status = 'Approve'
                        Historycategory.transactype = 'Approve'
                        Historycategory.save()                  
                    return redirect('category_show')               
                return render(request,'category_approval.html',{'Historycategory': Historycategory})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login') 
      
@login_required
def category_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','Show', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                historyupdate = historycategory.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historycategory.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historycategory.objects.filter(transactype__in=['Forapproval'])                
               
                categorys = category.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='category_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                edit_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['EDIT', 'Edit']).values_list('accesscode', flat=True))
                show_edit_button = any(permission.holder == 1 for permission in edit_permissions)
                delete_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['DELETE', 'Delete']).values_list('accesscode', flat=True))
                show_delete_button = any(permission.holder == 1 for permission in delete_permissions)
                insert_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['INSERT','Insert', 'ADD', 'Add']).values_list('accesscode', flat=True))
                show_insert_button = any(permission.holder == 1 for permission in insert_permissions)
                 # filter_status = request.GET.get('filter_status')
                search_query = request.GET.get('search_query')
                if search_query:categorys = categorys.filter( Q(providercategoryname__icontains=search_query))
                return render(request, 'category_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'categorys': categorys,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
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
def category_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Category = category.objects.get(recordno=pk)
                transactype = 'Edit'
                status='Active'
                if request.method == 'POST':
                    print(request.POST)
                    Category.providercategoryname = request.POST['providercategoryname'].strip().replace("  ", " ").title()
                    Category.providercategoryshortname = request.POST['providercategoryshortname'].strip().replace("  ", " ").title()
                    Category.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    Category.ordernumber = request.POST['ordernumber']
                    Category.transactby = userRoleid
                    Category.transactdate = datetime.now()
                    Category.transactype =  transactype      
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='category_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Category.transactype = transactype
                            Category.save()  
                            categoryhistory_save(Category,transactype) 
                            return redirect('category_show')
                        else:
                            recordno = pk
                            categorycode = Category.categorycode
                            providercategoryname = request.POST['providercategoryname'].strip().replace("  ", " ").title()
                            providercategoryshortname = request.POST['providercategoryshortname'].strip().replace("  ", " ").title()
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            ordernumber = request.POST['ordernumber']
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historycategory(recordno=recordno,categorycode=categorycode, providercategoryname=providercategoryname, providercategoryshortname=providercategoryshortname, remarks=remarks, ordernumber=ordernumber,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)  
                            data.save() 
                        return redirect('category_show')         
                    return redirect('category_show')   
                return render(request,'category_edit.html',{'Category': Category})       
            else:
                return redirect('home')
        else:
            return redirect('home') 
    return redirect('login')  

@login_required
def category_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historycategory = historycategory.objects.get(recordnohist=pk)
                Category = category.objects.get(recordno=Historycategory.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historycategory.transactype = 'Disapprove'
                            Historycategory.status = 'Disapprove'
                            Historycategory.save()             
                    else:
                        Category.categorycode = Historycategory.categorycode
                        Category.providercategoryname = Historycategory.providercategoryname
                        Category.providercategoryshortname = Historycategory.providercategoryshortname
                        Category.remarks = Historycategory.remarks
                        Category.ordernumber = Historycategory.ordernumber
                        Category.status = 'Active'
                        Category.transactby = userRoleid
                        Category.transactdate = datetime.now()                           
                        Category.transactype = transactype
                        Category.save() 
                        Historycategory.status = 'Approve'
                        Historycategory.transactype = 'Approve'
                        Historycategory.save()               
                    return redirect('category_show')
                return render(request,'category_edited.html',{'Historycategory': Historycategory,'Category': Category})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

        
@login_required
def category_delete(request, pk):
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
                Category = category.objects.get(recordno=pk)
                transactype = 'Terminate'
                Category.transactby = userRoleid
                Category.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='category_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Category.transactby = userRoleid
                            Category.transactdate = datetime.now()
                            Category.transactype = transactype
                            Category.status = 'Deactive'
                            Category.save()
                            categoryhistory_save(Category, transactype)
                            return redirect('category_show')                                             
                    else:
                        
                        Category.status = 'Deactive'
                        Category.save()
                        recordno = pk
                        categorycode = Category.categorycode
                        providercategoryname = Category.providercategoryname
                        providercategoryshortname = Category.providercategoryshortname
                        remarks = Category.remarks
                        ordernumber = Category.ordernumber
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historycategory(recordno=recordno,categorycode=categorycode, providercategoryname=providercategoryname, providercategoryshortname=providercategoryshortname, remarks=remarks, ordernumber=ordernumber,transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)  
                        data.save() 
                
                        return redirect('category_show')
                    return render(request, 'category_delete.html', {'Category': Category,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def category_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='category_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historycategory = historycategory.objects.get(recordnohist=pk)
                Category = category.objects.get(recordno=Historycategory.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historycategory.transactype = 'Edit'
                            Historycategory.status = 'Approve'
                            Historycategory.save()  
                            Category.transactype = 'edit'
                            Category.status = 'Active'
                            Category.save()            
                    else:
                        Historycategory.transactype = 'Edit'
                        Historycategory.status = 'Terminate'
                        Historycategory.save()  
                        Category.transactype = 'Terminate'
                        Category.status = 'Terminate'
                        Category.save()                
                    return redirect('category_show')
                return render(request,'category_terminate.html',{'Historycategory': Historycategory})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login') 

def categoryhistory_save(obj, transactype):
    category = obj
    data = historycategory(
        recordno=category.recordno,
        categorycode=category.categorycode,
        providercategoryname=category.providercategoryname,
        providercategoryshortname=category.providercategoryshortname,
        ordernumber=category.ordernumber,
        remarks=category.remarks,
        status=category.status,
        transactby=0,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
