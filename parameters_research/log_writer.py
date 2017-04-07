# -*- coding: utf-8 -*-

from datetime import datetime as dt  # for the logs ans saves
import global_vars as g



#===========================================#
# function initiate_log:
# in: string user_name, string game_name,
#     positive int nb_simulations,
#     positive int nb_epochs, positive int max_score
# out: the openned log file
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
    result_log.write('types array: %s\n'%(g.global_types_array))
    result_log.write('weights array: %s\n'%(g.global_init_weights_array))
    result_log.write('rewards array: %s\n'%(g.global_rewards_array))
    result_log.write('punishs array: %s\n'%(g.global_punishs_array))
    result_log.write('inner sizes_array: %s\n'%(g.global_inner_sizes_array))
    result_log.write('links array: %s\n'%(g.global_links_array))
    result_log.write('===================================================================================\n')
    result_log.write('rl_gamma: %s\nrl_epsilon: %s\nwas_loaded: %s\n'%(rl_gamma, rl_epsilon, was_loaded))
    result_log.write('===================================================================================\n')

    return result_log



#===========================================#
# function write_log:
# in: log: the log fil
#     int simul: current simul
#     int epoch: current epoch
#     int score: current score
# out: nothing
#-------------------------------------------#
# print some results in the log
#===========================================#

def write_log(log, simul, epoch, score):
    log.write('simulation: %s, epoch: %s, score: %s\n'%(simul, epoch, score))
