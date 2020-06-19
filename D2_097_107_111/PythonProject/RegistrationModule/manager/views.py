from django.shortcuts import render
from register.models import Manager,Customer,Feedback,Images,Videos,ManagerEvent,Event,CustomerEvent
from django.template.context_processors import csrf
from django.contrib.sessions.models import Session
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
import re

from datetime import datetime

# Create your views here.
def deleteAll(request):
    m=Manager.objects.all().delete()
    return HttpResponse('deleted')

def deleteevent(request):
    ManagerEvent.objects.filter(event_ID_id=2).delete()
    return HttpResponse('deleted')

"""def logchecker(request):
    if 'manager' in request.session:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('/manager/managerlogin/')
"""

def mverifyuser(request):
    uname=request.POST.get('uname','')
    id=request.POST.get('id','')
    mb=request.POST.get('mobileno','')

    ma=Manager.objects.filter(m_email=id,m_mobileno=mb,m_username=uname)
    if ma.exists():
        return render(request,'msetpassword.html',{'mid':id})
    else:
        return render(request,'mresetpassword.html',{'msg':"Invalid credentials."})

def msetpassword(request):
    password=request.POST.get('pass','')
    confpass=request.POST.get('confpass','')
    mid=request.POST.get('mid','')

    if password == confpass:
        ma=Manager.objects.filter(m_email=mid)
        ma.update(m_password=password)
        return render(request,'managerlogin.html',{'pass':"Password is reset successfully."})
    else:
        return render(request,'msetpassword.html',{'msg':"Invalid password"})

def setcredential(request):
    muname=request.POST.get('muname','')
    password=request.POST.get('mpassword','')
    eid=request.POST.get('email','')

    m=Manager.objects.filter(m_email=eid)
    if m.exists():
        m.update(m_username=muname,m_password=password)
        return HttpResponse(muname)
        #return render(request,'managerlogin.html',{})
    else:
        return render(request,'setCredential.html',{'msg':"Invalid credentials."})

def mlogout(request):
    c={}
    c.update(csrf(request))
    try:
        del request.session['manager']
    except KeyError:
        pass
    return HttpResponseRedirect("/login/loginhome/")

def managerlogin(request):
    c={}
    c.update(csrf(request))
    return render(request,'managerlogin.html',c)

def loginverify(request):
    musername=request.POST.get('username','')
    mpassword=request.POST.get('password','')

    m=Manager.objects.filter(m_username=musername,m_password=mpassword)
    if m.exists():
        m=m[:1].get()
        request.session['manager']=m.m_username
        msg='Welcome '+m.m_name

        return render(request,'managerhome.html',{'msg':msg})
    else:
        msg='Manager '+m.get().m_name+' does not exist.'
        return render(request,'managerlogin.html',{'msg':msg})

def givefeedback(request):
    username=request.session['manager']
    feedback=request.POST.get('feedback','')
    date_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    f=Feedback(F_ID=username,feedback=feedback,date=date_time)
    f.save()
    msg="Your feedback is sent."
    return render(request,'givefeedback.html',{'msg':msg})

def createevent(request):
    if "manager" in request.session:
        eventname=request.POST.get('eventname','')
        me=Manager.objects.get(m_username=request.session["manager"])
        eventtype=me.m_event_type
        eventtime=request.POST.get('eventtime','')
        eventdate=request.POST.get('eventdate','')
        eventduration=request.POST.get('eventduration','')
        eventvenue=request.POST.get('eventvenue','')
        eventdes=request.POST.get('eventdescription','')
        contactno=request.POST.get('contactno','')
        eventimage=request.FILES['event_image']

        e=Event(event_name=eventname,event_type=eventtype,event_duration=eventduration,event_time=eventtime,event_date=eventdate,event_venue=eventvenue,event_description=eventdes,event_contact_no=contactno,event_image=eventimage)
        e.save()
        eobj=Event.objects.latest('event_ID')

        for more in request.FILES.getlist('images'):
            i=Images(event_ID=eobj,more_images=more)
            i.save()
        for more in request.FILES.getlist('videos'):
            v=Videos(event_ID=eobj,more_videos=more)
            v.save()

        i=Images.objects.filter(event_ID=eobj)         #getting the image object of this event to pass it to showevent.html
        v=Videos.objects.filter(event_ID=eobj)

        musername=request.session["manager"]

        m=Manager.objects.get(m_username=musername)
        me=ManagerEvent(m_username=m,event_ID=eobj,m_event_status="created")    #Saving to admin-events
        me.save()
        return render(request,'mshowevent.html',{'eventobj': eobj,'event_status':me.m_event_status,'media_url':settings.MEDIA_URL,'iobj':i, 'vobj' : v })
    else:
        return render(request,'managerlogin.html',c)

