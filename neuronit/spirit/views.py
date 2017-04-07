from django.core import management
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render









def index(request):

    
    return render(request,'play/play.html',context);



            
    



# Create your views here.

