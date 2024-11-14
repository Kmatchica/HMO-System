from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from department_app.models import department,historydepartment
from roles_app.models import roles, historyroles
from .models import User
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm
from django.http import JsonResponse
from department_app.models import department
from roles_app.models import roles
from permission_app.models import permission
from login_app.models import User, historylogin
from access_app.models import access, historyaccess
from django.contrib.auth.decorators import login_required
from modulelist_app.models import moduleslist, historymoduleslist
from django.conf import settings
import importlib
from django.urls import URLPattern, URLResolver
from datetime import datetime
from django.db.models import Max
from django.contrib import messages
from django.db.models.functions import Upper

###################################### login User ########################################
def login_user(request):
    if not User.objects.exists():
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        status='Active'
        departmentcode_max = department.objects.all().aggregate(Max('departmentcode'))
        departmentcode_nextvalue = 1 if departmentcode_max['departmentcode__max'] == None else departmentcode_max['departmentcode__max'] + 1
        Department = department(departmentcode=departmentcode_nextvalue, departmentname="Admin", departmentshortname="admin",transactby=transactby,transactdate=transactdate,transactype=transactype)
        Department.save()
        departmenthistory_save(Department, transactype)


    # Create a Access List
        access_list = [
            access(accesscode=1, accessname="List" ,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            access(accesscode=2, accessname="Edit",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            access(accesscode=3, accessname="Add",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            access(accesscode=4, accessname="View",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            access(accesscode=5, accessname="Delete",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            access(accesscode=6, accessname="Approver",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            ]
        for acc in access_list:
                if not access.objects.filter(accesscode=acc.accesscode).exists():
                    acc.save()
                    acesshistory_save(acc, transactype)

    # Create a Modulelist
        
        modules_list = [
            moduleslist(modulecode=1, modulename="Access", moduleshortname="Access", moduleappname="access_app"  ,transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            moduleslist(modulecode=2, modulename="Modulelist", moduleshortname="Modulelist", moduleappname="modulelist_app",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            moduleslist(modulecode=3, modulename="Login", moduleshortname="Login", moduleappname="login_app",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            moduleslist(modulecode=4, modulename="Roles", moduleshortname="Roles", moduleappname="roles_app",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            moduleslist(modulecode=5, modulename="Permission", moduleshortname="Permission", moduleappname="permission_app",transactby=transactby,transactdate=transactdate,transactype=transactype, status=status),
            
            ]
        for modules in modules_list:
                if not moduleslist.objects.filter(modulecode=modules.modulecode).exists():
                    modules.save()
                    modulelisthistory_save(modules, transactype)
        # Create a roles    
        moduless = moduleslist.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])
        dataaccess = access.objects.exclude(transactype__in=['delete', 'suspend', 'terminate'])                              
        roleid_max = roles.objects.all().aggregate(Max('roleid'))
        roleid_nextvalue = 1 if roleid_max['roleid__max'] == None else roleid_max['roleid__max'] + 1 
        data = roles(roleid=roleid_nextvalue,rolename="Admin", roledisplayname="Admin", roledescription="Admin",transactby=transactby,transactdate=transactdate,transactype=transactype,status="Active")
        data.save()
        roleshistory_save(data, transactype) 
        for module in moduless:
            for codeaccess in dataaccess:
             permission_save(roleid_nextvalue, module.modulecode, codeaccess.accesscode)
                 

        department_instance = department.objects.get(departmentcode=departmentcode_nextvalue)
        roles_instance = roles.objects.get(roleid=roleid_nextvalue)
        user = User.objects.create_user(userid= '1',username = 'Joel', email='payatas.joel.cct@gmail.com', password='testing', first_name="Joel", middle_name="Pineda", last_name="Sandoval", contact_number="09551173169",departmentcode=department_instance,roleid=roles_instance,transactby="0",transactdate=datetime.now(),transactype='add',status='Active'  )
        user.save()
        loginhistory_save(user,transactype)
        return redirect('login')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if the user is active
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Your account is inactive.')
                return redirect('login')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required
def home(request):
    if request.user.is_authenticated:  
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        dataaccess = access.objects.all()
        moduless= moduleslist.objects.all()
        installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
        installed_apps = [app for app in installed_apps if moduless.filter(moduleappname=app).exists()]
        url_names = {}
        for app in installed_apps:
            try:
                module = importlib.import_module(f'{app}.urls')
                urlpatterns = getattr(module, 'urlpatterns')
                app_url_names = []
                for p in urlpatterns:
                    if isinstance(p, URLPattern):
                        if p.name and ('_insert' in p.name or '_show' in p.name):
                            app_url_names.append(p.name)
                    elif isinstance(p, URLResolver):
                        for q in p.url_patterns:
                            if q.name and ('_insert' in q.name or '_show' in q.name):
                                app_url_names.append(q.name)
                url_names[app] = app_url_names
            except ImportError:
                pass
        context = {
            
            'userRoleid': userRoleid,
            'permissions': permissions,
            'moduless': moduless,
            'dataaccess': dataaccess,
            'url_names': url_names,
            'installed_apps': installed_apps
        }
        return render(request, 'home.html', context)
    return redirect('login')


###################################### user creation ########################################
@login_required
def login_insert(request):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['ADD', 'Add', 'Insert', 'INSERT']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                departments = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                roless = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])                     
                if request.method == 'POST':
                    username = request.POST['username']
                    email = request.POST['email']
                    first_name = request.POST['first_name'].strip().replace("  ", " ").title()
                    middle_name = request.POST['middle_name'].strip().replace("  ", " ").title()
                    last_name = request.POST['last_name'].strip().replace("  ", " ").title()
                    contact_number = request.POST['contact_number']
                    departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                    roleid = roles.objects.get(roleid=request.POST['roleid'])
                    password = request.POST['password']
                    password2 = request.POST['password']
                    remarks = request.POST['remarks']
                    Status = 'Active'
                    status = 'For Approval'
                    transactby = userRoleid
                    transactype = 'add'
                    Transactypes = 'Forapproval' 
                    transactdate = datetime.now()
                    if password == password2:
                        if User.objects.filter(username=username).exists():
                            return render(request, 'login_insert.html', {'error': 'Username already exists','departments':departments, 'roless':roless})
                        elif User.objects.filter(email=email).exists():
                            return render(request, 'login_insert.html', {'error': 'Email already exists','departments':departments, 'roless':roless})
                        elif User.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name).exists():
                            return render(request, 'login_insert.html', {'error': 'User with the entered first name, middle name, and last name already exists','departments':departments, 'roless':roless})
                        else:
                            userid_max = User.objects.all().aggregate(Max('userid'))
                            userid_nextvalue = 1 if userid_max['userid__max'] == None else userid_max['userid__max'] + 1
                            if User.objects.annotate(uppercase_firstname=Upper('first_name'), uppercase_middlename=Upper('middle_name'), uppercase_lastname=Upper('last_name')).filter(uppercase_firstname=first_name.upper(), uppercase_middlename=middle_name.upper(), uppercase_lastname=last_name.upper()):
                                messages.error(request, "The User is already Exist.")  
                            else:
                                userRoleid = request.user.roleid
                                userRoleid = userRoleid.roleid  
                                permissions = permission.objects.filter(roleid=userRoleid)
                                modulelist = moduleslist.objects.filter(moduleappname='login_app')  
                                modulecodes = [module.modulecode for module in modulelist]
                                permissions = permissions.filter(modulecode__in=modulecodes)
                                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                                permissions = permissions.filter(accesscode__in=accesscodes)
                                holder_values = [permission.holder for permission in permissions]
                                if holder_values:
                                    if holder_values[0] == 1:
                                        user = User.objects.create_user(username=username, email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact_number, departmentcode=departmentcode, roleid=roleid,userid=userid_nextvalue,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=Status)
                                        user.set_password(password)
                                        user.save()
                                        loginhistory_save(user, transactype)
                                        return redirect('login_show')
                                    else:
                                        if historylogin.objects.annotate(uppercase_firstname=Upper('first_name'), uppercase_middlename=Upper('middle_name'), uppercase_lastname=Upper('last_name')).filter(uppercase_firstname=first_name.upper(), uppercase_middlename=middle_name.upper(), uppercase_lastname=last_name.upper(),transactype='Forapproval'):
                                            messages.error(request, "The User is already Exist.") 
                                        else:   
                                            Logincode_max = historylogin.objects.all().aggregate(Max('recordnohist')) 
                                            Logincode_nextvalue = 1 if Logincode_max['recordnohist__max'] == None else Logincode_max['recordnohist__max']+ 1
                                            recordnohist_max = historylogin.objects.all().aggregate(Max('recordnohist')) 
                                            recordno_nextvalue = 1 if recordnohist_max['recordnohist__max'] == None else recordnohist_max['recordnohist__max']+ 1
                                            data = historylogin(recordno=recordno_nextvalue,username=username, email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact_number, departmentcode=departmentcode, roleid=roleid,userid=Logincode_nextvalue,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=Transactypes,status=status,password=password)
                                            data.save()
                                            return redirect('login_show')
                                        return render(request, 'login_insert.html', {'departments': departments,'roless': roless})
                    
                                return redirect('login_insert')              
                            return render(request, 'login_insert.html', {'departments': departments,'roless': roless})
                    
                    return render(request, 'login_insert.html', {'error': 'Passwords do not match','departments':departments, 'roless':roless})
                else:
                    return render(request, 'login_insert.html', {'departments': departments,'roless': roless})
            return redirect('home')
        return redirect('home')
    return redirect(request, 'login.html')            

    #####################################
def permission_save(roleCodes, moduleCode, accessCode):

    data = permission(
        roleid = roleCodes,
        modulecode = moduleCode,
        accesscode = accessCode,
        holder = 1
    )
    data.save()


@login_required
def login_delete(request, pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['DELETE', 'Delete','Remove', 'REMOVE']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                users = User.objects.get(recordno=pk)
                transactype = 'Terminate'
                users.transactby = userRoleid
                users.transactdate = datetime.now()       
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='login_app')  
                modulecodes = [module.modulecode for module in modulelist]
                permissions = permissions.filter(modulecode__in=modulecodes)
                accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                permissions = permissions.filter(accesscode__in=accesscodes)
                holder_values = [permission.holder for permission in permissions]
                if holder_values:
                    if holder_values[0] == 1:
                            if request.method == 'POST':
                                users.transactby = userRoleid
                                users.transactdate = datetime.now()
                                users.transactype = transactype
                                users.status = 'Deactive'
                                users.is_active = 'False'
                                users.save()
                                loginhistory_save(users, transactype)
                                return redirect('login_show') 
                            return render(request, 'login_delete.html', {'users': users,})                                           
                    else:
                        
                        users.status = 'Deactive'
                        users.save()
                        recordno = pk
                        userid = users.userid
                        username = users.username
                        email = users.email
                        first_name = users.first_name
                        middle_name = users.middle_name
                        last_name = users.last_name
                        contact_number = users.contact_number
                        departmentcode = users.departmentcode
                        roleid = users.roleid
                        password = users.password
                        remarks = users.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status = 'For Terminate'
                        transactypes = 'Forterminate'
                        transactby = userRoleid
                        transactdate = datetime.now()
                        data = historylogin(recordno=recordno,username=username, email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact_number, departmentcode=departmentcode, roleid=roleid,userid=userid,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status,password=password)                   
                        data.save() 
                        loginhistory_save(data, transactype)
                        return redirect('login_show')
                    
                return redirect('home')
            else:   
             return redirect('login') 
        else:
         return redirect('home') 
    return redirect('login') 
###################################### user terminate ########################################
@login_required
def login_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historylogin = historylogin.objects.get(recordnohist=pk)
                users = User.objects.get(recordno=Historylogin.recordno)
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historylogin.transactype = 'Approve'
                            Historylogin.status = 'Approve'
                            Historylogin.save()  
                            users.transactype = 'edit'
                            users.status = 'Active'
                            users.save()            
                    else:
                        Historylogin.transactype = 'Terminate'
                        Historylogin.status = 'Terminate'
                        Historylogin.save()  
                        users.transactype = 'Terminate'
                        users.status = 'Terminate'
                        users.is_active = 'False'
                        users.save()                
                    return redirect('login_show')
                return render(request,'login_terminate.html',{'Historylogin': Historylogin})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  



@login_required
def login_terminate(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historylogin = historylogin.objects.get(recordnohist=pk)
                users = User.objects.get(recordno=Historylogin.recordno)
                Department = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])                     
                
                if request.method == 'POST':
                    if 'Disapprove' in request.POST:
                        if 'Disapprove' in request.POST:
                            Historylogin.transactype = 'Approve'
                            Historylogin.status = 'Approve'
                            Historylogin.save()  
                            users.transactype = 'edit'
                            users.status = 'Active'
                            users.save()            
                    else:
                        Historylogin.transactype = 'Terminate'
                        Historylogin.status = 'Terminate'
                        Historylogin.save()  
                        users.transactype = 'Terminate'
                        users.status = 'Terminate'
                        users.save()                
                    return redirect('login_show')
                return render(request,'login_terminate.html',{'Historylogin': Historylogin,'Department': Department,'Roles': Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')  

##################################### User approval ########################################
@login_required
def login_approval(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historylogin = historylogin.objects.get(recordnohist=pk)
                Department = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                transactype = 'add'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historylogin.transactype = 'Disapprove'
                            Historylogin.status = 'Disapprove'
                            Historylogin.save()             
                    else:
                        userid = Historylogin.userid
                        username = Historylogin.username
                        email = Historylogin.email
                        first_name = Historylogin.first_name
                        middle_name = Historylogin.middle_name
                        last_name = Historylogin.last_name
                        contact_number = Historylogin.contact_number
                        departmentcode = Historylogin.departmentcode
                        roleid = Historylogin.roleid
                        password = Historylogin.password
                        remarks = Historylogin.remarks
                        transactby = userRoleid
                        transactdate = datetime.now()                           
                        transactype = transactype
                        status='Active'
                        user = User.objects.create_user(username=username, email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact_number, departmentcode=departmentcode, roleid=roleid,userid=userid,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactype,status=status)
                        user.set_password(password)
                        user.save()                       
                        Historylogin.status = 'Approve'
                        Historylogin.transactype = 'Approve'
                        Historylogin.save()                  
                    return redirect('login_show')               
                return render(request,'login_approval.html',{'Historylogin': Historylogin,'Department':Department, 'Roles':Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    

##################################### User edited ########################################
@login_required
def login_edited(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['approver','Approver']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1: 
                Historylogin = historylogin.objects.get(recordnohist=pk)
                users = User.objects.get(recordno=Historylogin.recordno)
                Department = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                
                transactype = 'edit'
                if request.method == 'POST':
                    if 'delete' in request.POST:
                        if 'delete' in request.POST:
                            Historylogin.transactype = 'Disapprove'
                            Historylogin.status = 'Disapprove'
                            Historylogin.save()             
                    else:
                       
                        users.userid = Historylogin.userid
                        users.username = Historylogin.username
                        users.email = Historylogin.email
                        users.first_name = Historylogin.first_name
                        users.middle_name = Historylogin.middle_name
                        users.last_name = Historylogin.last_name
                        users.contact_number = Historylogin.contact_number
                        users.departmentcode = Historylogin.departmentcode
                        users.roleid = Historylogin.roleid
                        users.remarks = Historylogin.remarks
                        users.transactby = userRoleid
                        users.transactdate = datetime.now()                           
                        transactype = transactype
                        users.status = 'Active'
                        users.save() 
                        Historylogin.status = 'Approve'
                        Historylogin.transactype = 'Approve'
                        Historylogin.save()               
                    return redirect('login_show')
                return render(request,'login_edited.html',{'Historylogin': Historylogin,'users': users,'Department':Department, 'Roles':Roles})       
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')    


###################################### logout User ####################################### 
def logout_user(request):
    logout(request)
    return redirect('login')
###################################### change password #######################################
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('change_password_done')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

def change_password_done(request):
    return render(request,'change_password_done.html')

##################################### Login Show #########################################
@login_required
def login_show(request):
    if request.user.is_authenticated:   
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        Permissions = permission.objects.filter(roleid=userRoleid)
        dataaccess = access.objects.all()
        moduless= moduleslist.objects.all()
        installed_apps = [app for app in settings.INSTALLED_APPS if '_app' in app]
        installed_apps = [app for app in installed_apps if moduless.filter(moduleappname=app).exists()]
        url_names = {}
        for app in installed_apps:
            try:
                module = importlib.import_module(f'{app}.urls')
                urlpatterns = getattr(module, 'urlpatterns')
                app_url_names = []
                for p in urlpatterns:
                    if isinstance(p, URLPattern):
                        if p.name and ('_insert' in p.name or '_show' in p.name):
                            app_url_names.append(p.name)
                    elif isinstance(p, URLResolver):
                        for q in p.url_patterns:
                            if q.name and ('_insert' in q.name or '_show' in q.name):
                                app_url_names.append(q.name)
                url_names[app] = app_url_names
            except ImportError:
                pass  
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['LIST', 'List','View', 'SHOW']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                users = User.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                historyupdate = historylogin.objects.filter(transactype__in=['Forupdate'])
                historyterminate = historylogin.objects.filter(transactype__in=['Forterminate'])
                historyapproval= historylogin.objects.filter(transactype__in=['Forapproval'])
                userRoleid = request.user.roleid
                userRoleid = userRoleid.roleid
                permissions = permission.objects.filter(roleid=userRoleid)
                modulelist = moduleslist.objects.filter(moduleappname='login_app')  
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
                                                                                          
                return render(request, 'login_show.html', {
                'show_edit_button': show_edit_button,
                'show_delete_button': show_delete_button,
                'show_insert_button': show_insert_button,
                'show_view_button': show_view_button,
                'users': users,
                'historyapproval': historyapproval,
                'historyupdate': historyupdate,
                'historyterminate': historyterminate,
                'Permissions': Permissions,
                'dataaccess': dataaccess,
                'moduless': moduless,
                'url_names': url_names,
                'installed_apps': installed_apps
                })
            else:
             return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')

#################################### edit user ##############################################
@login_required
def login_edit(request,pk):
    if request.user.is_authenticated:
        userRoleid = request.user.roleid
        userRoleid = userRoleid.roleid
        permissions = permission.objects.filter(roleid=userRoleid)
        modulelist = moduleslist.objects.filter(moduleappname='login_app')  
        modulecodes = [module.modulecode for module in modulelist]
        permissions = permissions.filter(modulecode__in=modulecodes)
        accesscodes = access.objects.filter(accessname__in=['EDIT', 'Edit','UPDATE', 'Update']).values_list('accesscode', flat=True)
        permissions = permissions.filter(accesscode__in=accesscodes)
        holder_values = [permission.holder for permission in permissions]
        if holder_values:
            if holder_values[0] == 1:
                Department = department.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                Roles = roles.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove'])
                users = User.objects.get(recordno=pk)
                transactype = 'Edit'
                if request.method == 'POST':
                    print(request.POST)
                    users.username = request.POST['username']
                    users.email = request.POST['email']
                    users.first_name = request.POST['first_name'].strip().replace("  ", " ").title()
                    users.middle_name = request.POST['middle_name'].strip().replace("  ", " ").title()
                    users.last_name = request.POST['last_name'].strip().replace("  ", " ").title()
                    users.contact_number = request.POST['contact_number']
                    users.departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                    users.roleid = roles.objects.get(roleid=request.POST['roleid'])
                    users.remarks = request.POST['remarks']
                    users.transactby = userRoleid
                    users.transactdate = datetime.now()       
                    permissions = permission.objects.filter(roleid=userRoleid)
                    modulelist = moduleslist.objects.filter(moduleappname='login_app')  
                    modulecodes = [module.modulecode for module in modulelist]
                    permissions = permissions.filter(modulecode__in=modulecodes)
                    accesscodes = access.objects.filter(accessname__in=['approver', 'Approver']).values_list('accesscode', flat=True)
                    permissions = permissions.filter(accesscode__in=accesscodes)
                    holder_values = [permission.holder for permission in permissions]
                    if holder_values:
                        if holder_values[0] == 1:
                            users.transactype = transactype
                            users.save()  
                            loginhistory_save(users,transactype) 
                            return redirect('login_show')
                        else:
                            recordno = pk
                            userid=users.userid
                            username = request.POST['username']
                            email = request.POST['email']
                            first_name = request.POST['first_name'].strip().replace("  ", " ").title()
                            middle_name = request.POST['middle_name'].strip().replace("  ", " ").title()
                            last_name = request.POST['last_name'].strip().replace("  ", " ").title()
                            contact_number = request.POST['contact_number']
                            departmentcode = department.objects.get(departmentcode=request.POST['departmentcode'])
                            roleid = roles.objects.get(roleid=request.POST['roleid'])
                            remarks = request.POST['remarks']
                            status = 'For Update'
                            transactypes = 'Forupdate'
                            transactby = userRoleid
                            transactdate = datetime.now()
                            data = historylogin(userid=userid,recordno=recordno,username=username, email=email, first_name=first_name, middle_name=middle_name, last_name=last_name, contact_number=contact_number, departmentcode=departmentcode, roleid=roleid,remarks=remarks,transactby=transactby,transactdate=transactdate,transactype=transactypes,status=status)
                            data.save()                       
                        return redirect('login_show')         
                    return redirect('home')   
                return render(request,'login_edit.html',{'users':users,'Department':Department, 'Roles':Roles})       
            else:
                return redirect('home')
        else:
         return redirect('home') 
    return redirect('login')



########################################
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

def acesshistory_save(obj, transactype):
    acess = obj
    data = historyaccess(
        recordno=acess.recordno,
        accesscode=acess.accesscode,
        accessname=acess.accessname,
        remarks=acess.remarks,
        status=acess.status,
        transactby=acess.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()    

def modulelisthistory_save(obj, transactype):
    moduleslist = obj
    data = historymoduleslist(
        recordno=moduleslist.recordno,
        modulecode=moduleslist.modulecode,
        modulename=moduleslist.modulename,
        moduleshortname=moduleslist.moduleshortname,
        moduleappname=moduleslist.moduleappname,
        status=moduleslist.status,
        transactby=moduleslist.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()

def roleshistory_save(obj, transactype):
    roles = obj
    data = historyroles(
        recordno=roles.recordno,
        roleid=roles.roleid,
        rolename=roles.rolename,
        roledisplayname=roles.roledisplayname,
        roledescription=roles.roledescription,
        transactby=0,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()

def loginhistory_save(obj, transactype):
    User = obj
    data = historylogin(
        recordno=User.recordno,
        userid= User.userid,
        username = User.username,
        first_name = User.first_name,
        middle_name = User.middle_name,
        last_name = User.last_name,
        email = User.email,
        departmentcode = User.departmentcode,
        roleid = User.roleid,
        contact_number = User.contact_number,
        mobile_number = User.mobile_number,
        street_address = User.street_address,
        location = User.location,
        region = User.region,
        province = User.province,
        city = User.city,
        barangay = User.barangay,
        postal = User.postal,
        status = User.status,
        remarks = User.remarks,
        transactby=User.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()