from django.shortcuts import render
from play.models import Game, BestScore


def dashboard(request):
    game_list = Game.objects.all()
    best_score_list = BestScore.objects.all().order_by('-best_score')
    context = {
        'game_list': game_list,
        'best_score_list': best_score_list,
    }
    return render(request, 'dashboard/dashboard.html', context)
