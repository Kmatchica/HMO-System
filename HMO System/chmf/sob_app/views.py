from django.shortcuts import render, redirect
from datetime import datetime
from .models import Sob, SobHistory
from django.db.models import Max

# Create SOB Header

def sob_insert(request):
    if request.method == "POST":
        sobname = request.POST['sobname']
        sobshortname = request.POST['sobshortname']
        remarks = request.POST['remarks']
        transactby = 0
        transactdate = datetime.now()
        transacttype = 'add'

        #Getting the max value of SOB code, then computing for the next value in preparation for inserting a new record
        sobcode_max = Sob.objects.all().aggregate(Max('sobcode'))
        sobcode_nextvalue = 0 if sobcode_max['sobcode__max'] == None else sobcode_max['sobcode__max'] + 1

        data = Sob(sobcode=sobcode_nextvalue, sobname=sobname, sobshortname=sobshortname, remarks=remarks, transactby=transactby, transactdate=transactdate, transacttype=transacttype)
        data.save()

        #Call the function for keeping history
        sobhistory_save(data, transacttype)
  
        return redirect('/sob')
    else:
        return render(request, 'sob-insert.html')
    
# Retrive SOB

def sob_show(request):
    sobs = Sob.objects.exclude(transacttype = 'delete')
    return render(request,'sob-show.html',{'sobs':sobs})

# Update SOB

def sob_edit(request,pk):
    sob = Sob.objects.get(recordno=pk)
    transacttype = 'edit'

    if request.method == 'POST':
        print(request.POST)
        sob.sobname = request.POST['sobname']
        sob.sobshortname = request.POST['sobshortname']
        sob.remarks = request.POST['remarks']
        sob.transactby = 0
        sob.transactdate = datetime.now()
        sob.transacttype = transacttype
        sob.save()

        #Call the function for keeping history
        sobhistory_save(sob, transacttype)

        return redirect('/sob')
    context = {
        'sob': sob,
    }

    return render(request,'sob-edit.html',context)

# Delete SOB

def sob_remove(request, pk):
    sob = Sob.objects.get(recordno=pk)
    transacttype = 'delete'

    if request.method == 'POST':

        #Set values and update the record
        sob.transactby = 0
        sob.transactdate = datetime.now()
        sob.transacttype = transacttype
        sob.save()

        #Call the function for keeping history
        sobhistory_save(sob, transacttype)

        return redirect('/sob')

    context = {
        'sob': sob,
    }

    return render(request, 'sob-remove.html', context)

def sobhistory_save(obj, transacttype):
    sob = obj
    #Set values and insert the just updated record to history table that can be used for audit trail
    data = SobHistory(recordno = sob.recordno,
    sobcode = sob.sobcode,
    sobname = sob.sobname,
    sobshortname = sob.sobshortname,
    remarks = sob.remarks,
    transactby = 0,
    transactdate = datetime.now(),
    transacttype = transacttype)
    data.save()