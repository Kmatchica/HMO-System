from django.shortcuts import render, redirect
from datetime import datetime
from .models import clientstatus, historyclientstatus
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.
########################## new function##################### 

def statusinsert(request):   
    if request.method == "POST":
        clientstatusname = request.POST['clientstatusname'].strip().replace("  ", " ").title()
        clientstatusshortname = request.POST['clientstatusshortname'].strip().replace("  ", " ").title()
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        clientstatuscode_max = clientstatus.objects.all().aggregate(Max('clientstatuscode'))
        clientstatuscode_nextvalue = 1 if clientstatuscode_max['clientstatuscode__max'] == None else clientstatuscode_max['clientstatuscode__max'] + 1
        if clientstatus.objects.annotate(uppercase_clientstatusname=Upper('clientstatusname')).filter(uppercase_clientstatusname=clientstatusname.upper()):
            messages.error(request, " Status Name already Exist.") 
        else:
            data = clientstatus(clientstatuscode = clientstatuscode_nextvalue, 
                                clientstatusname=clientstatusname, 
                                clientstatusshortname=clientstatusshortname, 
                                remarks = remarks, 
                                transactby=transactby,
                                transactdate=transactdate,
                                transactype=transactype)
            data.save()
            historystatus_save(data, transactype)
            return redirect('statusshow')    
        return render(request, 'clientstatusinsert.html')  
    return render(request, 'clientstatusinsert.html')  

def statusshow(request):
    Status = clientstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete']).order_by('-transactdate')
    return render(request,'clientstatusshow.html', {'StatusList':Status} )

def statusedit(request,pk):
    Status = clientstatus.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            Status.clientstatusname = request.POST['clientstatusname']
            Status.clientstatusshortname = request.POST['clientstatusshortname']
            Status.remarks = request.POST['remarks']
            Status.save()   
            return redirect('statusshow')
    context = {
        'Status': Status,
    }

    return render(request,'statusedit.html',context)

def statusdelete(request, pk):
    Status = clientstatus.objects.get(recordno=pk)

    if request.method == 'POST':
        Status.delete()
        return redirect('statusshow')

    context = {
        'Status': Status,
    } 
    return render(request, 'clientstatusdelete.html', context)

def historystatus_save(obj, transactype):
    status = obj
    data = historyclientstatus(
        recordno=status.recordno,
        clientstatuscode=status.clientstatuscode,
        clientstatusname=status.clientstatusname,
        clientstatusshortname=status.clientstatusshortname,
        remarks=status.remarks,
        transactby=status.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()