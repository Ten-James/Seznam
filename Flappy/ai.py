import numpy as np

def sgn(x):
    return np.math.tanh(x)

def sign(value):
    return 1 if value > 0 else 0


class Neuron:

    def __init__(self, Count_Vstupy):
        self.w = np.random.randn(Count_Vstupy + 1)

    def activate(self, vstupy):
        y = (np.append(vstupy, [1]) * self.w).sum()
        return sgn(y)
    
    def Debug(self):
        return len(self.w)


class Network:
    def __init__(self, layers):
        self.neurons = []
        last = layers[0]
        for layer in layers:
            pole = []
            for i in range(layer):
                pole.append(Neuron(last))
            self.neurons.append(pole)
            last = layer

    def Debug(self):
        for neuronL in self.neurons:
            for neuron in neuronL:
                print(neuron.Debug(), end="\t")
            print("\n",end="")
    
    def getData(self):
        data= []
        for neuronL in self.neurons:
            lay = []
            for neuron in neuronL:
                lay.append(np.asarray(neuron.w))
            data.append(np.asarray(lay))
        return np.asarray(data)

    def getRandomData(self):
        data= []
        for neuronL in self.neurons:
            lay = []
            for neuron in neuronL:
                lay.append(np.random.randn(len(neuron.w)))
            data.append(np.asarray(lay))
        return np.asarray(data)


    def setData(self, data):
        for row, dat in enumerate(data):
            for col, weights in enumerate(dat):
                self.neurons[row][col].w = weights


    def Clac(self, vstupy, layer = 0):
        if layer == len(self.neurons):
            return sign(vstupy)
        vystup = np.zeros(len(self.neurons[layer]))
        for index, neuron in enumerate(self.neurons[layer]):
            vystup[index] = neuron.activate(vstupy)
        return self.Clac(vystup, layer=layer+1)

        





if __name__ == '__main__':
    netw = Network([2,1])
    print(netw.Clac([2,3]))