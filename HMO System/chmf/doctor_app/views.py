from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from .models import doctor, historydoctor
from provider_app.models import provider
from providerstatus_app.models import providerstatus
from specialization_app.models import specialization
from datetime import datetime 
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from permission_app.models import permission
from access_app.models import access
from doctorstatus_app.models import doctorstatus
from modulelist_app.models import moduleslist
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.

@login_required
def doctor_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                specializations = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                if request.method == "POST":
                    specializationcode = specialization.objects.get(specializationcode=request.POST['specializationcode'])
                    firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                    middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                    lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                    mobilenumber = request.POST['mobilenumber'].strip().replace("  ", " ")
                    landlinenumber = request.POST['landlinenumber'].strip().replace("  ", " ")
                    emailaddres = request.POST['emailaddres'].strip().replace("  ", " ")
                    address = request.POST['address'].strip().replace("  ", " ").title()
                    locationcode = provider.objects.get(locationcode=request.POST['locationcode'])
                    professionalfee = request.POST['professionalfee']
                    doctorstatuscode = doctorstatus.objects.get(doctorstatuscode=request.POST['doctorstatuscode'])
                    remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                    accreditdate= request.POST['accreditdate']
                    disaccreditdate= request.POST['disaccreditdate']
                    reaccreditdate= request.POST['reaccreditdate']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactdate = datetime.now()
                    transactype = 'add'
                    Transactypes = 'Forapproval'
                    doctorcode_max = doctor.objects.all().aggregate(Max('doctorcode'))
                    doctorcode_nextvalue = 1 if doctorcode_max['doctorcode__max'] == None else doctorcode_max['doctorcode__max'] + 1
                    if doctor.objects.annotate(uppercase_firstname=Upper('firstname'), uppercase_middlename=Upper('middlename'), uppercase_lastname=Upper('lastname')).filter(uppercase_firstname=firstname.upper(), uppercase_middlename=middlename.upper(), uppercase_lastname=lastname.upper()):
                        messages.error(request, "The User is already Exist.")  
                    else:
                        userRoleid = request.user.roleid
                        userRoleid = userRoleid.roleid  
                        permissions = permission.objects.filter(roleid=userRoleid)
                        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
                        modulecodes = [module.modulecode for module in modulelist]
                        permissions = permissions.filter(modulecode__in=modulecodes)
                        accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                        permissions = permissions.filter(accesscode__in=accesscodes)
                        holder_values = [permission.holder for permission in permissions]
                        if holder_values:
                            if holder_values[0] == 1:
                                data = doctor(accreditdate=accreditdate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,doctorcode=doctorcode_nextvalue, specializationcode=specializationcode, firstname=firstname, middlename=middlename, lastname=lastname,  mobilenumber=mobilenumber, landlinenumber=landlinenumber, emailaddres=emailaddres, address=address, locationcode=locationcode, professionalfee=professionalfee, doctorstatuscode=doctorstatuscode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status)
                                data.save()
                                doctorhistory_save(data, transactype)
                                return redirect('doctor_show')
                            else:
                                Doctorcode_max = historydoctor.objects.all().aggregate(Max('recordnohist')) 
                                Doctor_nextvalue = 1 if Doctorcode_max['recordnohist__max'] == None else Doctorcode_max['recordnohist__max']
                                
                                recordnohist_max = historydoctor.objects.all().aggregate(Max('recordnohist')) 
                                recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']
                                data = historydoctor(accreditdate=accreditdate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=Doctor_nextvalue,doctorcode=recordno_nextvalue, specializationcode=specializationcode, firstname=firstname, middlename=middlename, lastname=lastname, mobilenumber=mobilenumber, landlinenumber=landlinenumber, emailaddres=emailaddres, address=address, locationcode=locationcode, professionalfee=professionalfee, doctorstatuscode=doctorstatuscode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactypes,status=status)
                                data.save()
                                return redirect('doctor_show')
                        return redirect('home')              
                    return render(request, 'doctor_insert.html',{'providers':providers, 'specializations':specializations, 'Doctorstatus':Doctorstatus})  
                return render(request, 'doctor_insert.html',{'providers':providers, 'specializations':specializations, 'Doctorstatus':Doctorstatus})  
            else:
                return redirect('home')
        else:
         return redirect('home')
    return redirect(request, 'login.html')  


