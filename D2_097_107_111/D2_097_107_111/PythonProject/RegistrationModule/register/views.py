from django.shortcuts import render
from django.template.context_processors import csrf
from register.models import Customer,Manager
from django.http import HttpResponseRedirect
import re
# Create your views here.
def registration(request):
    c={}
    c.update(csrf(request))
    return render(request,'getRegistrationDetails.html',c)

def deleteAll(request):
    c={}
    c.update(csrf(request))
    C=Manager.objects.all().delete()
    return render(request,'getRegistrationDetails.html',c)

def verifyDetails(request):
    name=request.POST.get('name','')
    address=request.POST.get('address','')
    mobile_no=request.POST.get('mobile_no','')
    email=request.POST.get('email','')
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    conpassword=request.POST.get('conpassword','')

    regex_mobile="^\d{10}$"
    regex_email="^\w+@\D+.\D+$"
    valid_email=re.search(regex_email,email)
    valid_mobile=re.search(regex_mobile,mobile_no)

    details={'name':name,'address':address,'mobile_no':mobile_no,'email':email,'username':username,'password':password ,'valid_email':valid_email}
    if(len(name)<20 and len(mobile_no)==10 and len(username)<15 and password==conpassword and valid_email!=None and valid_mobile!=None):
        c=Customer(c_username=username,c_name=name,c_address=address,c_mobileno=mobile_no,c_email=email,c_password=password)
        c.save()
        return render(request,"successfulRegistration.html",details)
    else:
        return render(request,"invalidCredentials.html",details)