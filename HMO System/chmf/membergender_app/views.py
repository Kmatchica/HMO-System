from django.shortcuts import render, redirect
from datetime import datetime
from .models import membergender, historymembergender
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
# Create your views here.
########################## new function##################### 


def membergenderinsert(request):   
    if request.method == "POST":
        membergendername = request.POST['membergendername'].strip().replace("  ", " ").title()
        membergendershortname = request.POST['membergendershortname'].strip().replace("  ", " ").title()
        membergenderremarks = request.POST['membergenderremarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        membergendercode_max = membergender.objects.all().aggregate(Max('membergendercode'))
        membergendercode_nextvalue = 1 if membergendercode_max['membergendercode__max'] == None else membergendercode_max['membergendercode__max'] + 1
        if membergender.objects.annotate(uppercase_membergendername=Upper('membergendername')).filter(uppercase_membergendername=membergendername.upper()):
            messages.error(request, "member Status Name already Exist.") 
        else:
            data = membergender(membergendercode = membergendercode_nextvalue, 
                                membergendername=membergendername, 
                                membergendershortname=membergendershortname, 
                                membergenderremarks = membergenderremarks, 
                                transactby=transactby,transactdate=transactdate,
                                transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            data.save()
            historymembergender_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('/membergender')    
        return render(request, 'membergenderinsert.html')  
    return render(request, 'membergenderinsert.html')  

def membergendershow(request):
    memberGenders = membergender.objects.exclude(transactype = 'delete')
    return render(request,'membergendershow.html', {'memberGenderList':memberGenders} )

def membergenderedit(request,pk):
    memberGender = membergender.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            memberGender.membergendername = request.POST['membergendername']
            memberGender.membergendershortname = request.POST['membergendershortname']
            memberGender.membergenderremarks = request.POST['membergenderremarks']
            memberGender.save()  
            historymembergender_save(memberGender, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('/membergender')
    context = {
        'membergender': memberGender,
    }

    return render(request,'membergenderedit.html',context)

def membergenderdelete(request, pk):
    memberGender = membergender.objects.get(recordno=pk)

    if request.method == 'POST':
        memberGender.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        memberGender.save()
        historymembergender_save(memberGender, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('/membergender')

    context = {
        'membergender': memberGender,
    } 

    return render(request, 'membergenderdelete.html', context)

def historymembergender_save(obj, transactype):
    membergender = obj
    data = historymembergender(
        recordno=membergender.recordno,
        membergendercode=membergender.membergendercode,
        membergendername=membergender.membergendername,
        membergenderremarks=membergender.membergenderremarks,
        transactby=membergender.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()