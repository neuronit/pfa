# -*- coding: utf-8 -*-
#############################################
#              CartPole-v0                  #
#############################################

#############################################
#              dependencies                 #
#############################################


import gym
import sys
import os.path
from user_param import *
from hyperopt import fmin,tpe,hp,rand
from datetime import datetime as dt
from neuralNetworkMaster import mlp
from neuralNetworkMaster import elman
from neuralNetworkMaster import jordan
import matplotlib.pyplot as plt
import numpy as np

#############################################
#       user params are like this           #
#############################################


# parameters modifying the behaviour of the network

# global weight_multiplicator                       # multiplicator of a returned observation, allow to scale observations in order to make the network differentiate them
# weight_multiplicator = 0.25
# global victory_reward
# victory_reward = 0                                 # reward at win
# global defeat_punishment
# defeat_punishment = 1                              # punishment given when the game is lost (pool fall or cart get out of bound)
# global network_param
# network_param = [4]                                # shape of hidden layers
#
# network_type = "mlp"                             # network_type ("mlp", "elman")
#
# # parameters modifying the result display (might not be change by a common user)
#
# max_score = 200                          # score which makes the game end (200 is the basic OpenAI gym value)
# nb_seq = 1000                           # lenght of a simulation
# nb_simulation = 100                        # number of simulations
# save_frequency = 100
# gamma = 0.6
#
# pro_level_exists = 0                               # if set to 1, the network stop learning after winning a game



#############################################
#                  code                     #
#############################################

global trial_nr_in_hyperopt
trial_nr_in_hyperopt = 1 #initialize counter of "evals"/trials


today = dt.now()
result_log = open("log " + str(today.day) + "-" + str(today.month) + "-" + str(today.year) + " " + str(today.hour) + ":" + str(today.minute) +":" + str(today.second) + ".txt",'w')

result_log.write('===================================================================================\n')
result_log.write('number of simulations : %s, number of epochs : %s, max score : %s\n'%(nb_simulation,nb_seq,max_score))
result_log.write('===================================================================================\n')

score_evolution = np.zeros([nb_simulation,nb_seq])
# axis = [i for i in range(nb_seq)]

def loadsave(array,episode,path=None):
    if nb_simulation == 1 :
        if len(sys.argv) > 5:
            path = sys.argv[5]
        if path != None:
            if episode == 0:
                if os.path.isfile(path) :
                    array = np.load(path)
                    print "file loaded"
                else :
                    np.save(path,array)
                    print "file created"
            else:
                np.save(path,array)
                print "file saved at episode " + str(episode)
    return array



def Mcar(network,seq,lrate=.1, momentum=0.1):
    env = gym.make('CartPole-v0')
    learning = 1
    epsilon = 0.05
    power = 1
    i = 0
    successful_learning = 0
    for i_episode in range(nb_seq):
        if (i_episode%save_frequency) == 0 or (i_episode==nb_seq-1):
            #TODO: Que faites-vous ici ? Je ne vois aucun fichier sauvegardé, et vu la rapidité d'exécution ça semble inutile de sauvegarder aussi souvent pour ce jeu
            # print "saving network.weights"
            network.weights = loadsave(network.weights,i_episode)
        observation = env.reset()
        answer_sequence = []
        for t in range(max_score):
            #env.render()
            network_result = network.propagate_forward(observation)
            if network_result[0]>0 :                                                                  # transform the network result into an action usable by the Open AI environnement
                action = 1
                ans = "right"
            else:
                action = 0
                ans = "left"
            #print "action :" , ans , network_result[0]                                                # printing result in order to know if the network makes a "strong" decision
            answer_sequence = [ans] + answer_sequence
            observation, reward, done, info = env.step(action)
            # if learning ==  1 :
            #     if not done:                                                                          # the network is rewarded while the cart is alive
            #          if ans == "right" :
            #              network.propagate_backward(0,lrate,momentum)
            #          else :
            #              network.propagate_backward(0,lrate,momentum)
            if done :                                                                                 # apply the defeat punishment when the cart dies
                #print ans
                if learning == 1 :
                    successful_learning = 0
                    power = 1
                    i = 0
                    while power > epsilon and i < len(answer_sequence):
                        if answer_sequence[i] == "right" :
                            network.propagate_backward(-defeat_punishment,power,lrate,momentum)

                        else :
                            network.propagate_backward(defeat_punishment,power,lrate,momentum)
                        i+=1
                        power*=gamma
                #print("Episode finished after {} timesteps".format(t+1))
                score_evolution[seq][i_episode]=t+1
                break
            if t == max_score-1 :                                                                     # if the cart survives, gives it the maximum score
                if pro_level_exists == 1 :                                                            # if pro_level is set to 1, stop learning
                    successful_learning += 1
                    if successful_learning == 20:
                        learning = 0
                while power > epsilon and i < len(answer_sequence):
                    if answer_sequence[i] == "right" :
                        network.propagate_backward(victory_reward,power,lrate,momentum)

                    else :
                        network.propagate_backward(-victory_reward,power,lrate,momentum)
                    i+=1
                    power*=gamma
                score_evolution[seq][i_episode] = t+1

