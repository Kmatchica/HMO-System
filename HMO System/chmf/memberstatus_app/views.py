from django.shortcuts import render, redirect
from datetime import datetime
from .models import memberstatus, historymemberstatus
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.contrib import messages
from django.db.models.functions import Upper
from django.conf import settings
# Create your views here.
########################## new function##################### 


def memberstatusinsert(request):   
    if request.method == "POST":
        memberstatusname = request.POST['memberstatusname'].strip().replace("  ", " ").title()
        memberstatusshortname = request.POST['memberstatusshortname'].strip().replace("  ", " ").title()
        memberstatusremarks = request.POST['memberstatusremarks'].strip().replace("  ", " ").title()
        transactby = 0
        transactdate = datetime.now()
        memberstatuscode_max = memberstatus.objects.all().aggregate(Max('memberstatuscode'))
        memberstatuscode_nextvalue = 1 if memberstatuscode_max['memberstatuscode__max'] == None else memberstatuscode_max['memberstatuscode__max'] + 1
        if memberstatus.objects.annotate(uppercase_memberstatusname=Upper('memberstatusname')).filter(uppercase_memberstatusname=memberstatusname.upper()):
            messages.error(request, "member Status Name already Exist.") 
        else:
            data = memberstatus(memberstatuscode = memberstatuscode_nextvalue, 
                                memberstatusname=memberstatusname, 
                                memberstatusshortname=memberstatusshortname, 
                                memberstatusremarks = memberstatusremarks, 
                                transactby=transactby,transactdate=transactdate,
                                transactype=settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            data.save()
            historymemberstatus_save(data, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-ADD'])
            return redirect('memberstatusshow')    
        return render(request, 'memberstatusinsert.html')  
    return render(request, 'memberstatusinsert.html')  

def memberstatusshow(request):
    memberstatuss = memberstatus.objects.exclude(transactype = 'delete')
    return render(request,'memberstatusshow.html', {'memberStatusList':memberstatuss} )

def memberstatusedit(request,pk):
    memberStatus = memberstatus.objects.get(recordno=pk)
    if request.method == 'POST':
            print(request.POST)
            memberStatus.memberstatusname = request.POST['memberstatusname']
            memberStatus.memberstatusshortname = request.POST['memberstatusshortname']
            memberStatus.memberstatusremarks = request.POST['memberstatusremarks']
            memberStatus.save()  
            historymemberstatus_save(memberStatus, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-EDIT'])
            return redirect('memberstatusshow')
    context = {
        'memberStatus': memberStatus,
    }

    return render(request,'memberstatusedit.html',context)

def memberstatusdelete(request, pk):
    memberStatus = memberstatus.objects.get(recordno=pk)

    if request.method == 'POST':
        memberStatus.transactype = settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE']
        memberStatus.save()
        historymemberstatus_save(memberStatus, settings.GLOBAL_VARIABLES['TRANSACT-TYPE-DELETE'])
        return redirect('memberstatusshow')

    context = {
        'memberStatus': memberStatus,
    } 

    return render(request, 'memberstatusdelete.html', context)

def historymemberstatus_save(obj, transactype):
    memberstatus = obj
    data = historymemberstatus(
        recordno=memberstatus.recordno,
        memberstatuscode=memberstatus.memberstatuscode,
        memberstatusname=memberstatus.memberstatusname,
        memberstatusremarks=memberstatus.memberstatusremarks,
        transactby=memberstatus.transactby,
        transactdate=datetime.now(),
        transactype=transactype
        
    )
    data.save()