def mgetpreviousevent(request):
    if "manager" in request.session:
        eventname=request.POST.get('eventname','')
        eventdate=request.POST.get('eventdate','')
        eventvenue=request.POST.get('eventvenue','')
        e=Event.objects.filter(event_name=eventname,event_date=eventdate,event_venue=eventvenue)
        if e.exists():
            event=e[:1].get()
            m=ManagerEvent.objects.filter(m_username=request.session["manager"],event_ID_id=event.event_ID)
            if m.exists() and m[:1].get().m_event_status=="created":
                i=Images.objects.filter(event_ID=event)
                v=Videos.objects.filter(event_ID=event)
                return render(request,'mupdate.html',{'eventobj': event,'media_url':settings.MEDIA_URL , 'iobj' : i ,'vobj' : v})
            else:
                return render(request,'mupdateevent.html',{'msg':"Something is wrong"})
        else:
            return render(request,'mupdateevent.html',{'msg':"Something is wrong"})
    else:
        return render(request,'managerlogin.html',None)

def updateevent(request):
    if "manager" in request.session:
        eventname=request.POST.get('eventname','')
        eventtype=request.POST.get('eventtype','')
        eventtime=request.POST.get('eventtime','')
        eventdate=request.POST.get('eventdate','')
        eventduration=request.POST.get('eventduration','')
        eventvenue=request.POST.get('eventvenue','')
        eventdes=request.POST.get('eventdescription','')
        contactno=request.POST.get('contactno','')

        eid=request.POST.get('eventobj','')

        #return HttpResponse(eventimage)
        e=Event.objects.filter(event_ID=eid)
        e.update(event_name=eventname,event_type=eventtype,event_time=eventtime,event_date=eventdate,event_duration=eventduration,event_venue=eventvenue,event_description=eventdes,event_contact_no=contactno)
        e=Event.objects.get(event_ID=eid)

        for more in request.FILES.getlist('images'):         #Saving images to Images table
            i=Images(event_ID=e,more_images=more)
            i.save()
        for more in request.FILES.getlist('videos'):         #Saving videos to Videos table
            v=Videos(event_ID=e,more_videos=more)
            v.save()

        i=Images.objects.filter(event_ID=e)
        v=Videos.objects.filter(event_ID=e)
        me=ManagerEvent.objects.get(m_username=request.session["manager"],event_ID=eid)
        return render(request,'mshowevent.html',{'eventobj': e,'media_url':settings.MEDIA_URL,'event_status':me.m_event_status,'iobj':i,'vobj':v})
    else:
        return render(request,'managerlogin.html',c)

def mmoredetails(request):
    eventid=request.POST.get('eventid','')
    e=Event.objects.get(event_ID=eventid)
    ilist=[]
    vlist=[]
    images=Images.objects.filter(event_ID_id=eventid)
    for each in images:
        ilist.append(each)

    videos=Videos.objects.filter(event_ID_id=eventid)
    for each in videos:
        vlist.append(each)

    return render(request,'mmoredetails.html',{'eventobj':e,'media_url':settings.MEDIA_URL,'iobj':ilist,'vobj':vlist})

def viewcreatedevent(request):
    m=ManagerEvent.objects.filter(m_event_status="created")
    eventlist=[]
    for each in m:
        eid=each.event_ID_id
        e=Event.objects.get(event_ID=eid)
        eventlist.append(e)
    return render(request,'viewcreatedevent.html',{'eventobj':eventlist,'media_url':settings.MEDIA_URL})

def sendevent(request):
    me=ManagerEvent.objects.filter(m_username_id=request.session["manager"])
    elist=[]
    x=0
    for each in me:
        eid=each.event_ID_id
        status=each.m_event_status
        if status == "created":
            e=Event.objects.get(event_ID=eid)
            elist.append(e)

    return render(request,'sendevent.html',{'list':elist,'media_url':settings.MEDIA_URL})

