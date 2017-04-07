from django.http import Http404
from django.shortcuts import render
from play.models import Game, Save


def load(request):
    if request.method == "POST":
        save = Save.objects.filter(name=request.POST.get("sel1")).first()
        return render(request, 'play/play.html')
    if request.user.is_authenticated():
        save_list = Save.objects.filter(player_name=request.user.username).order_by('-date')
        context = {
            'save_list': save_list,
        }
        return render(request, 'load/load.html', context)
    else:
        raise Http404
