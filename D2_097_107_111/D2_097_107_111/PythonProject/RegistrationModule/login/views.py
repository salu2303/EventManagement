from django.shortcuts import render
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def loginhome(request):
    c={}
    c.update(csrf(request))
    return render(request,'loginhome.html',c)

def loginchecker(request):
    return HttpResponse(request.path)