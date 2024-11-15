from django.shortcuts import render, redirect
from datetime import datetime
from .models import member, historymember
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
from membergender_app.models import membergender
from memberstatus_app.models import memberstatus
from utils.utils import generate_code, generate_policy_number
from client_app.models import client
# Create your views here.
########################## new function##################### 



def memberinsert(request):   
    memberStatus = memberstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    memberGender = membergender.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == "POST":
        membercode = generate_code(member, 'membercode', padding_width=6)
        policynumber = generate_policy_number(request.POST['clientcode'], membercode)
        thirdpartyid = request.POST['thirdpartyid'].strip().replace("  ", " ").title()
        otherid = request.POST['otherid'].strip().replace("  ", " ").title()
        clientcode = client.objects.get(clientcode=request.POST['clientcode'])
        branchcode = int(request.POST['branchcode'])
        membertypecode = int(request.POST['membertypecode'])
        lastname = request.POST['lastname'].strip().replace("  ", " ").title()
        firstname = request.POST['firstname'].strip().replace("  ", " ").title()
        middlename = request.POST['middlename'].strip().replace("  ", " ").title()
        birthdate = request.POST['birthdate']
        enrollage = int(request.POST['enrollage'])
        gendercode = membergender.objects.get(membergendercode=request.POST['gendercode'])
        civilstatuscode = int(request.POST['civilstatuscode'])
        effectivedate = request.POST['effectivedate']
        expirydate = request.POST['expirydate']
        renewaldate = request.POST['renewaldate']
        reinstateddate = request.POST['reinstateddate']
        cancellationdate = request.POST['cancellationdate']
        statuscode = memberstatus.objects.get(memberstatuscode=request.POST['statuscode'])
        hib = int(request.POST['hib'])
        covid = int(request.POST['covid'])
        tin = request.POST['tin'].strip().replace("  ", " ").title()
        address = request.POST['address'].strip().replace("  ", " ").title()
        locationcode = int(request.POST['locationcode'])
        contactnumber = request.POST['contactnumber'].strip().replace("  ", " ").title()
        emailaddress = request.POST['emailaddress'].strip().replace("  ", " ").title()
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        membercode = generate_code(member, 'membercode', padding_width=6)
        if member.objects.annotate(uppercase_membername=Upper('firstname')).filter(uppercase_membername=firstname.upper()):
            if member.objects.annotate(uppercase_membername=Upper('middlename')).filter(uppercase_membername=middlename.upper()):
                if member.objects.annotate(uppercase_membername=Upper('lastname')).filter(uppercase_membername=lastname.upper()):
                    messages.error(request, "Member Status Name already Exist.") 
        else:
            data = member(
                            membercode = membercode, 
                            policynumber = policynumber,
                            thirdpartyid = thirdpartyid,
                            otherid = otherid,
                            clientcode = clientcode,
                            branchcode = branchcode,
                            membertypecode = membertypecode,
                            lastname = lastname,
                            firstname = firstname,
                            middlename = middlename,
                            birthdate = birthdate,
                            enrollage = enrollage,
                            gendercode = gendercode,
                            civilstatuscode = civilstatuscode,
                            effectivedate = effectivedate,
                            expirydate = expirydate,
                            renewaldate = renewaldate,
                            reinstateddate = reinstateddate,
                            cancellationdate = cancellationdate,
                            statuscode = statuscode,
                            hib = hib,
                            covid = covid,
                            tin = tin,
                            address = address,
                            locationcode = locationcode,
                            contactnumber = contactnumber,
                            emailaddress = emailaddress,
                            remarks = remarks,
                            transactby=transactby,transactdate=transactdate,
                            transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD']
                        )
            data.save()
            historymember_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('/member')    
        return render(request, 'memberinsert.html', {'memberGender': memberGender, 'memberStatus': memberStatus, 'Clients' : Clients})  
    return render(request, 'memberinsert.html', {'memberGender': memberGender, 'memberStatus': memberStatus, 'Clients' : Clients})  

def membershow(request):
    Members = member.objects.exclude(transactype = 'delete')
    return render(request,'membershow.html', {'memberList':Members})
def memberedit(request,pk):
    Member = member.objects.get(recordno=pk)
    memberStatus = memberstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    memberGender = membergender.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == 'POST':
            print(request.POST)
            Member.policynumber = request.POST['policynumber']
            Member.thirdpartyid = request.POST['thirdpartyid']
            Member.otherid = request.POST['otherid']
            Member.clientcode = request.POST['clientcode']
            Member.branchcode = request.POST['branchcode']
            Member.membertypecode = request.POST['membertypecode']
            Member.lastname = request.POST['lastname']
            Member.firstname = request.POST['firstname']
            Member.middlename = request.POST['middlename']
            Member.birthdate = request.POST['birthdate']
            Member.enrollage = request.POST['enrollage']
            Member.gendercode = membergender.objects.get(membergendercode=request.POST['gendercode'])
            Member.civilstatuscode = request.POST['civilstatuscode']
            Member.effectivedate = request.POST['effectivedate']
            Member.expirydate = request.POST['expirydate']
            Member.renewaldate = request.POST['renewaldate']
            Member.reinstateddate = request.POST['reinstateddate']
            Member.cancellationdate = request.POST['cancellationdate']
            Member.statuscode = memberstatus.objects.get(memberstatuscode=request.POST['statuscode'])
            Member.hib = request.POST['hib']
            Member.covid = request.POST['covid']
            Member.tin = request.POST['tin']
            Member.address = request.POST['address']
            Member.locationcode = request.POST['locationcode']
            Member.contactnumber = request.POST['contactnumber']
            Member.emailaddress = request.POST['emailaddress']
            Member.remarks = request.POST['remarks']
            Member.save()  
            historymember_save(Member, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('/member')

    return render(request,'memberedit.html', {'member' : Member, 'memberStatus':memberStatus, 'memberGender' : memberGender, 'Clients' : Clients})

def memberdelete(request, pk):
    Member = member.objects.get(recordno=pk)

    if request.method == 'POST':
        Member.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        Member.save()
        historymember_save(Member, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('/member')

    context = {
        'member': Member,
    } 

    return render(request, 'memberdelete.html', context)

def historymember_save(obj, transactype):
    member = obj
    data = historymember(
        recordno=member.recordno,
        membercode=member.membercode,
        policynumber=member.policynumber,
        thirdpartyid=member.thirdpartyid,
        otherid=member.otherid,
        clientcode=member.clientcode,
        branchcode=member.branchcode,
        membertypecode=member.membertypecode,
        lastname=member.lastname,
        firstname=member.firstname,
        middlename=member.middlename,
        birthdate=member.birthdate,
        enrollage=member.enrollage,
        gendercode=member.gendercode,
        civilstatuscode=member.civilstatuscode,
        effectivedate=member.effectivedate,
        expirydate=member.expirydate,
        renewaldate=member.renewaldate,
        reinstateddate=member.reinstateddate,
        cancellationdate=member.cancellationdate,
        statuscode=member.statuscode,
        hib=member.hib,
        covid=member.covid,
        tin=member.tin,
        address=member.address,
        locationcode=member.locationcode,
        contactnumber=member.contactnumber,
        emailaddress=member.emailaddress,
        remarks=member.remarks,
        transactby=member.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()