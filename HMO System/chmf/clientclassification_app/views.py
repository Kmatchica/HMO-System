from django.shortcuts import render, redirect
from datetime import datetime
from .models import clientclassification, historyclientclassification
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
# Create your views here.
########################## new function##################### 

def clientclassificationinsert(request):   
    if request.method == "POST":
        clientclassificationname = request.POST['clientclassificationname'].strip().replace("  ", " ").title()
        clientclassificationremarks = request.POST['clientclassificationremarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'
        clientclassificationcode_max = clientclassification.objects.all().aggregate(Max('clientclassificationcode'))
        clientclassificationcode_nextvalue = 1 if clientclassificationcode_max['clientclassificationcode__max'] == None else clientclassificationcode_max['clientclassificationcode__max'] + 1
        if clientclassification.objects.annotate(uppercase_clientclassificationname=Upper('clientclassificationname')).filter(uppercase_clientclassificationname=clientclassificationname.upper()):
            messages.error(request, "Client classification Name already Exist.") 
        else:
            data = clientclassification(clientclassificationcode = clientclassificationcode_nextvalue, clientclassificationname=clientclassificationname, clientclassificationremarks = clientclassificationremarks, transactby=transactby,transactdate=transactdate,transactype=transactype)
            data.save()
            historyclientclassification_save(data, transactype)
            return redirect('clientclassificationshow')    
        return render(request, 'clientclassificationinsert.html')  
    return render(request, 'clientclassificationinsert.html')  

def clientclassificationshow(request):
    clientClassifications = clientclassification.objects.all()
    return render(request,'clientclassificationshow.html', {'clientClassifications':clientClassifications} )

def clientclassificationedit(request,pk):
    clientClassification = clientclassification.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            clientClassification.clientclassificationname = request.POST['clientclassificationname']
            clientClassification.clientclassificationremarks = request.POST['clientclassificationremarks']
            clientClassification.save()   
            return redirect('clientclassificationshow')
    context = {
        'clientClassification': clientClassification,
    }

    return render(request,'clientclassificationedit.html',context)

def clientclassificationdelete(request, pk):
    clientClassification = clientclassification.objects.get(recordno=pk)

    if request.method == 'POST':
        clientClassification.delete()
        return redirect('clientclassificationshow')

    context = {
        'clientClassification': clientClassification,
    }

    return render(request, 'clientclassificationdelete.html', context)

def historyclientclassification_save(obj, transactype):
    clientclassification = obj
    data = historyclientclassification(
        recordno=clientclassification.recordno,
        clientclassificationcode=clientclassification.clientclassificationcode,
        clientclassificationname=clientclassification.clientclassificationname,
        clientclassificationremarks=clientclassification.clientclassificationremarks,
        transactby=clientclassification.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()