from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect,HttpResponse
from register.models import Event,Manager,CustomerEvent,Customer,Feedback,Admin

from django.shortcuts import redirect
from django.contrib.sessions.models import Session

from datetime import datetime

# Create your views here.
def alldeleteCustomer(request):
    c=CustomerEvent.objects.all().delete()
    return HttpResponse("deleted all cevent/customers..")

def cverifyuser(request):
    uname=request.POST.get('uname','')
    id=request.POST.get('id','')
    mb=request.POST.get('mobileno','')

    cu=Customer.objects.filter(c_username=uname,c_email=id,c_mobileno=mb)
    if cu.exists():
        return render(request,'csetpassword.html',{'cid':id})
    else:
        return render(request,'cresetpassword.html',{'msg':"Invalid credentials.",'cid':id,'mb': mb})

def setpassword(request):
    password=request.POST.get('pass','')
    confpass=request.POST.get('confpass','')
    cid=request.POST.get('cid','')

    if password == confpass:
        cu=Customer.objects.filter(c_email=cid)
        cu.update(c_password=password)
        return render(request,'customerlogin.html',{'pass':"Password is reset successfully."})
    else:
        return render(request,'csetpassword.html',{'msg':"Invalid password"})

def customerlogin(request):
    c={}
    c.update(csrf(request))
    return render(request,'customerlogin.html',c)

def cloginverify(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')

    c=Customer.objects.filter(c_username=username,c_password=password)
    if c.exists():
        request.session["customer"]=username
        return HttpResponseRedirect('/customer/homepage/')
    else:
        msg="Invalid Username"
        return render(request,'customerlogin.html',{'msg':msg})

def clogout(request):
    try:
        del request.session["customer"]
    except KeyError:
        pass
    return HttpResponseRedirect('/login/loginhome/')

def homepage(request):
    if "customer" in request.session:
        s=Session.objects.get(session_key=request.session.session_key)
        dic=s.get_decoded()
        return render(request,'homepage.html',{'name':dic,'current':request.session["customer"]})
    else:
        msg="You are not logged in."
        return render(request,'customerlogin.html',{'msg':msg})

def bookevent(request):
    c={}
    c.update(csrf(request))
    m=Manager.objects.all()
    etype=[]
    for each in m:
        if each.m_event_type not in etype:
            etype.append(each.m_event_type)
    if len(etype) == 0:
        return render(request,'bookevent.html',{'notetype': True , 'etype': etype })
    else:
        return render(request,'bookevent.html',{'etype':etype})

def searchevent(request):
    eventtype=request.POST.get('eventtype','')
    eventvenue=request.POST.get('eventvenue','')
    eventdate=request.POST.get('eventdate','')
    eventtime=request.POST.get('eventtime','')
    eventcost=request.POST.get('eventcost','')

    event_type2=request.POST.get('event_type2','')
    cus=Customer.objects.get(c_username=request.session["customer"])
    if eventtype=="Other":
        a=Admin.objects.get()
        auser=a.AD_ID
        c=CustomerEvent(m_username=auser,c_username=cus,event_type=event_type2,event_venue=eventvenue,event_date=eventdate,event_time=eventtime,event_cost=eventcost,event_status="requested")
        c.save()
        return render(request,'bookevent.html',{'requestmade': True})
    else:
        m=Manager.objects.get(m_event_type=eventtype)
        muser=m.m_username
        c=CustomerEvent(m_username=muser,c_username=cus,event_type=eventtype,event_venue=eventvenue,event_date=eventdate,event_time=eventtime,event_cost=eventcost,event_status="requested")
        c.save()
        return render(request,'bookevent.html',{'requestmade': True})

    """e=Event.objects.filter(event_type=eventtype,event_venue=eventvenue)
    if e.exists():#If at that place that type of event has been occurred already.
        ce=CustomerEvent.objects.filter(event_type=eventtype,event_venue=eventvenue,event_date=eventdate,event_time=eventtime)
        if ce.exists():#If at that place that type of event has been occurred already at that date and time..So sorry..
            ce=None
            msg="That event slot is already taken."
        else:#If that type,time,date and at that place the event has not been occurred so make request to manager to make event in given cost
            m=Manager.objects.get(m_event_type=eventtype)
            ce=CustomerEvent(c_username=request.session['customer'],m_username=m,event_status="requested",event_type=eventtype,event_cost=eventcost,event_venue=eventvenue,event_date=eventdate,event_time=eventtime)
            ce.save()
            msg="Your event is reqested.with correct all"
    else:#If at that place event has not been occurred yet.
        m=Manager.objects.get(m_event_type=eventtype)
        ce=CustomerEvent(c_username=request.session['customer'],m_username=m,event_status="requested",event_type=eventtype,event_cost=eventcost,event_venue=eventvenue,event_date=eventdate,event_time=eventtime)
        ce.save()
        msg="Your event is reuested.with eventtype and eventvenue"
    return render(request,'bookevent.html',{'msg':msg,'ceobj':ce,'submit':True})"""

def makerequest(request):
    eventtype=request.POST.get('eventtype','')
    eventvenue=request.POST.get('eventvenue','')
    eventdate=request.POST.get('eventdate','')
    eventtime=request.POST.get('eventtime','')

    m=Manager.objects.get(m_event_type=eventtype)
    be=CustomerEvent(m_username=m,event_status="requested",event_type=eventtype,event_venue=eventvenue,event_date=eventdate,event_time=eventtime)
    be.save()
    return render(request,'makerequest.html',{'request_made':True})

def viewrequestedeventstatus(request):
    cus=Customer.objects.get(c_username=request.session["customer"])
    ce=CustomerEvent.objects.filter(c_username=cus)
    return render(request,'viewrequestedeventstatus.html',{'ceobj':ce})

def help(request):
    c={}
    c.update(csrf(request))
    return render(request,'help.html',c)

def cgivefeedback(request):
    username=request.session['customer']
    feedback=request.POST.get('feedback','')
    date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    f=Feedback(F_ID=username,feedback=feedback,date=date_time)
    f.save()
    msg="Your feedback is sent."
    return render(request,'help.html',{'msg':msg})

def profile(request):
    if "customer" in request.session:
        username=request.session["customer"]
        c=Customer.objects.get(c_username=username)
        return render(request,'profile.html',{'cusobj':c})
    else:
        msg="You are not logged in."
        return render(request,'customerlogin.html',{'msg':msg})

def cviewprofile(request):
    username=request.session["customer"]
    c=Customer.objects.get(c_username=username)
    return render(request,'ceditprofile.html',{'cobj':c})

def editprofile(request):
    if "customer" in request.session:
        uname=request.POST.get('uname','')
        name=request.POST.get('name','')
        address=request.POST.get('address','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        mobileno=request.POST.get('mobileno','')
        c=Customer.objects.filter(c_username=uname)
        c.update(c_username=uname,c_name=name,c_address=address,c_email=email,c_password=password,c_mobileno=mobileno)
        return HttpResponseRedirect('/customer/profile/')
    else:
        msg="You are not logged in."
        return render(request,'customerlogin.html',{'msg':msg})