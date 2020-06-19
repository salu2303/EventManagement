# Create your views here.
from django.shortcuts import render
from register.models import Admin
from django.http import HttpResponseRedirect , HttpResponse
from django.template.context_processors import csrf
from register.models import Images,Videos
from register.models import Event, ManagerEvent,AdminEvent,Manager,Feedback,CustomerEvent

from RegistrationModule.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.conf import settings
from django.contrib.sessions.models import Session
import re
from django.utils.dateparse import parse_date
from datetime import datetime

# Create your views here.

def deleteAll(request):
    c={}
    c.update(csrf(request))
    a=Manager.objects.all()
    count=a.count()
    a.delete()
    return render(request,'addadmin.html',{'a':count})

def verifyuser(request):
    id=request.POST.get('id','')
    a=Admin.objects.filter(AD_ID=id)
    if a.exists():
        return render(request,'setpassword.html',{'a':a})
    else:
        return render(request,'resetpassword.html',{'msg':"Invalid ID"})

def setpassword(request):
    password=request.POST.get('pass','')
    confpassword=request.POST.get('confpass','')
    aid=request.POST.get('aid','')

    if password == confpassword:
        a=Admin.objects.filter(AD_ID=aid)
        a.update(AD_password=password)
        return render(request,'adminlogin.html',{'pass':"Password is reset successfully."})
    else:
        return render(request,'setpassword.html',{'msg':"Invalid password"})
def deleteAllEvent(request):
    c={}
    c.update(csrf(request))
    e=Event.objects.all().delete()
    i=Images.objects.all().delete()
    return render(request,'addevent.html',c)

def alogout(request):
    Session.objects.all().delete()
    """key=request.session['admin']
    s=Session.objects.get(session_key=request.session.session_key)
    dic=s.get_decoded()
    del dic['admin']"""
    #request.session.set_expiry(0),{'dic':dic}
    #return HttpResponseRedirect('/login/loginhome/')
    return HttpResponseRedirect("/login/loginhome/")

def adminlogin(request):
    c={}
    c.update(csrf(request))
    return render(request,'adminlogin.html',c)

def loginverify(request):
    a_id=request.POST.get('id','')
    a_pass=request.POST.get('password','')

    request.session['admin']=a_id
    a=Admin.objects.filter(AD_ID=a_id , AD_password=a_pass)
    if a.exists():
        return HttpResponseRedirect('/adminmodule/adminhome/')
    else:
        return HttpResponseRedirect('/adminmodule/adminlogin/')

def adminhome(request):
    c={}
    c.update(csrf(request))
    if 'admin' in request.session:
        s=Session.objects.get(session_key=request.session.session_key)
        dic=s.get_decoded()
        return render(request,'adminhome.html',{'dic':dic,'request':request})
    else:
        msg="You are not logged in."
        return render(request,'adminlogin.html',{'msg':msg})

def addadmin(request):
    c={}
    c.update(csrf(request))
    return render(request,'addadmin.html',c)

def storeadmin(request):
    a_id=request.POST.get('id','')
    a_pass=request.POST.get('password','')

    all=Admin.objects.all().count()
    if all!=1:
        a=Admin(AD_ID=a_id,AD_password=a_pass)
        a.save()
        return HttpResponseRedirect('/adminmodule/adminlogin/')
    else:
        return render(request,'storeadmin.html',{})

def addevent(request):
    if 'admin' in request.session:
        eventname=request.POST.get('eventname','')
        eventtype=request.POST.get('eventtype','')
        eventtime=request.POST.get('eventtime','')
        eventdate=request.POST.get('eventdate','')
        eventduration=request.POST.get('eventduration','')
        eventvenue=request.POST.get('eventvenue','')
        eventdes=request.POST.get('eventdescription','')
        contactno=request.POST.get('contactno','')
        eventimage=request.FILES['event_image']

        e=Event(event_name=eventname,event_type=eventtype,event_duration=eventduration,event_time=eventtime,event_date=eventdate,event_venue=eventvenue,event_description=eventdes,event_contact_no=contactno,event_image=eventimage)
        e.save()
        event=Event.objects.get(event_name=eventname,event_type=eventtype,event_duration=eventduration,event_time=eventtime,event_date=eventdate,event_venue=eventvenue,event_description=eventdes,event_contact_no=contactno,event_image=eventimage)

        for more in request.FILES.getlist('images'):
            i=Images(event_ID=event,more_images=more)
            i.save()
        for more in request.FILES.getlist('videos'):
            v=Videos(event_ID=event,more_videos=more)
            v.save()

        i=Images.objects.filter(event_ID=event)         #getting the image object of this event to pass it to showevent.html
        v=Videos.objects.filter(event_ID=event)
        admin=Admin.objects.get()
        a=AdminEvent(AD_ID=admin,event_ID=event)    #Saving to admin-events
        a.save()
        return render(request,'showevent.html',{'eventobj': e,'media_url':settings.MEDIA_URL,'iobj':i, 'vobj' : v ,'eventmode': "uploaded" })
    else:
        return render(request,'adminlogin.html',c)

