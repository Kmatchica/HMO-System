from django.shortcuts import render, redirect
from .models import franchise, historyfranchise
from datetime import datetime 
from django.db.models import Max
from department_app.models import department
from roles_app.models import roles
from permission_app.models import permission
from login_app.models import User
from access_app.models import access
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist
from MeansofFranchise_app.models import MeansofFranchise
from Franchisestatus_app.models import Franchisestatus
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from datetime import datetime

def has_permission(user, access_names):
    """Check if the user has the required permissions."""
    if user.is_authenticated:
        userRoleid = user.roleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='franchise_app')
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=access_names, status='Active').values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [perm.holder for perm in permissions]
        return holder_values and holder_values[0] == 1
    return False


@login_required
def franchise_insert(request):
    if request.user.is_authenticated:  
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['ADD', 'Add', 'Insert', 'INSERT']):
                MeansOfFranchise = MeansofFranchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                FranchiseStatus = Franchisestatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST": 
                    clientname = request.POST['clientname'].strip().replace("  ", " ").title()
                    clientshortname = request.POST['clientshortname'].strip().replace("  ", " ").title()
                    clientclassificationcode = request.POST['clientclassificationcode'].strip()
                    address = request.POST['address'].strip().replace("  ", " ")
                    contactnumber = request.POST['contactnumber']
                    email = request.POST['email'].strip().replace("  ", " ")
                    contactperson = request.POST['contactperson'].strip().replace("  ", " ").title()
                    contactpersondesignation = request.POST['contactpersondesignation'].strip().replace("  ", " ").title()
                    signatoryname = request.POST['signatoryname'].strip().replace("  ", " ").title()
                    signatorydesignation = request.POST['signatorydesignation'].strip().replace("  ", " ").title()
                    totalmembers = request.POST['totalmembers']
                    totaldependents = request.POST['totaldependents'].strip()
                    totalemployees = request.POST['totalemployees'].strip()
                    existinghmo = request.POST['existinghmo'].strip().replace("  ", " ").title()
                    sobtypeid = request.POST['sobtypeid'].strip()
                    meansofknowingid = MeansofFranchise.objects.get(meansofknowingid=request.POST['meansofknowingid'])
                    referredby = request.POST['referredby'].strip().replace("  ", " ").title()
                    franchisestatusid = Franchisestatus.objects.get(franchisestatusid=request.POST['franchisestatusid'])
                    disapprovalreason = request.POST['disapprovalreason'].strip().replace("  ", " ")
                    istpa = request.POST['istpa']
                    adminfee = request.POST['adminfee']
                    networkaccessfee = request.POST['networkaccessfee']
                    locationcode = request.POST['locationcode'].strip()
                    remarks = request.POST['remarks'].strip().replace("  ", " ")
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactype = 'Forapproval'
                    status = 'Active'
                    Status = 'For approval'
                    franchisecode_max = historyfranchise.objects.all().aggregate(Max('recordnohist'))
                    franchisecode_nextvalue = 1 if franchisecode_max['franchisecode__max'] == None else franchisecode_max['franchisecode__max'] + 1
                    if franchise.objects.annotate(uppercase_clientname=Upper('clientname')).filter(uppercase_clientname=clientname.upper()):
                        messages.error(request, "The Clientname is already Exist.")  
                    else:
                        if has_permission(request.user,['approver','Approver']):
                            data = franchise(
                            franchisecode=franchisecode_nextvalue,
                            clientname=clientname,
                            clientshortname=clientshortname,
                            clientclassificationcode=clientclassificationcode,
                            address=address,
                            contactnumber=contactnumber,
                            email=email,
                            contactperson=contactperson,
                            contactpersondesignation=contactpersondesignation,
                            signatoryname=signatoryname,
                            signatorydesignation=signatorydesignation,
                            totalmembers=totalmembers,
                            totaldependents=totaldependents,
                            totalemployees=totalemployees,
                            existinghmo=existinghmo,
                            sobtypeid=sobtypeid,
                            meansofknowingid=meansofknowingid,
                            referredby=referredby,
                            franchisestatusid=franchisestatusid,
                            disapprovalreason=disapprovalreason,
                            istpa=istpa,
                            adminfee=adminfee,
                            networkaccessfee=networkaccessfee,
                            locationcode=locationcode,
                            remarks=remarks,
                            transactby=transactby,
                            transactdate=transactdate,
                            transactype=transactype, 
                            status=status)
                            data.save()
                            franchisehistory_save(data, transactype)
                            return redirect('franchise_show')
                        else:
                            recordnohist_max = historyfranchise.objects.all().aggregate(Max('recordnohist')) 
                            recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                            agentid_max = historyfranchise.objects.all().aggregate(Max('recordnohist')) 
                            Accesscode_nextvalue = 1 if agentid_max['recordnohist__max'] == None else agentid_max['recordnohist__max']+ 1
                            data = historyfranchise(
                            recordno=recordno_nextvalue, 
                            franchisecode=Accesscode_nextvalue,
                            clientname=clientname,
                            clientshortname=clientshortname,
                            clientclassificationcode=clientclassificationcode,
                            address=address,
                            contactnumber=contactnumber,
                            email=email,
                            contactperson=contactperson,
                            contactpersondesignation=contactpersondesignation,
                            signatoryname=signatoryname,
                            signatorydesignation=signatorydesignation,
                            totalmembers=totalmembers,
                            totaldependents=totaldependents,
                            totalemployees=totalemployees,
                            existinghmo=existinghmo,
                            sobtypeid=sobtypeid,
                            meansofknowingid=meansofknowingid,
                            referredby=referredby,
                            franchisestatusid=franchisestatusid,
                            disapprovalreason=disapprovalreason,
                            istpa=istpa,
                            adminfee=adminfee,
                            networkaccessfee=networkaccessfee,
                            locationcode=locationcode,
                            remarks=remarks, 
                            transactby=transactby,
                            transactdate=transactdate,
                            transactype=Transactype, 
                            status=Status)
                            data.save()
                            return redirect('franchise_show')
                    return render(request, 'franchise_insert.html',{'MeansOfFranchise':MeansOfFranchise,'FranchiseStatus':FranchiseStatus})
        return redirect('franchise_insert')
    return redirect('login')
        
