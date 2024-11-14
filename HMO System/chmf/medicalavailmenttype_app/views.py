from django.shortcuts import render, redirect
from datetime import datetime
from .models import availmenttype, historyavailmenttype
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
# Create your views here.
########################## new function##################### 


def availmenttypeinsert(request):   
    if request.method == "POST":
        availmenttypename = request.POST['availmenttypename'].strip().replace("  ", " ").title()
        availmenttypeshortname = request.POST['availmenttypeshortname'].strip().replace("  ", " ").title()
        availmenttyperemarks = request.POST['remarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        availmenttypecode_max = availmenttype.objects.all().aggregate(Max('availmenttypecode'))
        availmenttypecode_nextvalue = 1 if availmenttypecode_max['availmenttypecode__max'] == None else availmenttypecode_max['availmenttypecode__max'] + 1
        if availmenttype.objects.annotate(uppercase_availmenttypename=Upper('availmenttypename')).filter(uppercase_availmenttypename=availmenttypename.upper()):
            messages.error(request, "Availment type Name already Exist.") 
        else:
            data = availmenttype(availmenttypecode = availmenttypecode_nextvalue, 
                                availmenttypename=availmenttypename, 
                                availmenttypeshortname=availmenttypeshortname, 
                                remarks = availmenttyperemarks, 
                                transactby=transactby,transactdate=transactdate,
                                transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            data.save()
            historyavailmenttype_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('availmenttypeshow')    
        return render(request, 'availmenttypeinsert.html')  
    return render(request, 'availmenttypeinsert.html')  

def availmenttypeshow(request):
    availmentTypes = availmenttype.objects.exclude(transactype = 'delete')
    return render(request,'availmenttypeshow.html', {'availmenttypeList':availmentTypes} )

def availmenttypeedit(request,pk):
    availmentTypes = availmenttype.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            availmentTypes.availmenttypename = request.POST['availmenttypename']
            availmentTypes.availmenttypeshortname = request.POST['availmenttypeshortname']
            availmentTypes.remarks = request.POST['remarks']
            availmentTypes.save()  
            historyavailmenttype_save(availmentTypes, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('availmenttypeshow')
    context = {
        'availmenttype': availmentTypes,
    }

    return render(request,'availmenttypeedit.html',context)

def availmenttypedelete(request, pk):
    availmentTypes = availmenttype.objects.get(recordno=pk)

    if request.method == 'POST':
        availmentTypes.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        availmentTypes.save()
        historyavailmenttype_save(availmentTypes, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('availmenttypeshow')

    context = {
        'availmenttype': availmentTypes,
    } 

    return render(request, 'availmenttypedelete.html', context)

def historyavailmenttype_save(obj, transactype):
    availmenttype = obj
    data = historyavailmenttype(
        recordno=availmenttype.recordno,
        availmenttypecode=availmenttype.availmenttypecode,
        availmenttypename=availmenttype.availmenttypename,
        availmenttypeshortname=availmenttype.availmenttypeshortname,
        availmenttyperemarks=availmenttype.remarks,
        transactby=availmenttype.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()