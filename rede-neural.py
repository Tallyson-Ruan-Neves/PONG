# import numpy

class Neural(object):
    def __init__(self, layers):
        self.layers = layers
        self.input_layer = layers[0]
        self.output_layer = layers[-1]
        self.hidden_layer = layers[1:-1]
        print(self.layers,
        self.input_layer,
        self.output_layer,
        self.hidden_layer)
        
        
n = Neural([2,3,3,4])