@login_required
def franchise_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver','Approver']):
                Historyfranchise = historyfranchise.objects.get(recordnohist=pk)
                transactype = 'add'
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                            Historyfranchise.transactype = 'Disapprove'
                            Historyfranchise.status = 'Disapprove'
                            Historyfranchise.save()             
                    else:
                        recordno = Historyfranchise.recordno,
                        franchisecode=Historyfranchise.franchisecode,
                        clientname=Historyfranchise.clientname,
                        clientshortname=Historyfranchise.clientshortname,
                        clientclassificationcode=Historyfranchise.clientclassificationcode,
                        address=Historyfranchise.address,
                        contactnumber=Historyfranchise.contactnumber,
                        email=Historyfranchise.email,
                        contactperson=Historyfranchise.contactperson,
                        contactpersondesignation=Historyfranchise.contactpersondesignation,
                        signatoryname=Historyfranchise.signatoryname,
                        signatorydesignation=Historyfranchise.signatorydesignation,
                        totalmembers=Historyfranchise.totalmembers,
                        totaldependents=Historyfranchise.totaldependents,
                        totalemployees=Historyfranchise.totalemployees,
                        existinghmo=Historyfranchise.existinghmo,
                        sobtypeid=Historyfranchise.sobtypeid,
                        meansofknowingid=Historyfranchise.meansofknowingid,
                        referredby=Historyfranchise.referredby,
                        franchisestatusid=Historyfranchise.franchisestatusid,
                        disapprovalreason=Historyfranchise.disapprovalreason,
                        istpa=Historyfranchise.istpa,
                        adminfee=Historyfranchise.adminfee,
                        networkaccessfee=Historyfranchise.networkaccessfee,
                        locationcode=Historyfranchise.locationcode,
                        remarks=Historyfranchise.remarks, 
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = 'add'
                        status='Active'
                        data = franchise(
                            franchisecode=franchisecode,
                            clientname=clientname,
                            clientshortname=clientshortname,
                            clientclassificationcode=clientclassificationcode,
                            address=address,
                            contactnumber=contactnumber,
                            email=email,
                            contactperson=contactperson,
                            contactpersondesignation=contactpersondesignation,
                            signatoryname=signatoryname,
                            signatorydesignation=signatorydesignation,
                            totalmembers=totalmembers,
                            totaldependents=totaldependents,
                            totalemployees=totalemployees,
                            existinghmo=existinghmo,
                            sobtypeid=sobtypeid,
                            meansofknowingid=meansofknowingid,
                            referredby=referredby,
                            franchisestatusid=franchisestatusid,
                            disapprovalreason=disapprovalreason,
                            istpa=istpa,
                            adminfee=adminfee,
                            networkaccessfee=networkaccessfee,
                            locationcode=locationcode,
                            remarks=remarks, 
                            transactby=transactby,
                            transactdate=transactdate,
                            transactype=transactype, 
                            status=status)       
                        data.save()                       
                        Historyfranchise.status = 'Approve'
                        Historyfranchise.transactype = 'Approve'
                        Historyfranchise.save()                  
                    return redirect('franchise_show')               
                return render(request,'franchise_approval.html',{'Historyfranchise': Historyfranchise})        
    return redirect('login')        