def avg_list(x,y,z,s):

    global victory_reward
    global weight_multiplicator
    global defeat_punishment
    global network_param
    global network_size

    global trial_nr_in_hyperopt

    if len(sys.argv) == 1:
        print "Hyperopt trial #", trial_nr_in_hyperopt

    weight_multiplicator = x
    defeat_punishment = y
    victory_reward = z
    network_param = [s]
    result_log.write ("weight multiplicator : %s\ndefeat punishment : %s\nvictory reward : %s\nnetwork param : %s\n" % (x,y,z,s))
    network_size = [4]+network_param+[1]
    print network_size
    if network_type == "mlp":
        network = mlp.MLP(*network_size)
    if network_type =="elman":
        network = elman.Elman(*network_size)

    for i in range(nb_simulation) :
        network.set_init_weights_scale(weight_multiplicator) #xav
        network.reset()
        Mcar(network,i)
    # ret =  max_score-np.average(score_evolution)
    ret =  max_score-np.average(score_evolution) # loss averaged accross epochs
    final_loss =  max_score-np.mean(score_evolution[:,-1]) #real final loss
    if len(sys.argv) == 1 :
        print "Hyperopt trial #", trial_nr_in_hyperopt
        trial_nr_in_hyperopt += 1
    result_log.write('-----------------------------------------------------------------------------------\n')
    # result_log.write("resultat :                                                          %s\n" %(ret))
    result_log.write("Statistics average on all epochs:\n")
    result_log.write("score:                                                                          %s\n" %(np.average(score_evolution)))
    result_log.write("loss  (lower is better, between 0~200):                                         %s\n" %(ret))
    result_log.write("\n")
    result_log.write("Statistics average on the last epoch (end of simulation):\n")
    result_log.write("score:                                                                          %s\n" %(np.mean(score_evolution[:,-1])))
    result_log.write("loss  (lower is better, between 0~200):                                         %s\n" %(max_score-np.mean(score_evolution[:,-1])))
    result_log.write('===================================================================================\n')
    # return ret
    return final_loss

# hyper opt part #


############################################
############################################
############### MAIN    ####################
############################################
############################################

#Param info
    # weight_multiplicator = x
    # defeat_punishment = y
    # victory_reward = z
    # network_param = s
trial_nr_in_hyperopt = 1

if len(sys.argv) == 1: #hyperopt==1 :

    print "using hyperopt ..."
    best = fmin(fn = lambda (x, y, z,s): avg_list(x,y,z,s),
                space = [hp.loguniform('x',np.log(0.001), np.log(10)), #weight_multiplicator
                         - hp.loguniform('y',np.log(0.01), np.log(100)), #defeat_punishment
                         hp.loguniform('z',np.log(0.01), np.log(1000)), # victory_reward
                         1 + hp.randint('s',49)], #network_param
                # space = [hp.uniform('x',0,10),
                #          hp.uniform('y',-10,10),
                #          hp.uniform('z',0,20),
                #          1 + hp.randint('s',8)],
                algo=tpe.suggest, # recherche avec optimisateur bayésien (les 20 premières 'evals' sont aléatoires)
                # algo=rand.suggest, # recherche aléatoire
                max_evals = 3000)
    str_end_hyperopt = "Resultat fourni par HyperOpt ('y' est une valeur négative, rajouter un '-' devant la valeur affichée) :\n%s\n" %(str(best))
    result_log.write(str_end_hyperopt)
    print str_end_hyperopt

else :
    if len(sys.argv) <= 4:
        print " use : \npython cartPoleTry.py weight_multiplicator defeat_punishment victory_reward network_param [save_file]"
    else :
        avg_list( float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]))



        for i in range(nb_simulation) :
            # plt.plot(axis,score_evolution[i],label="simulation n " + str(i))
            plt.plot(range(nb_seq),score_evolution[i,:],label="simulation n " + str(i))

        # plt.legend()
        plt.xlabel("Training epochs")
        plt.ylabel("score")
        plt.title("weight multiplicator : " + str(weight_multiplicator) + ", victory reward : " + str(victory_reward) + ", defeat punishment: " + str(defeat_punishment) + ",\n network size : " + str(network_size) + ", stop learning after winning : " + str(pro_level_exists))
        # plt.show()

        print "shape mean score evolutoin", np.mean(score_evolution, axis=0).shape
        print "shape", len(range(nb_seq))
        plt.figure()
        # on moyenne le long des lignes (i.e. des différentes simulations),
            #c'est à dire qu'on n'a plus qu'une seule ligne à la fin qui contient toutes les moyennes pour chaque epoch de simulation
        plt.plot(range(nb_seq),np.mean(score_evolution, axis=0)) # (axis=0 is for row) Axis or axes along which the means are computed.
        plt.xlabel("Training epochs")
        plt.ylabel("score")
        plt.title("weight multiplicator : " + str(weight_multiplicator) + ", victory reward : " + str(victory_reward) + ", defeat punishment: " + str(defeat_punishment) + ",\n network size : " + str(network_size) + ", stop learning after winning : " + str(pro_level_exists))


result_log.close() #xav: save details of run into text file
plt.show()
