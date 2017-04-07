# -*- coding: utf-8 -*-

# Method to catch exception, will be used to print errors to user
# try:
#     create_gammas(-1, 0.1)
# except Exception as exception:
#     x, =  exception.args
#     print x





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



#############################################
#                  code                     #
#############################################



#===========================================#
# global vars
#===========================================#

global global_types_array          # string array: networks' types 
                                   # (among "IN" and "OUT" for the first and last elements which are the limits of the graph,
                                   #  "mlp", "elman" and  "jordan" for the networks, or "op_plus", "op_minus", etc for the operators)

global global_init_weights_array        # float array: weight_multiplicator used for each network's init
global global_rewards_array        # float array: victory_reward for each network
global global_punishs_array        # float array: defeat_punishment for each network
                                   ## weights, rewards and punishs = 0 for the types "IN", "OUT" and the operators

global global_inner_sizes_array    # positive int list array: each element i of global_inner_sizes_array corresponds to the network of index i.
                                   #                          So global_inner_sizes_array[i] is the list containing the sizes of all layers,
                                   #                          except the first one which depends of the last layer size of the network before.
                                   
global global_links_array          # positive int list array: each element i of global_links_array corresponds to the network of index i.
                                   #                          So global_links_array[i] is the list containing the index of all the reachable
                                   #                          neighbors of the network of index i.
                                   
global nb_networks
global networks    ## networks[0] = networks[n-1] = -1, all others are instances of networks or operators

global networks_answers_sequences

global global_save
global global_load



#===========================================#
# function create_gammas:
# IN: rl_gamma
# OUT: float array gammas: gammas[i] = rl_gamma ** i
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
# function save:
# IN: int i_epoch, nb_epochs & save_frequency: used to know if it is time to save
#     int i_simul: how many simulsations to save (in term of networks weights)
#     array save_header: what to save first
# OUT: the save path if saved, else the boelean False 
#-------------------------------------------#
# Saves the global_save into a file named after
# the user, the game and the date.
# The file is created if it doesn't exists.
#-------------------------------------------#
# What do we want about the weights ?
#     --> to update the networks' weights
# So we arrange the global_load into a list of weights,
# orderer by increasing number of simulation then
# by increasing id_network, so at each new simulation
# we just have to pop the begining of global_load into
# the networks' weights
#===========================================#

def save(i_epoch, nb_epochs, i_simul, save_frequency, save_header) :
    global nb_networks
    global networks
    global networks_weights
    global global_save
    global_save = []
    if (i_epoch%save_frequency) == 0 or (i_epoch == nb_epochs-1): # We want to save at the frequency save_frequency
                                                                  # and at the last epoch.
        for i_net in range(1, nb_networks-1):  # Saving all networks.
            networks_weights[i_simul][i_net] = networks[i_net].weights # Updating the weights from the networks themselves for this simulation
        global_save += save_header # Erasing former save /!\ need a copy
        for simul in range(i_simul+1): # we want to save the previous and the current simuls, so range(i_simul+1)
            for net in range(nb_networks):
                global_save.append( networks_weights[simul][net] ) # Update the current weights.
        user_name = save_header[6][0]
        game_name = save_header[6][1]
        today = dt.now()
        save_path = "saves/save_" + user_name + "_" + game_name + "_" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + "_" + str(today.hour) + "-" + str(today.minute) +"-" + str(today.second) + ".npz"
        np.savez(save_path, *global_save)
        return save_path
    else:
        return False


    
#===========================================#
# function load:
# IN: a path ".../file.npz" to load
# OUT: the params needed to run multi_networks,
#-------------------------------------------#
# Loads the file "path", extracts the informations
# to run the function multi_networks() with the
# correct parameters, and global_path contains the
# weights of the networks for each simulation.
# Raise an exception if the path is incorrect.
#-------------------------------------------#
# What do we want about the weights ?
#     --> to update the networks' weights
# we arrange the global_load into a list of weights,
# orderer by increasing number of simulation, then
# by increasing id_network, so at each new simulation
# we just have to pop the begining of global_load into
# the networks' weights
#===========================================#

def load(path):
    global global_load
    global_load = []
    if os.path.isfile(path) : # the file exists
        npzfile = np.load(path) # this doesn't load in the correct order, so we have to reorder it
        _load = ['arr_{}'.format(i) for i in range(len(npzfile.files))] # reordered
        global_load = [npzfile[i] for i in _load] # loaded in good order

        # extracting the header        # When the header is extracted, the weights remain and will be load during the multi_networks() function 
        # ---------------------        # because we need the instantiated networks to update their weights.
        params = []
        for i in range(6):   # concerns all the "global_***_arrays"
            params.append(global_load.pop(0))
        _load = global_load.pop(0)   # It concatenates with an array which contains: user_name, nb_networks, game_name, game_observation_size, game_decision_size, max_score, nb_epochs, nb_simulations, save_frequency, rl_gamma and rl_epsilon.
        params.append(_load[0])         # user
        params.append(_load[1])         # game
        params.append(int(_load[2]))    # observation_size
        params.append(int(_load[3]))    # decision_size
        params.append(int(_load[4]))    # max_score
        params.append(int(_load[5]))    # nb_epochs
        params.append(int(_load[6]))    # nb_simulations
        params.append(int(_load[7]))    # save_freq
        params.append(float(_load[8]))  # rl_gamma
        params.append(float(_load[9]))  # rl_epsilon
        params += [True]  # Last parameter: was_loaded = True.
        # --------------------- header extracted
        
        return params
    else:
        raise Exception('Uncorrect path to load')
   
    

