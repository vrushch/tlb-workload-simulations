import numpy as np
import random

class TLBSimulator:
    def __init__(self, size, replacement_policy='LRU'):
        self.size = size
        self.replacement_policy = replacement_policy
        self.cache = []
        self.hits = 0
        self.misses = 0

        self.all= []

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
                    self.cache.pop(0)
                else:
                    self.cache.pop(0)
            self.cache.append(address)

    def stats(self):
        f = open("address_hpc.txt", "w")
        f.write(",".join(self.all))
        return f"TLB Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {self.hits / (self.hits + self.misses):.2f}"

def tlb_access_simulation(data, tlb):
    for i in range(len(data)):
        address = id(data) + i * data.itemsize
        tlb.access(address)

# TLB Simulator initialization
tlb = TLBSimulator(size=128, replacement_policy='LRU')

# Simulate HPC data processing workload
def data_processing_simulation(data_size, tlb):
    # Generate large dataset
    data = np.random.rand(data_size)

    # Simulate TLB access for reading the data
    tlb_access_simulation(data, tlb)

    # Example operation 1: Filtering data
    filtered_data = data[data > 0.5]
    tlb_access_simulation(filtered_data, tlb)

    # Example operation 2: Aggregation
    sum_data = np.sum(data)
    tlb.access(id(sum_data))

    # Example operation 3: Statistical Analysis
    mean_data = np.mean(data)
    tlb.access(id(mean_data))

# Run the simulation for a number of iterations
for _ in range(10):
    data_processing_simulation(1000, tlb)  # Process 1 million data points

# Print TLB stats
print(tlb.stats())
