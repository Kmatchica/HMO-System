from django.shortcuts import render, redirect
from datetime import datetime
from .models import roomtype, roomtypehistory
from django.db.models import Max

# Create Room Type

def roomtype_insert(request):
    if request.method == "POST":
        roomname = request.POST['roomname']
        roomshortname = request.POST['roomshortname']
        remarks = request.POST['remarks']
        transactby = 0
        transactdate = datetime.now()
        transactype = 'add'

        #Getting the max value of product code, then computing for the next value in preparation for inserting a new record
        roomcode_max = roomtype.objects.all().aggregate(Max('roomcode'))
        roomcode_nextvalue = 0 if roomcode_max['roomcode__max'] == None else roomcode_max['roomcode__max'] + 1

        data = roomtype(roomcode=roomcode_nextvalue, roomname=roomname, roomshortname=roomshortname, remarks=remarks, transactby=transactby, transactdate=transactdate, transactype=transactype)
        data.save()

        #Call the function for keeping history
        roomtypehistory_save(data, transactype)
  
        return redirect('/roomtype')
    else:
        return render(request, 'roomtype-insert.html')
    
# Retrive Room Type

def roomtype_show(request):
    Roomtype = roomtype.objects.exclude(transactype = 'delete')
    return render(request,'roomtype-show.html',{'Roomtype':Roomtype})

# Update Room Type

def roomtype_edit(request,pk):
    Roomtype = roomtype.objects.get(recordno=pk)
    transactype = 'edit'

    if request.method == 'POST':
        print(request.POST)
        Roomtype.roomname = request.POST['roomname']
        Roomtype.roomshortname = request.POST['roomshortname']
        Roomtype.remarks = request.POST['remarks']
        Roomtype.transactby = 0
        Roomtype.transactdate = datetime.now()
        Roomtype.transactype = transactype
        Roomtype.save()

        #Call the function for keeping history
        roomtypehistory_save(Roomtype, transactype)

        return redirect('/roomtype')
    context = {
        'Roomtype': Roomtype,
    }

    return render(request,'roomtype-edit.html',context)

# Delete Room Type

def roomtype_remove(request, pk):
    Roomtype = roomtype.objects.get(recordno=pk)
    transactype = 'delete'

    if request.method == 'POST':

        #Set values and update the record
        Roomtype.transactby = 0
        Roomtype.transactdate = datetime.now()
        Roomtype.transactype = transactype
        Roomtype.save()

        #Call the function for keeping history
        roomtypehistory_save(Roomtype, transactype)

        return redirect('/roomtype')

    context = {
        'Roomtype': Roomtype,
    }

    return render(request, 'roomtype-remove.html', context)

def roomtypehistory_save(obj, transactype):
    roomtype = obj
    #Set values and insert the just updated record to history table that can be used for audit trail
    data = roomtypehistory(recordno = roomtype.recordno,
    roomcode = roomtype.roomcode,
    roomname = roomtype.roomname,
    roomshortname = roomtype.roomshortname,
    remarks = roomtype.remarks,
    transactby = 0,
    transactdate = datetime.now(),
    transactype = transactype)
    data.save()