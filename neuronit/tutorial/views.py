from django.shortcuts import render

from play.models import *
from play.forms import GlobalParametersForm
# Create your views here.

def index(request):

    form = ReseauForm()
    globalForm= GlobalParametersForm()


    reseau_list= Reseau.objects.all()
    
    game_list= Game.objects.all()
    reseau_info= Reseau_info.objects.all()
    
    context= {
        'reseau_list': reseau_list,
        'game_list': game_list,
        'form': form,
        'reseau_info': reseau_info,
        'globalForm': globalForm,

        }


    
    return render(request,'tutorial/tutorial.html', context)