@login_required   
def franchise_show(request):
     if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['LIST', 'List','View', 'SHOW']):
                historyupdate = historyfranchise.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historyfranchise.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historyfranchise.objects.filter(transactype__in=['Forapproval'])
                Franchise = franchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='franchise_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                edit_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['EDIT', 'Edit']).values_list('accesscode', flat=True))
                show_edit_button = any(permission.holder == 1 for permission in edit_permissions)
                delete_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['DELETE', 'Delete']).values_list('accesscode', flat=True))
                show_delete_button = any(permission.holder == 1 for permission in delete_permissions)
                insert_permissions = permissions.filter(accesscode__in=access.objects.filter(accessname__in=['INSERT','Insert', 'ADD', 'Add']).values_list('accesscode', flat=True))
                show_insert_button = any(permission.holder == 1 for permission in insert_permissions)
                return render(request, 'franchise_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'Franchise': Franchise,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                })                
        return redirect('home')                
     return redirect('login')
       
@login_required       
def franchise_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['EDIT', 'Edit','UPDATE', 'Update']):
            Franchise = franchise.objects.get(recordno=pk)
            MeansOfFranchise = MeansofFranchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
            FranchiseStatus = Franchisestatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
            transactype = 'Edit'
            status='Active'
            if request.method == 'POST':
                print(request.POST)
                Franchise.clientname = request.POST['clientname'].strip().replace("  ", " ").title()
                Franchise.clientshortname = request.POST['clientshortname'].strip().replace("  ", " ").title()
                Franchise.clientclassificationcode = request.POST['clientclassificationcode'].strip()
                Franchise.address = request.POST['address'].strip().replace("  ", " ")
                Franchise.contactnumber = request.POST['contactnumber']
                Franchise.email = request.POST['email'].strip().replace("  ", " ")
                Franchise.contactperson = request.POST['contactperson'].strip().replace("  ", " ").title()
                Franchise.contactpersondesignation = request.POST['contactpersondesignation'].strip().replace("  ", " ").title()
                Franchise.signatoryname = request.POST['signatoryname'].strip().replace("  ", " ").title()
                Franchise.signatorydesignation = request.POST['signatorydesignation'].strip().replace("  ", " ").title()
                Franchise.totalmembers = request.POST['totalmembers']
                Franchise.totaldependents = request.POST['totaldependents'].strip()
                Franchise.totalemployees = request.POST['totalemployees'].strip()
                Franchise.existinghmo = request.POST['existinghmo'].strip().replace("  ", " ").title()
                Franchise.sobtypeid = request.POST['sobtypeid'].strip()
                Franchise.meansofknowingid = MeansofFranchise.objects.get(meansofknowingid=request.POST['meansofknowingid'])
                Franchise.referredby = request.POST['referredby'].strip().replace("  ", " ").title()
                Franchise.franchisestatusid = Franchisestatus.objects.get(franchisestatusid=request.POST['franchisestatusid'])
                Franchise.disapprovalreason = request.POST['disapprovalreason'].strip().replace("  ", " ")
                Franchise.istpa = request.POST['istpa']
                Franchise.adminfee = request.POST['adminfee']
                Franchise.networkaccessfee = request.POST['networkaccessfee']
                Franchise.locationcode = request.POST['locationcode'].strip()
                Franchise.remarks = request.POST['remarks'].strip().replace("  ", " ")
                Franchise.transactby = userRoleid
                Franchise.transactdate = datetime.now()
                Franchise.transactype = 'edit'     
                if has_permission(request.user, ['approver', 'Approver']):
                    Franchise.transactype = transactype
                    Franchise.save()  
                    franchisehistory_save(Franchise,transactype) 
                    return redirect('franchise_show')
                else:
                    recordno = pk
                    franchisecode=Franchise.franchisecode
                    clientname = request.POST['clientname'].strip().replace("  ", " ").title()
                    clientshortname = request.POST['clientshortname'].strip().replace("  ", " ").title()
                    clientclassificationcode = int(request.POST['clientclassificationcode'].strip())
                    address = request.POST['address'].strip().replace("  ", " ")
                    contactnumber = request.POST['contactnumber']
                    email = request.POST['email'].strip().replace("  ", " ")
                    contactperson = request.POST['contactperson'].strip().replace("  ", " ").title()
                    contactpersondesignation = request.POST['contactpersondesignation'].strip().replace("  ", " ").title()
                    signatoryname = request.POST['signatoryname'].strip().replace("  ", " ").title()
                    signatorydesignation = request.POST['signatorydesignation'].strip().replace("  ", " ").title()
                    totalmembers = request.POST['totalmembers']
                    totaldependents = request.POST['totaldependents'].strip()
                    totalemployees = request.POST['totalemployees'].strip()
                    existinghmo = request.POST['existinghmo'].strip().replace("  ", " ").title()
                    sobtypeid = request.POST['sobtypeid'].strip()
                    meansofknowingid = MeansofFranchise.objects.get(meansofknowingid=request.POST['meansofknowingid'])
                    referredby = request.POST['referredby'].strip().replace("  ", " ").title()
                    franchisestatusid = Franchisestatus.objects.get(franchisestatusid=request.POST['franchisestatusid'])
                    disapprovalreason = request.POST['disapprovalreason'].strip().replace("  ", " ")
                    istpa = request.POST['istpa']
                    adminfee = request.POST['adminfee']
                    networkaccessfee = request.POST['networkaccessfee']
                    locationcode = request.POST['locationcode'].strip()
                    remarks = request.POST['remarks'].strip().replace("  ", " ")
                    status = 'For Update'
                    transactypes = 'Forupdate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historyfranchise(recordno=recordno,
                                            franchisecode=franchisecode,
                                            clientname=clientname,
                                            clientshortname=clientshortname,
                                            clientclassificationcode=clientclassificationcode,
                                            address=address,
                                            contactnumber=contactnumber,
                                            email=email,
                                            contactperson=contactperson,
                                            contactpersondesignation=contactpersondesignation,
                                            signatoryname=signatoryname,
                                            signatorydesignation=signatorydesignation,
                                            totalmembers=totalmembers,
                                            totaldependents=totaldependents,
                                            totalemployees=totalemployees,
                                            existinghmo=existinghmo,
                                            sobtypeid=sobtypeid,
                                            meansofknowingid=meansofknowingid,
                                            referredby=referredby,
                                            franchisestatusid=franchisestatusid,
                                            disapprovalreason=disapprovalreason,
                                            istpa=istpa,
                                            adminfee=adminfee,
                                            networkaccessfee=networkaccessfee,
                                            locationcode=locationcode,
                                            remarks=remarks, 
                                            transactby=transactby,
                                            transactdate=transactdate,
                                            transactype=transactypes, 
                                            status=status)      
                    data.save() 
                    return redirect('coopagent_show')            
            return render(request,'coopagent_edit.html',{'MeansOfFranchise': MeansOfFranchise,'FranchiseStatus': FranchiseStatus,'Franchise': Franchise})       
        return redirect('home')
    return redirect('login')     

