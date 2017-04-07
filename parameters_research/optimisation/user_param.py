##############################################
# parameters than can be defined by the user #
##############################################

# parameters modifying the behaviour of the network
 
global weight_multiplicator                       # multiplicator of a returned observation, allow to scale observations in order to make the network differentiate them
weight_multiplicator = 0.25
global victory_reward
victory_reward = 0                                 # reward at win
global defeat_punishment
defeat_punishment = 1                              # punishment given when the game is lost (pool fall or cart get out of bound)
global network_param
network_param = [4]                                # shape of hidden layers

network_type = "mlp"                             # network_type ("mlp", "elman")

# parameters modifying the result display (might not be change by a common user)

max_score = 200                          # score which makes the game end (200 is the basic OpenAI gym value)
nb_seq = 300                           # lenght of a simulation
nb_simulation = 10                        # number of simulations
save_frequency = 10000
gamma = 0.6
hyperopt = 0                              # set to 1 to launch with hyperopt, 0 for normal use
pro_level_exists = 0                               # if set to 1, the network stop learning after winning a game
