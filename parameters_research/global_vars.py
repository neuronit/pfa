# -*- coding: utf-8 -*-

#===========================================#
# global vars
#===========================================#

global global_types_array          # string array: networks' types 
                                   # (among "in" and "out" for the first and last elements which are the limits of the graph,
                                   #  "mlp", "elman" and  "jordan" for the networks, or "op_plus", "op_minus", etc for the operators)

global global_init_weights_array   # float array: weight_multiplicator used for each network's init
global global_rewards_array        # float array: victory_reward for each network
global global_punishs_array        # float array: defeat_punishment for each network
                                   ## weights, rewards and punishs = 0 for the types "in", "out" and the operators

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