#===========================================#
# function initiate_log:
# IN: string user_name, string game_name,
#     positive int nb_simulations,
#     positive int nb_epochs, positive int max_score
# OUT: the openned log file
#-------------------------------------------#
# Creates a text file containing a lot of
# informations about the execution, and returns
# the opened file.
#===========================================#

def initiate_log (user_name, game_name, nb_simulations, nb_epochs, max_score, rl_gamma, rl_epsilon, was_loaded):
    today = dt.now()
    result_log = open("logs/log_" + user_name + "_" + game_name + "_" + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + "_" + str(today.hour) + "-" + str(today.minute) +"-" + str(today.second) + ".txt",'w')
    result_log.write('===================================================================================\n')
    result_log.write('user name: %s\ngame name: %s\nnumber of simulations: %s\nnumber of epochs: %s\nmax score: %s\n'%(user_name, game_name, nb_simulations, nb_epochs, max_score))
    result_log.write('===================================================================================\n')
    result_log.write('types array: %s\n'%(global_types_array))
    result_log.write('weights array: %s\n'%(global_init_weights_array))
    result_log.write('rewards array: %s\n'%(global_rewards_array))
    result_log.write('punishs array: %s\n'%(global_punishs_array))
    result_log.write('inner sizes_array: %s\n'%(global_inner_sizes_array))
    result_log.write('links array: %s\n'%(global_links_array))
    result_log.write('===================================================================================\n')
    result_log.write('rl_gamma: %s\nrl_epsilon: %s\nwas_loaded: %s\n'%(rl_gamma, rl_epsilon, was_loaded))
    result_log.write('===================================================================================\n')

    return result_log



#===========================================#
# function write_log:
# IN: log: the log fil
#     int simul: current simul
#     int epoch: current epoch
#     int score: current score
# OUT: nothing
#-------------------------------------------#
# print some results in the log
#===========================================#

def write_log(log, simul, epoch, score):
    log.write('simulation: %s, epoch: %s, score: %s\n'%(simul, epoch, score))


#===========================================#
# function create_network:
# IN: positive int id_network, string network_type,
#     positive int array size_tab
# OUT: the instance of the network
#-------------------------------------------#
# Returns the instance of the network of the
# good type and size and with the weights
# corretly setted. The networks are also reseted.
#############################################
# IF YOU WANT TO ADD MORE NETWORKS TYPES:
# Don't forget to import files,
# and copy these lines at the correct place:
# if network_type == "myType":
#    new_network = myFileWithoutExtension.MyNetworkClass(*size_tab)
#===========================================#

def create_network(id_network, network_type, size_tab):
    global global_init_weights_array
    if network_type == "IN" or network_type == "OUT": # should never happend, it's an emergency case
        return -1
    # if network
    # ----------
    if network_type == "mlp" or network_type == "elman" or network_type == "jordan" :
        if network_type == "mlp":
            new_network = mlp.MLP(*size_tab)
        if network_type == "elman":
            new_network = elman.Elman(*size_tab)
        if network_type == "jordan":
            new_network = jordan.Jordan(*size_tab)
        # weights init
        new_network.set_init_weights_scale(global_init_weights_array[id_network])
        new_network.reset()

    # if operator
    # -----------
    else :
        if network_type == "op_tempo":
            new_network = operators.OpTempo()
        elif network_type == "op_plus":
            new_network = operators.OpPlus()
        elif network_type == "op_minus":
            new_network = operators.OpMinus()
        elif network_type == "op_mult":
            new_network = operators.OpMult()
        elif network_type == "op_divide":
            new_network = operators.OpDivide()
        elif network_type == "op_avg":
            new_network = operators.OpAvg()
        elif network_type == "op_recomp":
            new_network = operators.OpRecomp()
        elif network_type == "op_decomp":
            new_network = operators.OpDecomp(*(size_tab[1:]))
        # not recognized
        # --------------
        else:
            raise Exception("/!\ network of type = '" + network_type + "' not recognized")

    return new_network



#===========================================#
# function cycle_exists:
# IN: nothing
# OUT: a boolean
#-------------------------------------------#
# Returns True if there is a cycle,
# else returns False.
# Uses a breadth-first search algortihm
#===========================================#

