from django.shortcuts import render, redirect
from datetime import datetime
from .models import clientsob, historyclientsob
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from client_app.models import client
# Create your views here.
########################## new function##################### 


def clientsobinsert(request):   
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == "POST":
        clientcode = client.objects.get(clientcode=request.POST['clientcode'])
        sobcode = request.POST['sobcode']
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        clientsobcode_max = clientsob.objects.all().aggregate(Max('clientsobcode'))
        clientsobcode_nextvalue = 1 if clientsobcode_max['clientsobcode__max'] == None else clientsobcode_max['clientsobcode__max'] + 1
        data = clientsob(clientsobcode = clientsobcode_nextvalue, 
                         clientcode=clientcode, 
                         sobcode=sobcode, 
                         remarks = remarks, 
                         transactby=transactby,
                         transactdate=transactdate,
                         transactype=transactype)
        data.save()
        historyclientsob_save(data, transactype)
        return redirect('clientsobshow')    
    return render(request, 'clientsobinsert.html', {'clients': Clients})  

def clientsobshow(request):
    clientsobs = clientsob.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete']).order_by('-transactdate')
    return render(request,'clientsobshow.html', {'clientsobList':clientsobs} )

def clientsobedit(request,pk):
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    clientSob = clientsob.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            clientSob.clientcode = client.objects.get(clientcode=request.POST['clientcode'])
            clientSob.sobcode = request.POST['sobcode']
            clientSob.remarks = request.POST['remarks']
            clientSob.save()   
            return redirect('clientsobshow')
    context = {
        'clientsob': clientSob,
        'clients' : Clients
    }

    return render(request,'clientsobedit.html',context)

def clientsobdelete(request, pk):
    clientSob = clientsob.objects.get(recordno=pk)

    if request.method == 'POST':
        clientSob.delete()
        return redirect('clientsobshow')

    context = {
        'clientsob': clientSob,
    } 

    return render(request, 'clientsobdelete.html', context)

def historyclientsob_save(obj, transactype):
    clientsob = obj
    data = historyclientsob(
        recordno=clientsob.recordno,
        clientsobcode=clientsob.clientsobcode,
        clientcode=clientsob.clientcode,
        sobcode=clientsob.sobcode,
        remarks=clientsob.remarks,
        transactby=clientsob.transactby,
        transactdate=datetime.now(),
        transactype=transactype
    )
    data.save()