
# pip3 install PyOpenGL PyOpenGL_accelerate

import numpy as np
import random
from OpenGL.GL import *
from OpenGL.GLUT import *

class TLBSimulator:
    def __init__(self, size, replacement_policy='LRU'):
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
                    self.cache.pop(0)
                else:
                    self.cache.pop(0)
            self.cache.append(address)

    def stats(self):
        f = open("address_graphics.txt", "w")
        f.write(",".join(self.all))
        return f"TLB Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {self.hits / (self.hits + self.misses):.2f}"

# Initialize OpenGL (This is a minimal setup)
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow('OpenGL Window')

# TLB Simulator initialization
tlb = TLBSimulator(size=100, replacement_policy='LRU')

def simulate_graphics_operations():
    # Simulate texture loading
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    tlb.access(texture_id)

    # Simulate shader compilation
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    tlb.access(vertex_shader)
    tlb.access(fragment_shader)

    # Simulate buffer creation
    buffer_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer_id)
    tlb.access(buffer_id)

    # Cleanup (not typically done every frame, but for demonstration)
    glDeleteTextures([texture_id])
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    glDeleteBuffers(1, [buffer_id])

# Run the simulation for a number of frames
for _ in range(60):  # Assuming 60 frames per second
    simulate_graphics_operations()

# Print TLB stats
print(tlb.stats())
