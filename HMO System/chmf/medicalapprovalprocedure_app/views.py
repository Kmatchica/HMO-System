from django.shortcuts import render, redirect
from datetime import datetime
from .models import approvalprocedure, historyapprovalprocedure
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
from medicalprocedures_app.models import medicalprocedures 
from doctor_app.models import doctor
# Create your views here.
########################## new function##################### 



def medicalapprovalprocedureinsert(request):   
    medicalProcedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == "POST":
        procedurecode = medicalprocedures.objects.get(procedurecode=request.POST['procedurecode'])
        doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
        professionalfee = int(request.POST['professionalfee'])
        confinementamount = int(request.POST['confinementamount'])
        otheramount = int(request.POST['otheramount'])
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        approvalcode_max = approvalprocedure.objects.all().aggregate(Max('approvalcode'))
        approvalcode_nextvalue = 1 if approvalcode_max['approvalcode__max'] == None else approvalcode_max['approvalcode__max'] + 1

        data = approvalprocedure(approvalcode = approvalcode_nextvalue, 
                        procedurecode = procedurecode,
                        doctorcode = doctorcode,
                        professionalfee = professionalfee,
                        confinementamount = confinementamount,
                        otheramount = otheramount,
                        remarks = remarks,
                        transactby=transactby,transactdate=transactdate,
                        transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
        data.save()
        historyapprovalprocedure_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
        return redirect('approvalprocedureshow')    
    return render(request, 'approvalprocedureinsert.html', {'medicalProcedures': medicalProcedures, 'Doctors': Doctor})  

def medicalapprovalprocedureshow(request):
    approvalProcedure = approvalprocedure.objects.exclude(transactype = 'delete')
    return render(request,'approvalprocedureshow.html', {'approvalProcedureList':approvalProcedure})

def medicalapprovalprocedureedit(request,pk):
    approvalProcedure = approvalprocedure.objects.get(recordno=pk)
    medicalProcedures = medicalprocedures.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    Doctor = doctor.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == 'POST':
            print(request.POST)
            approvalProcedure.procedurecode = medicalprocedures.objects.get(procedurecode=request.POST['procedurecode'])
            approvalProcedure.doctorcode = doctor.objects.get(doctorcode=request.POST['doctorcode'])
            approvalProcedure.professionalfee = int(request.POST['professionalfee'])
            approvalProcedure.confinementamount = int(request.POST['confinementamount'])
            approvalProcedure.otheramount = int(request.POST['otheramount'])
            approvalProcedure.remarks = request.POST['remarks']
            approvalProcedure.save()  
            historyapprovalprocedure_save(approvalProcedure, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('approvalprocedureshow')
    return render(request,'approvalprocedureedit.html', {'approvalProcedure' : approvalProcedure, 'medicalProcedures':medicalProcedures, 'Doctors' : Doctor})

def medicalapprovalproceduredelete(request, pk):
    approvalProcedure = approvalprocedure.objects.get(recordno=pk)

    if request.method == 'POST':
        approvalProcedure.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        approvalProcedure.save()
        historyapprovalprocedure_save(approvalProcedure, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('approvalprocedureshow')

    context = {
        'approvalProcedure': approvalProcedure,
    } 

    return render(request, 'approvalproceduredelete.html', context)

def historyapprovalprocedure_save(obj, transactype):
    approvalprocedure = obj
    data = historyapprovalprocedure(
        recordno=approvalprocedure.recordno,
        approvalcode= approvalprocedure.approvalcode,
        procedurecode=approvalprocedure.procedurecode,
        doctorcode = approvalprocedure.doctorcode,
        professionalfee = approvalprocedure.professionalfee,
        confinementamount = approvalprocedure.confinementamount,
        otheramount = approvalprocedure.otheramount,
        remarks=approvalprocedure.remarks,
        transactby=approvalprocedure.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()