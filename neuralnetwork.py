import numpy as np
class NeuralNetwork:
    def __init__(self,inputSize):
        super().__init__()
        self.layers = []
        self.inputSize = inputSize
        self.n = Neuron(inputSize)
    def addLayer(self,size=1):
        nLayer = []
        if(len(self.layers) == 0):
            layerInputSize = self.inputSize
        else:
            layerInputSize = len(self.layers[-1])
        for i in range(size):
            nLayer.append(Neuron(layerInputSize))
        
        self.layers.append(nLayer)
    def predict(self,x):
        for idx1,l in enumerate(self.layers):
            for idx2,n in enumerate(l):
                if(idx1 == 0):
                    n.feedforward(x)
                else:
                    i = np.array([])
                    for idx3, prevNeuron in enumerate(self.layers[idx1-1]):
                        i = np.append(i,prevNeuron.output)
                    n.feedforward(i)
                
                print(n.output)
        print("-------------------------------------")
        output = np.array([])

        for outputNeurons in self.layers[-1]:
            output = np.append(output,outputNeurons.output)

        return output

    def adjust(self,target):
        # bug: adjusting weights works fine if there is one layer. but runs into trouble with more than one. I think its just me not understanding backpropogations of neurons to full extent and to adjust biases
        # despite this the nn runs best with one neuron and achieves the goal
        for l in self.layers:
            for n in l:
                n.backprop(target)
class Neuron:
    def __init__(self,inputSize):
        super().__init__()
        self.weights = np.random.standard_normal(inputSize)
        
    def activation(self,x):
        return 1/(1+np.exp(-x))
    def sig_deriv(self,x):
        return self.activation(x)*(1-self.activation(x))
    def feedforward(self,inputs):
        self.input = inputs
        self.output = self.activation(np.matmul(self.weights,self.input))
        return self.output
    def backprop(self,target):
        adjustment = np.dot(self.input.T,2*(target - self.output) * self.sig_deriv(self.output))
        self.weights += adjustment
      