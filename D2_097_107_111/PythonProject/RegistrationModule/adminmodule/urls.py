from django.conf.urls import url
from django.urls import path,re_path
from django.views.generic import TemplateView
from . import views
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static
#from adminmodule.views import loginCheck

urlpatterns=[
    url(r'^adminlogin/$',views.adminlogin),
    url(r'^addadmin/$',views.addadmin),
    url(r'^storeadmin/$',views.storeadmin),
    url(r'^deleteAll/$',views.deleteAll),
    url(r'^adminhome/$',views.adminhome),
    url(r'^loginverify/$',views.loginverify),

    url(r'^customerrequestedevent/$',views.customerrequestedevent),
    path('customerrequestedevent.html',lambda request: render(request,'customerrequestedevent')),
    url(r'^admindonotacceptevent/$',views.admindonotacceptevent),
    url(r'^adminacceptevent/$',views.adminacceptevent),
    url(r'^rejectedevent/$',views.rejectedevent),
    
    url(r'^moredetails/$',views.moredetails),
    #Manage Event
    #Way-I to render html page directy

    #url(r'^addevent.html$',TemplateView.as_view(template_name="addevent.html"),name="addevent"),
    
    #Way-II
    path('addevent.html',lambda request: render(request,'addevent.html')),
    path('updateevent.html',lambda request: render(request,'updateevent.html')),
    path('deleteevent.html',lambda request: render(request,'deleteevent.html')),

    path('addmanager.html',lambda request:render(request,'addmanager.html')),
    path('updatemanager.html',lambda request:render(request,'updatemanager.html')),
    path('deletemanager.html',lambda request:render(request,'deletemanager.html')),

    url(r'^addevent/$',views.addevent),
    url(r'^deleteAllEvent/$',views.deleteAllEvent),
    url(r'^getpreviousevent/$',views.getpreviousevent),
    url(r'^updateevent/$',views.updateevent),
    url(r'^deleteevent/$',views.deleteevent),
    url(r'^approvedevent/$',views.approvedevent),
    url(r'^unapprovedevent/$',views.unapprovedevent),
    url(r'^newlycreatedevent/$',views.newlycreatedevent),
    url(r'^allevent/$',views.allevent),
    url(r'^alogout/$',views.alogout),

    url(r'^addmanager/$',views.addmanager),
    url(r'^deletemanager/$',views.deletemanager),
    url(r'^viewmanager/$',views.viewmanager),

    url(r'^viewfeedback/$',views.viewfeedback),
    url(r'^makeasapproved/$',views.makeasapproved),
    url(r'^makeasrejected/$',views.makeasrejected),
    

    url(r'^manageyourevents.html/$',lambda request: render(request,'manageyourevents.html')),
    url(r'^manageyourmanager.html/$',lambda request: render(request,'manageyourmanager.html')),


     path('resetpassword.html',lambda request: render(request,'resetpassword.html')),

     url(r'^verifyuser/$',views.verifyuser),
     url(r'^setpassword/$',views.setpassword),
]

"""urlpatterns+=[
    path(r'(?P<path>.*)',loginCheck.as_view(),name="LH")
]"""