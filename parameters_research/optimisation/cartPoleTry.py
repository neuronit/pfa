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
from hyperopt import fmin,tpe,hp
from datetime import datetime as dt
from neuralNetworkMaster import mlp
from neuralNetworkMaster import elman
from neuralNetworkMaster import jordan
import matplotlib.pyplot as plt
import numpy as np

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
axis = [i for i in range(nb_seq)]
        
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
                        network.propagate_backward(victory_reward*power,lrate,momentum)
                        
                    else :                                                                          
                        network.propagate_backward(-victory_reward*power,lrate,momentum)
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
    if network_type == "mlp":
        network = mlp.MLP(*network_size)
    if network_type =="elman":
        network = elman.Elman(*network_size)
        
    for i in range(nb_simulation) :
        network.set_init_weights_scale(weight_multiplicator) #xav
        network.reset()
        Mcar(network,i)
    ret =  max_score-np.average(score_evolution)
    if len(sys.argv) == 1 :
        print "Hyperopt trial #", trial_nr_in_hyperopt
        trial_nr_in_hyperopt += 1
    result_log.write('-----------------------------------------------------------------------------------\n')
    result_log.write("resultat :                                                          %s\n" %(ret))
    result_log.write('===================================================================================\n')
    return ret

# hyper opt part #

 
#Param info
    # weight_multiplicator = x
    # defeat_punishment = y
    # victory_reward = z
    # network_param = s
trial_nr_in_hyperopt = 1

if len(sys.argv) == 1: #hyperopt==1 :

    print "using hyperopt ..."
    best = fmin(fn = lambda (x, y, z,s): avg_list(x,y,z,s),
                space = [hp.uniform('x',0,10),
                         hp.uniform('y',-10,10),
                         hp.uniform('z',0,20),
                         1 + hp.randint('s',10)],
                algo=tpe.suggest,
                max_evals = 1)

    result_log.write("Resultat fourni par HyperOpt :\n%s\n" %(str(best)))
    print best

else :
    if len(sys.argv) <= 4:
        print " use : \npython cartPoleTry.py weight_multiplicator defeat_punishment victory_reward network_param [save_file]"
    else :
        avg_list( float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]))


    
        for i in range(nb_simulation) :
            plt.plot(axis,score_evolution[i],label="simulation n " + str(i))

        plt.legend()
        plt.xlabel("Training epochs")
        plt.ylabel("score")
        plt.title("weight multiplicator : " + str(weight_multiplicator) + ", victory reward : " + str(victory_reward) + ", defeat punishment: " + str(defeat_punishment) + ",\n network size : " + str(network_size) + ", stop learning after winning : " + str(pro_level_exists))
        plt.show()

result_log.close()