def cycle_exists():
    global global_links_array
    global nb_networks
    fifo = [ i for i in global_links_array[0] ] # Neighbors of the "IN" network.
    marked = [ False for i in range(nb_networks) ]
    marked[0] = True
    for i in fifo:
        marked[i] = True
    visited = [ False for i in range(nb_networks) ]
    visited[0] = True

    while fifo:   # The list fifo is not empty.
        id_network = fifo.pop(0)
        visited[id_network] = True
        for i in global_links_array[id_network]:
            if visited[i]:    # One of my reachable neighbour has already been visited.
                return True   # => there is a cycle
            if not marked[i]:
                marked[i] = True
                fifo.append(i)
    return False  # No cycle found.



#===========================================#
# function breadth_init:
# IN: positive int observation_size, the size of the vector given by the OpenAI Gym env
#     positive int decision_size, the size of the decision to give to the OpenAI Gym env
# OUT: nothing
#-------------------------------------------#
# Initializes all the networks with:
# - correct size, indeed the first layer size
#   is the same as the last layer size of the
#   layer before,
# - init weigths setted,
# - networks are reseted,
# - instances are saved into the array networks[].
# We need to propagate the last layer size to all
# the reachable neighbour, because we don't know
# from where comes the propagation.
#===========================================#

def breadth_init(observation_size, decision_size):
    global global_types_array
    global global_inner_sizes_array
    global global_links_array
    global nb_networks
    global networks
    
    fifo = [ (i, observation_size) for i in global_links_array[0] ]    # don't visit the network of index 0 as his type is "IN", it is a faked network
    marked = [ False for i in range(nb_networks) ]
    marked[0] = True
    for (i,o) in fifo:
        marked[i] = True
    networks[0] = -1
    networks[nb_networks-1] = -1
    
    while fifo:    # The list fifo is not empty.
        # network's init
        # --------------
        (id_network, first_layer_size) = fifo.pop(0)
        if (global_types_array[id_network] == "OUT"):    # End reached, we don't want to instantiate the "OUT" network, so returns. Because we explore in breadth first, the last network to be reached is sure to be the exit.
            if (first_layer_size != decision_size):   # The decision size is incorrect.
                raise Exception("/!\ Incorrect dimensions for the decision vector")
            return
        network_type = global_types_array[id_network]
        size_tab = [first_layer_size] + global_inner_sizes_array[id_network]
        networks[id_network] = create_network(id_network, network_type, size_tab)
        
        # fifo completion for breadth init
        # --------------------------------
        if global_inner_sizes_array[id_network] : # For operators go else, they have no inner layers.
            last_layer_size = global_inner_sizes_array[id_network][-1]
        else: 
            last_layer_size = first_layer_size
        # Then we differ case with the operator of decomposition since it needs to communique different sizes to the networks after it.
        j = 0
        for i in global_links_array[id_network]:
            if not marked[i]:
                marked[i] = True
                if global_types_array[id_network] == "op_decomp":
                    fifo += [(i, global_inner_sizes_array[id_network][j])]
                    j += 1
                else :
                    fifo += [ (i, last_layer_size) ]
                    
    raise Exception("/!\ Execution never reach 'OUT'")

    

#===========================================#
# function breadth_propagate:
# IN: float array observation, the vector given by the OpenAI Gym env at every movements
# OUT: (id, result) the id of the networks which gave the answer to "OUT" node, and the result
#-------------------------------------------#
# two points:
# - fifo.pop(0) isn't enough when the operators take several parameters,
#   so we capture all the results to propagate in the current networks,
#   store their index (they will be removed from the fifo stack) into a
#   lifo stack to be sure one pop won't prevent the others (as we pop
#   in the decreasing order of index)
# - we don't know, out of this function, which network's should throw
#   the result into "OUT", so we need to return the result (and we are
#   sure that the execution will reach "OUT" thanks to breadth_init())
#===========================================#

def breadth_propagate(observation):
    global global_links_array
    global networks
    global networks_answers_sequences
    fifo = [ (i, observation) for i in global_links_array[0] ] # Doesn't visit the network of index 0 as his type is "IN", it is a faked network.
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
            
        result = networks[id_network].propagate_forward(*result_array_to_propagate)
        networks_answers_sequences[id_network].insert(0,np.copy(result)) # Saving the sequences for the reinforcement learning.
        # fifo completion for breadth propag
        # ----------------------------------
        # we differ case with the operator of decomposition since it needs to communique different results to the networks after it.
        j = 0
        for i in global_links_array[id_network]:
            if (global_types_array[i] == "OUT"):
                return id_network, result
            if global_types_array[id_network] == "op_decomp":
                fifo += [(i, result[j])]
                j += 1
            else :
                fifo += [(i, result)]

    
#===========================================#
# function reinforcement_learning:
# IN: 
# OUT: 
#===========================================#