@login_required
def franchise_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver', 'Approver']):
                MeansOfFranchise = MeansofFranchise.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                FranchiseStatus = Franchisestatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'Edit'
                Historyfranchise = historyfranchise.objects.get(recordnohist=pk)
                Franchise = franchise.objects.get(recordno=Historyfranchise.recordno)
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                            Historyfranchise.transactype = 'Disapprove'
                            Historyfranchise.status = 'Disapprove'
                            Historyfranchise.save()
                            return redirect('franchise_show')            
                    else:
                        Franchise.clientname = Historyfranchise.clientname
                        Franchise.clientshortname = Historyfranchise.clientshortname
                        Franchise.clientclassificationcode = Historyfranchise.clientclassificationcode
                        Franchise.address = Historyfranchise.address
                        Franchise.contactnumber = Historyfranchise.contactnumber
                        Franchise.email = Historyfranchise.email
                        Franchise.contactperson = Historyfranchise.contactperson
                        Franchise.contactpersondesignation = Historyfranchise.contactpersondesignation
                        Franchise.signatoryname = Historyfranchise.signatoryname
                        Franchise.signatorydesignation = Historyfranchise.signatorydesignation
                        Franchise.totalmembers = Historyfranchise.totalmembers
                        Franchise.totaldependents = Historyfranchise.totaldependents
                        Franchise.totalemployees = Historyfranchise.totalemployees
                        Franchise.existinghmo = Historyfranchise.existinghmo
                        Franchise.sobtypeid = Historyfranchise.sobtypeid
                        Franchise.meansofknowingid = Historyfranchise.meansofknowingid 
                        Franchise.referredby = Historyfranchise.referredby
                        Franchise.franchisestatusid = Historyfranchise.franchisestatusid
                        Franchise.disapprovalreason = Historyfranchise.disapprovalreason
                        Franchise.istpa = Historyfranchise.istpa
                        Franchise.adminfee = Historyfranchise.adminfee
                        Franchise.networkaccessfee = Historyfranchise.networkaccessfee
                        Franchise.locationcode = Historyfranchise.locationcode
                        Franchise.remarks = Historyfranchise.remarks
                        Franchise.status = 'Active'
                        Franchise.transactby = userRoleid
                        Franchise.transactdate = datetime.now()                           
                        Franchise.transactype = transactype
                        Franchise.save() 
                        Historyfranchise.status = 'Approve'
                        Historyfranchise.transactype = 'Approve'
                        Historyfranchise.save()               
                        return redirect('franchise_show')
                return render(request,'franchise_edited.html',{'Historyfranchise': Historyfranchise,'Franchise': Franchise,'FranchiseStatus': FranchiseStatus,'MeansOfFranchise': MeansOfFranchise})              
        return redirect('home') 
    return redirect('login') 
            
