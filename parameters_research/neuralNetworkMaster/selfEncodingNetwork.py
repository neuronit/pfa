
import numpy as np
from neuralNetworkMaster import mlp

SEN = mlp.MLP(4,3,4)

def Encode(network,samples,epochs=5000,lrate=.1, momentum=0.1):
    #Train
    print "Starting learning ... "
    for i in range(epochs):
        n = np.random.randint(samples.shape[0])
        network.propagate_forward( samples[n] )
        network.propagate_backward( samples[n], lrate, momentum )
    print  "Learning complete"
    # Test
    for i in range(samples.shape[0]):
        o = network.propagate_forward( samples[i] )
        print "\nsample number     :",i, "\ninput             :", samples[i],"\ncalculated output :", o
    print


# Encoding
# ---------------------------------

samples = np.zeros([5, 4])
SEN.reset()
samples[0] = (0,0,0,0)
samples[1] = (1,1,1,1)
samples[2] = (0,1,0,1)
samples[3] = (1,1,0,0)
samples[4] = (1,0,1,1)
Encode(SEN,samples)

