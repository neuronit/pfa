from django.shortcuts import render
from .models import Carousel, LearnLink, LearnPresentation
from play.models import Game


def homepage(request):
    item_list = Carousel.objects.all()
    game_list = Game.objects.all()

    context = {
        'game_list': game_list,
        'item_list': item_list,
        'item_ids': range(len(item_list)),
    }
    return render(request, 'homepage.html', context)


def learn(request):
    game_list=Game.objects.all()
    link_list = LearnLink.objects.all()
    presentation_list = LearnPresentation.objects.all()

    context = {
        'game_list': game_list,
        'link_list': link_list,
        'presentation_list': presentation_list,
        }
    return render(request,'learn.html',context)
