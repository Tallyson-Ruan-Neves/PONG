import numpy as np

class Neural(object):
    def __init__(self, layers):
        self.layers = layers
        self.input_layer = layers[0]
        self.output_layer = layers[-1]
        self.hidden_layer = layers[1:-1]
                
        self.biases = [np.random.randn(y, 1) for y in self.layers[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(self.layers[:-1], self.layers[1:])]
        
    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))
    
    def sigmoid_derivative(self, z):
        return self.sigmoid(z) * (1 - self.sigmoid(z))
    
    def feedforward(self, input):
        for bias, weight in zip(self.biases, self.weights):
            input = self.sigmoid(np.dot(weight, input) + bias)
        return input
    
    def backpropagation(self, x, y, learning_rate=0.01):
        a = x
        activations = [a]
        zs = []

        for bias, weight in zip(self.biases, self.weights):
            z = np.dot(weight, a) + bias
            zs.append(z)
            a = self.sigmoid(z)
            activations.append(a)

        # Backward pass
        delta = (activations[-1] - y) * self.sigmoid_derivative(zs[-1])
        nabla_b = [delta]
        nabla_w = [np.dot(delta, activations[-2].T)]

        for i in range(2, len(self.layers)):
            z = zs[-i]
            sp = self.sigmoid_derivative(z)
            delta = np.dot(self.weights[-i+1].T, delta) * sp
            nabla_b.insert(0, delta)
            nabla_w.insert(0, np.dot(delta, activations[-i-1].T))

        self.weights = [w - learning_rate * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - learning_rate * nb for b, nb in zip(self.biases, nabla_b)]

    def calculate_loss(self, predicted, target):
        return np.mean((predicted - target) ** 2)

    def train(self, training_data, epochs, learning_rate):
        for epoch in range(epochs):
            total_loss = 0.0
            for x, y in training_data:
                predicted = self.feedforward(x)
                total_loss += self.calculate_loss(predicted, y)
                self.backpropagation(x, y, learning_rate)
            average_loss = total_loss / len(training_data)
            print(f"Epoch {epoch + 1}/{epochs}, Average Loss: {average_loss}")
            
    def save_parameters(self, filename):
        np.savez(filename, weights=self.weights, biases=self.biases)

    def load_parameters(self, filename):
        data = np.load(filename)
        self.weights = data['weights']
        self.biases = data['biases']
        
    def predict(self, input):
        output = self.feedforward(input)
        return output

if __name__ == '__main__':
    rn = Neural([8, 6, 6, 3])
    training_data = [(np.random.randn(8, 1), np.random.randn(3, 1)) for _ in range(10000)]
    epochs = 10

    rn.train(training_data, epochs)
    rn.predict(np.random.randn(8, 1))