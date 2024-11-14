from django.shortcuts import render, redirect
from datetime import datetime
from .models import MeansofFranchise, historymeansoffranchise
from django.db.models import Max
from permission_app.models import permission
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.db.models import Q
# Create your views here.

def has_permission(user, access_names):
    if user.is_authenticated:
        userRoleid = user.roleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='MeansofFranchise_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False


@login_required
def MeansofFranchise_insert(request):
    if request.user.is_authenticated:
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                    userRoleid = request.user.roleid
                    userRoleid = userRoleid.roleid
                    if request.method == "POST":
                        means = request.POST['means']
                        Status = 'Active'
                        status = 'For Approval'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        transactype = 'add'
                        Transactypes = 'Forapproval'                                                 
                        meansofknowingidid_max = historymeansoffranchise.objects.all().aggregate(Max('recordnohist'))
                        meansofknowingid_nextvalue = 1 if meansofknowingidid_max['recordnohist__max'] == None else meansofknowingidid_max['recordnohist__max'] + 1
                        if MeansofFranchise.objects.annotate(uppercase_means=Upper('means')).filter(uppercase_means=means.upper()):
                            messages.error(request, "Already Exist.") 
                        else:
                            if has_permission(request.user, ['approver', 'Approver']):
                                    data = MeansofFranchise(meansofknowingid=meansofknowingid_nextvalue,
                                                            means=means, 
                                                            transactby=transactby,transactdate=transactdate,
                                                            transactype=transactype,
                                                            status=Status)
                                    data.save()
                                    MeansofFranchisehistory_save(data, transactype)
                                    return redirect('MeansofFranchise_show')
                            else:                            
                                Historymeansoffranchise_max = historymeansoffranchise.objects.all().aggregate(Max('recordnohist')) 
                                Historymeansoffranchise_nextvalue = 1 if Historymeansoffranchise_max['recordnohist__max'] == None else Historymeansoffranchise_max['recordnohist__max']                                
                                data = historymeansoffranchise(recordno=Historymeansoffranchise_nextvalue, 
                                                                meansofknowingid=Historymeansoffranchise_nextvalue, 
                                                                means=means,
                                                                transactby=transactby,
                                                                transactdate=transactdate, 
                                                                transactype=Transactypes,
                                                                status=status)
                                data.save()
                                return redirect('MeansofFranchise_show')              
                    return render(request, 'MeansofFranchise_insert.html')
        return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def MeansofFranchise_approval(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver', 'Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historymeansoffranchise = historymeansoffranchise.objects.get(recordnohist=pk)
            transactype = 'add'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historymeansoffranchise.transactype = 'Disapprove'
                        Historymeansoffranchise.status = 'Disapprove'
                        Historymeansoffranchise.save()  
                        return redirect('MeansofFranchise_show')           
                else:
                    meansofknowingid = Historymeansoffranchise.meansofknowingid
                    means = Historymeansoffranchise.means                 
                    transactby = userRoleid
                    transactdate = datetime.now()                           
                    transactype = transactype
                    status='Active'
                    data = MeansofFranchise(meansofknowingid=meansofknowingid,means=means,transactby=transactby,transactdate=transactdate, transactype=transactype,status=status)     
                    data.save()                       
                    Historymeansoffranchise.status = 'Approve'
                    Historymeansoffranchise.transactype = 'Approve'
                    Historymeansoffranchise.save()                  
                return redirect('MeansofFranchise_show')               
            return render(request,'MeansofFranchise_approval.html',{'Historymeansoffranchise': Historymeansoffranchise})       
        return redirect('home') 
    return redirect('login')    


@login_required   
def MeansofFranchise_show(request):
    if request.user.is_authenticated:   
       if has_permission(request.user, ['LIST', 'List','View', 'SHOW']):
                MeansOfFranchise = MeansofFranchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historymeansoffranchise.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historymeansoffranchise.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historymeansoffranchise.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='MeansofFranchise_app')  
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
                if search_query:MeansOfFranchise = MeansOfFranchise.filter(Q(statusname_icontains=search_query))                                                                            
                return render(request, 'MeansofFranchise_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'MeansOfFranchise': MeansOfFranchise
                })
       return redirect('home')
    return redirect('login')

@login_required
def MeansofFranchise_edit(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['EDIT', 'Edit','UPDATE', 'Update']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            MeansOfFranchise = MeansofFranchise.objects.get(recordno=pk)
            transactype = 'Edit'
            if request.method == 'POST':
                print(request.POST)
                MeansOfFranchise.means = request.POST['means'].strip().replace("  ", " ").title()
                MeansOfFranchise.transactby = userRoleid
                MeansOfFranchise.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):
                    MeansOfFranchise.transactype = transactype
                    MeansOfFranchise.save()  
                    MeansofFranchisehistory_save(MeansOfFranchise,transactype) 
                    return redirect('MeansofFranchise_show')
                else:
                    recordno = pk
                    meansofknowingid = MeansOfFranchise.meansofknowingid
                    means = request.POST['means'].strip().replace("  ", " ").title()
                    status = 'For Update'
                    transactypes = 'Forupdate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historymeansoffranchise(recordno=recordno, meansofknowingid=meansofknowingid,means=means, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)                            
                    data.save()                       
                return redirect('MeansofFranchise_show')          
            return render(request,'MeansofFranchise_edit.html',{'MeansOfFranchise': MeansOfFranchise}) 
        return redirect('home')       
    return redirect('login')          

