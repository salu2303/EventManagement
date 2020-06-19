from django.shortcuts import render
from register.models import Event,Admin,AdminEvent,Manager,ManagerEvent,CustomerEvent,Customer,Images,Videos
# Create your views here.

def ViewCustomers(request):
    c=Customer.objects.all()
    return render(request,'showdb.html',{'type': "Customer" ,'cobj': c})

def ViewManagers(request):
    m=Manager.objects.all()
    return render(request,'showdb.html',{'type': "Manager" ,'mobj': m})

def ViewAdmin(request):
    a=Admin.objects.all()
    return render(request,'showdb.html',{'type': "Admin" ,'aobj': a})

def ViewCustomerEvents(request):
    ce=CustomerEvent.objects.all()
    return render(request,'showdb.html',{'type': "CustomerEvent" ,'ceobj': ce})

def ViewAdminEvents(request):
    ae=AdminEvent.objects.all()
    return render(request,'showdb.html',{'type': "AdminEvent" ,'aeobj': ae})

def ViewManagerEvents(request):
    me=ManagerEvent.objects.all()
    return render(request,'showdb.html',{'type': "ManagerEvent" ,'meobj': me})

def ViewEvents(request):
    e=Event.objects.all()
    return render(request,'showdb.html',{'type': "Event" ,'eobj': e})

def ViewImages(request):
    i=Images.objects.all()
    return render(request,'showdb.html',{'type': "Images" ,'iobj': i})

def ViewVideos(request):
    v=Videos.objects.all()
    return render(request,'showdb.html',{'type': "Videos" ,'vobj': v})

def All(request):
    c=Customer.objects.all()
    m=Manager.objects.all()
    a=Admin.objects.all()
    ce=CustomerEvent.objects.all()
    ae=AdminEvent.objects.all()
    me=ManagerEvent.objects.all()
    e=Event.objects.all()
    return render(request,'showdb.html',{'type':"all" , 'cobj': c, 'mobj': m , 'aobj': a , 'ceobj': ce , 'aeobj': ae , 'meobj': me , 'eobj': e  })