@login_required
def franchise_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['DELETE', 'Delete','Remove', 'REMOVE']):
                Franchise = franchise.objects.get(recordno=pk)
                transactype = 'Terminate'
                Franchise.transactby = userRoleid
                Franchise.transactdate = datetime.now()       
                if has_permission(request.user, ['approver', 'Approver']):
                    if request.method == 'POST':
                        Franchise.transactby = userRoleid
                        Franchise.transactdate = datetime.now()
                        Franchise.transactype = transactype
                        Franchise.status = 'Deactive'
                        Franchise.save()
                        franchisehistory_save(Franchise, transactype)
                        return redirect('franchise_show')                                             
                else:
                    Franchise.status = 'Deactive'
                    Franchise.save()
                    recordno = pk
                    franchisecode = Franchise.franchisecode
                    clientname = Franchise.clientname
                    clientshortname = Franchise.clientshortname
                    clientclassificationcode = Franchise.clientclassificationcode
                    address = Franchise.address
                    contactnumber = Franchise.contactnumber
                    email = Franchise.email
                    contactperson = Franchise.contactperson
                    contactpersondesignation = Franchise.contactpersondesignation
                    signatoryname = Franchise.signatoryname
                    signatorydesignation = Franchise.signatorydesignation
                    totalmembers = Franchise.totalmembers
                    totaldependents = Franchise.totaldependents
                    totalemployees = Franchise.totalemployees
                    existinghmo = Franchise.existinghmo
                    sobtypeid = Franchise.sobtypeid
                    meansofknowingid = Franchise.meansofknowingid 
                    referredby = Franchise.referredby
                    franchisestatusid = Franchise.franchisestatusid
                    disapprovalreason = Franchise.disapprovalreason
                    istpa = Franchise.istpa
                    adminfee = Franchise.adminfee
                    networkaccessfee = Franchise.networkaccessfee
                    locationcode = Franchise.locationcode
                    remarks = Franchise.remarks
                    transactby = userRoleid
                    transactdate = datetime.now()
                    status = 'For Terminate'
                    transactypes = 'Forterminate'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    data = historyfranchise(recordno=recordno,
                                            franchisecode=franchisecode,
                                            clientname=clientname,
                                            clientshortname=clientshortname,
                                            clientclassificationcode=clientclassificationcode,
                                            address=address,
                                            contactnumber=contactnumber,
                                            email=email,
                                            contactperson=contactperson,
                                            contactpersondesignation=contactpersondesignation,
                                            signatoryname=signatoryname,
                                            signatorydesignation=signatorydesignation,
                                            totalmembers=totalmembers,
                                            totaldependents=totaldependents,
                                            totalemployees=totalemployees,
                                            existinghmo=existinghmo,
                                            sobtypeid=sobtypeid,
                                            meansofknowingid=meansofknowingid,
                                            referredby=referredby,
                                            franchisestatusid=franchisestatusid,
                                            disapprovalreason=disapprovalreason,
                                            istpa=istpa,
                                            adminfee=adminfee,
                                            networkaccessfee=networkaccessfee,
                                            locationcode=locationcode,
                                            remarks=remarks, 
                                            transactby=transactby,
                                            transactdate=transactdate,
                                            transactype=transactypes, 
                                            status=status)
                    data.save() 
                    return redirect('franchise_show')
                return render(request, 'franchise_delete.html', {'Franchise': Franchise})
        return redirect('home')
    return redirect('login')  

