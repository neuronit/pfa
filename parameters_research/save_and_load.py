# -*- coding: utf-8 -*-

#############################################
#              dependencies                 #
#############################################

import sys
import os.path
import numpy as np
# others
import global_vars as g 


#############################################
#                  code                     #
#############################################



#===========================================#
# function save:
# in: int i_epoch, nb_epochs & save_frequency: used to know if it is time to save
#     int i_simul: how many simulsations to save (in term of networks weights)
#     array save_header: what to save first
# out: the save path if saved, else the boelean False 
#-------------------------------------------#
# Saves the global_save into a file save_path.
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

def save(save_path, i_epoch, nb_epochs, i_simul, save_frequency, save_header) :
    if save_path is None:
        return False
    g.global_save = []
    if (i_epoch%save_frequency) == 0 or (i_epoch == nb_epochs-1): # We want to save at the frequency save_frequency
                                                                  # and at the last epoch.
        for i_net in range(1, g.nb_networks-1):  # Saving all networks.
            g.networks_weights[i_simul][i_net] = g.networks[i_net].weights # Updating the weights from the networks themselves for this simulation
        g.global_save += save_header # Erasing former save /!\ need a copy
        for simul in range(i_simul+1): # we want to save the previous and the current simuls, so range(i_simul+1)
            for net in range(g.nb_networks):
                g.global_save.append( g.networks_weights[simul][net] ) # Update the current weights.

        user_name = save_header[6][0]
        game_name = save_header[6][1]
        np.savez(save_path, *g.global_save)
        return save_path
    else:
        return False


    
#===========================================#
# function load:
# in: a path ".../file.npz" to load
# out: the params needed to run multi_networks,
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
    g.global_load = []
    if os.path.isfile(path) : # the file exists
        npzfile = np.load(path) # this doesn't load in the correct order, so we have to reorder it
        _load = ['arr_{}'.format(i) for i in range(len(npzfile.files))] # reordered
        g.global_load = [npzfile[i] for i in _load] # loaded in good order

        # extracting the header        # When the header is extracted, the weights remain and will be load during the multi_networks() function 
        # ---------------------        # because we need the instantiated networks to update their weights.
        params = []
        for i in range(6):   # concerns all the "global_***_arrays"
            params.append(g.global_load.pop(0))
        _load = g.global_load.pop(0)   # It concatenates with an array which contains: user_name, g.nb_networks, game_name, game_observation_size, game_decision_size, max_score, nb_epochs, nb_simulations, save_frequency, rl_gamma and rl_epsilon.
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
   
    
