# -*- coding: utf-8 -*-

#############################################
#              dependencies                 #
#############################################

import gym # the env
import sys
import os.path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt  # for the logs ans saves
# networks
# --------
from neuralNetworkMaster import mlp
from neuralNetworkMaster import elman
from neuralNetworkMaster import jordan
from neuralNetworkMaster import operators
# others
import global_vars as g
from graph_init import *
from save_and_load import *
from log_writer import *



#############################################
#                  code                     #
#############################################



#===========================================#
# function create_gammas:
# in: rl_gamma
# out: float array gammas: gammas[i] = rl_gamma ** i
#===========================================#

def create_gammas(rl_gamma, rl_epsilon):
    if (rl_gamma < 0 or rl_gamma >= 1 or rl_epsilon <= 0):
        raise Exception('Uncorrect gamma or epsilon')
    gammas = [1, rl_gamma]
    power = 1
    while gammas[power] > rl_epsilon:
        gammas.append(gammas[power]*rl_gamma)
        power += 1
    return gammas



#===========================================#
# function breadth_propagate:
# in: float array observation, the vector given by the OpenAI Gym env at every movements
# out: (id, result) the id of the networks which gave the answer to "out" node, and the result
#-------------------------------------------#
# two points:
# - fifo.pop(0) isn't enough when the operators take several parameters,
#   so we capture all the results to propagate in the current networks,
#   store their index (they will be removed from the fifo stack) into a
#   lifo stack to be sure one pop won't prevent the others (as we pop
#   in the decreasing order of index)
# - we don't know, out of this function, which network's should throw
#   the result into "out", so we need to return the result (and we are
#   sure that the execution will reach "out" thanks to breadth_init())
#===========================================#

def breadth_propagate(observation):
    fifo = [ (i, observation) for i in g.global_links_array[0] ] # Doesn't visit the network of index 0 as his type is "in", it is a faked network.
    while fifo: # The list fifo isn't empty
        # propagation
        # -----------
        (id_network, result_to_propagate) = fifo.pop(0)
        result_array_to_propagate = [result_to_propagate]
        pop_indexes = []
        for i in range(len(fifo)):
            (id_prime, result_prime) = fifo[i]
            if id_prime == id_network: # Gathers several parameters, for operators
                pop_indexes.insert(0,i)
                result_array_to_propagate.append(result_prime)
        for i in pop_indexes:
            fifo.pop(i)
            
        result = g.networks[id_network].propagate_forward(*result_array_to_propagate)
        g.networks_answers_sequences[id_network].insert(0,np.copy(result)) # Saving the sequences for the reinforcement learning.
        # fifo completion for breadth propag
        # ----------------------------------
        # we differ case with the operator of decomposition since it needs to communique different results to the networks after it.
        j = 0
        for i in g.global_links_array[id_network]:
            if (g.global_types_array[i] == "out"):
                return id_network, result
            if g.global_types_array[id_network] == "op_decomp":
                fifo += [(i, result[j])]
                j += 1
            else :
                fifo += [(i, result)]

    
#===========================================#
# function reinforcement_learning:
# in: 
# out: 
#===========================================#

# def reinforcement_learning(done, current_score, max_score, gammas, rl_epsilon, id_result_giver, errors): # no need to alter anything since a new game wiil begin just after this function, which is called at defeat or at victory
                                           
#     power = 0                 
#     # building errors that will be backwarded into all the networks
#     # last_answer = networks_answers_sequences[id_result_giver][current_score]
#     for gamma in gammas:
#         # answer_to_bw = networks_answers_sequences[id_result_giver][current_score - power]
#         # real_target = target + last_answer - answer_to_bw
#         sign = np.sign(g.networks_answers_sequences[id_result_giver][power])
#         if (done) :
#             target = -sign * g.global_punishs_array[id_result_giver]
#         elif (current_score == max_score-1) :
#             target =  sign * g.global_rewards_array[id_result_giver]
#         errors.insert( 0, g.networks[id_result_giver].propagate_backward(target, gammas[power]) )
#         power += 1
            
    # backwarding the errors
    # for id_net in range(1, g.nb_networks-1): # all networks except "in", "out" and 
    #     if id_net != id_result_giver :     # <-- the result giver (already done)
    #         for id_err in range(len(errors)):
    #             target = g.networks_answers_sequences[id_net][current_score - id_err] + errors[id_err]
    #             if (done) :
    #                 real_target = presumed_target * g.global_punishs_array[id_result_giver]
    #             elif (current_score == max_score-1) :
    #                 real_target = presumed_target * g.global_rewards_array[id_result_giver]
    #             g.networks[id_net].propagate_backward(target, gammas[id_err]) 