@login_required
def franchise_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        if has_permission(request.user, ['approver', 'Approver']): 
                Historyfranchise = historyfranchise.objects.get(recordnohist=pk)
                Franchise = franchise.objects.get(recordno=Historyfranchise.recordno)
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                            Historyfranchise.transactype = 'Approve'
                            Historyfranchise.status = 'Approve'
                            Historyfranchise.save()  
                            Franchise.transactype = 'edit'
                            Franchise.status = 'Active'
                            Franchise.save()            
                    else:
                        Historyfranchise.transactype = 'Terminate'
                        Historyfranchise.status = 'Terminate'
                        Historyfranchise.save()  
                        Franchise.transactype = 'Terminate'
                        Franchise.status = 'Terminate'
                        Franchise.save()                
                        return redirect('franchise_show')
                return render(request,'franchise_terminate.html',{'Historyfranchise': Historyfranchise,'Franchise': Franchise})       
          
        return redirect('home')
    return redirect('login') 

def franchisehistory_save(obj, transactype):
    
    franchise = obj
    data = historyfranchise(
        recordno=franchise.recordno,
        franchisecode = franchise.franchisecode,
        clientname = franchise.clientname,
        clientshortname = franchise.clientshortname,
        clientclassificationcode = franchise.clientclassificationcode,
        address = franchise.address,
        contactnumber = franchise.contactnumber,
        email = franchise.email,
        contactperson = franchise.contactperson,
        contactpersondesignation = franchise.contactpersondesignation,
        signatoryname = franchise.signatoryname,
        signatorydesignation = franchise.signatorydesignation,
        totalmembers = franchise.totalmembers,
        totaldependents = franchise.totaldependents,
        totalemployees = franchise.totalemployees,
        existinghmo = franchise.existinghmo,
        sobtypeid = franchise.sobtypeid,
        meansofknowingid = franchise.meansofknowingid ,
        referredby = franchise.referredby,
        franchisestatusid = franchise.franchisestatusid,
        disapprovalreason = franchise.disapprovalreason,
        istpa = franchise.istpa,
        adminfee = franchise.adminfee,
        networkaccessfee = franchise.networkaccessfee,
        locationcode = franchise.locationcode,
        remarks = franchise.remarks,
        status=franchise.status,
        transactby=franchise.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()