def send(request):
    eventid=request.POST.get('event_id','')
    me=ManagerEvent.objects.filter(event_ID=eventid)
    me.update(m_event_status="unapproved")
    return HttpResponseRedirect('/manager/sendevent/')

def viewapprovedevent(request):
    me=ManagerEvent.objects.filter(m_event_status="approved")
    eventlist=[]
    for each in me:
        eid=each.event_ID_id
        e=Event.objects.get(event_ID=eid)
        eventlist.append(e)
    return render(request,'viewapprovedevent.html',{'eventobj':eventlist,'media_url':settings.MEDIA_URL})

def viewrejectedevent(request):
    me=ManagerEvent.objects.filter(m_event_status="rejected")
    eventlist=[]
    for each in me:
        eid=each.event_ID_id
        e=Event.objects.get(event_ID=eid)
        eventlist.append(e)
    return render(request,'viewrejectedevent.html',{'eventobj':eventlist,'media_url':settings.MEDIA_URL})

def viewprofile(request):
    if "manager" in request.session:
        m=Manager.objects.filter(m_username=request.session["manager"])
        if m.exists():
            m=m[0]
            msg=""
        else:
            msg="Manager not found."
        return render(request,'viewprofile.html',{'msg':msg,'mobj':m})
    else:
        return render(request,'managerlogin.html',{'msg':"You are not loged in."})

def editprofile(request):
    if request.POST.get('submit') == "Edit":
        mname=request.POST.get('mname','')
        musername=request.POST.get('musername','')
        maddress=request.POST.get('maddress','')
        mmobileno=request.POST.get('mmobileno','')
        memail=request.POST.get('memail','')
        meventtype=request.POST.get('meventtype','')
        mpassword=request.POST.get('mpassword','')
        mconpassword=request.POST.get('mconpassword','')

        regex_mobile="^\d{10}$"
        regex_email="^\w+@\D+.\D+$"
        valid_email=re.search(regex_email,memail)
        valid_mobile=re.search(regex_mobile,mmobileno)
        if valid_email!=None and valid_mobile!=None and mpassword==mconpassword:
            m=Manager.objects.filter(m_username=request.session["manager"])
            m.update(m_username=musername,m_name=mname,m_address=maddress,m_mobileno=mmobileno,m_email=memail,m_event_type=meventtype,m_password=mpassword)
            msg="Successfully edited the manager "+mname

            m=Manager.objects.get(m_username=request.session["manager"])
            return render(request,'viewprofile.html',{'msg':msg,'mobj':m})
        else:
            msg="Somethig went wrong."
            m=Manager.objects.get(m_username=request.session["manager"])
            return render(request,'editprofile.html',{'msg':msg,'mobj':m})
    else:
        m=Manager.objects.get(m_username=request.session["manager"])
        return render(request,'editprofile.html',{'mobj':m})

def viewrequestedevents(request):
    manager=request.session["manager"]
    ce=CustomerEvent.objects.filter(m_username=manager,event_status="requested")
    if ce.exists():
        return render(request,'viewrequestedevents.html',{'ceobj':ce,'manager':manager})
    else:
        return render(request,'viewrequestedevents.html',{'ceobj':False,'manager':manager})

def acceptevent(request):
    cuser=request.POST.get('id1','')
    etype=request.POST.get('id2','')
    evenue=request.POST.get('id3','')

    ce=CustomerEvent.objects.filter(c_username=cuser,event_type=etype,event_venue=evenue)
    ce.update(event_status="accepted")
    return HttpResponseRedirect("/manager/viewrequestedevents/")

def donotacceptevent(request):
    cuser=request.POST.get('id1','')
    etype=request.POST.get('id2','')
    evenue=request.POST.get('id3','')

    ce=CustomerEvent.objects.filter(c_username=cuser,event_type=etype,event_venue=evenue)
    ce.update(event_status="rejected")
    return HttpResponseRedirect("/manager/viewrequestedevents/")

def sendrequesttoadmin(request):
    cid=request.POST.get('id','')
    ce=CustomerEvent.objects.filter(id=cid)
    ce.update(event_status="requestedToadmin")
    return HttpResponseRedirect("/manager/viewrequestedevents/")