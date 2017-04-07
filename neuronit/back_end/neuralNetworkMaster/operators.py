import numpy as np

class Operators:
    weights = -1    
    def propagate_backward(self, target, gammar, lrate= 0.1, momentum = 0.1):
        error = target - self.ret
        return error

    def reset(self):
        return 0

    def set_init_weight_scale(self,x):
        return

class OpTempo(Operators):
    
    def __init__(self):
        return

    def propagate_forward(self,*data):
        # self.ret = [data] # Warning ! It's a tuple
        # return self.ret
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        for i in range(s[0]):
            for j in range(s[1]):
                self.ret[j] = data[i][j]    
        return self.ret



class OpPlus(Operators):

    def __init__(self):
        return
    
    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        for i in range(s[0]):
            for j in range(s[1]):
                self.ret[j] += data[i][j]    
        return self.ret

class OpAvg(Operators):

    def __init__(self):
        return

    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        for i in range(s[0]):
            for j in range(s[1]):
                self.ret[j] += data[i][j]
        self.ret /= s[0]
        return self.ret

class OpMinus(Operators):

    def __init__(self):
        return
        
    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        for j in range(s[1]):
            self.ret[j] = data[0][j] - data[1][j]       
        return self.ret
        
class OpDivide(Operators):

    def __init__(self):
        return
        
    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        for j in range(s[1]):
            if data[1][j] == 0 :
                print "division par zero\n"
                sys.exit()
            self.ret[j] = data[0][j] / data[1][j]           #a verifier
        return self.ret
        
class OpMult(Operators):
    
    def __init__(self):
        return
    
    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1])
        self.ret += 1
        for i in range(s[0]):
            for j in range(s[1]):
                self.ret[j] *= data[i][j]            #a verifier
        return self.ret
        
class OpRecomp(Operators):

    def __init__(self):
        return
    
    def propagate_forward(self, *data):
        s = np.shape(data)
        self.ret = np.zeros(s[1]*s[0])
        for i in range(s[0]):
            for j in range(s[1]):
                self.ret[i*s[1]+j] = data[i][j]
        return self.ret

class OpDecomp(Operators):

    def __init__(self,*args):
        self.sizes = args
        return
    
    def propagate_forward(self, *data):
        data = data[0]
        current_deepness = 0
        self.ret = []
        for i in range(len(self.sizes)):
            retinter = []
            for j in range(self.sizes[i]):
                retinter.append(data[current_deepness])
                current_deepness += 1
            self.ret.append(retinter)
        return self.ret

#test
# maliste3 = [[1,2,3,4],[3,4,1,2],[0,5,0,5]]
# maliste2 = [[1,2,3,4],[1,2,3,4]]
# maliste1 = [[1,2,3,4]]


# monplus = OpPlus()
# print "mon plus " ,monplus.propagate_forward(*maliste3)

# monavg = OpAvg()
# print "mon Avg " ,monavg.propagate_forward(*maliste3)

# monmoins = OpMinus()
# print "mon minus " ,monmoins.propagate_forward(*maliste2)

# monfois = OpMult()
# print "mon fois" ,monfois.propagate_forward(*maliste3)

# mondiv = OpDivide()
# print "mon div" ,mondiv.propagate_forward(*maliste2)

# monrecomp = OpRecomp()
# print "mon recomp" ,monrecomp.propagate_forward(*maliste3)

# mondecomp = OpDecomp(2,1,1)
# print "mon decomp", mondecomp.propagate_forward(*maliste1)
