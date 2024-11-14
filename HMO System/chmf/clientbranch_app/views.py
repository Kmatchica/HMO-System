from django.shortcuts import render, redirect
from datetime import datetime
from .models import branch, historybranch
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from client_app.models import client
from clientstatus_app.models import clientstatus

def branchinsert(request): 
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])  
    clientStatusList = clientstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])  
    if request.method == "POST":
        clientcode = client.objects.get(clientcode=request.POST['clientcode'])
        branchname = request.POST['branchname'].strip().replace("  ", " ").title()
        branchshortname = request.POST['branchshortname'].strip().replace("  ", " ").title()
        statuscode = clientstatus.objects.get(clientstatuscode=request.POST['statuscode'])
        tin = request.POST['tin']
        address = request.POST['tin']
        locationcode = request.POST['locationcode']
        contactnumber = request.POST['contactnumber']
        emailaddress = request.POST['emailaddress']
        remarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        branchcode_max = branch.objects.all().aggregate(Max('branchcode'))
        branchcode_nextvalue = 1 if branchcode_max['branchcode__max'] == None else branchcode_max['branchcode__max'] + 1
        data = branch(branchcode = branchcode_nextvalue, 
                            clientcode=clientcode, 
                            branchname=branchname, 
                            branchshortname = branchshortname,
                            statuscode = statuscode,
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
        historybranch_save(data, transactype)
        return redirect('branchshow')    
    return render(request, 'clientbranchinsert.html', {'clients' : Clients, 'clientStatusList' : clientStatusList})  

def branchshow(request):
    branches = branch.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete']).order_by('-transactdate')
    return render(request,'clientbranchshow.html', {'branchList':branches} )

def branchedit(request,pk):
    Clients = client.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])  
    clientStatusList = clientstatus.objects.exclude(transactype__in=['Delete', 'Terminate','Disapprove', 'delete'])  
    Branch = branch.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            Branch.clientcode = client.objects.get(clientcode=request.POST['clientcode'])
            Branch.branchname = request.POST['branchname'].strip().replace("  ", " ").title()
            Branch.branchshortname = request.POST['branchshortname'].strip().replace("  ", " ").title()
            Branch.statuscode = clientstatus.objects.get(clientstatuscode=request.POST['statuscode'])
            Branch.tin = request.POST['tin']
            Branch.address = request.POST['address']
            Branch.locationcode = request.POST['locationcode']
            Branch.contactnumber = request.POST['contactnumber']
            Branch.emailaddress = request.POST['emailaddress']
            Branch.remarks = request.POST['remarks'].strip().replace("  ", " ").title()
            transactype = 'edit' 
            Branch.save()   
            historybranch_save(Branch, transactype)
            return redirect('branchshow')
    context = {
        'branch': Branch,
        'clients' : Clients,
        'clientStatusList': clientStatusList
    }

    return render(request,'clientbranchedit.html',context)

def branchdelete(request, pk):
    Branch = branch.objects.get(recordno=pk)
    transacttype = 'delete'

    if request.method == 'POST':
       Branch.transactype = transacttype
       Branch.save()
       historybranch_save(Branch, transacttype)
       return redirect('branchshow')

    context = {
        'branch': Branch,
    } 

    return render(request, 'clientbranchdelete.html', context)

def historybranch_save(obj, transacttype):
    branch = obj
    data = historybranch(
        recordno=branch.recordno,
        branchcode=branch.branchcode,
        clientcode=branch.clientcode,
        branchname=branch.branchname,
        branchshortname=branch.branchshortname,
        statuscode=branch.statuscode,
        tin = branch.tin,
        locationcode = branch.locationcode,
        contactnumber = branch.contactnumber,
        emailaddress = branch.emailaddress,
        address = branch.address,
        remarks=branch.remarks,
        transactby=branch.transactby,
        transactdate=datetime.now(),
        transactype=transacttype
        
    )
    data.save()