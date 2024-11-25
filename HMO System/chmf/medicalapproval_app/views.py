from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
from .models import approval, historyapproval, member, historymember, availmentstatus, availmenttype, doctor, provider, diagnosis
from utils.models import CodeCounter
from utils.utils import generate_approval_code, generate_code, increment_counter
# Create your views here.
########################## new function##################### 


def approvalinsert(request):  
    policyNumbers = member.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    # historymemberList = historymember.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Doctors = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    diagnosisList = diagnosis.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])

    availmentstatusList = availmentstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    availmenttypeList = availmenttype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == "POST":
        status = request.POST['status']
        status_prefix = "1C" if status == "Approved" else "1D"
        approvalcode = increment_counter(status_prefix)
        policynumber = member.objects.get(policynumber=request.POST['policynumber'])
        # memberrecordnohist = historymember.objects.get(memberrecordnohist=request.POST['memberrecordnohist'])
        availmentdate = request.POST['availmentdate']
        providercode = provider.objects.get(providercode=request.POST['providercode'])
        doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
        callername = request.POST['callername'].strip().replace("  ", " ").title()
        availmenttypecode = availmenttype.objects.get(availmenttypecode=request.POST['availmenttypecode'])
        initialdiagnosis = diagnosis.objects.get(diagnosiscode=request.POST['initialdiagnosis'])
        finaldiagnosis = diagnosis.objects.get(diagnosiscode=request.POST['finaldiagnosis'])
        idpresented = request.POST['idpresented'].strip().replace("  ", " ").title()
        statuscode = availmentstatus.objects.get(availmentstatuscode=request.POST['statuscode'])
        disapproved = request.POST['disapproved'].strip().replace("  ", " ").title()
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()

        data = approval(approvalcode = approvalcode, 
                        policynumber = policynumber,
                        availmentdate = availmentdate,
                        doctorcode = doctorcode,
                        providercode = providercode,
                        callername = callername,
                        availmenttypecode = availmenttypecode,
                        initialdiagnosis = initialdiagnosis,
                        finaldiagnosis = finaldiagnosis,
                        idpresented = idpresented,
                        statuscode = statuscode,
                        disapproved = disapproved,
                        remarks = remarks,
                        transactby=transactby,
                        transactdate=transactdate,
                        transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
        data.save()
        historyapproval_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
        return redirect('approvalshow')    
    return render(request, 'approvalinsert.html', 
                { 
                    'policyNumbers': policyNumbers, 
                    # 'historymemberList': historymemberList,
                    'Doctors': Doctors,
                    'Providers': Providers,
                    'diagnosisList': diagnosisList,
                    'availmentstatusList': availmentstatusList,
                    'availmenttypeList': availmenttypeList,
                })  

def approvalshow(request):
    Approval = approval.objects.exclude(transactype = 'delete')
    diagnosis_dict = {d.diagnosiscode: d for d in diagnosis.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])}
    return render(request,'approvalshow.html', {'approvalList':Approval, 'diagnosis_dict': diagnosis_dict})

def approvaledit(request,pk):
    Approval = approval.objects.get(recordno=pk)
    policyNumbers = member.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    # historymemberList = historymember.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Providers = provider.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Doctors = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    diagnosisList = diagnosis.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    availmentstatusList = availmentstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    availmenttypeList = availmenttype.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == 'POST':
            print(request.POST)
            Approval.policynumber = member.objects.get(policynumber=request.POST['policynumber'])
            # approval.memberrecordnohist = historymember.objects.get(memberrecordnohist=request.POST['memberrecordnohist'])
            Approval.availmentdate = request.POST['availmentdate']
            Approval.providercode = provider.objects.get(providercode=request.POST['providercode'])
            Approval.doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
            Approval.callername = request.POST['middlename'].strip().replace("  ", " ").title()
            Approval.initialdiagnosis = diagnosis.get(diagnosiscode=request.POST['initialdiagnosis'])
            Approval.finaldiagnosis = diagnosis.get(diagnosiscode=request.POST['finaldiagnosis'])
            Approval.idpresented = request.POST['middlename'].strip().replace("  ", " ").title()
            Approval.statuscode = availmentstatus.objects.get(availmentstatuscode=request.POST['availmentstatuscode'])
            Approval.disapproved = request.POST['disapproved'].strip().replace("  ", " ").title()
            Approval.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
            Approval.save()  
            historyapproval_save(Approval, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('approvalshow')
    return render(request,'approvaledit.html', 
                    {
                        'approval' : Approval, 
                        'policyNumbers': policyNumbers, 
                        # 'historymemberList': historymemberList,
                        'Doctors': Doctors,
                        'Providers': Providers,
                        'diagnosisList': diagnosisList,
                        'availmentstatusList': availmentstatusList,
                        'availmenttypeList': availmenttypeList,
                    })

def approvaldelete(request, pk):
    approval = approval.objects.get(recordno=pk)

    if request.method == 'POST':
        approval.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        approval.save()
        historyapproval_save(approval, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('approvalshow')

    context = {
        'approval': approval,
    } 

    return render(request, 'approvaldelete.html', context)

def historyapproval_save(obj, transactype):
    approval = obj
    data = historyapproval(
        recordno=approval.recordno,
        approvalcode = approval.approvalcode, 
        policynumber = approval.policynumber,
        # memberrecordnohist = approval.memberrecordnohist ,
        availmentdate = approval.availmentdate,
        doctorcode = approval.doctorcode,
        providercode = approval.providercode,
        callername = approval.callername,
        availmenttypecode = approval.availmenttypecode,
        initialdiagnosis = approval.initialdiagnosis,
        finaldiagnosis = approval.finaldiagnosis,
        idpresented = approval.idpresented,
        statuscode = approval.statuscode,
        disapproved = approval.disapproved,
        remarks = approval.remarks,
        transactby=approval.transactby,
        transactdate=datetime.now(),
        transactype=transactype

    )
    data.save()