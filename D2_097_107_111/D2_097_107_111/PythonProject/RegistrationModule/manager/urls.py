from django.conf.urls import url
from django.urls import path
from django.shortcuts import render
from . import views
urlpatterns=[
    url(r'^deleteAll/$',views.deleteAll),
    url(r'^givefeedback/$',views.givefeedback),
    url(r'^createevent/$',views.createevent),
    url(r'^managerlogin/$',views.managerlogin),
    url(r'^loginverify/$',views.loginverify),
    url(r'^mlogout/$',views.mlogout),
    url(r'^mgetpreviousevent/$',views.mgetpreviousevent),
    url(r'^updateevent/$',views.updateevent),
    url(r'^viewcreatedevent/$',views.viewcreatedevent),
    url(r'^deleteevent/$',views.deleteevent),
    url(r'^sendevent/$',views.sendevent),
    url(r'^send/$',views.send),
    url(r'^viewapprovedevent/$',views.viewapprovedevent),
    url(r'^viewrejectedevent/$',views.viewrejectedevent),
    url(r'^viewprofile/$',views.viewprofile),
    url(r'^editprofile/$',views.editprofile),
    url(r'^viewrequestedevents/$',views.viewrequestedevents),
    url(r'^acceptevent/$',views.acceptevent),
    url(r'^donotacceptevent/$',views.donotacceptevent),
    url(r'^sendrequesttoadmin/$',views.sendrequesttoadmin),
    #url(r'^logchecker/$',views.logchecker),

    url(r'^mverifyuser/$',views.mverifyuser),
    url(r'^msetpassword/$',views.msetpassword),
    url(r'^mmoredetails',views. mmoredetails),

    path('base2.html',lambda request: render(request,'base2.html')),
    path('managerhome.html',lambda request: render(request,'managerhome.html')),
    path('createevent.html',lambda request: render(request,'createevent.html')),
    path('mupdateevent.html',lambda request: render(request,'mupdateevent.html')),
    path('editprofile.html',lambda request: render(request,'editprofile.html')),
    path('givefeedback.html',lambda request: render(request,'givefeedback.html')),
    path('setCredential.html',lambda request: render(request,'setCredential.html')),
    path('manageevent.html',lambda request: render(request,'manageevent.html')),
    path('mmoredetails.html',lambda request: render(request,'mmoredetails.html')),

    path('mresetpassword.html',lambda request: render(request,'mresetpassword.html')),

    url(r'^setcredential/$',views.setcredential),
]