def reinforcement_learning(done, current_score, max_score, gammas, rl_epsilon, id_result_giver, errors): # no need to alter anything since a new game wiil begin just after this function, which is called at defeat or at victory
    global networks_answer_sequence
    global global_punishs_array
    global global_rewards_array
    global networks
    global nb_networks
    global networks_weights
                                           
    power = 0                 
    # building errors that will be backwarded into all the networks
    # last_answer = networks_answers_sequences[id_result_giver][current_score]
    #while gammas[power] > rl_epsilon and power <= current_score :
    for gamma in gammas:
        # answer_to_bw = networks_answers_sequences[id_result_giver][current_score - power]
        # real_target = target + last_answer - answer_to_bw
        presumed_target = np.sign(networks_answers_sequences[id_result_giver][current_score - power])
        if (done) :
            real_target = presumed_target * global_punishs_array[id_result_giver]
        elif (current_score == max_score-1) :
            real_target = presumed_target * global_rewards_array[id_result_giver]
        errors.insert( 0, networks[id_result_giver].propagate_backward(real_target, gammas[power]) )
        power += 1
            
    # backwarding the errors
    for id_net in range(1, nb_networks-1): # all networks except "IN", "OUT" and 
        if id_net != id_result_giver :     # <-- the result giver (already done)
            for id_err in range(len(errors)):
                target = networks_answers_sequences[id_net][current_score - id_err] + errors[id_err]
                if (done) :
                    real_target = presumed_target * global_punishs_array[id_result_giver]
                elif (current_score == max_score-1) :
                    real_target = presumed_target * global_rewards_array[id_result_giver]
                networks[id_net].propagate_backward(target, gammas[id_err]) 


# Trying to debug
# -------------
# def reinforcement_learning(done, current_score, max_score, gammas, rl_epsilon, id_result_giver, errors): # no need to alter anything since a new game wiil begin just after this function, which is called at defeat or at victory
#     global networks_answers_sequences
#     global global_rewards_array
#     global global_punishs_array
#     if done: # Defeat
#         power = 0
#         for gamma in gammas:
#             sign = np.sign(networks_answers_sequences[id_result_giver][power][0])
#             networks[id_result_giver].propagate_backward(-sign*global_punishs_array[id_result_giver], gammas[power])
#             power += 1
    
#     else: # victory
#         power = 0
#         for gamma in gammas:
#             sign = np.sign(networks_answers_sequences[id_result_giver][power])
#             networks[id_result_giver].propagate_backward(sign*global_rewards_array[id_result_giver]/2, gammas[power])
#             power += 1


                    
#===========================================#
# function" multi_networks:
# IN: string array p_types_array:       networks' types (among "IN" and "OUT" for the first and last elements which are the limits of the graph,
#                                       "mlp", "elman" and  "jordan" for the networks, or "op_plus", "op_minus", etc for the operators)
#     float array p_weights_array:      weight_multiplicator used for each network's init
#     float array p_rewards_array:      victory_reward for each network
#     float array p_punishs_array:      defeat_punishment for each network
#                                       ## weights, rewards and punishs = 0 for the types "IN", "OUT" and the operators
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
# OUT: nothing
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

    global global_types_array 
    global global_init_weights_array
    global global_rewards_array
    global global_punishs_array
    global global_inner_sizes_array
    global global_links_array      
    global nb_networks
    global networks
    global networks_weights
    global networks_answers_sequences
    global global_save
    global global_load
    
    # assigning the global vars valide for all the simulations
    # --------------------------------------------------------
    global_types_array = p_types_array
    global_init_weights_array = p_weights_array
    global_rewards_array = p_rewards_array
    global_punishs_array = p_punishs_array
    global_inner_sizes_array = p_inner_sizes_array
    global_links_array = p_links_array
    nb_networks = len(global_types_array)

    # finding cycles --> infinite calcul
    if(cycle_exists()):
        raise Exception("/!\ There is a forbidden cycle")
    
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
    networks_weights = [ [-1 for i in range(nb_networks)] for i in range(nb_simulations)]



    ########################
    # BEGINING OF THE GAME #
    ########################
    for i_simul in range (nb_simulations):  
        networks = [-1 for i in range(nb_networks)]
        breadth_init(game_observation_size, game_decision_size)
        # loading
        if was_loaded :  # It remains to update the weights for this simulation.
            for i_net in range(nb_networks):   # After the "for", global_load[0] = networks[0] for the next simulation.
                networks[net].weights = global_load.pop(0).tolist()
        

                
        for i_epoch in range(nb_epochs): # One epoch is like one game : it lasts until the victory or the defeat.
            save(i_epoch, nb_epochs, i_simul, save_frequency, save_header)   # saving
            observation = env.reset()   # new game
            errors = []    # float array: contains the errors compute by backwarding the targets into the decision giver network.
            networks_answers_sequences = [ [] for i in range(nb_networks) ]   # The answer sequence of each network is saved in order to opperate the reinforced learning.


            
            for current_score in range(max_score): # For each decision until we win or lost.
                networks_answers_sequences[0].append(observation) # if we want to animate the game
                id_result_giver, result = breadth_propagate(observation)
                if result[0] > 0 : # Transforming the networks graph result (so the result of the last network branched onto the "OUT")
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

    log.close()










#############################################
#                 Running                   #
#############################################

if len(sys.argv) == 2: # one arg : loading path
    params = load(sys.argv[1])
    multi_netwoks(*params)

