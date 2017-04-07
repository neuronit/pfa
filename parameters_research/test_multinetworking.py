# -*- coding: utf-8 -*-

#############################################
#              dependencies                 #
#############################################

import gym # the env
import sys
import os.path
import matplotlib.pyplot as plt
import numpy as np
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
from multinetworking import *



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

        # data to save
        g.global_types_array =        ["in","mlp","out"]
        g.global_init_weights_array = [ -1,  0.25,  -1 ]
        g.global_rewards_array =      [ -1,  200,   -1 ]
        g.global_punishs_array =      [ -1,  -1,    -1 ]
        g.global_inner_sizes_array =  [ [],  [4,1], [] ]
        g.global_links_array =        [ [1], [2],   [] ]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1, mlp.MLP(4,4,1), -1]
        
        user_name = "user"
        game_name = "game"
        game_observation_size = 4
        game_decision_size = 1
        max_score = 200
        nb_epochs = 500
        nb_simulations = 5
        g.networks_weights = [ [-1 for i in range(g.nb_networks)] for i in range(nb_simulations)]
        g.networks_weights[0][0] = 42  # test the previous changes are saved
        save_frequency = 1
        rl_gamma = 0.6
        rl_epsilon = 0.1
        # usage: save(i_epoch, nb_epoch, i_simul, save_frequency, save_header)
        # test the save with multiple simulations, and frequency = i_epoch to be sure it will be saved
        i_epoch = 50
        i_simul = 2  
        save_frequency = i_epoch
        
        save_header = [g.global_types_array, g.global_init_weights_array,
                       g.global_rewards_array, g.global_punishs_array,
                       g.global_inner_sizes_array, g.global_links_array,
                       [user_name, game_name,
                        game_observation_size, game_decision_size, 
                        max_score, nb_epochs, nb_simulations,
                        save_frequency, rl_gamma, rl_epsilon]]
        path = save("test.npz", i_epoch, nb_epochs, i_simul, save_frequency, save_header)
        assert(os.path.isfile(path))  # the file exists
        assert(save_header == [g.global_types_array, g.global_init_weights_array,
                               g.global_rewards_array, g.global_punishs_array,
                               g.global_inner_sizes_array, g.global_links_array,
                               [user_name, game_name,
                                game_observation_size, game_decision_size, 
                                max_score, nb_epochs, nb_simulations,
                                save_frequency, rl_gamma, rl_epsilon]])   # the header is constant
        _weights = g.networks_weights[:i_simul+1][:g.nb_networks]
        for w in _weights:
            save_header += w    
        assert(g.global_save == save_header)

        # test the unsave: frequency > i_epoch
        save_frequency = i_epoch + 1
        assert(not save("save", i_epoch, nb_epochs, i_simul, save_frequency, save_header))
        print "Test save() ... OK"

        

        
    def _test__load():
             
        # data to save
        g.global_types_array =        ["in","mlp","out"]
        g.global_init_weights_array = [ -1,  0.25,  -1 ]
        g.global_rewards_array =      [ -1,  200,   -1 ]
        g.global_punishs_array =      [ -1,  -1,    -1 ]
        g.global_inner_sizes_array =  [ [],  [4,1], [] ]
        g.global_links_array =        [ [1], [2],   [] ]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1, mlp.MLP(4,4,1), -1]
        
        user_name = "user"
        game_name = "game"
        game_observation_size = 4
        game_decision_size = 1
        max_score = 200
        nb_epochs = 100
        nb_simulations = 10
        g.networks_weights = [ [-1 for i in range(g.nb_networks)] for i in range(nb_simulations)]
        g.networks_weights[0][0] = 42  # test the previous changes are saved and loaded
        save_frequency = 1
        rl_gamma = 0.6
        rl_epsilon = 0.1
        
        save_header = [g.global_types_array, g.global_init_weights_array,
                       g.global_rewards_array, g.global_punishs_array,
                       g.global_inner_sizes_array, g.global_links_array,
                       [user_name, game_name,
                        game_observation_size, game_decision_size, 
                        max_score, nb_epochs, nb_simulations,
                        save_frequency, rl_gamma, rl_epsilon]]
        
        # usage: save(i_epoch, nb_epoch, i_simul, save_frequency, save_header)
        # test the load with multiple simulations
        i_epoch = 50
        i_simul = 2  
        path = save("test2.npz", i_epoch, nb_epochs, i_simul, save_frequency, save_header)
        ret = load(path)
        true_params = [ g.global_types_array,
                        g.global_init_weights_array,
                        g.global_rewards_array,
                        g.global_punishs_array,
                        g.global_inner_sizes_array,
                        g.global_links_array,
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
                        True ]
        
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
        for i_net in range(len(g.global_load)):
            _weights.append(g.global_load.pop(0).tolist())
            
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

        g.global_links_array =       [ [1], [0,2], [] ]
        g.nb_networks = len(g.global_links_array)
        assert(cycle_exists()), "There should be a cycle within this graph"
        g.global_links_array =       [ [1], [2,0], [] ]
        g.nb_networks = len(g.global_links_array)
        g.networks = [-1 for i in range(g.nb_networks)]
        assert (cycle_exists()), "There should be a cycle within this graph"
        # - no cycle test
        g.global_links_array =       [ [1], [2], [] ]
        g.nb_networks = len(g.global_links_array)
        assert (not cycle_exists()), "There is a forbidden cycle within the graph"

        
        

    def _test__breadth_init():

        #simple case
        g.global_types_array =        ["in","mlp","out"]
        g.global_init_weights_array = [ -1,  0.25,  -1 ]
        g.global_rewards_array =      [ -1,  5,     -1 ]
        g.global_punishs_array =      [ -1,  1,     -1 ]
        g.global_inner_sizes_array =  [ [],  [2,1], [] ]
        g.global_links_array =        [ [1], [2],   [] ]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(4, 1)
        assert (len(g.networks[1].layers[0])-1 == 4) # warn the bias -> -1
        assert (len(g.networks[1].layers[1]) == 2)
        assert (len(g.networks[1].layers[2]) == 1)

        # - op_decomp
        # - op_plus / op_mult with >2 links
        g.global_types_array =        ["in","op_decomp","jordan","elman","mlp","op_avg","out"]
        g.global_init_weights_array = [ -1,  -1,      1,       1,      1,    -1,       -1]
        g.global_rewards_array =      [ -1,  -1,      10,      10,     10,   -1,       -1]
        g.global_punishs_array =      [ -1,  -1,      1,       1,      1,    -1,       -1]
        g.global_inner_sizes_array =  [ [],  [2,1,1], [2,1],   [1,1],  [1,1],[],       []]
        g.global_links_array =        [ [1], [2,3,4], [5],     [5],    [5],  [6],      []]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(4, 1)
        assert (len(g.networks[2].layers[0])-1-1 == 2) # warn the bias and the +firsthidden_layer -> -1-2
        assert (len(g.networks[2].layers[1]) == 2)
        assert (len(g.networks[2].layers[2]) == 1)
        assert (len(g.networks[3].layers[0])-1-1 == 1) # warn the bias and the +exitsize -> -1-1
        assert (len(g.networks[3].layers[1]) == 1)
        assert (len(g.networks[3].layers[2]) == 1)
        assert (len(g.networks[4].layers[0])-1 == 1) # warn the bias -> -1
        assert (len(g.networks[4].layers[1]) == 1)
        assert (len(g.networks[4].layers[2]) == 1)

        # bad decision size
        g.global_links_array =       [ [1], [2,6,4], [5],     [5],    [5],  [6],      []]
        g.networks = [-1 for i in range(g.nb_networks)]
        ok = False
        try:
            breadth_init(4, 2)
        except:
            ok = True
        assert(ok)
        print "Test breadth_init() ... OK"

        
    def _test__breadth_propag():
        
        #simple case
        g.global_types_array =        ["in","op_plus","out"]
        g.global_init_weights_array = [ -1,  -1,    -1 ]
        g.global_rewards_array =      [ -1,  -1,    -1 ]
        g.global_punishs_array =      [ -1,  -1,    -1 ]
        g.global_inner_sizes_array =  [ [],  [],    [] ]
        g.global_links_array =        [ [1,1], [2], [] ]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(4, 4)
        g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]
        giver_id, result = breadth_propagate([1,1,1,1])
        assert(giver_id == 1)
        assert(result.tolist() == [2,2,2,2])
        
        # - op_decomp
        # - op_plus / op_mult with >2 links
        g.global_types_array =        ["in","op_decomp","jordan","elman","mlp","op_avg","out"]
        g.global_init_weights_array = [ -1,  -1,      1,       1,      1,    -1,       -1]
        g.global_rewards_array =      [ -1,  -1,      10,      10,     10,   -1,       -1]
        g.global_punishs_array =      [ -1,  -1,      1,       1,      1,    -1,       -1]
        g.global_inner_sizes_array =  [ [],  [2,1,1], [2,1],   [1,1],  [1,1],[],       []]
        g.global_links_array =        [ [1], [2,3,4], [5],     [5],    [5],  [6],      []]
        g.nb_networks = len(g.global_types_array)
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(4, 1)
        g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]
        giver_id, result = breadth_propagate([0,0,0,0])
        assert(giver_id ==  5)

        # giver before end
        g.global_links_array =       [ [1], [2,6,4], [5],     [5],    [5],  [6],      []]
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(4, 1)
        g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]
        giver_id, result = breadth_propagate([0,0,0,0])
        assert(giver_id ==  1)

        # expected results
        g.global_types_array =        ["in","op_decomp","op_plus","op_tempo","op_minus","out"]
        g.global_init_weights_array = [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_rewards_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_punishs_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_inner_sizes_array =  [ [],  [1,1,1],    [],       [],        [],        []  ]
        g.global_links_array =        [ [1], [2,2,3],    [4],      [4],       [5],       []  ]
        g.nb_networks = len(g.global_types_array) 
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(3, 1)
        g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]
        giver_id, result = breadth_propagate([1,1,1])
        assert(giver_id ==  4)
        assert(result == [1])


        # operators
        g.global_types_array =        ["in","op_decomp","op_plus","op_tempo","op_minus","out"]
        g.global_init_weights_array = [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_rewards_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_punishs_array =      [ -1,  -1,         -1,       -1,        -1,        -1  ]
        g.global_inner_sizes_array =  [ [],  [1,1,1],    [],       [],        [],        []  ]
        g.global_links_array =        [ [1], [2,2,3],    [4],      [4],       [5],       []  ]
        g.nb_networks = len(g.global_types_array) 
        g.networks = [-1 for i in range(g.nb_networks)]
        breadth_init(3, 1)
        g.networks_answers_sequences = [ [] for i in range(g.nb_networks) ]
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
        p_types_array =       ["in","mlp","out"]
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
        print "Test reinforcement_learning() ... OK"
            



    def _test__multi_networks():
        #simple case
        p_types_array =       ["in","mlp","out"]
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
        p_types_array =       ["in","mlp","jordan","elman","op_minus","out"]
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
    _test__reinforcement_learning()
    _test__multi_networks()
