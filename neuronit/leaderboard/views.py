from django.http import Http404
from django.shortcuts import render
from play.models import Game, BestScore

NUMBER_ROWS_LEADERBOARD = 20


def leaderboard(request, game_id=1):
    game_list = Game.objects.all()
    if int(game_id) > len(game_list):
        raise Http404
    best_score_list = BestScore.objects.filter(game=game_id).order_by('-best_score')
    print_list = best_score_list[:NUMBER_ROWS_LEADERBOARD]
    my_score = None
    if request.user.is_authenticated():
        my_score = BestScore.objects.filter(game=game_id).filter(player_name=request.user.username).order_by(
            '-best_score').first()
    context = {
        'game_list': game_list,
        'best_score_list': print_list,
        'game_id': int(game_id),
        'my_score': my_score,
    }
    return render(request, 'leaderboard/leaderboard.html', context)