# Trying to debug
# -------------
def reinforcement_learning(done, current_score, max_score, gammas, rl_epsilon, id_result_giver, errors): # no need to alter anything since a new game wiil begin just after this function, which is called at defeat or at victory
    if done: # Defeat
        power = 0
        for gamma in gammas:
            sign = np.sign(g.networks_answers_sequences[id_result_giver][power][0])
            g.networks[id_result_giver].propagate_backward(-sign*g.global_punishs_array[id_result_giver], gammas[power])
            power += 1
    
    else: # victory
        power = 0
        for gamma in gammas:
            sign = np.sign(g.networks_answers_sequences[id_result_giver][power])
            g.networks[id_result_giver].propagate_backward(sign*g.global_rewards_array[id_result_giver]/2, gammas[power])
            power += 1


                    
#===========================================#
# function" multi_networks:
# in: string array p_types_array:       networks' types (among "in" and "out" for the first and last elements which are the limits of the graph,
#                                       "mlp", "elman" and  "jordan" for the networks, or "op_plus", "op_minus", etc for the operators)
#     float array p_weights_array:      weight_multiplicator used for each network's init
#     float array p_rewards_array:      victory_reward for each network
#     float array p_punishs_array:      defeat_punishment for each network
#                                       ## weights, rewards and punishs = 0 for the types "in", "out" and the operators
#
#     positive int list array p_inner_sizes_array:      Each element i of global_inner_sizes_array corresponds to the network of index i.
#                                                       so global_inner_sizes_array[i] is the list containing the sizes of all layers,
#                                                       except the first one which depends of the last layer size of the network before.
#
#     positive int list array p_links_array:            Each element i of global_links_array corresponds to the network of index i.
#                                                       So global_links_array[i] is the list containing the index of all the reachable
#                                                       neighbors of the network of index i.
#
#     string user_name                        used for saving the logs and the results
#     string game_name,                       ex 'CartPole-v0'
#     positive int game_observation_size,     number of dimensions for the observation vector 
#     positive int game_decision_size,        positive int: number of dimensions for the decision vector 
#     positive int max_score = 200,           positive int: score which makes the game end (200 is the basic OpenAI gym value)
#     positive int nb_epochs = 1000,          positive int: lenght of a simulation (in term of number of games victories or deafeats)
#     positive int nb_simulations = 10,        positive int: number of simulations
#     positive int save_frequency = 100,      positive int: the networks are saved at frequency of save_frequency*epochs
#     flaot in [0,1[ rl_gamma = 0.6,          used for the reinforced learning (if gamma = 0 there won't have reinforced learning)
#     rl_epsilon = 0.05,
#     was_loaded = False
#
# out: nothing
#===========================================#

