from django.shortcuts import render, redirect
from datetime import datetime
from .models import diagnosis, historydiagnosis
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
# Create your views here.
########################## new function##################### 


def diagnosisinsert(request):   
    if request.method == "POST":
        diagnosisname = request.POST['diagnosisname'].strip().replace("  ", " ").title()
        diagnosisshortname = request.POST['diagnosisshortname'].strip().replace("  ", " ").title()
        diagnosisremarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        diagnosiscode_max = diagnosis.objects.all().aggregate(Max('diagnosiscode'))
        diagnosiscode_nextvalue = 1 if diagnosiscode_max['diagnosiscode__max'] == None else diagnosiscode_max['diagnosiscode__max'] + 1
        if diagnosis.objects.annotate(uppercase_diagnosisname=Upper('diagnosisname')).filter(uppercase_diagnosisname=diagnosisname.upper()):
            messages.error(request, "Diagnosis Name already Exist.") 
        else:
            data = diagnosis(diagnosiscode = diagnosiscode_nextvalue, 
                                diagnosisname=diagnosisname, 
                                diagnosisshortname=diagnosisshortname, 
                                remarks = diagnosisremarks, 
                                transactby=transactby,transactdate=transactdate,
                                transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            data.save()
            historydiagnosis_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('diagnosisshow')    
        return render(request, 'diagnosisinsert.html')  
    return render(request, 'diagnosisinsert.html')  

def diagnosisshow(request):
    Diagnosis = diagnosis.objects.exclude(transactype = 'delete')
    return render(request,'diagnosisshow.html', {'diagnosisList':Diagnosis} )

def diagnosisedit(request,pk):
    Diagnosis = diagnosis.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            Diagnosis.diagnosisname = request.POST['diagnosisname']
            Diagnosis.diagnosisshortname = request.POST['diagnosisshortname']
            Diagnosis.remarks = request.POST['remarks']
            Diagnosis.save()  
            historydiagnosis_save(Diagnosis, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('diagnosisshow')
    context = {
        'diagnosis': Diagnosis,
    }

    return render(request,'diagnosisedit.html',context)

def diagnosisdelete(request, pk):
    Diagnosis = diagnosis.objects.get(recordno=pk)

    if request.method == 'POST':
        Diagnosis.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        Diagnosis.save()
        historydiagnosis_save(Diagnosis, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('diagnosisshow')

    context = {
        'diagnosis': Diagnosis,
    } 

    return render(request, 'diagnosisdelete.html', context)

def historydiagnosis_save(obj, transactype):
    diagnosis = obj
    data = historydiagnosis(
        recordno=diagnosis.recordno,
        diagnosiscode=diagnosis.diagnosiscode,
        diagnosisname=diagnosis.diagnosisname,
        diagnosisshortname=diagnosis.diagnosisshortname,
        remarks=diagnosis.remarks,
        transactby=diagnosis.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()