#def newlycreatedevent(request):

def getpreviousevent(request):
    eventname=request.POST.get('eventname','')
    eventtype=request.POST.get('eventtype','')
    date_str=request.POST.get('eventdate','')
    eventdate = parse_date(date_str)
    eventvenue=request.POST.get('eventvenue','')
    e=Event.objects.filter(event_name=eventname,event_type=eventtype,event_date=eventdate,event_venue=eventvenue)
    if e.exists():
        x=True
        event=e[:1].get()
        i=Images.objects.filter(event_ID=event)
        v=Videos.objects.filter(event_ID=event)
        return render(request,'updateevent.html',{'eventobj': event,'media_url':settings.MEDIA_URL ,'x' : x, 'iobj' : i ,'vobj' : v})
    else:
        x=False
        notexist=True
    return render(request,'updateevent.html',{'notexist':notexist})

def updateevent(request):
    if "admin" in request.session:
        eventname=request.POST.get('eventname','')
        eventtype=request.POST.get('eventtype','')
        eventtime=request.POST.get('eventtime','')
        eventdate=request.POST.get('eventdate','')
        eventduration=request.POST.get('eventduration','')
        eventvenue=request.POST.get('eventvenue','')
        eventdes=request.POST.get('eventdescription','')
        contactno=request.POST.get('contactno','')

        eid=request.POST.get('eventobj','')

        e=Event.objects.filter(event_ID=eid)
        e.update(event_name=eventname,event_type=eventtype,event_time=eventtime,event_date=eventdate,event_duration=eventduration,event_venue=eventvenue,event_description=eventdes,event_contact_no=contactno)
        e=Event.objects.get(event_ID=eid)
        event=Event.objects.get(event_name=eventname)

        for more in request.FILES.getlist('images'):         #Saving images to Images table
            i=Images(event_ID=event,more_images=more)
            i.save()
        for more in request.FILES.getlist('videos'):         #Saving videos to Videos table
            v=Videos(event_ID=event,more_videos=more)
            v.save()

        i=Images.objects.filter(event_ID=event)
        v=Videos.objects.filter(event_ID=event)
        return render(request,'showevent.html',{'eventobj': e,'media_url':settings.MEDIA_URL,'iobj':i,'vobj':v,'eventmode': "updated" })
    else:
        return render(request,'adminlogin.html',c)

def deleteevent(request):
    if "admin" in request.session:
        eventid=request.POST.get('eventid','')
        e=Event.objects.filter(event_ID=eventid)
        x=False
        y=False
        if e.exists():
            y=True
            e.delete()
        else:
            x=True
        return render(request,'deleteevent.html',{'x':x,'y':y})
    else:
        return render(request,'adminlogin.html',c)

def approvedevent(request):
    if "admin" in request.session:
        a=AdminEvent.objects.all()
        eventlist=[]
        imagelist=[]
        videolist=[]
        for each_event in a:
            eid=each_event.event_ID_id
            e=Event.objects.get(event_ID=eid)
            i=Images.objects.filter(event_ID_id=e)
            v=Videos.objects.filter(event_ID_id=e)
            eventlist.append(e)
            imagelist.append(i)
            videolist.append(v)
        me=ManagerEvent.objects.filter(m_event_status="approved")
        for each in me:
            eid=each.event_ID_id
            e=Event.objects.get(event_ID=eid)
            i=Images.objects.filter(event_ID_id=e)
            v=Videos.objects.filter(event_ID_id=e)
            eventlist.append(e)
            imagelist.append(i)
            videolist.append(v)
        return render(request,'approvedevent.html',{'eventobj': eventlist,'media_url' : settings.MEDIA_URL,'iobj' : imagelist,'vobj' : videolist})
    else:
        return render(request,'adminlogin.html',c)

def newlycreatedevent(request):
    if "admin" in request.session:
        me=ManagerEvent.objects.filter(m_event_status='created')
        elist=[]
        for each in me:
            eid=each.event_ID_id
            e=Event.objects.get(event_ID=eid)
            elist.append(e)
        return render(request,'newlycreatedevent.html',{'eventobj':elist})
    else:
        return render(request,'adminlogin.html',c)

def allevent(request):
    if "admin" in request.session:
        e=Event.objects.all()
        if e.exists():
            return render(request,'allevent.html',{'eventobj':e})
        else:
            return render(request,'allevent.html',{'notevent': True})
    else:
        return render(request,'adminlogin.html',c)

