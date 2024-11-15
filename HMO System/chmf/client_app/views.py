from django.shortcuts import render, redirect
from datetime import datetime
from .models import client, historyclient
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from clientclassification_app.models import clientclassification
from clientstatus_app.models import clientstatus
from utils.utils import generate_code

def clientinsert(request):   
    clientClassificationList = clientclassification.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    clientStatusList = clientstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == "POST":
        clientparentcode = 0
        clientclassificationcode = clientclassification.objects.get(clientclassificationcode=request.POST['clientclassificationcode'])
        clientname = request.POST['clientname']
        clientshortname = request.POST['clientshortname']
        subscriptiondate = request.POST['subscriptiondate']
        effectivedate = request.POST['effectivedate']
        expirydate = request.POST['expirydate']
        renewaldate = request.POST['renewaldate']
        statuscode = clientstatus.objects.get(clientstatuscode=request.POST['statuscode'])
        registrationnumber = request.POST['registrationnumber']
        gascheduledate = request.POST['gascheduledate']
        tin = request.POST['tin']
        address = request.POST['address']
        locationcode = request.POST['locationcode']
        contactnumber = request.POST['contactnumber']
        emailaddress = request.POST['emailaddress']
        remarks = request.POST['remarks']
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        clientcode = generate_code(client, 'clientcode', padding_width=5)
        data = client(clientcode = clientcode, 
                        clientparentcode=clientparentcode,
                        clientclassificationcode = clientclassificationcode,
                        clientname = clientname,
                        clientshortname = clientshortname,
                        subscriptiondate = subscriptiondate,
                        effectivedate = effectivedate,
                        expirydate = expirydate,
                        renewaldate = renewaldate,
                        statuscode = statuscode,
                        registrationnumber = registrationnumber,
                        gascheduledate = gascheduledate,
                        tin = tin,
                        address = address,
                        locationcode = locationcode,
                        contactnumber = contactnumber,
                        emailaddress = emailaddress,
                        remarks = remarks,
                        transactby=transactby,
                        transactdate=transactdate,
                        transactype=transactype)
        data.save()
        historyclient_save(data, transactype)
        return redirect('clientshow')    
    return render(request, 'clientinsert.html', {'clientClassificationList' : clientClassificationList, 'clientStatusList' : clientStatusList})  

def clientshow(request):
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete']).order_by('-transactdate')
    return render(request,'clientshow.html', {'clientList':Clients} )

def clientedit(request,pk):
    Client = client.objects.get(recordno=pk)
    clientClassificationList = clientclassification.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    clientStatusList = clientstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])
    if request.method == 'POST':
            print(request.POST)
            Client.clientparentcode = 0
            Client.clientclassificationcode = clientclassification.objects.get(clientclassificationcode=request.POST['clientclassificationcode'])
            Client.clientname = request.POST['clientname']
            Client.clientshortname = request.POST['clientshortname']
            Client.subscriptiondate = request.POST['subscriptiondate']
            Client.effectivedate = request.POST['effectivedate']
            Client.expirydate = request.POST['expirydate']
            Client.renewaldate = request.POST['renewaldate']
            Client.statuscode = clientstatus.objects.get(clientstatuscode=request.POST['statuscode'])
            Client.registrationnumber = request.POST['registrationnumber']
            Client.gascheduledate = request.POST['gascheduledate']
            Client.tin = request.POST['tin']
            Client.address = request.POST['address']
            Client.locationcode = request.POST['locationcode']
            Client.contactnumber = request.POST['contactnumber']
            Client.emailaddress = request.POST['emailaddress']
            Client.remarks = request.POST['remarks']
            transacttype = 'edit'
            Client.save()   
            historyclient_save(Client, transacttype)
            return redirect('clientshow')
    context = {
        'client': Client,
        'clientClassificationList' : clientClassificationList,
        'clientStatusList': clientStatusList
    }

    return render(request,'clientedit.html',context)

def clientdelete(request, pk):
    Client = client.objects.get(recordno=pk)
    transacttype = 'delete' 

    if request.method == 'POST':
        Client.transactype = transacttype
        Client.save()
        historyclient_save(Client, Client.transactype)
        return redirect('clientshow')

    context = {
        'client': Client,
    } 

    return render(request, 'clientdelete.html', context)

def historyclient_save(obj, transacttype):
    client = obj
    data = historyclient(
        recordno=client.recordno,
        clientcode=client.clientcode,
        clientparentcode=client.clientparentcode,
        clientclassificationcode=client.clientclassificationcode,
        clientname=client.clientname,
        clientshortname=client.clientshortname,
        subscriptiondate=client.subscriptiondate,
        effectivedate=client.effectivedate,
        expirydate=client.expirydate,
        renewaldate=client.renewaldate,
        statuscode=client.statuscode,
        registrationnumber=client.registrationnumber,
        gascheduledate=client.gascheduledate,
        tin=client.tin,
        address=client.address,
        locationcode=client.locationcode,
        contactnumber=client.contactnumber,
        emailaddress=client.emailaddress,
        remarks=client.remarks,
        transactby=client.transactby,
        transactdate=datetime.now(),
        transactype=transacttype
        
    )
    data.save()