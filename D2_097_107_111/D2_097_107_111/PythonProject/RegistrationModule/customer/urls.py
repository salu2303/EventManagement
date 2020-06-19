from django.conf.urls import url
from django.shortcuts import render
from django.urls import path
from . import views
urlpatterns = [
    url(r'^profile/$',views.profile),
    url(r'^homepage/$',views.homepage),
    url(r'^bookevent/$',views.bookevent),
    url(r'^searchevent/$',views.searchevent),
    url(r'^viewrequestedeventstatus/$',views.viewrequestedeventstatus),
    url(r'^cloginverify/$',views.cloginverify),
    url(r'^clogout/$',views.clogout),
    url(r'^customerlogin/$',views.customerlogin),
    url(r'^cviewprofile/$',views.cviewprofile),
    url(r'^editprofile/$',views.editprofile),
    url(r'^cgivefeedback/$',views.cgivefeedback),


    url(r'^alldeleteCustomer/$',views.alldeleteCustomer),
    #url(r'^makerequest/$',views.makerequest),

    path('help.html',lambda request: render(request,'help.html')),
    path('bookevent.html',lambda request: render(request,'bookevent.html')),
    path('makerequest.html',lambda request: render(request,'makerequest.html')),
    path('viewrequestedeventstatus.html',lambda request: render(request,'viewrequestedeventstatus.html')),


    path('cresetpassword.html',lambda request: render(request,'cresetpassword.html')),
    url(r'^cverifyuser/',views.cverifyuser),
    url(r'^setpassword/',views.setpassword),
]