if len(sys.argv) > 2:
    multi_networks(*sys.argv)

    
    
########################################################################################
#======================================================================================#
#--------------------------------    TESTING   ----------------------------------------#
#======================================================================================#
########################################################################################


if len(sys.argv) == 1: # no args => defines (for performance when no testing) and runs tests

    print "Running test ..."

    

    def _test__create_gammas():
        gammas = create_gammas(0.5, 0.1)
        expected = [1, 0.5, 0.25, 0.125, 0.0625]
        assert (gammas == expected)    
        count = 0
        try:
            create_gammas(-1, 0.1)
        except:
            count += 1
        try:
            create_gammas(1, 0.1)
        except:
            count += 1
        try:
            create_gammas(1.1, 0.1)
        except:
            count += 1
        try:
            create_gammas(0.5, 0)
        except:
            count += 1
        try:
            create_gammas(0.5, -0.1)
        except:
            count += 1
        assert(count == 5)
        print "Test create_gammas() ... OK"



        
    def _test__save():
        global global_save
        global global_types_array
        global global_init_weights_array
        global global_rewards_array
        global global_punishs_array
        global global_inner_sizes_array
        global global_links_array
        global nb_networks
        global networks
        global networks_weights

        # data to save
        global_types_array =        ["IN","mlp","OUT"]
        global_init_weights_array = [ -1,  0.25,  -1 ]
        global_rewards_array =      [ -1,  200,   -1 ]
        global_punishs_array =      [ -1,  -1,    -1 ]
        global_inner_sizes_array =  [ [],  [4,1], [] ]
        global_links_array =        [ [1], [2],   [] ]
        nb_networks = len(global_types_array)
        networks = [-1, mlp.MLP(4,4,1), -1]
        
        user_name = "user"
        game_name = "game"
        game_observation_size = 4
        game_decision_size = 1
        max_score = 200
        nb_epochs = 500
        nb_simulations = 5
        networks_weights = [ [-1 for i in range(nb_networks)] for i in range(nb_simulations)]
        networks_weights[0][0] = 42  # test the previous changes are saved
        save_frequency = 1
        rl_gamma = 0.6
        rl_epsilon = 0.1
        # usage: save(i_epoch, nb_epoch, i_simul, save_frequency, save_header)
        # test the save with multiple simulations, and frequency = i_epoch to be sure it will be saved
        i_epoch = 50
        i_simul = 2  
        save_frequency = i_epoch
        
        save_header = [global_types_array, global_init_weights_array,
                       global_rewards_array, global_punishs_array,
                       global_inner_sizes_array, global_links_array,
                       [user_name, game_name,
                        game_observation_size, game_decision_size, 
                        max_score, nb_epochs, nb_simulations,
                        save_frequency, rl_gamma, rl_epsilon]]
        path = save(i_epoch, nb_epochs, i_simul, save_frequency, save_header)
        assert(os.path.isfile(path))  # the file exists
        assert(save_header == [global_types_array, global_init_weights_array,
                               global_rewards_array, global_punishs_array,
                               global_inner_sizes_array, global_links_array,
                               [user_name, game_name,
                                game_observation_size, game_decision_size, 
                                max_score, nb_epochs, nb_simulations,
                                save_frequency, rl_gamma, rl_epsilon]])   # the header is constant
        _weights = networks_weights[:i_simul+1][:nb_networks]
        for w in _weights:
            save_header += w    
        assert(global_save == save_header)

        # test the unsave: frequency > i_epoch
        save_frequency = i_epoch + 1
        assert(not save(i_epoch, nb_epochs, i_simul, save_frequency, save_header))
        print "Test save() ... OK"

        

        
    def _test__load():
        global global_save
        global global_types_array
        global global_init_weights_array
        global global_rewards_array
        global global_punishs_array
        global global_inner_sizes_array
        global global_links_array
        global nb_networks
        global networks
        global networks_weights
        
        # data to save
        global_types_array =        ["IN","mlp","OUT"]
        global_init_weights_array = [ -1,  0.25,  -1 ]
        global_rewards_array =      [ -1,  200,   -1 ]
        global_punishs_array =      [ -1,  -1,    -1 ]
        global_inner_sizes_array =  [ [],  [4,1], [] ]
        global_links_array =        [ [1], [2],   [] ]
        nb_networks = len(global_types_array)
        networks = [-1, mlp.MLP(4,4,1), -1]
        
        user_name = "user"
        game_name = "game"
        game_observation_size = 4
        game_decision_size = 1
        max_score = 200
        nb_epochs = 100
        nb_simulations = 10
        networks_weights = [ [-1 for i in range(nb_networks)] for i in range(nb_simulations)]
        networks_weights[0][0] = 42  # test the previous changes are saved and loaded
        save_frequency = 1
        rl_gamma = 0.6
        rl_epsilon = 0.1
        
        save_header = [global_types_array, global_init_weights_array,
                       global_rewards_array, global_punishs_array,
                       global_inner_sizes_array, global_links_array,
                       [user_name, game_name,
                        game_observation_size, game_decision_size, 
                        max_score, nb_epochs, nb_simulations,
                        save_frequency, rl_gamma, rl_epsilon]]
        
        # usage: save(i_epoch, nb_epoch, i_simul, save_frequency, save_header)
        # test the load with multiple simulations
        i_epoch = 50
        i_simul = 2  
        path = save(i_epoch, nb_epochs, i_simul, save_frequency, save_header)
        ret = load(path)
        true_params = [ global_types_array,
                        global_init_weights_array,
                        global_rewards_array,
                        global_punishs_array,
                        global_inner_sizes_array,
                        global_links_array,
                        user_name,
                        game_name,
                        game_observation_size,
                        game_decision_size,
                        max_score,
                        nb_epochs,
                        nb_simulations,
                        save_frequency,
                        rl_gamma,
                        rl_epsilon,
                        True]
        
        assert(len(ret) == len(true_params))
        for i in range(6):
            assert(len(ret[i]) == len(true_params[i]))
            for j in range(len(ret[i])):
                assert(ret[i][j] == true_params[i][j])
        for i in range(6, len(ret)):
            assert(ret[i] == true_params[i])

        # What do we want about the weights ? --> to update the networks' weights
        # we arrange the global_load in a file of weights,
        # orderer by increasing number of simulation, then
        # by increasing id_network, so at each new simulation
        # we just have to pop the begining of global_load into
        # the networks' weights
        _weights = []
        for i_net in range(len(global_load)):
            _weights.append(global_load.pop(0).tolist())
            
        #print _weights, networks_weights    #### visually, lots of problem trying to test equality of arrays
        # for simul in range(i_simul+1):
        #     for net in range(nb_networks):
        #         a = _weights[simul*nb_networks+net]
        #         b = networks_weights[simul][net]
        #         assert(a == b)
        
        # test bad path
        path = "not_this_path"
        ok = False
        try:
            load(path)
        except:
            ok = True
        assert(ok)
        print "Test load() ... OK"
        
        

        
    def _test__cycle_exists():
        # - cycle tests
        global global_links_array
        global nb_networks
        global_links_array =       [ [1], [0,2], [] ]
        nb_networks = len(global_links_array)
        assert(cycle_exists()), "There should be a cycle within this graph"
        global_links_array =       [ [1], [2,0], [] ]
        nb_networks = len(global_links_array)
        networks = [-1 for i in range(nb_networks)]
        assert (cycle_exists()), "There should be a cycle within this graph"
        # - no cycle test
        global_links_array =       [ [1], [2], [] ]
        nb_networks = len(global_links_array)
        assert (not cycle_exists()), "There is a forbidden cycle within the graph"

        
        

    def _test__breadth_init():
        global global_types_array
        global global_init_weights_array
        global global_rewards_array
        global global_punishs_array
        global global_inner_sizes_array
        global global_links_array
        global networks
        global nb_networks

        #simple case
        global_types_array =        ["IN","mlp","OUT"]
        global_init_weights_array = [ -1,  0.25,  -1 ]
        global_rewards_array =      [ -1,  5,     -1 ]
        global_punishs_array =      [ -1,  1,     -1 ]
        global_inner_sizes_array =  [ [],  [2,1], [] ]
        global_links_array =        [ [1], [2],   [] ]
        nb_networks = len(global_types_array)
        networks = [-1 for i in range(nb_networks)]
        breadth_init(4, 1)
        assert (len(networks[1].layers[0])-1 == 4) # warn the bias -> -1
        assert (len(networks[1].layers[1]) == 2)
        assert (len(networks[1].layers[2]) == 1)

        # - op_decomp
        # - op_plus / op_mult with >2 links
        global_types_array =        ["IN","op_decomp","jordan","elman","mlp","op_avg","OUT"]
        global_init_weights_array = [ -1,  -1,      1,       1,      1,    -1,       -1]
        global_rewards_array =      [ -1,  -1,      10,      10,     10,   -1,       -1]
        global_punishs_array =      [ -1,  -1,      1,       1,      1,    -1,       -1]
        global_inner_sizes_array =  [ [],  [2,1,1], [2,1],   [1,1],  [1,1],[],       []]
        global_links_array =        [ [1], [2,3,4], [5],     [5],    [5],  [6],      []]
        nb_networks = len(global_types_array)
        networks = [-1 for i in range(nb_networks)]
        breadth_init(4, 1)
        assert (len(networks[2].layers[0])-1-1 == 2) # warn the bias and the +firsthidden_layer -> -1-2
        assert (len(networks[2].layers[1]) == 2)
        assert (len(networks[2].layers[2]) == 1)
        assert (len(networks[3].layers[0])-1-1 == 1) # warn the bias and the +exitsize -> -1-1
        assert (len(networks[3].layers[1]) == 1)
        assert (len(networks[3].layers[2]) == 1)
        assert (len(networks[4].layers[0])-1 == 1) # warn the bias -> -1
        assert (len(networks[4].layers[1]) == 1)
        assert (len(networks[4].layers[2]) == 1)

        # bad decision size
        global_links_array =       [ [1], [2,6,4], [5],     [5],    [5],  [6],      []]
        networks = [-1 for i in range(nb_networks)]
        ok = False
        try:
            breadth_init(4, 2)
        except:
            ok = True
        assert(ok)
        print "Test breadth_init() ... OK"

        
    def _test__breadth_propag():
        global global_types_array
        global global_init_weights_array
        global global_rewards_array
        global global_punishs_array
        global global_inner_sizes_array
        global global_links_array
        global networks
        global nb_networks
        global networks_answers_sequences
        
        #simple case
        global_types_array =        ["IN","op_plus","OUT"]
        global_init_weights_array = [ -1,  -1,    -1 ]
        global_rewards_array =      [ -1,  -1,    -1 ]
        global_punishs_array =      [ -1,  -1,    -1 ]
        global_inner_sizes_array =  [ [],  [],    [] ]
        global_links_array =        [ [1,1], [2], [] ]
        nb_networks = len(global_types_array)
        networks = [-1 for i in range(nb_networks)]
        breadth_init(4, 4)
        networks_answers_sequences = [ [] for i in range(nb_networks) ]
        giver_id, result = breadth_propagate([1,1,1,1])
        assert(giver_id == 1)
        assert(result.tolist() == [2,2,2,2])
        
        # - op_decomp
        # - op_plus / op_mult with >2 links
        global_types_array =        ["IN","op_decomp","jordan","elman","mlp","op_avg","OUT"]
        global_init_weights_array = [ -1,  -1,      1,       1,      1,    -1,       -1]
        global_rewards_array =      [ -1,  -1,      10,      10,     10,   -1,       -1]
        global_punishs_array =      [ -1,  -1,      1,       1,      1,    -1,       -1]
        global_inner_sizes_array =  [ [],  [2,1,1], [2,1],   [1,1],  [1,1],[],       []]
        global_links_array =        [ [1], [2,3,4], [5],     [5],    [5],  [6],      []]
        nb_networks = len(global_types_array)
        networks = [-1 for i in range(nb_networks)]
        breadth_init(4, 1)
        networks_answers_sequences = [ [] for i in range(nb_networks) ]
        giver_id, result = breadth_propagate([0,0,0,0])
        assert(giver_id ==  5)

        # giver before end
        global_links_array =       [ [1], [2,6,4], [5],     [5],    [5],  [6],      []]
        networks = [-1 for i in range(nb_networks)]
        breadth_init(4, 1)
        networks_answers_sequences = [ [] for i in range(nb_networks) ]
        giver_id, result = breadth_propagate([0,0,0,0])
        assert(giver_id ==  1)

        # expected results
        global_types_array =        ["IN","op_decomp","op_plus","op_tempo","op_minus","OUT"]
        global_init_weights_array = [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_rewards_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_punishs_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_inner_sizes_array =  [ [],  [1,1,1],    [],       [],        [],        []  ]
        global_links_array =        [ [1], [2,2,3],    [4],      [4],       [5],       []  ]
        nb_networks = len(global_types_array) 
        networks = [-1 for i in range(nb_networks)]
        breadth_init(3, 1)
        networks_answers_sequences = [ [] for i in range(nb_networks) ]
        giver_id, result = breadth_propagate([1,1,1])
        assert(giver_id ==  4)
        assert(result == [1])


        # operators
        global_types_array =        ["IN","op_decomp","op_plus","op_tempo","op_minus","OUT"]
        global_init_weights_array = [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_rewards_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_punishs_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        global_inner_sizes_array =  [ [],  [1,1,1],    [],       [],        [],        []  ]
        global_links_array =        [ [1], [2,2,3],    [4],      [4],       [5],       []  ]
        nb_networks = len(global_types_array) 
        networks = [-1 for i in range(nb_networks)]
        breadth_init(3, 1)
        networks_answers_sequences = [ [] for i in range(nb_networks) ]
        giver_id, result = breadth_propagate([1,1,1])
        assert(giver_id ==  4)
        assert(result == [1])

        print "Test breadth_propag() ... OK"


        
    def _test__reinforcement_learning():
        # Version d'apprentissage non corrigée (pas d'apprentissage pendant la victoire) :
        # Hyperopt trial # 3000
        # Resultat fourni par HyperOpt ('y' est une valeur négative, rajouter un '-' devant la valeur affichée) :
        # {'y': 0.26276664905448405, 'x': 0.1908486277831362, 's': 45, 'z': 0.2706882443595372}
        # -------------------------------------------------------------
        # Version d'apprentissage corrigée :
        # Hyperopt trial # 3000
        # Resultat fourni par HyperOpt ('y' est une valeur négative, rajouter un '-' devant la valeur affichée) :
        # {'y': 0.1560650012178876, 'x': 0.18636298764849027, 's': 34, 'z': 0.06957097548475873}
        # -------------------------------------------------------------
        # Attributions des paramètres :
        # weight_multiplicator = x
        # defeat_punishment = y
        # victory_reward = z
        # network_param = [s]
        
        # simple case
        p_types_array =       ["IN","mlp","OUT"]
        p_weights_array =     [ -1,  0.18636298764849027,  -1 ]
        p_rewards_array =     [ -1,  0.06957097548475873,   -1 ]
        p_punishs_array =     [ -1,  -0.1560650012178876,    -1 ]
        p_inner_sizes_array = [ [],  [34,1], [] ]
        p_links_array =       [ [1], [2],   [] ]

        multi_networks (p_types_array,
                        p_weights_array,
                        p_rewards_array,
                        p_punishs_array,
                        p_inner_sizes_array,
                        p_links_array,
                        "toto",
                        'CartPole-v0', 
                        4,
                        1,
                        max_score = 200,
                        nb_epochs = 300,
                        nb_simulations = 1,
                        save_frequency = 2000,
                        rl_gamma = 0.6,
                        rl_epsilon = 0.1,
                        was_loaded = False
                    )

        # print "Test reinforcement_learning() ... OK"
        nb_epochs = 300
        max_score = 200
        network = mlp.MLP(4,34,1)
        network.set_init_weights_scale(0.18636298764849027)
        network.reset()
        epsilon = 0.1
        defeat_punishment = -0.1560650012178876
        victory_reward = 0.06957097548475873
        gamma = 0.6
        score_evolution = []
        power = 1
        i = 0

        env = gym.make('CartPole-v0')
        for i_epoch in range(nb_epochs):
            observation = env.reset()
            answer_sequence = []
            for current_score in range(max_score):
                network_result = network.propagate_forward(observation)

                if network_result[0]>0 :      
                    action = 1
                    ans = "right"
                else:
                    action = 0
                    ans = "left"
                answer_sequence = [ans] + answer_sequence
                observation, reward, done, info = env.step(action)
                if done :
                    power = 1
                    i = 0
                    while power > epsilon and i < len(answer_sequence):
                        if answer_sequence[i] == "right" :
                            network.propagate_backward(-defeat_punishment,power)
                        
                        else :
                            network.propagate_backward(defeat_punishment,power)
                        i+=1
                        power*=gamma
                    score_evolution.append(current_score+1)
                    break
                if current_score == max_score-1 :
                    power = 1
                    i = 0
                    while power > epsilon and i < len(answer_sequence):
                        if answer_sequence[i] == "right" :
                            network.propagate_backward(victory_reward,power)
                        else :
                            network.propagate_backward(-victory_reward,power)
                        i+=1
                        power*=gamma
                    score_evolution.append(current_score+1)
        plt.figure()
        plt.plot(range(nb_epochs),score_evolution)
        plt.show()
            



    def _test__multi_networks():
        #simple case
        p_types_array =       ["IN","mlp","OUT"]
        p_weights_array =     [ -1,  0.25,  -1 ]
        p_rewards_array =     [ -1,  5,     -1 ]
        p_punishs_array =     [ -1,  1,     -1 ]
        p_inner_sizes_array = [ [],  [2,1], [] ]
        p_links_array =       [ [1], [2],   [] ]

        multi_networks (p_types_array,
                        p_weights_array,
                        p_rewards_array,
                        p_punishs_array,
                        p_inner_sizes_array,
                        p_links_array,
                        "toto",
                        'CartPole-v0', 
                        4,
                        1,
                        max_score = 200,
                        nb_epochs = 100,
                        nb_simulations = 2,
                        save_frequency = 1,
                        rl_gamma = 0.6,
                        rl_epsilon = 0.05,
                        was_loaded = False
                    )

        # - severals targets to init from one network
        # - order of propag for op_minus / op_divide
        p_types_array =       ["IN","mlp","jordan","elman","op_minus","OUT"]
        p_weights_array =     [ -1,  1,    1,       1,      -1,       -1]
        p_rewards_array =     [ -1,  10,   10,      10,     -1,       -1]
        p_punishs_array =     [ -1,  1,    1,       1,      -1,       -1]
        p_inner_sizes_array = [ [],  [2,2],[2,1],   [2,2,1],[],       []]
        p_links_array =       [ [1], [2,3],[4],     [4],    [5],      []]

        multi_networks (p_types_array,
                        p_weights_array,
                        p_rewards_array,
                        p_punishs_array,
                        p_inner_sizes_array,
                        p_links_array,
                        "toto",
                        'CartPole-v0', 
                        4,
                        1,
                        max_score = 200,
                        nb_epochs = 100,
                        nb_simulations = 2,
                        save_frequency = 1,
                        rl_gamma = 0.6,
                        rl_epsilon = 0.05,
                        was_loaded = False
                      )
        print "Test multi_networks() ... OK"




    
    _test__create_gammas()
    _test__save()
    _test__load()
    _test__cycle_exists()
    _test__breadth_init()
    _test__breadth_propag()
    _test__reinforcement_learning() # bad results of learning for now
    #_test__multi_networks()