@login_required
def MeansofFranchise_edited(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historymeansoffranchise = historymeansoffranchise.objects.get(recordnohist=pk)
            MeansOfFranchise = MeansofFranchise.objects.get(recordno=Historymeansoffranchise.recordno)
            transactype = 'edit'
            if request.method == 'POST':
                if 'delete' in request.POST:
                        Historymeansoffranchise.transactype = 'Disapprove'
                        Historymeansoffranchise.status = 'Disapprove'
                        Historymeansoffranchise.save()
                        return redirect('MeansofFranchise_show')             
                else:
                    MeansOfFranchise.meansofknowingid = Historymeansoffranchise.meansofknowingid
                    MeansOfFranchise.means = Historymeansoffranchise.means                  
                    MeansOfFranchise.transactby = userRoleid
                    MeansOfFranchise.transactdate = datetime.now()                           
                    MeansOfFranchise.transactype = transactype
                    MeansOfFranchise.status = 'Active'
                    MeansOfFranchise.save() 
                    Historymeansoffranchise.status = 'Approve'
                    Historymeansoffranchise.transactype = 'Approve'
                    Historymeansoffranchise.save()               
                return redirect('MeansofFranchise_show')
            return render(request,'MeansofFranchise_edited.html',{'Historymeansoffranchise': Historymeansoffranchise,'MeansOfFranchise': MeansOfFranchise})       
        return redirect('home')
    return redirect('login')     

@login_required
def MeansofFranchise_delete(request, pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['Delete','delete']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            MeansOfFranchise = MeansofFranchise.objects.get(recordno=pk)
            transactype = 'Terminate'
            MeansOfFranchise.transactby = userRoleid
            MeansOfFranchise.transactdate = datetime.now()       
            if has_permission(request.user, ['approver','Approver']):
                if request.method == 'POST':
                    MeansOfFranchise.transactby = userRoleid
                    MeansOfFranchise.transactdate = datetime.now()
                    MeansOfFranchise.transactype = transactype
                    MeansOfFranchise.status = 'Deactive'
                    MeansOfFranchise.save()
                    MeansofFranchisehistory_save(MeansOfFranchise, transactype)
                    return redirect('MeansofFranchise_show') 
                return render(request, 'MeansofFranchise_delete.html', {'MeansOfFranchise': MeansOfFranchise})                                             
            else:                       
                MeansOfFranchise.status = 'Deactive'
                MeansOfFranchise.save()
                recordno = pk
                meansofknowingid = MeansOfFranchise.meansofknowingid
                means = MeansOfFranchise.means  
                
                status = 'For Terminate'
                transactypes = 'Forterminate'
                transactby = userRoleid
                transactdate = datetime.now()
                data = historymeansoffranchise(recordno=recordno, meansofknowingid=meansofknowingid,means=means, transactby=transactby,transactdate=transactdate, transactype=transactypes,status=status)
                data.save() 
                return redirect('MeansofFranchise_show')
        return redirect('home')
    return redirect('login') 

@login_required
def MeansofFranchise_terminate(request,pk):
    if request.user.is_authenticated:
        if has_permission(request.user, ['approver','Approver']):
            userRoleid = request.user.roleid
            userRoleid = userRoleid.roleid
            Historymeansoffranchise = historymeansoffranchise.objects.get(recordnohist=pk)
            MeansOfFranchise = MeansofFranchise.objects.get(recordno=Historymeansoffranchise.recordno)
            if request.method == 'POST':
                if 'Disapprove' in request.POST:
                    Historymeansoffranchise.transactype = 'Approve'
                    Historymeansoffranchise.status = 'Approve'
                    Historymeansoffranchise.save()  
                    MeansOfFranchise.transactype = 'edit'
                    MeansOfFranchise.status = 'Active'
                    MeansOfFranchise.save()            
                else:
                    Historymeansoffranchise.transactype = 'Terminate'
                    Historymeansoffranchise.status = 'Terminate'
                    Historymeansoffranchise.save()  
                    MeansOfFranchise.transactype = 'Terminate'
                    MeansOfFranchise.status = 'Terminate'
                    MeansOfFranchise.save()                
                return redirect('MeansofFranchise_show')
            return render(request,'MeansofFranchise_terminate.html',{'Historymeansoffranchise': Historymeansoffranchise,'MeansOfFranchise': MeansOfFranchise})       
        return redirect('home')
    return redirect('login')  

def MeansofFranchisehistory_save(obj, transactype):
    MeansofFranchise = obj
    data = historymeansoffranchise(
        recordno=MeansofFranchise.recordno,
        meansofknowingid = MeansofFranchise.meansofknowingid,
        means = MeansofFranchise.means,              
        status=MeansofFranchise.status,
        transactby=MeansofFranchise.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
