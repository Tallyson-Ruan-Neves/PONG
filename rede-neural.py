import numpy as np

class Neural(object):
    def __init__(self, layers):
        self.layers = layers
        self.input_layer = layers[0]
        self.output_layer = layers[-1]
        self.hidden_layer = layers[1:-1]
        
        # print(self.layers,
        # self.input_layer,
        # self.output_layer,
        # self.hidden_layer)
        
        self.weights = [np.random.randn(y, 1) for y in self.layers[1:]]
        self.biases = [np.random.randn(y, x) for x, y in zip(self.layers[:-1], self.layers[1:])]
        
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))
    
    def feedforward(self, a):
        for bias, weight in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(weight, a) + bias)
        return a
            
        
        
n = Neural([8,6,6,3])
# print(n.biases, n.weights)