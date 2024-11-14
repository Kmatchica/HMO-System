from django.shortcuts import render, redirect
from datetime import datetime
from .models import availmentstatus, historyavailmentstatus
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
# Create your views here.
########################## new function##################### 


def availmentstatusinsert(request):   
    if request.method == "POST":
        availmentstatusname = request.POST['availmentstatusname'].strip().replace("  ", " ").title()
        availmentstatusshortname = request.POST['availmentstatusshortname'].strip().replace("  ", " ").title()
        availmentstatusremarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        availmentstatuscode_max = availmentstatus.objects.all().aggregate(Max('availmentstatuscode'))
        availmentstatuscode_nextvalue = 1 if availmentstatuscode_max['availmentstatuscode__max'] == None else availmentstatuscode_max['availmentstatuscode__max'] + 1
        if availmentstatus.objects.annotate(uppercase_availmentstatusname=Upper('availmentstatusname')).filter(uppercase_availmentstatusname=availmentstatusname.upper()):
            messages.error(request, "Availment Status Name already Exist.") 
        else:
            data = availmentstatus(availmentstatuscode = availmentstatuscode_nextvalue, 
                                availmentstatusname=availmentstatusname, 
                                availmentstatusshortname=availmentstatusshortname, 
                                remarks = availmentstatusremarks, 
                                transactby=transactby,transactdate=transactdate,
                                transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            data.save()
            historyavailmentstatus_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('availmentstatusshow')    
        return render(request, 'availmentstatusinsert.html')  
    return render(request, 'availmentstatusinsert.html')  

def availmentstatusshow(request):
    availmentStatuss = availmentstatus.objects.exclude(transactype = 'delete')
    return render(request,'availmentstatusshow.html', {'availmentstatusList':availmentStatuss} )

def availmentstatusedit(request,pk):
    availmentStatus = availmentstatus.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            availmentStatus.availmentstatusname = request.POST['availmentstatusname']
            availmentStatus.availmentstatusshortname = request.POST['availmentstatusshortname']
            availmentStatus.remarks = request.POST['remarks']
            availmentStatus.save()  
            historyavailmentstatus_save(availmentStatus, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('availmentstatusshow')
    context = {
        'availmentstatus': availmentStatus,
    }

    return render(request,'availmentstatusedit.html',context)

def availmentstatusdelete(request, pk):
    availmentStatus = availmentstatus.objects.get(recordno=pk)

    if request.method == 'POST':
        availmentStatus.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        availmentStatus.save()
        historyavailmentstatus_save(availmentStatus, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('availmentstatusshow')

    context = {
        'availmentstatus': availmentStatus,
    } 

    return render(request, 'availmentstatusdelete.html', context)

def historyavailmentstatus_save(obj, transactype):
    availmentstatus = obj
    data = historyavailmentstatus(
        recordno=availmentstatus.recordno,
        availmentstatuscode=availmentstatus.availmentstatuscode,
        availmentstatusname=availmentstatus.availmentstatusname,
        availmentstatusshortname=availmentstatus.availmentstatusshortname,
        availmentstatusremarks=availmentstatus.remarks,
        transactby=availmentstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()