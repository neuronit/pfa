from django.core import management
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
import gym
from .models import *
from .forms import GlobalParametersForm
import json
import os
import sys
import numpy as np

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg

import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np



sys.path.append(os.path.abspath("../back_end/"))


from back_end import multinetworking as mnw
 


def index(request):



    if request.method == 'POST':

        globalForm=GlobalParametersForm(request.POST)
        form= ReseauForm(request.POST)

        
        if form.is_valid():

            #process data in form.cleaned_data as required

            weight=form.cleaned_data['weight']
            victory=form.cleaned_data['victory']
            defeat=form.cleaned_data['defeat']
            hidden_layers=form.cleaned_data['network_layers']
            
            #print(weight,defeat,victory,hidden_layers);
        if globalForm.is_valid():

            epochs=globalForm.cleaned_data['epochs']
            simulations=globalForm.cleaned_data['simulations']
            #print(epochs,simulations)
            return JsonResponse({'success':'true'})
    else:
        form = ReseauForm()
        globalForm= GlobalParametersForm(request.POST)
        
    
    # env=gym.make('CartPole-v0')
    reseau_list= Reseau.objects.all()
    game_list= Game.objects.all()
    reseau_info= Reseau_info.objects.all()
    username=request.user.username
    # bestScore_array = [];
    # for game in game_list:
    #     bestScore_array.append([game.game_name, BestScore.objects.filter(game=game).order_by('-best_score').first().best_score])
    # print(bestScore_array)
    context= {
        'reseau_list': reseau_list,
        'game_list': game_list,
        'form': form,
        'reseau_info': reseau_info,
        'globalForm': globalForm,
        'username': username,
        # 'bestScore_array': bestScore_array
        }

    
    return render(request,'play/play.html',context)


def result_network(request):

    graph = request.GET;

    reseau_list= Reseau.objects.all()
    game_list= Game.objects.all()
    reseau_info= Reseau_info.objects.all()
    
    context= {
        'reseau_list': reseau_list,
        'game_list': game_list,
        'reseau_info': reseau_info,
        } 

    g = dict(graph).keys()[0]
    d = json.loads(g)

    inner = []
    inn = []
    for i in d['p_inner_sizes_array']:
        inn = []
        for j in i:
            inn.append(eval(j))
        inner.append(np.copy(inn))

    print d['p_links_array']

    game_played = Game.objects.filter(game_name=d['game_name']).first() 
    
    save = Save(file="", player_name=d['user_name'], game=game_played,
                name="unknown")
    save.save()


    try:

        save_path, have_been_saved, score_evolution = mnw.multi_networks (d['p_types_array'],
                                                                          d['p_weights_array'],
                                                                          d['p_rewards_array'],
                                                                          d['p_punishs_array'],
                                                                          inner,#d['p_inner_sizes_array'],
                                                                          d['p_links_array'],
                                                                          d['user_name'],
                                                                          d['game_name'],
                                                                          d['game_observation_size'],
                                                                          d['game_decision_size'], 
                                                                          d['max_score'], 
                                                                          d['nb_epochs'], 
                                                                          d['nb_simulations'], 
                                                                          d['save_frequency'], 
                                                                          d['rl_gamma'], 
                                                                          d['rl_epsilon'],
                                                                          d['was_loaded'])
        


    except Exception as exception:
        x, =  exception.args
        print x
        return HttpResponse("error", status=404)
        return JsonResponse({'error':'true'})


    # print d['p_types_array'][1], d['p_weights_array'][1], d['p_rewards_array'][1], d['p_punishs_array'][1], inner [1], d['p_links_array'][1]
    # print save_path, have_been_saved, score_evolution



    ## PLOTING
    
    nb_simulations = d['nb_simulations']
    nb_epochs = d['nb_epochs']

    plt.figure()
    
    for i in range(nb_simulations) :
        plt.plot(range(nb_epochs), score_evolution[i],label="simulation n " + str(i))
    plt.legend()
    plt.xlabel("Training epochs")
    plt.ylabel("Score")
    plt.title("Each graph result")

    if (nb_simulations > 1):
        plt.figure()
        # Return the mean along the row.
        plt.plot(range(nb_epochs),np.mean(score_evolution, axis=0)) # (axis=0 is for row) Axis or axes along which the means are computed.
        plt.xlabel("Training epochs")
        plt.ylabel("Total score")
        plt.title("Mean result")

    plt.show()
    
    # canvas = FigureCanvasAgg(f)
    # response = HttpResponse(content_type='image/png')
    # canvas.print_png(response)
    # matplotlib.pyplot.close(f)

    # return response
                
    
    return JsonResponse({'success':'true'})


def result(request):

    reseau_list= Reseau.objects.all()
    game_list= Game.objects.all()
    reseau_info= Reseau_info.objects.all()

    context= {
        'reseau_list': reseau_list,
        'game_list': game_list,
        'reseau_info': reseau_info,        
        }    

    return JsonResponse({'success':'true'})


# Create your views here.