def addmanager(request):
    if "admin" in request.session:
        mname=request.POST.get('mname','')
        maddress=request.POST.get('maddress','')
        mmobileno=request.POST.get('mmobileno','')
        memail=request.POST.get('memail','')
        meventtype=request.POST.get('meventtype','')

        regex_mobile="^\d{10}$"
        regex_email="^\w+@\D+.\D+$"
        valid_email=re.search(regex_email,memail)
        valid_mobile=re.search(regex_mobile,mmobileno)
        if len(mmobileno)==10 :
            m=Manager(m_name=mname,m_address=maddress,m_mobileno=mmobileno,m_email=memail,m_event_type=meventtype)
            m.save()
            msg="Successfully added the manager "+mname

            res = send_mail("####Successfully Registered####", EMAIL_HOST_USER , "hello",[memail],html_message='Please set your username and password to access the the website.'+'<h4><a href="http://hena123.pythonanywhere.com/manager/setCredential.html">Click here</a></h4>'+" to set username and password.",fail_silently=False,)
            return render(request,'addmanager.html',{'msg': msg,'res':res})
        else:
            msg="Something is wrong."
            return render(request,'addmanager.html',{'msg':msg})
    else:
        c={}
        c.update(csrf(request))
        return render(request,'adminlogin.html',c)

def deletemanager(request):
    musername=request.POST.get('musername','')
    m=Manager.objects.filter(m_username=musername)
    if m.exists():
        me=m.first()
        memail=me.m_email
        deleted=m.count()
        m.delete()
        if deleted==1:
            msg="Successfully deleted the manager "+musername+" and also sent mail."
            res = send_mail("Dismiss from Event management website", EMAIL_HOST_USER ,"hello",[memail],html_message='You are fired from Event management website by admin for some issue.',fail_silently=False,)
        else:
            msg="Something went wrong."
    else:
        msg="Manager does not exist."
    return render(request,'deletemanager.html',{'msg':msg})

def viewmanager(request):
    m=Manager.objects.all()
    return render(request,'viewmanager.html',{'manager':m})

def viewfeedback(request):
    f=Feedback.objects.all()
    return render(request,'viewfeedback.html',{'feedback':f})

def unapprovedevent(request):
    me=ManagerEvent.objects.filter(m_event_status="unapproved")
    eventlist=[]
    for each in me:
        eid=each.event_ID_id
        e=Event.objects.get(event_ID=eid)
        eventlist.append(e)
    return render(request,'unapprovedevent.html',{'eventobj':eventlist,'media_url' : settings.MEDIA_URL})

def makeasapproved(request):
    eid=request.POST.get('event_id','')
    me=ManagerEvent.objects.filter(event_ID_id=eid)
    me.update(m_event_status="approved")
    return HttpResponseRedirect('/adminmodule/unapprovedevent/')

def makeasrejected(request):
    eid=request.POST.get('event_id','')
    me=ManagerEvent.objects.filter(event_ID_id=eid)
    me.update(m_event_status="rejected")
    return HttpResponseRedirect('/adminmodule/unapprovedevent/')

def customerrequestedevent(request):
    ce=CustomerEvent.objects.filter(event_status="requested",m_username=request.session["admin"])
    return render(request,'customerrequestedevent.html',{'ceobj':ce})

def adminacceptevent(request):
    cuser=request.POST.get('id1','')
    etype=request.POST.get('id2','')
    evenue=request.POST.get('id3','')

    ce=CustomerEvent.objects.filter(c_username=cuser,event_type=etype,event_venue=evenue)
    ce.update(event_status="accepted")
    return HttpResponseRedirect("/adminmodule/customerrequestedevent/")

def admindonotacceptevent(request):
    cuser=request.POST.get('id1','')
    etype=request.POST.get('id2','')
    evenue=request.POST.get('id3','')

    ce=CustomerEvent.objects.filter(c_username=cuser,event_type=etype,event_venue=evenue)
    ce.update(event_status="rejected")
    return HttpResponseRedirect("/adminmodule/customerrequestedevent/")

def rejectedevent(request):
    me=ManagerEvent.objects.filter(m_event_status="rejected")
    eventlist=[]
    for each in me:
        eid=each.event_ID_id
        e=Event.objects.get(event_ID=eid)
        eventlist.append(e)
    return render(request,'rejectedevent.html',{'eventobj':eventlist,'media_url' : settings.MEDIA_URL})

def moredetails(request):
    eventid=request.POST.get('eventid','')
    e=Event.objects.get(event_ID=eventid)
    eventstatus=request.POST.get('eventstatus','')
    ilist=[]
    vlist=[]
    images=Images.objects.filter(event_ID_id=eventid)
    for each in images:
        ilist.append(each)

    videos=Videos.objects.filter(event_ID_id=eventid)
    for each in videos:
        vlist.append(each)
    return render(request,'moredetails.html',{'eobj':e,'iobj':ilist,'vobj':vlist,'eventstatus':eventstatus})