import numpy as np

class TLBSimulator:
    def __init__(self, size, replacement_policy='FIFO'):
        self.size = size
        self.replacement_policy = replacement_policy
        self.cache = []
        self.hits = 0
        self.misses = 0

        self.all = []

    def access(self, address):
        self.all.append(str(address))
        if address in self.cache:
            self.hits += 1
            if self.replacement_policy == 'LRU':
                self.cache.remove(address)
                self.cache.append(address)
        else:
            self.misses += 1
            if len(self.cache) >= self.size:
                if self.replacement_policy == 'FIFO':
                    self.cache.pop(0)  # FIFO: remove the first element
                else:
                    # LRU: remove least recently used
                    self.cache.pop(0)
            self.cache.append(address)

    def stats(self):
        f = open("address_nn.txt", "w")
        f.write(",".join(self.all))
        #print(self.all)
        return f"TLB Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {self.hits / (self.hits + self.misses):.2f}"

# Function to simulate TLB access for a numpy array
def tlb_access_simulation(matrix, tlb):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # Simulating the memory address; this is a simplification
            address = id(matrix) + i * matrix.strides[0] + j * matrix.strides[1]
            tlb.access(address)

# TLB Simulator initialization
tlb = TLBSimulator(size=128, replacement_policy='LRU')

# Sigmoid activation function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Input datasets
inputs = np.array([[0,0,1],
                   [1,1,1],
                   [1,0,1],
                   [0,1,1]])
expected_output = np.array([[0],[1],[1],[0]])

# Seed for random number generation for reproducibility
np.random.seed(1)

# Initialize weights randomly with mean 0
hidden_weights = np.random.uniform(size=(3, 4))
output_weights = np.random.uniform(size=(4, 1))

# Learning rate
lr = 0.1

# Training process
for _ in range(10000):
    # Forward propagation
    hidden_layer_activation = np.dot(inputs, hidden_weights)
    tlb_access_simulation(hidden_layer_activation, tlb)
    hidden_layer_output = sigmoid(hidden_layer_activation)

    output_layer_activation = np.dot(hidden_layer_output, output_weights)
    tlb_access_simulation(output_layer_activation, tlb)
    predicted_output = sigmoid(output_layer_activation)

    # Backpropagation
    error = expected_output - predicted_output
    d_predicted_output = error * sigmoid_derivative(predicted_output)
    
    error_hidden_layer = d_predicted_output.dot(output_weights.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    # Updating Weights
    output_weights += hidden_layer_output.T.dot(d_predicted_output) * lr
    tlb_access_simulation(output_weights, tlb)
    hidden_weights += inputs.T.dot(d_hidden_layer) * lr
    tlb_access_simulation(hidden_weights, tlb)

# Output
print('Final output after training:')
print(predicted_output)

# TLB Stats
print(tlb.stats())
