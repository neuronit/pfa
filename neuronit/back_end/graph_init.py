# -*- coding: utf-8 -*-

#############################################
#              dependencies                 #
#############################################

# networks
# --------
from neuralNetworkMaster import mlp
from neuralNetworkMaster import elman
from neuralNetworkMaster import jordan
from neuralNetworkMaster import operators
# others
import global_vars as g



#===========================================#
# function create_network:
# in: positive int id_network, string network_type,
#     positive int array size_tab
# out: the instance of the network
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
    
    if network_type == "in" or network_type == "out": # should never happend, it's an emergency case
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
        new_network.set_init_weights_scale(g.global_init_weights_array[id_network])
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
# in: nothing
# out: a boolean
#-------------------------------------------#
# Returns True if there is a cycle,
# else returns False.
# Uses a breadth-first search algortihm
#===========================================#

def cycle_exists():
    fifo = [ i for i in g.global_links_array[0] ] # Neighbors of the "in" network.
    marked = [ False for i in range(g.nb_networks) ]
    marked[0] = True
    for i in fifo:
        marked[i] = True
    visited = [ False for i in range(g.nb_networks) ]
    visited[0] = True

    while fifo:   # The list fifo is not empty.
        id_network = fifo.pop(0)
        visited[id_network] = True
        for i in g.global_links_array[id_network]:
            if visited[i]:    # One of my reachable neighbour has already been visited.
                return True   # => there is a cycle
            if not marked[i]:
                marked[i] = True
                fifo.append(i)
    return False  # No cycle found.



#===========================================#
# function breadth_init:
# in: positive int observation_size, the size of the vector given by the OpenAI Gym env
#     positive int decision_size, the size of the decision to give to the OpenAI Gym env
# out: nothing
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
    
    fifo = [ (i, observation_size) for i in g.global_links_array[0] ]    # don't visit the network of index 0 as his type is "in", it is a faked network
    marked = [ False for i in range(g.nb_networks) ]
    marked[0] = True
    for (i,o) in fifo:
        marked[i] = True
    g.networks[0] = -1
    g.networks[g.nb_networks-1] = -1

    
    while fifo:    # The list fifo is not empty.
        # network's init
        # --------------
        (id_network, first_layer_size) = fifo.pop(0)
        if (g.global_types_array[id_network] == "out"):    # End reached, we don't want to instantiate the "out" network, so returns. Because we explore in breadth first, the last network to be reached is sure to be the exit.
            if (first_layer_size != decision_size):   # The decision size is incorrect.
                raise Exception("/!\ Incorrect dimensions for the decision vector")
            return
        network_type = g.global_types_array[id_network]
        if isinstance(g.global_inner_sizes_array[id_network], list):
            size_tab = [first_layer_size] + g.global_inner_sizes_array[id_network]
        else:
            size_tab = [first_layer_size] + g.global_inner_sizes_array[id_network].tolist()

        g.networks[id_network] = create_network(id_network, network_type, size_tab)
        
        # fifo completion for breadth init
        # --------------------------------
        if isinstance(g.global_inner_sizes_array[id_network], list):
            if g.global_inner_sizes_array[id_network]  : # For operators go else, they have no inner layers.
                last_layer_size = g.global_inner_sizes_array[id_network][-1]
            else: 
                last_layer_size = first_layer_size
        else:
            if g.global_inner_sizes_array[id_network].tolist() :   # For operators go else, they have no inner layers.
                last_layer_size = g.global_inner_sizes_array[id_network][-1]
            else: 
                last_layer_size = first_layer_size
        # Then we differ case with the operator of decomposition since it needs to communique different sizes to the networks after it.
        j = 0
        for i in g.global_links_array[id_network]:
            if not marked[i]:
                marked[i] = True
                if g.global_types_array[id_network] == "op_decomp":
                    fifo += [(i, g.global_inner_sizes_array[id_network][j])]
                    j += 1
                else :

                    fifo += [ (i, last_layer_size) ]
                    
    raise Exception("/!\ Execution will never reach 'out'")