def multi_networks (p_types_array,
                    p_weights_array,
                    p_rewards_array,
                    p_punishs_array,
                    p_inner_sizes_array,
                    p_links_array,
                    user_name,
                    game_name,
                    game_observation_size,
                    game_decision_size,   
                    max_score = 200,      
                    nb_epochs = 1000,     
                    nb_simulations = 10,   
                    save_frequency = 100, 
                    rl_gamma = 0.6,    
                    rl_epsilon = 0.05,
                    was_loaded = False
                    ):
    
    # assigning the global vars valide for all the simulations
    # --------------------------------------------------------
    g.global_types_array = p_types_array
    g.global_init_weights_array = p_weights_array
    g.global_rewards_array = p_rewards_array
    g.global_punishs_array = p_punishs_array
    g.global_inner_sizes_array = p_inner_sizes_array
    g.global_links_array = p_links_array
    g.nb_networks = len(g.global_types_array)

    # finding cycles --> infinite calcul # NO MORE NEEDED thanks to the grid
    # if(cycle_exists()):
    #     raise Exception("/!\ There is a forbidden cycle")
    
    # log creation
    log = initiate_log(user_name, game_name, nb_simulations, nb_epochs, max_score, rl_gamma, rl_epsilon, was_loaded)
    # running the game
    env = gym.make(game_name)
    # preparing reinforcement learning
    gammas = create_gammas(rl_gamma, rl_epsilon)  # float array: gammas[i] = rl_gamma ** i, putted here for optimisation because of their are a lot of repetitions
    # prepare the plot
    score_evolution = np.zeros([nb_simulations, nb_epochs])
    # prepare the save
    save_header = [p_types_array, p_weights_array,
                   p_rewards_array, p_punishs_array,
                   p_inner_sizes_array, p_links_array,
                   [user_name, game_name,
                    game_observation_size, game_decision_size, 
                    max_score, nb_epochs, nb_simulations,
                    save_frequency, rl_gamma, rl_epsilon]
                   ] # don't put was_loaded into the header, it just serve on the loading
    g.networks_weights = [ [-1 for i in range(g.nb_networks)] for i in range(nb_simulations)]
    save_path = None
    if user_name is not None: # The player is connected
        today = dt.now()
        save_path = "saves/save_" + user_name + "_" + game_name + "_" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + "_" + str(today.hour) + "-" + str(today.minute) +"-" + str(today.second) + ".npz"
    has_been_saved = False

    ########################
    # BEGINING OF THE GAME #
    ########################
    for i_simul in range (nb_simulations):  
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(game_observation_size, game_decision_size)
        # loading
        if was_loaded :  # It remains to update the weights for this simulation.
            for i_net in range(g.nb_networks):   # After the "for", global_load[0] = networks[0] for the next simulation.
                g.networks[net].weights = g.global_load.pop(0).tolist()
        

                
        for i_epoch in range(nb_epochs): # One epoch is like one game : it lasts until the victory or the defeat.

            if user_name is not None: # The player is connected    
                if(save(save_path, i_epoch, nb_epochs, i_simul, save_frequency, save_header)):   # saving
                    has_been_saved = True

            observation = env.reset()   # new game
            errors = []    # float array: contains the errors compute by backwarding the targets into the decision giver network.
            g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]   # The answer sequence of each network is saved in order to opperate the reinforced learning.


            
            for current_score in range(max_score): # For each decision until we win or lost.
                g.networks_answers_sequences[0].append(observation) # if we want to animate the game
                id_result_giver, result = breadth_propagate(observation)
                if result[0] > 0 : # Transforming the networks graph result (so the result of the last network branched onto the "out")
                                # into an action usable by the Open AI environnement
                    action = 1 # often means "right"
                else:
                    action = 0 # often means "left"
                #print "Action is:" + action + "with decision = " + networks_answers_sequences[0][current_score]   # Printing result in order to know if the network makes a "strong" (close to -1 or 1) decision, for debbug.
                observation, reward, done, info = env.step(action)


                
                # Reinforcement learning
                # ----------------------
                if done or (current_score == max_score-1):  # the game is ended by defeat or victory
                    reinforcement_learning(done, current_score, max_score, gammas, rl_epsilon, id_result_giver, errors)
                    score_evolution[i_simul][i_epoch] = current_score + 1
                    write_log(log, i_simul, i_epoch, current_score+1)
                    break   # in the case of defeat, finish with the current score


    # Made by the frontend now
    # for i in range(nb_simulations) :
    #     plt.plot(range(nb_epochs), score_evolution[i],label="simulation n " + str(i))
    # plt.legend()
    # plt.xlabel("Training epochs")
    # plt.ylabel("Score")
    # plt.title("Each graph result")

    # if (nb_simulations > 1):
    #     plt.figure()
    #     # Return the mean along the row.
    #     plt.plot(range(nb_epochs),np.mean(score_evolution, axis=0)) # (axis=0 is for row) Axis or axes along which the means are computed.
    #     plt.xlabel("Training epochs")
    #     plt.ylabel("Total score")
    #     plt.title("Mean result")

    # plt.show()

    log.close()

    return save_path, has_been_saved, score_evolution 