@login_required
def doctor_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctor = historydoctor.objects.get(recordnohist=pk)
                providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                ProviderStatus = providerstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                specializations = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])                
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctor.transactype = 'Disapprove'
                            Historydoctor.status = 'Disapprove'
                            Historydoctor.save()             
                    else:
                        doctorcode = Historydoctor.doctorcode
                        specializationcode = Historydoctor.specializationcode
                        firstname = Historydoctor.firstname
                        middlename = Historydoctor.middlename
                        lastname = Historydoctor.lastname
                        mobilenumber = Historydoctor.mobilenumber
                        landlinenumber = Historydoctor.landlinenumber
                        emailaddres = Historydoctor.emailaddres
                        address = Historydoctor.address
                        locationcode = Historydoctor.locationcode
                        professionalfee = Historydoctor.professionalfee
                        doctorstatuscode = Historydoctor.doctorstatuscode
                        remarks = Historydoctor.remarks
                        accreditdate= Historydoctor.accreditdate
                        disaccreditdate= Historydoctor.disaccreditdate
                        reaccreditdate= Historydoctor.reaccreditdate
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        data = doctor(accreditdate=accreditdate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,doctorcode=doctorcode, specializationcode=specializationcode, firstname=firstname, middlename=middlename, lastname=lastname, mobilenumber=mobilenumber, landlinenumber=landlinenumber, emailaddres=emailaddres, address=address, locationcode=locationcode, professionalfee=professionalfee, doctorstatuscode=doctorstatuscode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=status)
                        data.save()                       
                        Historydoctor.status = 'Approve'
                        Historydoctor.transactype = 'Approve'
                        Historydoctor.save()                  
                    return redirect('doctor_show')               
                return render(request,'doctor_approval.html',{'Historydoctor': Historydoctor,'providers':providers, 'specializations':specializations, 'ProviderStatus':ProviderStatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


@login_required
def doctor_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                historyupdate = historydoctor.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historydoctor.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historydoctor.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
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
                return render(request, 'doctor_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'Doctor': Doctor,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')


@login_required
def doctor_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                specializations = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctor = doctor.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    Doctor.specializationcode = specialization.objects.get(specializationcode=request.POST['specializationcode'])
                    Doctor.firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                    Doctor.middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                    Doctor.lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                    Doctor.mobilenumber = request.POST['mobilenumber']
                    Doctor.landlinenumber = request.POST['landlinenumber']
                    Doctor.emailaddres = request.POST['emailaddres']
                    Doctor.address = request.POST['address']
                    Doctor.locationcode = provider.objects.get(locationcode=request.POST['locationcode'])
                    Doctor.professionalfee = request.POST['professionalfee']
                    Doctor.doctorstatuscode = doctorstatus.objects.get(doctorstatuscode=request.POST['doctorstatuscode'])
                    Doctor.remarks = request.POST['remarks']
                    Doctor.accreditdate= request.POST['accreditdate']
                    Doctor.disaccreditdate= request.POST['disaccreditdate']
                    Doctor.reaccreditdate= request.POST['reaccreditdate']
                    Doctor.transactby = userRoleid
                    Doctor.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            Doctor.transactype = transactype
                            Doctor.save()  
                            doctorhistory_save(Doctor,transactype) 
                            return redirect('doctor_show')
                        else:
                            recordno = pk
                            doctorcode = Doctor.doctorcode
                            specializationcode = specialization.objects.get(specializationcode=request.POST['specializationcode'])
                            firstname = request.POST['firstname'].strip().replace("  ", " ").title()
                            middlename = request.POST['middlename'].strip().replace("  ", " ").title()
                            lastname = request.POST['lastname'].strip().replace("  ", " ").title()
                            mobilenumber = request.POST['mobilenumber'].strip().replace("  ", " ")
                            landlinenumber = request.POST['landlinenumber'].strip().replace("  ", " ")
                            emailaddres = request.POST['emailaddres'].strip().replace("  ", " ")
                            address = request.POST['address'].strip().replace("  ", " ").title()
                            locationcode = provider.objects.get(locationcode=request.POST['locationcode'])
                            professionalfee = request.POST['professionalfee']
                            doctorstatuscode = doctorstatus.objects.get(doctorstatuscode=request.POST['doctorstatuscode'])
                            remarks = request.POST['remarks'].strip().replace("  ", " ").title()
                            accreditdate= request.POST['accreditdate']
                            disaccreditdate= request.POST['disaccreditdate']
                            reaccreditdate= request.POST['reaccreditdate']
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historydoctor(accreditdate=accreditdate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=recordno,doctorcode=doctorcode, specializationcode=specializationcode, firstname=firstname, middlename=middlename, lastname=lastname, mobilenumber=mobilenumber, landlinenumber=landlinenumber, emailaddres=emailaddres, address=address, locationcode=locationcode, professionalfee=professionalfee, doctorstatuscode=doctorstatuscode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status)
                            data.save()                       
                        return redirect('doctor_show')         
                    return redirect('doctor_show')   
                return render(request,'doctor_edit.html',{'Doctor':Doctor, 'providers':providers, 'specializations':specializations, 'Doctorstatus':Doctorstatus})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

@login_required
def doctor_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historydoctor = historydoctor.objects.get(recordnohist=pk)
                Doctor = doctor.objects.get(recordno=Historydoctor.recordno)
                providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                specializations = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historydoctor.transactype = 'Disapprove'
                            Historydoctor.status = 'Disapprove'
                            Historydoctor.save()             
                    else:
                        Doctor.doctorcode = Historydoctor.doctorcode
                        Doctor.specializationcode = Historydoctor.specializationcode
                        Doctor.firstname = Historydoctor.firstname
                        Doctor.middlename = Historydoctor.middlename
                        Doctor.lastname = Historydoctor.lastname
                        Doctor.mobilenumber = Historydoctor.mobilenumber 
                        Doctor.landlinenumber = Historydoctor.landlinenumber
                        Doctor.emailaddres = Historydoctor.emailaddres
                        Doctor.address = Historydoctor.address
                        Doctor.locationcode = Historydoctor.locationcode
                        Doctor.professionalfee = Historydoctor.professionalfee
                        Doctor.doctorstatuscode = Historydoctor.doctorstatuscode
                        Doctor.remarks = Historydoctor.remarks
                        Doctor.accreditdate= Historydoctor.accreditdate
                        Doctor.disaccreditdate= Historydoctor.disaccreditdate
                        Doctor.reaccreditdate= Historydoctor.reaccreditdate
                        Doctor.transactby = userRoleid
                        Doctor.transactdate = datetime.now()                           
                        Doctor.transactype = transactype
                        Doctor.status = 'Active'
                        Doctor.save() 
                        Historydoctor.status = 'Approve'
                        Historydoctor.transactype = 'Approve'
                        Historydoctor.save()               
                    return redirect('doctor_show')
                return render(request,'doctor_edited.html',{'Historydoctor': Historydoctor,'Doctor': Doctor,'providers':providers, 'specializations':specializations, 'Doctorstatus':Doctorstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')     

@login_required
def doctor_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                Doctor = doctor.objects.get(recordno=pk)

                transactype = 'Terminate'
                Doctor.transactby = userRoleid
                Doctor.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                        if request.method == 'POST':
                            Doctor.transactby = userRoleid
                            Doctor.transactdate = datetime.now()
                            Doctor.transactype = transactype
                            Doctor.status = 'Deactive'
                            Doctor.save()
                            doctorhistory_save(Doctor, transactype)
                            return redirect('doctor_show')                                             
                    else:                       
                        Doctor.status = 'Deactive'
                        Doctor.save()
                        recordno = pk
                        doctorcode = Doctor.doctorcode
                        specializationcode = Doctor.specializationcode
                        firstname = Doctor.firstname
                        middlename = Doctor.middlename
                        lastname = Doctor.lastname
                        mobilenumber = Doctor.mobilenumber 
                        landlinenumber = Doctor.landlinenumber
                        emailaddres = Doctor.emailaddres
                        address = Doctor.address
                        locationcode = Doctor.locationcode
                        professionalfee = Doctor.professionalfee
                        doctorstatuscode = Doctor.doctorstatuscode
                        accreditdate= Doctor.accreditdate
                        disaccreditdate= Doctor.disaccreditdate
                        reaccreditdate= Doctor.reaccreditdate
                        remarks = Doctor.remarks
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historydoctor(accreditdate=accreditdate,disaccreditdate=disaccreditdate,reaccreditdate=reaccreditdate,recordno=recordno,doctorcode=doctorcode, specializationcode=specializationcode, firstname=firstname, middlename=middlename, lastname=lastname,  mobilenumber=mobilenumber, landlinenumber=landlinenumber, emailaddres=emailaddres, address=address, locationcode=locationcode, professionalfee=professionalfee, doctorstatuscode=doctorstatuscode,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status)
                        data.save()  
                        
                        return redirect('doctor_show')
                    return render(request, 'doctor_delete.html', {'Doctor': Doctor,})
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 

@login_required
def doctor_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='doctor_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver'],status__in=['Active']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Doctorstatus = doctorstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                specializations = specialization.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Historydoctor = historydoctor.objects.get(recordnohist=pk)
                Doctor = doctor.objects.get(recordno=Historydoctor.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historydoctor.transactype = 'Approve'
                            Historydoctor.status = 'Approve'
                            Historydoctor.save()  
                            Doctor.transactype = 'edit'
                            Doctor.status = 'Active'
                            Doctor.save()            
                    else:
                        Historydoctor.transactype = 'Terminate'
                        Historydoctor.status = 'Terminate'
                        Historydoctor.save()  
                        Doctor.transactype = 'Terminate'
                        Doctor.status = 'Terminate'
                        Doctor.save()                
                    return redirect('doctor_show')
                return render(request,'doctor_terminate.html',{'Historydoctor': Historydoctor,'Doctor': Doctor,'providers':providers, 'specializations':specializations, 'Doctorstatus':Doctorstatus})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

def doctorhistory_save(obj, transactype):
    doctor = obj
    data = historydoctor(
        recordno=doctor.recordno,
        doctorcode=doctor.doctorcode,
        specializationcode=doctor.specializationcode,
        firstname=doctor.firstname,
        middlename=doctor.middlename,
        lastname=doctor.lastname,
        mobilenumber=doctor.mobilenumber,
        landlinenumber=doctor.landlinenumber,
        emailaddres=doctor.emailaddres,
        address=doctor.address,
        locationcode=doctor.locationcode,
        professionalfee=doctor.professionalfee,
        doctorstatuscode=doctor.doctorstatuscode,
        remarks=doctor.remarks,
        status=doctor.status,
        transactby=doctor.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()